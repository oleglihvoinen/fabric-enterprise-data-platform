from src.pipeline_control import (
    PipelineState,
    finish_run,
    quarantine_record,
    record_counts,
    should_retry,
    start_run,
)


def test_failed_run_does_not_advance_watermark():
    state = PipelineState("customers", watermark="2026-10-01T10:00:00Z")
    run = start_run(state, "run-2", "2026-10-01T11:00:00Z")
    new_state, completed = finish_run(state, run, succeeded=False)
    assert new_state.watermark == "2026-10-01T10:00:00Z"
    assert completed.status.value == "FAILED"


def test_success_advances_watermark_only_after_completion():
    state = PipelineState("customers", watermark="2026-10-01T10:00:00Z")
    run = start_run(state, "run-2", "2026-10-01T11:00:00Z")
    new_state, _ = finish_run(state, run, succeeded=True)
    assert new_state.watermark == "2026-10-01T11:00:00Z"
    assert new_state.last_successful_run_id == "run-2"


def test_row_accounting_is_explicit():
    run = start_run(PipelineState("orders"), "r1", None)
    run = record_counts(run, 100, 98, 2)
    assert should_retry(run, max_reject_ratio=0.01) is True


def test_quarantine_preserves_original_payload_and_rule():
    q = quarantine_record({"id": "C10", "email": "bad"}, "invalid_email", "r1")
    assert q["business_key"] == "C10"
    assert q["payload"]["email"] == "bad"
    assert q["rule_id"] == "invalid_email"
