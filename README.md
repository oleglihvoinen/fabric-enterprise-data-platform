# Microsoft Fabric Enterprise Data Platform

An enterprise-grade **Microsoft Fabric lakehouse architecture** built around governed medallion layers from source ingestion through semantic consumption.

![Architecture](https://raw.githubusercontent.com/oleglihvoinen/oleglihvoinen.github.io/main/assets/architecture/fabric-enterprise-data-platform.png)

## Executive summary

The platform separates ingestion, source-fidelity storage, standardization, business modeling and semantic consumption into explicit architectural layers. This reduces coupling between source systems and analytics, improves lineage, and creates a stable foundation for Power BI, APIs and governed AI consumers.

## Architecture

ERP / CRM / APIs / files → Data Factory → OneLake/Lakehouse Bronze → PySpark + Delta Silver → Gold facts/aggregates → semantic model → Power BI / APIs / governed AI.

## Engineering design

- Fabric Data Factory ingestion boundary
- OneLake/Lakehouse Bronze source-fidelity layer
- PySpark transformations for standardization and validation
- Delta-based Silver models with data-quality indicators
- Gold business aggregates and dimensional structures
- SQL post-build quality checks
- semantic boundary for reusable business definitions
- CI validation for notebook source files

## Layer responsibilities

**Bronze** preserves source-oriented data with minimal transformation.  
**Silver** standardizes structure, identifiers, text values and quality indicators.  
**Gold** exposes business-ready facts, dimensions and aggregates.  
**Semantic consumption** provides consistent measures and definitions to Power BI, APIs and AI services.

## Enterprise hardening

A production deployment would add incremental/watermark ingestion, retry and idempotency controls, deployment pipelines, workspace/environment separation, RBAC, sensitivity controls, lineage, monitoring, semantic-model deployment automation and cost/performance governance.

## Repository scope

The repository implements transformation and architecture patterns. Provisioning and deployment of a live Microsoft Fabric tenant remain environment-specific concerns outside the repository.

**Technologies:** Microsoft Fabric · OneLake · Lakehouse · Data Factory · PySpark · Delta · SQL · Power BI · semantic models · data quality · CI/CD
