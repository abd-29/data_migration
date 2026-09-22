# NovaShop - Source to Target Mapping

## Table: customers

| customer_id | BIGINT AUTO_INCREMENT | customer_id | BIGINT | PRIMARY KEY, conserver l'ID source |
| first_name | VARCHAR(100) | first_name | VARCHAR(100) | NOT NULL |
| last_name | VARCHAR(100) | last_name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | email | VARCHAR(255) | NULL autorized |
| country | VARCHAR(100) | country | VARCHAR(100) | NOT NULL |
| created_at | DATETIME | created_at | TIMESTAMP | NOT NULL |
| updated_at | DATETIME | updated_at | TIMESTAMP | NOT NULL |


## Table: products

| Source MySQL | Source Type | Target PostgreSQL | Target Type | Notes                              |
|---|---|---|---|------------------------------------|
| product_id | BIGINT AUTO_INCREMENT | product_id | BIGINT | PRIMARY KEY, conserver l'ID source |
| sku | VARCHAR(50) | sku | VARCHAR(50) | UNIQUE                             |
| product_name | VARCHAR(255) | product_name | VARCHAR(255) | NOT NULL                           |
| category | VARCHAR(100) | category | VARCHAR(100) | NULL autorized                     |
| price | DECIMAL(10,2) | price | NUMERIC(10,2) | Valeur monétaire exacte            |
| stock_quantity | INT | stock_quantity | INTEGER | NOT NULL                           |
| created_at | DATETIME | created_at | TIMESTAMP | NOT NULL                           |
| updated_at | DATETIME | updated_at | TIMESTAMP | NOT NULL                           |


## Table: orders

| Source MySQL | Source Type | Target PostgreSQL | Target Type | Notes |
|---|---|---|---|---|
| order_id | BIGINT AUTO_INCREMENT | order_id | BIGINT | PRIMARY KEY, conserver l'ID source |
| customer_id | BIGINT | customer_id | BIGINT | NOT NULL, FK vers customers(customer_id) |
| order_status | VARCHAR(50) | order_status | VARCHAR(50) | NOT NULL |
| total_amount | DECIMAL(12,2) | total_amount | NUMERIC(12,2) | NOT NULL |
| order_date | DATETIME | order_date | TIMESTAMP | NOT NULL |
| updated_at | DATETIME | updated_at | TIMESTAMP | NOT NULL |



## Table: order_items

| Source MySQL | Source Type | Target PostgreSQL | Target Type | Notes |
|---|---|---|---|---|
| order_item_id | BIGINT AUTO_INCREMENT | order_item_id | BIGINT | PRIMARY KEY, conserver l'ID source |
| order_id | BIGINT | order_id | BIGINT | NOT NULL, FK vers orders(order_id) |
| product_id | BIGINT | product_id | BIGINT | NOT NULL, FK vers products(product_id) |
| quantity | INT | quantity | INTEGER | NOT NULL |
| unit_price | DECIMAL(10,2) | unit_price | NUMERIC(10,2) | NOT NULL |