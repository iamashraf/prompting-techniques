from prompting_techniques.techniques.self_consistency import extract_total


def test_extract_total_finds_the_computed_sum_after_the_equals_sign():
    report = (
        "## Reasoning\n"
        "- Total Financial Impact: $850,000 + $1,200,000 + $2,100,000 "
        "+ $220,000 + $45,000 + $310,000 = $4,725,000\n"
        "## Report\n"
        "The total financial impact of these disruptions is $4,725,000."
    )

    assert extract_total(report) == "4,725,000"


def test_extract_total_returns_none_when_no_total_is_stated():
    report = "## Reasoning\nNo combined or total figures are explicitly stated.\n"

    assert extract_total(report) is None
