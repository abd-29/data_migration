CREATE DATABASE IF NOT EXISTS mysqldb;

USE mysqldb;


CREATE TABLE customers (
    customer_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),

    country VARCHAR(100) NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE products (
    product_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    sku VARCHAR(50) NOT NULL UNIQUE,
    product_name VARCHAR(255) NOT NULL,

    category VARCHAR(100),

    price DECIMAL(10, 2) NOT NULL,

    stock_quantity INT NOT NULL DEFAULT 0,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE orders (
    order_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    customer_id BIGINT NOT NULL,

    order_status VARCHAR(50) NOT NULL,

    total_amount DECIMAL(12, 2) NOT NULL,

    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


CREATE TABLE order_items (
    order_item_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,

    quantity INT NOT NULL,

    unit_price DECIMAL(10, 2) NOT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);