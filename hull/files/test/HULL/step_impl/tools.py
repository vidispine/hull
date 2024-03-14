import base64
import errno
import json
import os
import shutil
import subprocess
import sys
import jsonschema
import yaml
import re

from dotty_dict import Dotty
from getgauge.python import Messages, before_scenario, before_step, data_store, step

from jsonschema import validate

TEST_EXECUTION_FOLDER = "./../test_execution"
WINDOWS_LINE_ENDING = '\r\n'
UNIX_LINE_ENDING = '\n'

@step("Fill data store with kind <kind>")
def fill_data_store_with_kind(kind):
    data_store.scenario.kind = kind

@step("Fill data store with kind <kind> and case <case>")
def fill_data_store_with_kind_and_case(kind, case):
    data_store.scenario.kind = kind
    data_store.scenario.case = case.lower()

@step("Fill data store with chart <chart> and suites <suites>")
def fill_data_store_with_chart_and_suites(chart, suites):
    data_store.scenario.chart = chart
    s = list()
    if not suites == "":
        s = suites.split(',')
    s.append("basic")
    data_store.scenario.suites = s

@step("Fill data store with case <case>, chart <chart> and suites <suites>")
def fill_data_store_with_case_chart_suites(case, chart, suites):
    data_store.scenario.case = case.lower()
    data_store.scenario.chart = chart
    s = list()
    if not suites == "":
        s = suites.split(',')
    s.append("basic")
    data_store.scenario.suites = s

@step("Fill data store with kind <kind>, case <case>, chart <chart> and suites <suites>")
def fill_data_store(kind, case, chart, suites):
    fill_data_store_with_kind_and_case(kind, case)
    fill_data_store_with_chart_and_suites(chart, suites)
    
@step("Copy folders to test execution folder")
def copy_folders_to_TEST_EXECUTION_FOLDER():
    copy_the_test_suites_source_folders_to_TEST_EXECUTION_FOLDER()
    copy_the_test_source_folder_to_TEST_EXECUTION_FOLDER()
    copy_the_test_chart_folders_to(data_store.scenario.case, data_store.scenario.chart)
    copy_the_hull_chart_files_to_test_execution_folder()

@step("Copy the test source folder to test execution folder")
def copy_the_test_source_folder_to_TEST_EXECUTION_FOLDER():
    copy_the_test_chart_folders_to(data_store.scenario.case, data_store.scenario.chart)

@step("Copy the test source folder for case <case> and chart <chart> to test execution folder")
def copy_the_test_chart_folders_to(case, chart):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    src_path_case = os.path.join(dir_path,'./../sources/cases', case)
    src_path_chart = os.path.join(dir_path,'./../sources/charts', chart)
    dst_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'chart', chart)
    try:
        copytree(src_path_case, dst_path)
        copytree(src_path_chart, dst_path)
    except Exception as e:
        print(f"Failed to copy {src_path_case} and {src_path_chart} to {dst_path}", e.__str__, "occurred.")
        assert False
    
    expected = os.path.join(src_path_case, 'expected.yaml')
    if os.path.exists(expected):
        try:
            if not "expected" in data_store.scenario:
                data_store.scenario["expected"] = {}
            data_store.scenario["expected"][case] = yaml.load(os.path.open(expected,newline='\n'))
        except Exception as e:
            print(f"Failed to read {expected}", e.__str__, "occurred.")
            assert False
    
    assert True

@step("Copy the suites source folders to test execution folder")
def copy_the_test_suites_source_folders_to_TEST_EXECUTION_FOLDER():
    for suite in data_store.scenario.suites:
        copy_the_suite_source_folder_for_case_and_chart_and_suite_to_TEST_EXECUTION_FOLDER(data_store.scenario.case, data_store.scenario.chart, suite)    

@step("Copy the suite source folder for case <case> and chart <chart> and suite <suite> to test execution folder")
def copy_the_suite_source_folder_for_case_and_chart_and_suite_to_TEST_EXECUTION_FOLDER(case, chart, suite):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    suite_folder = suite
    suite_file = suite
    if '/' in suite:
        suite_folder = suite.split('/')[0]
        suite_file = suite.split('/')[1]

    src_path = os.path.join(dir_path,'./../sources/cases/',suite_folder)
    dst_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'chart', chart)
    
    try:
        copytree(src_path, dst_path, 'files')
        
        expected = os.path.join(dir_path,'./../sources/cases/',suite_folder, 'expected.yaml')
        if os.path.exists(expected):
            if not "expected" in data_store.scenario:
                data_store.scenario["expected"] = {}
            data_store.scenario["expected"][suite] = yaml.safe_load(open(expected, newline='\r\n'))
    except Exception as e:
        print("Oops!", e.__str__, "occurred.")
        assert False
    assert True


@step("Clean the test execution folder")
def delete_the_TEST_EXECUTION_FOLDER():
    if os.environ.get("no_cleanup") != 'true':
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dst_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, "case", data_store.scenario.case)
        if os.path.isdir(dst_path):
            shutil.rmtree(dst_path, ignore_errors=True)
    else:
          print("Not cleaning up test execution folder.")
    assert True    

@step("Copy the HULL chart files to test execution folder")
def copy_the_hull_chart_files_to_test_execution_folder():
    copy_the_hull_chart_files_to_test_object_in_chart(data_store.scenario.case, data_store.scenario.chart)

@step("Copy the HULL chart files for test case <case> and chart <chart> to test execution folder")
def copy_the_hull_chart_files_to_test_object_in_chart(case, chart):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    hull_path = os.path.join(dir_path,'./../../../../')
    dst_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'chart', chart, "charts/hull-1.0.0/")
    try:
        copyfile(hull_path, "Chart.yaml", dst_path)
        copyfile(hull_path, "README.md", dst_path)
        copyfile(hull_path, "values.schema.json", dst_path)
        copyfile(hull_path, "values.yaml", dst_path)
        if os.environ.get("style") == 'single_file' or os.environ.get("default"):
            copyfile(hull_path, "hull.yaml", os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'chart', chart, "templates"))
        if os.environ.get("style") == 'multi_file':
            copytree(os.path.join(hull_path, "files/templates"), os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'chart', chart, "templates"))
        copytree(os.path.join(hull_path, "templates"), os.path.join(dst_path, "templates"))
    except Exception as e:
        print("Oops!", e.__str__, "occurred.")
        assert False
    assert True    

@step("Fail to render the templates for values file <values_file> to test execution folder because error contains <expected_error>")
def fail_to_render_the_templates_for_values_file_to_TEST_EXECUTION_FOLDER_because_error_contains(values_file, expected_error):
    fail_to_render_the_templates_to_namespace_namespace_for_values_file_to_TEST_EXECUTION_FOLDER_because_error_contains(values_file, "default", expected_error)

@step("Fail to render the templates for values file <values_file> to test execution folder and namespace <namespace> because error contains <expected_error>")
def fail_to_render_the_templates_to_namespace_namespace_for_values_file_to_TEST_EXECUTION_FOLDER_because_error_contains(values_file, namespace, expected_error):
    fail_to_render_the_templates_to_namespace_namespace_for_test_case_and_chart_and_values_file(data_store.scenario.case, data_store.scenario.chart, values_file, namespace, expected_error)

@step("Fail to render the templates for test case <case> and chart <chart> and values file <values_file> to test execution folder and namespace <namespace> because error contains <expected_error>")
def fail_to_render_the_templates_to_namespace_namespace_for_test_case_and_chart_and_values_file(case, chart, values_file, namespace, expected_error):
    result = render_chart(case, chart, values_file, namespace)
    if result.returncode != 0 and expected_error in str(result.stdout):
        assert True
    else:
        assert False, "With ExitCode " + str(result.returncode) + ", expected error " + expected_error + " not found in STDOUT: " + str(result.stdout)

@step("Lint the templates for values file <values_file> to namespace <namespace>")
def lint_the_templates_for_values_file_to_TEST_EXECUTION_FOLDER(values_file, namespace):
    if os.environ.get("no_lint") == 'true':
        print('Skipping Linting')
    else: 
        lint = lint_chart(data_store.scenario.case, data_store.scenario.chart, values_file, namespace)
        assert lint.returncode == 0, "Linting failed with ExitCode " + str(lint.returncode) + " STDOUT was:\n\n" + str(lint.stdout) + "\n\n and STDERR\n\n: " + str(lint.stderr)

@step("Render the templates for values file <values_file> to test execution folder and namespace <namespace>")
def render_the_templates_for_values_file_to_TEST_EXECUTION_FOLDER(values_file, namespace):
    render = render_chart(data_store.scenario.case, data_store.scenario.chart, values_file, namespace)
    #if result.returncode == 0:
    #    render_path = get_render_path(data_store.scenario.case, data_store.scenario.chart, values_file)
    #    with open(render_path) as reader:
    #        for line in reader.readlines():
    #            Messages.write_message(line)
    assert render.returncode == 0, "Rendering failed with ExitCode " + str(render.returncode) + " STDOUT was:\n\n" + str(render.stdout) + "\n\n and STDERR\n\n: " + str(render.stderr)

@step("Fill data store with rendered objects")
def fill_data_store_with_rendered_objects():
    get_objects(data_store.scenario.case, data_store.scenario.chart)

@step("Expected number of <count> objects of kind <kind> were rendered")
def check_that_expected_number_of_objects_of_kind_was_rendered(count, kind):
    found = len(data_store.scenario["objects_" + kind])
    assert int(count) == found, "Expected " + str(count) + " but found " + str(found)

@step("Expected number of <count> objects were rendered")
def check_that_expected_number_of_objects_was_rendered(count):
    check_that_expected_number_of_objects_of_kind_was_rendered(count, data_store.scenario.kind)

@step("Set test object to <name> of kind <kind>")
def set_test_object_to_of_kind(name, kind):
    objects_of_kind = "objects_" + kind
    assert name in data_store.scenario[objects_of_kind], f"Object with name {name} not found in objects of kind {kind}!"
    data_store.scenario.test_object = data_store.scenario[objects_of_kind][name]
    data_store.scenario.name = name


@step("Set test object to <name>")
def set_test_object_to(name):
    objects_of_kind = "objects_" + data_store.scenario.kind
    assert objects_of_kind in data_store.scenario, f"No object kind set!"
    return set_test_object_to_of_kind(name, data_store.scenario.kind)

@step("Test object <name> of kind <kind> does not exist")
def test_object_of_kind_does_not_exist(name, kind):
    try:
        data_store.scenario["objects_" + kind][name]
    except Exception as e:
        if e.__class__.__name__ == 'KeyError':
            assert True
            return
    assert False

@step("Test object <name> does not exist")
def test_object_does_not_exist(name):
    return test_object_of_kind_does_not_exist(name, data_store.scenario.kind)

@step("Test Object has key <key> with array value that has <count> items")
def test_object_has_key_with_array_value_that_has_items(key, value):
    assert data_store.scenario.test_object != None
    if isinstance(data_store.scenario.test_object[key], list): 
        assert_values_equal(len(data_store.scenario.test_object[key]), int(value), key)
    else:
        assert False

@step("Test Object has key <key> with dictionary value that has <count> items")
def test_object_has_key_with_dictionary_value_that_has_items(key, value):
    assert data_store.scenario.test_object != None
    if isinstance(data_store.scenario.test_object[key], dict): 
        for key in data_store.scenario.test_object[key].keys():            
            print(f'Found key: {key}')
            
        assert_values_equal(len(data_store.scenario.test_object[key].keys()), int(value), key)
    else:
        assert False

@step("Test Object has key <key> with map value that has <count> items which are not empty")
def test_object_has_key_with_map_value_that_has_non_empty_items(key, value):
    assert data_store.scenario.test_object != None
    dictionary = yaml.safe_load(data_store.scenario.test_object[key])
    if isinstance(dictionary, dict):
        for key in dictionary.keys():
            print(f'Found key: {key}')
            if not dictionary[key]:
                assert False, f"Key '{key}' has an empty value!"
        assert_values_equal(len(dictionary.keys()), int(value), key)
    else:
        assert False

@step("Test Object has key <key> with list value that has count of items greater than <count>")
def test_object_has_key_with_list_value_that_has_count_greater(key, value):
    assert data_store.scenario.test_object != None
    yamlList = yaml.safe_load(data_store.scenario.test_object[key])
    if isinstance(yamlList, list):
        for item in yamlList:
            print(f'Found item: {item}')
        assert len(yamlList) > int(value)
    else:
        assert False

@step("Test Object has key <key> with value <value>")
def test_object_has_key_with_value(key, value):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert_values_equal(data_store.scenario.test_object[key], value, key)

@step("Test Object has key <key> with value of key <expectedkey> from expected.yaml")
def test_object_has_key_with_value_of_key_from_expected_yaml(key, expectedkey):
    return test_object_has_key_with_value_of_key_from_expected_yaml_of_suite(key, expectedkey, data_store.scenario.case)

@step("Test Object has key <key> with value of key <expectedkey> from expected.yaml of suite <suite>")
def test_object_has_key_with_value_of_key_from_expected_yaml_of_suite(key, expectedkey, suite):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert key in data_store.scenario.test_object, f"Key {key} not found in Test Object!"
    assert 'expected' in  data_store.scenario, f"No expected entries found in Test Scenario"
    assert suite in data_store.scenario.expected, f"Suite {suite} not found in expected.yaml!"
    assert expectedkey in data_store.scenario.expected[suite], f"Expected Key {expectedkey} not found in Suite {suite} in expected.yaml!"
    assert_values_equal(data_store.scenario.test_object[key], data_store.scenario.expected[suite][expectedkey], key)

@step("Test Object has key <key> with Base64 encoded value of key <expectedkey> from expected.yaml of suite <suite>")
def test_object_has_key_with_base64_encoded_value_of_key_from_expected_yaml_of_suite(key, expectedkey, suite):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    decoded = base64.b64decode(data_store.scenario.test_object[key]).decode()
    assert_values_equal(
        data_store.scenario.expected[suite][expectedkey], decoded, key)

@step("Test Object has key <key> with value equaling object type")
def test_object_has_key_with_value_equaling_object_type(key):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert_values_equal(data_store.scenario.test_object[key], data_store.scenario.case.lower(), key)

@step("Test Object has key <key> with value equaling object instance name")
def test_object_has_key_with_value_equaling_object_instance_name(key):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert_values_equal(data_store.scenario.test_object[key], data_store.scenario.name, key)

@step("Test Object has key <key> with value equaling object instance key")
def test_object_has_key_with_value_equaling_object_instance_key(key):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert_values_equal(data_store.scenario.test_object[key], data_store.scenario.name.removeprefix("release-name-hull-test-"), key)

@step("Test Object has key <key> with value matching regex <regex>")
def test_object_has_key_with_value_matching_regex(key, regex):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"    
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert regex != None, "Regex cannot be empty!"
    compiled = re.compile(regex)
    assert compiled.match(data_store.scenario.test_object[key]), "The value '" + data_store.scenario.test_object[key] + "' was not matched by regex '" + regex + "'!"

@step("Test Object has key <key> with value containing <contains>")
def test_object_has_key_with_value_containing(key, contains):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"    
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert contains != None, "Contains string cannot be empty!"
    assert contains in data_store.scenario.test_object[key], "The value '" + data_store.scenario.test_object[key] + "' does not contain '" + contains + "'!"

@step("Test Object has key <key> with value not containing <contains>")
def test_object_has_key_with_value_containing(key, contains):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"    
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert contains != None, "Contains string cannot be empty!"
    assert contains not in data_store.scenario.test_object[key], "The value '" + data_store.scenario.test_object[key] + "' contains '" + contains + "'!"

@step("Test Object has key <key> set to true")
def test_object_has_key_set_to_true(key):
    test_object_has_key_with_value(key, True)

@step("Test Object has key <key> set to false")
def test_object_has_key_set_to_false(key):
    test_object_has_key_with_value(key, False)


@step("Test Object does not have key <key>")
def test_object_does_not_have_key(key):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    try:
        data_store.scenario.test_object[key]        
    except Exception as e:       
        if e.__class__.__name__ == 'KeyError':
            assert True
            return
    assert False

@step("Test Object has key <key> with integer value <value>")
def test_object_has_key_with_integer_value(key, value):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert_values_equal(data_store.scenario.test_object[key], int(value), key)

@step("Test Object has key <key> with null value")
def test_object_has_key_with_null_value(key):
    assert "test_object" in data_store.scenario != None, "No Test Object set!"
    assert data_store.scenario.test_object != None, "Test Object set to None!"
    assert_values_equal(data_store.scenario.test_object[key], None, key)

@step("Test Object has key <key> with Base64 encoded value of <value>")
def test_object_has_key_with_base64_encoded_value(key, value):
    assert data_store.scenario.test_object != None
    decoded = base64.b64decode(data_store.scenario.test_object[key]).decode()
    assert_values_equal(
        value, decoded, key)
    
@step("Test Object has key <key> with value <value> of key <scenario_key> from scenario data_store")
def test_object_has_key_with_value_of_key_from_scenario_data_store(key, scenario_key):
    test_object_has_key_with_value(key, data_store.scenario[scenario_key])
    
@step("All test objects have key <key> with value <value>")
def all_test_objects_have_key_with_value(key, value):
    test_objects = data_store.scenario["objects_" + data_store.scenario.kind]
    for i in test_objects:
        set_test_object_to(i)
        test_object_has_key_with_value(key, value)

@step("All test objects have key <key> with value matching regex <regex>")
def all_test_objects_have_key_with_value_matching_regex(key, regex):
    test_objects = data_store.scenario["objects_" + data_store.scenario.kind]
    for i in test_objects:
        set_test_object_to(i)
        test_object_has_key_with_value_matching_regex(key, regex)

@step("All test objects have key <key> with value of key <scenario_key> from scenario data_store")
def all_test_objects_have_key_with_value_of_key_from_data_store(key, scenario_key):
    test_objects = data_store.scenario["objects_" + data_store.scenario.kind]
    for i in test_objects:
        set_test_object_to(i)
        test_object_has_key_with_value_of_key_from_scenario_data_store(key, scenario_key)

@step("All test objects have key <key> with Base64 encoded value of <value>")
def all_test_objects_have_key_with_base64_value(key, value):
    test_objects = data_store.scenario["objects_" + data_store.scenario.kind]
    for i in test_objects:
        set_test_object_to(i)
        test_object_has_key_with_base64_encoded_value(key, value)

@step("All test objects have key <key> with Base64 encoded value of key <expectedkey> from expected.yaml of suite <suite>")
def all_test_objects_have_key_with_base64_encoded_value_of_key_from_expected_yaml_of_suite(key, expectedkey, suite):
    test_objects = data_store.scenario["objects_" + data_store.scenario.kind]
    for i in test_objects:
        set_test_object_to(i)
        test_object_has_key_with_base64_encoded_value(key, data_store.scenario.expected[suite][expectedkey])

@step("All test objects have key <key> with value of key <expectedkey> from expected.yaml of suite <suite>")
def all_test_objects_have_key_with_value_of_key_from_expected_yaml_of_suite(key, expectedkey, suite):
    test_objects = data_store.scenario["objects_" + data_store.scenario.kind]
    for i in test_objects:
        set_test_object_to(i)
        test_object_has_key_with_value(key, data_store.scenario.expected[suite][expectedkey])

@step("Validate")
def validate():
    test_objects = data_store.scenario.objects
    for i in test_objects:
        validate_test_object_against_json_schema(i)

@step("Fail to Validate because error contains <expected_error>")
def fail_to_validate(expected_error):
    try:
        validate()
    except Exception as e:
        if expected_error in str(e.__str__):
            print(f'Found expected message:\n\'{expected_error}\'\nin  exception message:\n\'{str(e.__str__)}\'')
            assert True
            return
        else:
            assert False, "Expected error " + expected_error + " not found in Exception message: " + str(e.__str__)

@step("Validate test object against JSON Schema")
def validate_test_object_against_json_schema(test_object):
    assert test_object != None    
    validateJson(test_object)

### non-steps

def assert_values_equal(actual, expected, key=None):
    if expected != actual:
        stop_debug = ""
    if (type(expected) == str and type(actual) == str ):
        expected = expected.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        actual = actual.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        if expected != actual:
            stop_debug = ""
        
    assert expected == actual, "For key '"+ key + "' there was expected value:\n\n" + str(expected) + "\n\nbut found:\n\n" + str(actual) + "\n\n"

def validateJson(test_object):
    
    schema_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./../schema")
    schema_version_split = str(test_object["apiVersion"]).split("/")
    schema_version = schema_version_split[0].split(".")[0]
    if len(schema_version_split) > 1:
        schema_version = schema_version + "-" + schema_version_split[1]
    schema_file = os.path.join(schema_dir, str(test_object["kind"]).lower().split(".")[0] + "-" + schema_version + ".json")
    if not os.path.exists(schema_file):
        schema_file = os.path.join(schema_dir, str(test_object["kind"]).lower().split(".")[0] + "-core-" + schema_version + ".json")
        
    with open(os.path.join(schema_dir, schema_file)) as json_file:
        schema = json.load(json_file)

        jsonschema.validate(instance=test_object.to_dict(), schema=schema)
    
def get_render_path(case, chart, values_file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'rendered', chart, 'templates',  'hull.yaml')

def lint_chart(case, chart, values_file):
    return lint_chart(case, chart, values_file, "default")

def lint_chart(case, chart, values_file, namespace):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chart_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'chart', chart)
    render_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'rendered')
    
    if not os.path.isdir(render_path):
        os.makedirs(render_path)
    
    suites = ()
    for suite in data_store.scenario.suites:
        suite_file = suite
        if '/' in suite:
            suite_file = suite.split('/')[1]
        suites += ("-f", os.path.join(chart_path, suite_file + ".values.hull.yaml"))
    
    args = ("helm", "lint", chart_path, "--debug", "--strict", "--namespace", namespace) + suites + ("-f",  os.path.join(chart_path, values_file))
    
    popen = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('STDOUT:\n', popen.stdout.decode("utf-8").replace("\n",os.linesep))
    print('STDERR:\n', popen.stderr.decode("utf-8").replace("\n",os.linesep) if popen.stderr is not None else "")
    return popen

def render_chart(case, chart, values_file, namespace):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chart_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'chart', chart)
    render_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'rendered')
    
    if not os.path.isdir(render_path):
        os.makedirs(render_path)
    
    suites = ()
    for suite in data_store.scenario.suites:
        suite_file = suite
        if '/' in suite:
            suite_file = suite.split('/')[1]
        suites += ("-f", os.path.join(chart_path, suite_file + ".values.hull.yaml"))
    
    args = ("helm", "template", chart_path, "--name-template", "release-name", "--debug", "--output-dir", render_path, "--namespace", namespace) + ("-f",  os.path.join(chart_path, values_file)) + suites
    
    popen = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('STDOUT:\n', popen.stdout.decode("utf-8").replace("\n",os.linesep))
    print('STDERR:\n', popen.stderr.decode("utf-8").replace("\n",os.linesep) if popen.stderr is not None else "")
    return popen

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                copyfile(os.path.dirname(s), os.path.basename(s), os.path.dirname(d))

def copy_yaml(src_path, dst_path):
    with open(src_path, 'r', encoding='utf8') as file:
        data = file.read()
        if data_store.scenario.case != "":
            data = data.replace("<OBJECT_TYPE>", data_store.scenario.case)
        if not os.path.isdir(os.path.dirname(dst_path)):
            os.makedirs(os.path.dirname(dst_path))
        dst_file = open(dst_path, "w", encoding='utf8')
        dst_file.write(data)
        dst_file.close()

def copyfile(src_dir, src_filename, dst_dir):
    if not os.path.isdir(os.path.dirname(dst_dir)):
        os.makedirs(os.path.dirname(dst_dir))
    if  os.path.splitext(src_filename)[1] == ".yaml":
        copy_yaml(os.path.join(src_dir, src_filename),  os.path.join(dst_dir, src_filename))
    else:
        shutil.copy2(os.path.join(src_dir, src_filename), os.path.join(dst_dir, src_filename))

def get_objects(case, chart):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    rendered_files_folder = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'rendered', chart, 'templates')
    rendered_file_path = os.path.join(dir_path, TEST_EXECUTION_FOLDER, 'case', case, 'rendered', chart, 'templates',  'hull.yaml')

    items = []
    for file in os.listdir(rendered_files_folder):
        with open(os.path.join(rendered_files_folder, file), encoding='utf-8', newline='\n') as file_in:
            
            item = None
            itemIndex = -1
            for line in file_in:
                if line.startswith("---"):
                    items.append([])
                items[itemIndex].append(line)
        
        data_store.scenario.objects = []
        for key in list(data_store.scenario.keys()):
            if key.startswith("objects_"):
                data_store.scenario[key] = dict()
            
        for i in items:
            
            item = Dotty(yaml.safe_load("".join(i)), separator='§')
            data_store.scenario.objects.append(item)
            if not ("objects_" + item['kind']) in data_store.scenario:
                data_store.scenario["objects_" + item['kind']] = dict()
            data_store.scenario["objects_" + item['kind']][item['metadata§name']] = item