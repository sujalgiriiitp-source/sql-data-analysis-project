-- ==============================================================
-- Project: Indian E-Commerce SQL Data Analysis
-- File: schema.sql
-- Description: Creates the PostgreSQL database schema for an 
--              e-commerce platform (like Amazon/Flipkart India).
--              Normalized to 3NF with constraints and indexes.
-- ==============================================================

-- 1. DROP EXISTING TABLES (If re-running script)
DROP TABLE IF EXISTS Payments CASCADE;
DROP TABLE IF EXISTS Order_Items CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Employees CASCADE;
DROP TABLE IF EXISTS Suppliers CASCADE;
DROP TABLE IF EXISTS Categories CASCADE;
DROP TABLE IF EXISTS Customers CASCADE;


-- 2. CREATE TABLES

-- Customers Table
CREATE TABLE Customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    pin_code VARCHAR(10),
    registration_date DATE DEFAULT CURRENT_DATE
);

-- Categories Table
CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL
);

-- Suppliers Table
CREATE TABLE Suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50)
);

-- Employees Table
CREATE TABLE Employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    department VARCHAR(50),
    hire_date DATE NOT NULL,
    salary NUMERIC(10, 2) CHECK (salary > 0),
    manager_id INT REFERENCES Employees(employee_id)
);

-- Products Table
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category_id INT REFERENCES Categories(category_id) ON DELETE SET NULL,
    supplier_id INT REFERENCES Suppliers(supplier_id) ON DELETE SET NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INT NOT NULL CHECK (stock_quantity >= 0),
    is_returnable BOOLEAN DEFAULT TRUE,
    rating NUMERIC(3, 2) CHECK (rating >= 0 AND rating <= 5)
);

-- Orders Table
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customers(customer_id) ON DELETE CASCADE,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    order_status VARCHAR(30) CHECK (order_status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned')),
    delivery_city VARCHAR(50),
    delivery_state VARCHAR(50)
);

-- Order Items Table
CREATE TABLE Order_Items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES Products(product_id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    total_price NUMERIC(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- Payments Table
CREATE TABLE Payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_mode VARCHAR(30) CHECK (payment_mode IN ('Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'COD')),
    payment_status VARCHAR(20) CHECK (payment_status IN ('Success', 'Failed', 'Pending')),
    amount NUMERIC(12, 2) NOT NULL CHECK (amount >= 0)
);


-- 3. CREATE INDEXES FOR PERFORMANCE OPTIMIZATION

-- Indexes on Foreign Keys (improves JOIN performance)
CREATE INDEX idx_products_category ON Products(category_id);
CREATE INDEX idx_products_supplier ON Products(supplier_id);
CREATE INDEX idx_orders_customer ON Orders(customer_id);
CREATE INDEX idx_order_items_order ON Order_Items(order_id);
CREATE INDEX idx_order_items_product ON Order_Items(product_id);
CREATE INDEX idx_payments_order ON Payments(order_id);

-- Indexes on frequently filtered columns
CREATE INDEX idx_customers_city ON Customers(city);
CREATE INDEX idx_customers_state ON Customers(state);
CREATE INDEX idx_orders_status ON Orders(order_status);
CREATE INDEX idx_orders_date ON Orders(order_date);
CREATE INDEX idx_payments_status ON Payments(payment_status);
CREATE INDEX idx_payments_mode ON Payments(payment_mode);
