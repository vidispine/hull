import os
import re
import shutil
import subprocess

import yaml
from dotty_dict import Dotty
from getgauge.python import step, data_store

STEP_IMPL = os.path.dirname(os.path.realpath(__file__))
TEST_ROOT = os.path.normpath(os.path.join(STEP_IMPL, '..'))
HULL_PATH = os.path.normpath(os.path.join(TEST_ROOT, '..', '..', '..'))
COOKBOOK = os.path.join(HULL_PATH, 'files', 'doc', 'cookbook.md')
HELM_BINARY = os.environ.get("helm_binary", "helm")


def cookbook_recipes():
    """The recipes of cookbook.md: the yaml block following each '<!-- recipe: <id> -->' marker."""
    with open(COOKBOOK, encoding='utf-8') as file:
        return dict(re.findall(r'<!-- recipe: (\S+) -->\n```yaml\n(.*?)\n```', file.read(), re.S))


def kube_version():
    with open(os.path.join(HULL_PATH, 'Chart.yaml'), encoding='utf-8') as file:
        return '.'.join(str(yaml.safe_load(file)['version']).split('.')[:2])


@step("Every recipe of the cookbook is tested")
def every_recipe_of_the_cookbook_is_tested():
    with open(os.path.join(TEST_ROOT, 'specs', 'cookbook.spec'), encoding='utf-8') as file:
        tested = set(re.findall(r'Render the cookbook recipe "([^"]+)"', file.read()))
    recipes = set(cookbook_recipes())
    assert recipes, "no recipes found in " + COOKBOOK
    assert recipes == tested, f"untested recipes {sorted(recipes - tested)}, unknown recipes {sorted(tested - recipes)}"


@step("Render the cookbook recipe <recipe>")
def render_the_cookbook_recipe(recipe):
    """Renders a recipe exactly as written, without the test suites, with the hull-test chart."""
    values = cookbook_recipes().get(recipe)
    assert values, f"recipe {recipe} not found in {COOKBOOK}"
    case_dir = os.path.join(TEST_ROOT, 'test_execution', 'case', 'cookbook')
    chart_dir = os.path.join(case_dir, 'chart', 'hull-test')
    shutil.rmtree(case_dir, ignore_errors=True)
    shutil.copytree(os.path.join(TEST_ROOT, 'sources', 'charts', 'hull-test'), chart_dir)
    chart_yaml = os.path.join(chart_dir, 'Chart.yaml')
    with open(chart_yaml, encoding='utf-8') as file:
        content = file.read().replace('<K8S_MAJOR_VERSION>', kube_version())
    with open(chart_yaml, 'w', encoding='utf-8') as file:
        file.write(content)
    hull_dir = os.path.join(chart_dir, 'charts', 'hull-1.0.0')
    os.makedirs(hull_dir)
    for name in ('Chart.yaml', 'values.yaml', 'values.schema.json', 'README.md'):
        shutil.copy(os.path.join(HULL_PATH, name), hull_dir)
    shutil.copytree(os.path.join(HULL_PATH, 'templates'), os.path.join(hull_dir, 'templates'))
    shutil.copy(os.path.join(HULL_PATH, 'hull.yaml'), os.path.join(chart_dir, 'templates'))
    values_file = os.path.join(chart_dir, f'{recipe}.values.yaml')
    with open(values_file, 'w', encoding='utf-8') as file:
        file.write(values + '\n')

    lint = subprocess.run([HELM_BINARY, 'lint', '--strict', chart_dir, '-f', values_file],
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert lint.returncode == 0, f"Linting recipe {recipe} failed:\n{lint.stdout}"
    render = subprocess.run([HELM_BINARY, 'template', chart_dir, '--kube-version', kube_version(), '--name-template',
                             'release-name', '--namespace', 'default', '-f', values_file],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert render.returncode == 0, f"Rendering recipe {recipe} failed:\n{render.stderr}"

    data_store.scenario.case = 'cookbook'
    data_store.scenario.chart = 'hull-test'
    data_store.scenario.kind = 'Deployment'
    # the assertion steps replace this placeholder in expected values
    data_store.scenario.environment = {"<K8S_MAJOR_VERSION>": kube_version()}
    data_store.scenario.objects = []
    for key in list(data_store.scenario.keys()):
        if key.startswith('objects_'):
            data_store.scenario[key] = dict()
    for document in yaml.safe_load_all(render.stdout):
        if not document:
            continue
        item = Dotty(document, separator='§')
        data_store.scenario.objects.append(item)
        data_store.scenario.setdefault('objects_' + document['kind'], dict())
        data_store.scenario['objects_' + document['kind']][document['metadata']['name']] = item
