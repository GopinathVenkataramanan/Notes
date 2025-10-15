-- Table to store different CMDB sources
CREATE TABLE cmdb_source (
    source_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    api_endpoint TEXT NOT NULL,
    auth_info JSONB, -- store encrypted credentials or tokens here
    last_sync TIMESTAMPTZ
);

-- Main Configuration Item (CI) table
CREATE TABLE configuration_item (
    ci_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id INT NOT NULL REFERENCES cmdb_source(source_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    ci_type VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(50),
    owner VARCHAR(255),
    location VARCHAR(255),
    manufacturer VARCHAR(255),
    version VARCHAR(100),
    serial_number VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB, -- raw data snapshot from CMDB for audit/troubleshooting
    UNIQUE (source_id, name) -- to avoid duplicate CI names per source
);

-- Table for dynamic/custom attributes of a CI
CREATE TABLE ci_attribute (
    attribute_id SERIAL PRIMARY KEY,
    ci_id UUID NOT NULL REFERENCES configuration_item(ci_id) ON DELETE CASCADE,
    attribute_name VARCHAR(255) NOT NULL,
    attribute_value TEXT,
    data_type VARCHAR(50),
    UNIQUE (ci_id, attribute_name)
);

-- Table for CI relationships (many-to-many)
CREATE TABLE ci_relationship (
    relationship_id SERIAL PRIMARY KEY,
    source_ci_id UUID NOT NULL REFERENCES configuration_item(ci_id) ON DELETE CASCADE,
    target_ci_id UUID NOT NULL REFERENCES configuration_item(ci_id) ON DELETE CASCADE,
    relationship_type VARCHAR(100) NOT NULL,
    UNIQUE (source_ci_id, target_ci_id, relationship_type)
);

-- IT or Business Services table
CREATE TABLE service (
    service_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    service_owner VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Join table for services linked to multiple CIs (many-to-many)
CREATE TABLE service_ci_link (
    service_id UUID NOT NULL REFERENCES service(service_id) ON DELETE CASCADE,
    ci_id UUID NOT NULL REFERENCES configuration_item(ci_id) ON DELETE CASCADE,
    PRIMARY KEY (service_id, ci_id)
);

-- Table to track lifecycle events related to CIs
CREATE TABLE lifecycle_event (
    event_id SERIAL PRIMARY KEY,
    ci_id UUID NOT NULL REFERENCES configuration_item(ci_id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    details TEXT
);

-- Audit log table for sync and operations
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    operation_type VARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE
    entity_type VARCHAR(50) NOT NULL,    -- CI, Relationship, Service, etc.
    entity_id UUID,                      -- Nullable if entity is unknown
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(50) NOT NULL,         -- SUCCESS, FAILED
    message TEXT                         -- Error or informational message
);



