from prompting_techniques import run_log


def test_save_run_writes_system_user_and_response_to_a_file(tmp_path, monkeypatch):
    monkeypatch.setattr(run_log, "RUNS_DIR", tmp_path)

    path = run_log.save_run("zero_shot", "be concise", "analyze this", "here is the report")

    content = path.read_text()
    assert path.parent == tmp_path
    assert "=== SYSTEM PROMPT ===\nbe concise" in content
    assert "=== USER PROMPT ===\nanalyze this" in content
    assert "=== RESPONSE ===\nhere is the report" in content
