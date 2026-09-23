# Changelog

All important changes to this project will be documented in this file.

# Changelog

All important changes to this project will be documented in this file.

## [v1.1.0] - Batch Migration and Refactoring

### Added

* Batch migration with a configurable batch size.
* Idempotent migrations using PostgreSQL `ON CONFLICT`.
* Update of existing rows during migration.
* Generic `migrate_table()` function.
* Shared database connection functions.
* Centralized migration queries for all tables.

### Changed

* Replaced `fetchall()` with `fetchmany()` for batch processing.
* Refactored the migration code 

### Tested

* Re-running the `customers` migration keeps the same number of rows.
* Updating a customer in MySQL correctly updates the same customer in PostgreSQL.
* Batch migration works for all existing tables


## **v1.0.0 - Initial Migration**

### Added

* MySQL source database with Docker.
* PostgreSQL target database with Docker.
* E-commerce database schema with: customers, products, orders and order_items
* Test data generation with Python and Faker.
* Initial audit of the MySQL source database.
* MySQL to PostgreSQL mapping documentation.
* Migration of all mysql tables
* Source IDs and foreign key relationships are preserved during migration.
* Basic validation of row counts and relationships.

### Known Issues

* Migration scripts are not idempotent yet.
* Data is loaded in memory with `fetchall()`.
* No batch processing yet.
* No checkpoint system yet.
* `orders.total_amount` may not match the total calculated from `order_items`.
* MySQL client encoding may require UTF-8 configuration.
