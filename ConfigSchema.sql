-- =========================
-- Table: config_settings
-- Stores key-value configurations for the ITSC product
-- =========================

CREATE TABLE config_settings (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL,
    value_type TEXT CHECK (value_type IN ('string', 'int', 'boolean', 'json', 'datetime')) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by TEXT
);

-- =========================
-- Table: audit_logs
-- Stores audit trails of changes (who did what and when)
-- =========================

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    action_type TEXT NOT NULL,                -- e.g., 'UPDATE', 'DELETE', 'INSERT'
    table_name TEXT,                          -- e.g., 'config_settings'
    record_id TEXT,                           -- ID of the affected record (as text)
    changed_by TEXT NOT NULL,                 -- username or user ID
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_data JSONB,                           -- JSON representation of old data
    new_data JSONB,                           -- JSON representation of new data
    description TEXT                          -- Optional textual description of change
);

-- =========================
-- Table: system_logs
-- Stores technical/system-level logs
-- =========================

CREATE TABLE system_logs (
    id SERIAL PRIMARY KEY,
    log_level TEXT CHECK (log_level IN ('INFO', 'WARN', 'ERROR', 'DEBUG')) NOT NULL,
    message TEXT NOT NULL,
    context JSONB,                            -- Optional structured data
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT                               -- e.g., 'auth-service', 'scheduler'
);

-- =========================
-- Table: log_settings (Optional)
-- Controls logging behavior per component
-- =========================

CREATE TABLE log_settings (
    component TEXT PRIMARY KEY,               -- e.g., 'auth-service', 'api-gateway'
    log_level TEXT CHECK (log_level IN ('INFO', 'WARN', 'ERROR', 'DEBUG')),
    is_enabled BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- Indexes for performance (optional but recommended)
-- =========================

CREATE INDEX idx_audit_logs_changed_at ON audit_logs (changed_at);
CREATE INDEX idx_system_logs_logged_at ON system_logs (logged_at);
CREATE INDEX idx_config_settings_key ON config_settings (key);

-- =========================
-- Example Triggers and Functions (optional)
-- Auto-audit changes to config_settings
-- =========================

-- Example: Function to insert audit log on config update
CREATE OR REPLACE FUNCTION log_config_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (
        action_type,
        table_name,
        record_id,
        changed_by,
        old_data,
        new_data,
        description
    )
    VALUES (
        'UPDATE',
        'config_settings',
        OLD.id::TEXT,
        CURRENT_USER,
        to_jsonb(OLD),
        to_jsonb(NEW),
        'Configuration setting updated'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to attach audit logging to updates
CREATE TRIGGER trg_config_settings_update
AFTER UPDATE ON config_settings
FOR EACH ROW
EXECUTE FUNCTION log_config_update();
