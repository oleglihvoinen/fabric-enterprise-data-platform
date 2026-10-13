from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum


class RunStatus(str, Enum):
    STARTED = "STARTED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class PipelineState:
    pipeline_name: str
    watermark: str | None = None
    last_successful_run_id: str | None = None


@dataclass(frozen=True)
class PipelineRun:
    run_id: str
    pipeline_name: str
    started_at: datetime
    status: RunStatus = RunStatus.STARTED
    candidate_watermark: str | None = None
    source_rows: int = 0
    accepted_rows: int = 0
    rejected_rows: int = 0


def start_run(state: PipelineState, run_id: str, candidate_watermark: str | None) -> PipelineRun:
    return PipelineRun(
        run_id=run_id,
        pipeline_name=state.pipeline_name,
        started_at=datetime.now(timezone.utc),
        candidate_watermark=candidate_watermark,
    )


def record_counts(run: PipelineRun, source_rows: int, accepted_rows: int, rejected_rows: int) -> PipelineRun:
    if min(source_rows, accepted_rows, rejected_rows) < 0:
        raise ValueError("row counts cannot be negative")
    if accepted_rows + rejected_rows != source_rows:
        raise ValueError("accepted + rejected must equal source")
    return replace(
        run,
        source_rows=source_rows,
        accepted_rows=accepted_rows,
        rejected_rows=rejected_rows,
    )


def finish_run(state: PipelineState, run: PipelineRun, succeeded: bool) -> tuple[PipelineState, PipelineRun]:
    status = RunStatus.SUCCEEDED if succeeded else RunStatus.FAILED
    completed = replace(run, status=status)

    # Critical rule: a failed run never advances the durable watermark.
    if not succeeded:
        return state, completed

    return (
        replace(
            state,
            watermark=run.candidate_watermark or state.watermark,
            last_successful_run_id=run.run_id,
        ),
        completed,
    )


def should_retry(run: PipelineRun, max_reject_ratio: float = 0.02) -> bool:
    if run.source_rows == 0:
        return False
    return (run.rejected_rows / run.source_rows) > max_reject_ratio


def quarantine_record(record: dict, rule_id: str, run_id: str) -> dict:
    return {
        "run_id": run_id,
        "rule_id": rule_id,
        "business_key": record.get("id") or record.get("business_key"),
        "payload": record,
        "quarantined_at": datetime.now(timezone.utc).isoformat(),
    }
