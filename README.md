# Data Migration Pipeline

Data engineering project that simulates the migration of an e-commerce database from MySQL to PostgreSQL.

The project includes initial data generation, incremental synchronization, validation, testing, CI, Docker and Airflow orchestration.

## Architecture

```text
Data generation
      ↓
    MySQL
      ↓
Incremental migration
      ↓
 PostgreSQL
      ↓
  Validation
```

The daily workflow is orchestrated with Apache Airflow:

```text
initialize_data
      ↓
generate_data
      ↓
 migrate_data
      ↓
validate_data
```

## Main Features

- MySQL source database
- PostgreSQL target database
- Docker-based environment
- Initial dataset generation with Faker
- Daily data generation
- Existing customers can place new orders
- Existing orders can be updated
- Batch migration
- Idempotent PostgreSQL UPSERT
- Checkpoint-based recovery
- Incremental synchronization with `updated_at`
- Migration logging
- Data validation
- Unit tests with pytest
- CI with GitHub Actions
- Daily orchestration with Apache Airflow

## Project Structure

```text
data_migration/
├── .github/              # GitHub Actions workflows
├── audit/                # Source audit and migration documentation
├── dags/                 # Airflow DAGs
├── logs/                 # Pipeline logs
├── mysql/                # MySQL initialization scripts
├── postgres/             # PostgreSQL initialization scripts
├── src/                  # Python pipeline code
├── tests/                # Unit tests
├── .env.example          # Environment variables example
├── CHANGELOG.md
├── config.py
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
└── requirements.txt
```

## Data Model

The simulated e-commerce database contains four main tables:

- `customers`
- `products`
- `orders`
- `order_items`

The migration preserves primary keys and relationships between tables.

## Migration Strategy

The initial migration uses primary-key checkpoints to process data in batches and resume after an interruption.

After the initial migration, synchronization becomes incremental and uses the `updated_at` column to detect new or modified records.

PostgreSQL UPSERT operations make the migration idempotent.

## Airflow Pipeline

Apache Airflow orchestrates the daily pipeline.

The DAG executes:

1. Database initialization when required
2. Daily data generation
3. MySQL to PostgreSQL migration
4. Data validation

The pipeline can be monitored directly from the Airflow web interface.

## Running the Project

Clone the repository and create the environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Build and start the containers:

```bash
docker compose up -d --build
```

The main services are:

```text
MySQL      → localhost:3307
PostgreSQL → localhost:5433
Airflow    → http://localhost:8080
```

Airflow manages the daily execution of the pipeline.

## Running Tests

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest -v
```

Tests are also executed automatically by GitHub Actions when code is pushed to the repository.

## Validation

The validation step compares the source and target databases after migration.

Current checks include row-count validation for:

- customers
- products
- orders
- order_items

## Technologies

- Python
- MySQL
- PostgreSQL
- Docker
- Docker Compose
- Apache Airflow
- pytest
- GitHub Actions
- Faker

## Versioning

Project changes are documented in `CHANGELOG.md`.

Git tags are used to track major project milestones.

## Purpose

This project was built as a practical data engineering challenge to explore the complete lifecycle of a database migration pipeline: source auditing, schema mapping, migration, incremental synchronization, reliability, testing, automation and orchestration.