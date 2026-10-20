import json
import os
import subprocess
import sys
import tempfile

from getgauge.python import step, data_store

STEP_IMPL = os.path.dirname(os.path.realpath(__file__))
IMPORT_SCRIPT = os.path.join(STEP_IMPL, '..', '..', '..', 'scripts', 'hull_import.py')
IMPORT_SOURCES = os.path.join(STEP_IMPL, '..', 'sources', 'import')
HELM_BINARY = os.environ.get("helm_binary", "helm")


@step("Import manifests <file> for release <release> in namespace <namespace> and verify the round trip")
def import_manifests_and_verify_the_round_trip(file, release, namespace):
    report_path = os.path.join(tempfile.mkdtemp(prefix="hull-import-report-"), "report.json")
    result = subprocess.run(
        [sys.executable, IMPORT_SCRIPT, "--verify", "--release-name", release, "--namespace", namespace,
         "--helm", HELM_BINARY, "--report", report_path, os.path.join(IMPORT_SOURCES, file)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stderr)
    report = {}
    if os.path.exists(report_path):
        with open(report_path, encoding="utf-8") as report_file:
            report = json.load(report_file)
    data_store.scenario["import_report"] = report
    data_store.scenario["import_values"] = result.stdout
    assert result.returncode == 0, f"Import of {file} did not verify, exit code {result.returncode}:\n{result.stderr}"
    verification = report.get("verification") or []
    assert verification and all(r["status"] == "identical" for r in verification), json.dumps(verification, indent=2)


@step("The import report has a note for <obj> containing <text>")
def the_import_report_has_a_note_for_object_containing(obj, text):
    notes = data_store.scenario.get("import_report", {}).get("notes", [])
    assert any(n["object"] == obj and text in n["message"] for n in notes), \
        f"No note for {obj} containing '{text}' in:\n" + "\n".join(f"{n['object']}: {n['message']}" for n in notes)


@step("The imported values contain <text>")
def the_imported_values_contain(text):
    assert text in data_store.scenario.get("import_values", ""), \
        f"'{text}' not found in the imported values:\n{data_store.scenario.get('import_values', '')}"
