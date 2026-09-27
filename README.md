# Microsoft Fabric Enterprise Data Platform

A portfolio/reference architecture for a governed **Microsoft Fabric lakehouse platform** using a medallion design from ingestion through semantic consumption.

![Architecture](https://raw.githubusercontent.com/oleglihvoinen/oleglihvoinen.github.io/main/assets/architecture/fabric-enterprise-data-platform.png)

## Architecture
ERP / CRM / APIs / files → Data Factory → OneLake/Lakehouse Bronze → PySpark + Delta Silver → Gold facts/aggregates → semantic model → Power BI / APIs / governed AI.

## What this repository demonstrates
- Fabric/OneLake/Lakehouse architecture
- Bronze/Silver/Gold separation
- PySpark cleansing, standardization and DQ indicators
- Delta-based transformation patterns
- Gold business aggregates
- SQL quality checks
- semantic-consumption boundary
- CI validation for notebook source files

This is a reference implementation: it does not claim that this repository provisions or deploys a live Fabric tenant.

## Production evolution
Incremental/watermark ingestion, deployment pipelines, environment/workspace separation, RBAC, lineage, monitoring, retries, data contracts, semantic-model deployment and cost/performance controls.

**Technologies:** Microsoft Fabric · OneLake · Lakehouse · Data Factory · PySpark · Delta · SQL · Power BI · semantic models · data quality
