import json

from decision_simulator.report import build_report, write_report


def test_report_is_json_serializable(tmp_path):
    report = build_report("D", ["A", "B"], "context", 2, ["A: yes"], "0.6.0")
    payload = json.loads(report.to_json())
    assert payload["decision"] == "D"
    assert payload["options"] == ["A", "B"]
    assert payload["rounds"] == 2
    assert payload["transcript"] == ["A: yes"]


def test_write_report_creates_parent_and_file(tmp_path):
    report = build_report("D", ["A", "B"], "", 1, ["A: yes"], "0.6.0")
    path = write_report(report, tmp_path / "reports" / "debate.json")
    assert path.exists()
    assert json.loads(path.read_text(encoding="utf-8"))["version"] == "0.6.0"


def test_write_report_replaces_existing_file(tmp_path):
    report = build_report("new", ["A", "B"], "", 1, [], "0.6.0")
    path = tmp_path / "debate.json"
    path.write_text("old", encoding="utf-8")
    write_report(report, path)
    assert json.loads(path.read_text(encoding="utf-8"))["decision"] == "new"
