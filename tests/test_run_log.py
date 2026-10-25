from prompting_techniques import run_log


def test_save_run_nests_under_a_per_technique_directory(tmp_path, monkeypatch):
    monkeypatch.setattr(run_log, "RUNS_DIR", tmp_path)

    path = run_log.save_run("zero_shot", "be concise", "analyze this", "here is the report")

    content = path.read_text()
    assert path.parent == tmp_path / "zero_shot"
    assert "=== SYSTEM PROMPT ===\nbe concise" in content
    assert "=== USER PROMPT ===\nanalyze this" in content
    assert "=== RESPONSE ===\nhere is the report" in content


def test_save_run_includes_the_label_in_the_filename_when_given(tmp_path, monkeypatch):
    monkeypatch.setattr(run_log, "RUNS_DIR", tmp_path)

    path = run_log.save_run("zero_shot", "sys", "user", "response", label="repro_temp0_runA")

    assert path.name.startswith("repro_temp0_runA_")
