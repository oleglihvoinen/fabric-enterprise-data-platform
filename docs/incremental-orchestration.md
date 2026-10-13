# Incremental orchestration contract

## Durable-watermark rule

A source watermark is **not** advanced when extraction starts. The candidate watermark is recorded with the run, but durable state advances only after Bronze persistence, Silver validation, Gold publication and required quality gates succeed.

This avoids a common failure mode where a partially failed pipeline skips source changes on retry.

## Run sequence

1. Read `pipeline_state.durable_watermark`.
2. Create a run record with a new `run_id` and candidate watermark.
3. Extract the bounded source interval.
4. Persist source-fidelity rows to Bronze with `run_id`, source timestamp and ingestion timestamp.
5. Transform into Silver using idempotent Delta `MERGE` semantics.
6. Route invalid records to the quarantine table rather than silently dropping them.
7. Build Gold only from accepted Silver records.
8. Execute quality and reconciliation checks.
9. If all required gates pass, mark the run successful and atomically advance the durable watermark.
10. On failure, leave the watermark unchanged so the same interval can be replayed.

## Fabric mapping

In Microsoft Fabric this control pattern can be implemented with Data Factory pipeline activities, a Warehouse/Lakehouse control table, notebook parameters and Delta MERGE operations. The Python module in `src/pipeline_control.py` is a locally testable representation of those state transitions.
