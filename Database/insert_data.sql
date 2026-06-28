-- ==============================================================
-- Project: Indian E-Commerce SQL Data Analysis
-- File: insert_data.sql
-- Description: Loads data from CSV files into the PostgreSQL 
--              database using the COPY command.
-- Note: Replace '/path/to/dataset/' with the actual absolute path
--       where your CSV files are located before running.
-- ==============================================================

-- 1. Load Customers
COPY Customers(customer_id, first_name, last_name, email, phone, address, city, state, pin_code, registration_date)
FROM '/path/to/dataset/customers.csv'
DELIMITER ','
CSV HEADER;

-- 2. Load Categories
COPY Categories(category_id, category_name)
FROM '/path/to/dataset/categories.csv'
DELIMITER ','
CSV HEADER;

-- 3. Load Suppliers
COPY Suppliers(supplier_id, supplier_name, contact_person, email, phone, city, state)
FROM '/path/to/dataset/suppliers.csv'
DELIMITER ','
CSV HEADER;

-- 4. Load Employees
COPY Employees(employee_id, first_name, last_name, email, phone, department, hire_date, salary, manager_id)
FROM '/path/to/dataset/employees.csv'
DELIMITER ','
CSV HEADER;

-- 5. Load Products
COPY Products(product_id, product_name, category_id, supplier_id, price, stock_quantity, is_returnable, rating)
FROM '/path/to/dataset/products.csv'
DELIMITER ','
CSV HEADER;

-- 6. Load Orders
COPY Orders(order_id, customer_id, order_date, total_amount, order_status, delivery_city, delivery_state)
FROM '/path/to/dataset/orders.csv'
DELIMITER ','
CSV HEADER;

-- 7. Load Order_Items
COPY Order_Items(order_item_id, order_id, product_id, quantity, unit_price, total_price)
FROM '/path/to/dataset/order_items.csv'
DELIMITER ','
CSV HEADER;

-- 8. Load Payments
COPY Payments(payment_id, order_id, payment_date, payment_mode, payment_status, amount)
FROM '/path/to/dataset/payments.csv'
DELIMITER ','
CSV HEADER;

-- Reset Sequences (Since we inserted data with explicit IDs, we need to update the sequences for SERIAL columns)
SELECT setval('customers_customer_id_seq', (SELECT MAX(customer_id) FROM Customers));
SELECT setval('categories_category_id_seq', (SELECT MAX(category_id) FROM Categories));
SELECT setval('suppliers_supplier_id_seq', (SELECT MAX(supplier_id) FROM Suppliers));
SELECT setval('employees_employee_id_seq', (SELECT MAX(employee_id) FROM Employees));
SELECT setval('products_product_id_seq', (SELECT MAX(product_id) FROM Products));
SELECT setval('orders_order_id_seq', (SELECT MAX(order_id) FROM Orders));
SELECT setval('order_items_order_item_id_seq', (SELECT MAX(order_item_id) FROM Order_Items));
SELECT setval('payments_payment_id_seq', (SELECT MAX(payment_id) FROM Payments));
