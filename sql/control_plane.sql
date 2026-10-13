-- Control-plane tables for a Fabric Warehouse or SQL analytics endpoint.
-- These tables separate durable pipeline state from individual run history.

create table if not exists pipeline_state (
    pipeline_name varchar(200) not null,
    durable_watermark varchar(200),
    last_successful_run_id varchar(100),
    updated_at datetime2,
    constraint pk_pipeline_state primary key (pipeline_name)
);

create table if not exists pipeline_run_audit (
    run_id varchar(100) not null,
    pipeline_name varchar(200) not null,
    started_at datetime2 not null,
    completed_at datetime2,
    status varchar(20) not null,
    candidate_watermark varchar(200),
    source_rows bigint,
    accepted_rows bigint,
    rejected_rows bigint,
    git_sha varchar(100),
    constraint pk_pipeline_run_audit primary key (run_id)
);

create table if not exists data_quality_quarantine (
    run_id varchar(100) not null,
    rule_id varchar(200) not null,
    business_key varchar(300),
    payload varchar(max),
    quarantined_at datetime2 not null
);
