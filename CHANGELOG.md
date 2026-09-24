# Changelog

All important changes to this project will be documented in this file.

## [v1.2.0] - Daily Data Generation and Testing

### Added
* Daily data generation for customers, orders and order items.
* Existing customers can place new orders.
* Existing order statuses can be updated.
* Incremental synchronization based on `updated_at`.
* Logging for migration and validation.
* Unit tests with pytest.

### Changed
* Migration mode now switches to incremental synchronization after the initial full migration.
* New order totals are calculated from their order items.

### Tested
* MySQL and PostgreSQL row counts remain synchronized.
* Incremental migration processes both new and updated rows.
* Core migration utility functions pass unit tests.


## [v1.1.0] - Reliable Migration Pipeline

### Added

* Batch migration with configurable batch size.
* Idempotent migration using PostgreSQL `ON CONFLICT`.
* Checkpoint system to resume interrupted migrations.
* Incremental synchronization using `updated_at`.

### Changed

* Refactored migration code to remove duplicated logic.
* Migration now supports both full migration and incremental synchronization.
* `order_items` now includes timestamp columns for incremental updates.

### Tested

* Migration can resume after an interruption.
* Updating existing rows in MySQL correctly updates PostgreSQL.
* Incremental synchronization only processes changed rows.

## [v1.0.0] - Initial Migration

### Added

* MySQL source database with Docker.
* PostgreSQL target database with Docker.
* E-commerce schema with `customers`, `products`, `orders` and `order_items`.
* Test data generation with Python and Faker.
* Initial source database audit.
* MySQL to PostgreSQL mapping documentation.
* Migration of all MySQL tables.
* Basic validation of row counts and relationships.

### Known Issues

* `orders.total_amount` may not match the total calculated from `order_items`.
* MySQL client encoding may require UTF-8 configuration.
