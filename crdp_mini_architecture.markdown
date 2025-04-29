# CRDP-Net Mini Architecture

## Overview
This is a scaled-down version of CRDP-Net, handling 50GB/day across 5 regions (Jakarta, NYC, London, Sydney, SaoPaulo). It uses the same technologies (Kafka, Cassandra, Spark, Airflow, Prometheus, Grafana) and follows best practices for a production-ready system.

## Architecture Components
- **Regions**: 5 (one per continent).
- **Kafka**: 1 broker, 1 Zookeeper, 5 topics (one per region), 2 partitions per topic.
- **Cassandra**: 15 nodes (3 per region).
- **Spark**: 1 cluster (1 master + 3 workers).
- **Orchestration**: Airflow with 5 DAGs.
- **Monitoring**: Prometheus and Grafana.

## Implementation Steps

### 1. Deploy Kafka and Zookeeper
- Deploy Zookeeper and Kafka broker.
- Create topics: `crdp-sensors-jakarta`, `crdp-sensors-nyc`, etc.

### 2. Deploy Cassandra Cluster
- Use `deploy_cassandra.sh` to deploy 15 nodes.
- Create `crdp` keyspace and tables with replication factor 3 per region.

### 3. Deploy Spark Cluster
- Deploy 1 Spark cluster with 1 master and 3 workers.
- Update `streaming_job.py` to process all 5 topics.

### 4. Implement Orchestration
- Deploy Airflow and generate DAGs for all regions.
- Test the workflow via the Airflow UI.

### 5. Test the Pipeline
- Run the pipeline and verify data in Cassandra for all regions.

### 6. Monitoring and Governance
- Deploy Prometheus and Grafana.
- Add TTL to tables (30 days).

### 7. Make Accessible Online
- Deploy on AWS EC2.
- Expose ports for Kafka, Cassandra, Spark UI, Airflow UI, and Grafana.
- Share public URLs with stakeholders.

## Best Practices
- **Fault Tolerance**: Kafka topics and Cassandra keyspace use replication.
- **Scalability**: Scripts automate deployment for easy scaling.
- **Monitoring**: Prometheus and Grafana provide visibility from day one.
- **Governance**: TTL ensures efficient storage management.