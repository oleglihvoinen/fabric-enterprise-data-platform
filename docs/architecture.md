# Architecture

1. **Ingestion** — Fabric Data Factory pipelines ingest ERP, CRM, API and file sources.
2. **Bronze** — immutable/raw Delta data is retained in OneLake/Lakehouse.
3. **Silver** — PySpark standardizes types, identifiers and reference values and adds data-quality indicators.
4. **Gold** — business-ready facts and aggregates are built for analytical consumption.
5. **Semantic layer** — reusable measures, dimensions and definitions sit above Gold.
6. **Consumption** — Power BI, APIs and governed AI/data agents use semantic/Gold assets.

Production evolution adds incremental ingestion, deployment pipelines, workspace separation, RBAC, lineage, monitoring, retries, data contracts and cost/performance controls.
