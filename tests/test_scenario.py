from prompting_techniques.scenario import build_business_context, load_events


def test_build_business_context_formats_each_event_as_a_labeled_block():
    events = [
        {"event_type": "Port Congestion", "region": "Asia"},
        {"event_type": "Labor Strike", "region": "Europe"},
    ]

    context = build_business_context(events)

    assert "========== Supply Chain Disruption Event 1 ==========" in context
    assert "Event Type: Port Congestion" in context
    assert "========== Supply Chain Disruption Event 2 ==========" in context
    assert "Event Type: Labor Strike" in context


def test_load_events_reads_the_shipped_sample_dataset():
    events = load_events()

    assert len(events) == 6
    assert events[0]["event_type"] == "Port Congestion"


def test_build_business_context_keeps_known_acronyms_upper_case():
    events = [{"revenue_at_risk_usd": "100"}]

    context = build_business_context(events)

    assert "Revenue At Risk USD: 100" in context
    assert "Usd" not in context
