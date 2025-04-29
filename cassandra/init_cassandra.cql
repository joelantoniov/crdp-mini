CREATE KEYSPACE crdp WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE crdp.sensor_metrics_v1 (
    region text, hour text, timestamp text,
    avg_temperature float, avg_humidity float, avg_pressure float, flood_risk float,
    PRIMARY KEY ((region, hour), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

CREATE TABLE crdp.alerts (
    region text, alert_time text, flood_risk float, alert_level text,
    PRIMARY KEY ((region), alert_time)
) WITH CLUSTERING ORDER BY (alert_time DESC);

