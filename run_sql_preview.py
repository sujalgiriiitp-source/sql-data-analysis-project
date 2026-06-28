import duckdb
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')

print("Connecting to local DuckDB and loading CSVs...")
con = duckdb.connect(database=':memory:')

# Load CSVs as tables
con.execute(f"CREATE TABLE Customers AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'customers.csv')}');")
con.execute(f"CREATE TABLE Products AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'products.csv')}');")
con.execute(f"CREATE TABLE Orders AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'orders.csv')}');")
con.execute(f"CREATE TABLE Order_Items AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'order_items.csv')}');")
con.execute(f"CREATE TABLE Categories AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'categories.csv')}');")
con.execute(f"CREATE TABLE Payments AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'payments.csv')}');")
con.execute(f"CREATE TABLE Employees AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'employees.csv')}');")
con.execute(f"CREATE TABLE Suppliers AS SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, 'suppliers.csv')}');")

print("\n--- Running Sample Queries from queries.sql ---\n")

print("1. Top 5 Categories by Total Revenue:")
q1 = """
SELECT c.category_name, SUM(oi.total_price) AS revenue
FROM Categories c
JOIN Products p ON c.category_id = p.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_name
ORDER BY revenue DESC
LIMIT 5;
"""
print(con.execute(q1).fetchdf().to_string(index=False))

print("\n2. Monthly Active Customers (MAC):")
q2 = """
WITH MonthlyCustomers AS (
    SELECT EXTRACT(MONTH FROM CAST(order_date AS TIMESTAMP)) AS month, 
           EXTRACT(YEAR FROM CAST(order_date AS TIMESTAMP)) AS year,
           COUNT(DISTINCT customer_id) AS active_customers
    FROM Orders
    GROUP BY EXTRACT(YEAR FROM CAST(order_date AS TIMESTAMP)), EXTRACT(MONTH FROM CAST(order_date AS TIMESTAMP))
)
SELECT year, month, active_customers 
FROM MonthlyCustomers 
ORDER BY year DESC, month DESC
LIMIT 5;
"""
print(con.execute(q2).fetchdf().to_string(index=False))

print("\n3. Top 3 States by Total Customers:")
q3 = """
SELECT state, COUNT(customer_id) AS total_customers
FROM Customers
GROUP BY state
ORDER BY total_customers DESC
LIMIT 3;
"""
print(con.execute(q3).fetchdf().to_string(index=False))

print("\nSQL Code execution successful!")
