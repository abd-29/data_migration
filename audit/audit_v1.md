NOVASHOP — SOURCE DATA AUDIT

Database
--------
MySQL 8
Database: mysqldb

Volumes
-------
customers       5,000
products          500
orders         20,000
order_items    60,088

DQ findings
-----------
DQ-001
51 customers have NULL email addresses.

DQ-002
43 email values are duplicated.

DQ-003
orders.total_amount does not match
SUM(order_items.quantity * unit_price).

DQ-004
Character display issue detected.
Database uses utf8mb4 but client session uses latin1.

Migration risks
---------------
- Monetary reconciliation
- Duplicate customer identifiers by email
- NULL handling
- Character encoding
- Referential integrity