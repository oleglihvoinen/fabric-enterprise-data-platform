# Microsoft Fabric Enterprise Data Platform

A governed **Microsoft Fabric lakehouse architecture** with medallion data layers plus an explicit incremental **pipeline control plane** for watermarks, replay, quarantine and run audit.

![Architecture](https://raw.githubusercontent.com/oleglihvoinen/oleglihvoinen.github.io/main/assets/architecture/fabric-enterprise-data-platform.png)

## Architecture

ERP / CRM / APIs / files → Data Factory → OneLake/Lakehouse Bronze → PySpark + Delta Silver → Gold facts/aggregates → semantic layer → Power BI / APIs / governed AI.

## Implemented engineering depth

- Fabric Data Factory ingestion boundary
- Bronze source-fidelity design
- PySpark/Delta Silver standardization patterns
- Gold business-model boundary
- semantic-consumption boundary
- durable pipeline watermark state
- candidate-vs-durable watermark separation
- failure rule that prevents watermark advancement after partial runs
- explicit source/accepted/rejected row accounting
- data-quality quarantine records preserving original payload and rule
- run audit/control tables
- retry decision based on reject ratio
- local unit tests for state transitions
- CI compiling notebooks and testing the control plane

## Incremental orchestration contract

The critical rule is: **a source watermark advances only after all required pipeline stages and quality gates succeed**. Failed runs leave durable state unchanged so the same interval remains replayable.

See `docs/incremental-orchestration.md` for the end-to-end control sequence.

## Repository scope

The repository implements architecture, transformation and control patterns. Provisioning a real Fabric tenant, workspace and deployment pipeline remains environment-specific.

**Technologies:** Microsoft Fabric · OneLake · Lakehouse · Data Factory · PySpark · Delta · SQL · pipeline control · watermarks · quarantine · Power BI · CI/CD
