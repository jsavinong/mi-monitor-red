CREATE TABLE IF NOT EXISTS device_health (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    "timestamp" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    cpu_usage INT,
    active_alarms VARCHAR(255)
);