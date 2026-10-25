from prompting_techniques.techniques.structured_output import verify


def test_verify_passes_when_totals_match_the_per_event_figures():
    report = {
        "disruptions": [
            {"financial_impact_usd": 100, "revenue_at_risk_usd": 500},
            {"financial_impact_usd": 200, "revenue_at_risk_usd": 300},
        ],
        "total_financial_impact_usd": 300,
        "total_revenue_at_risk_usd": 800,
    }

    assert verify(report, expected_event_count=2) is True


def test_verify_fails_when_a_stated_total_does_not_match():
    report = {
        "disruptions": [
            {"financial_impact_usd": 100, "revenue_at_risk_usd": 500},
            {"financial_impact_usd": 200, "revenue_at_risk_usd": 300},
        ],
        "total_financial_impact_usd": 999,
        "total_revenue_at_risk_usd": 800,
    }

    assert verify(report, expected_event_count=2) is False


def test_verify_fails_when_event_count_does_not_match():
    report = {
        "disruptions": [{"financial_impact_usd": 100, "revenue_at_risk_usd": 500}],
        "total_financial_impact_usd": 100,
        "total_revenue_at_risk_usd": 500,
    }

    assert verify(report, expected_event_count=2) is False
