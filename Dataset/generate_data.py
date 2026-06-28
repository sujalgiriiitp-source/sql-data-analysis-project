import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from datetime import datetime, timedelta

# Initialize Faker with Indian locale
fake = Faker('en_IN')
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Constants
NUM_CUSTOMERS = 10000
NUM_CATEGORIES = 20
NUM_SUPPLIERS = 100
NUM_EMPLOYEES = 50
NUM_PRODUCTS = 2000
NUM_ORDERS = 50000

# Directory for output
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_customers():
    print("Generating Customers...")
    data = []
    for i in range(1, NUM_CUSTOMERS + 1):
        reg_date = fake.date_between(start_date='-3y', end_date='today')
        data.append({
            'customer_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.unique.email(),
            'phone': fake.unique.phone_number()[:20],
            'address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'pin_code': fake.postcode(),
            'registration_date': reg_date
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(OUTPUT_DIR, 'customers.csv'), index=False)
    return df

def generate_categories():
    print("Generating Categories...")
    categories = [
        'Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Beauty', 
        'Sports', 'Toys', 'Automotive', 'Health', 'Grocery',
        'Furniture', 'Jewelry', 'Pet Supplies', 'Stationery', 'Garden',
        'Musical Instruments', 'Video Games', 'Luggage', 'Shoes', 'Watches'
    ]
    data = [{'category_id': i+1, 'category_name': cat} for i, cat in enumerate(categories)]
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(OUTPUT_DIR, 'categories.csv'), index=False)
    return df

def generate_suppliers():
    print("Generating Suppliers...")
    data = []
    for i in range(1, NUM_SUPPLIERS + 1):
        data.append({
            'supplier_id': i,
            'supplier_name': fake.company(),
            'contact_person': fake.name(),
            'email': fake.unique.company_email(),
            'phone': fake.unique.phone_number()[:20],
            'city': fake.city(),
            'state': fake.state()
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(OUTPUT_DIR, 'suppliers.csv'), index=False)
    return df

def generate_employees():
    print("Generating Employees...")
    departments = ['Sales', 'Support', 'IT', 'HR', 'Logistics', 'Marketing']
    data = []
    for i in range(1, NUM_EMPLOYEES + 1):
        manager_id = np.nan if i <= 5 else random.randint(1, 5) # First 5 are managers
        data.append({
            'employee_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.unique.email(),
            'phone': fake.unique.phone_number()[:20],
            'department': random.choice(departments),
            'hire_date': fake.date_between(start_date='-5y', end_date='today'),
            'salary': round(random.uniform(30000, 150000), 2),
            'manager_id': manager_id
        })
    df = pd.DataFrame(data)
    # Convert manager_id to integer type but keeping NaNs requires pandas Nullable Integer type
    df['manager_id'] = df['manager_id'].astype('Int64')
    df.to_csv(os.path.join(OUTPUT_DIR, 'employees.csv'), index=False)
    return df

def generate_products():
    print("Generating Products...")
    data = []
    for i in range(1, NUM_PRODUCTS + 1):
        data.append({
            'product_id': i,
            'product_name': fake.catch_phrase(),
            'category_id': random.randint(1, NUM_CATEGORIES),
            'supplier_id': random.randint(1, NUM_SUPPLIERS),
            'price': round(random.uniform(100, 50000), 2),
            'stock_quantity': random.randint(0, 500),
            'is_returnable': random.choices([True, False], weights=[0.8, 0.2])[0],
            'rating': round(random.uniform(1.0, 5.0), 2)
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(OUTPUT_DIR, 'products.csv'), index=False)
    return df

def generate_orders_and_related(customers_df, products_df):
    print("Generating Orders, Items, and Payments...")
    
    orders = []
    order_items = []
    payments = []
    
    order_statuses = ['Delivered', 'Delivered', 'Delivered', 'Shipped', 'Processing', 'Cancelled', 'Returned']
    payment_modes = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'COD']
    
    item_id_counter = 1
    
    customer_ids = customers_df['customer_id'].tolist()
    reg_dates = customers_df['registration_date'].tolist()
    cust_cities = customers_df['city'].tolist()
    cust_states = customers_df['state'].tolist()
    
    product_ids = products_df['product_id'].tolist()
    product_prices = products_df['price'].tolist()
    
    for order_id in range(1, NUM_ORDERS + 1):
        idx = random.randint(0, NUM_CUSTOMERS - 1)
        customer_id = customer_ids[idx]
        reg_date = reg_dates[idx]
        if isinstance(reg_date, str):
            reg_date = datetime.strptime(reg_date, '%Y-%m-%d').date()
        
        # Order date must be after registration date
        # Convert date to datetime for faker
        dt_start = datetime.combine(reg_date, datetime.min.time())
        order_date = fake.date_time_between_dates(datetime_start=dt_start)
        
        status = random.choice(order_statuses)
        
        # Generate Order Items
        num_items = random.randint(1, 5)
        order_total = 0
        
        for _ in range(num_items):
            p_idx = random.randint(0, NUM_PRODUCTS - 1)
            p_id = product_ids[p_idx]
            p_price = product_prices[p_idx]
            
            qty = random.randint(1, 3)
            total_price = qty * p_price
            
            order_items.append({
                'order_item_id': item_id_counter,
                'order_id': order_id,
                'product_id': p_id,
                'quantity': qty,
                'unit_price': p_price,
                'total_price': total_price
            })
            order_total += total_price
            item_id_counter += 1
            
        orders.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': order_date,
            'total_amount': order_total,
            'order_status': status,
            'delivery_city': cust_cities[idx],
            'delivery_state': cust_states[idx]
        })
        
        # Generate Payment
        payment_status = 'Success'
        if status == 'Cancelled':
            payment_status = random.choice(['Success', 'Failed', 'Pending'])
        elif status == 'Pending':
            payment_status = 'Pending'
            
        mode = random.choice(payment_modes)
        if mode == 'COD' and status in ['Delivered', 'Returned']:
            payment_status = 'Success'
            
        payments.append({
            'payment_id': order_id, # 1:1 relationship for simplicity
            'order_id': order_id,
            'payment_date': order_date + timedelta(minutes=random.randint(1, 60)),
            'payment_mode': mode,
            'payment_status': payment_status,
            'amount': order_total
        })

    orders_df = pd.DataFrame(orders)
    items_df = pd.DataFrame(order_items)
    payments_df = pd.DataFrame(payments)
    
    orders_df.to_csv(os.path.join(OUTPUT_DIR, 'orders.csv'), index=False)
    items_df.to_csv(os.path.join(OUTPUT_DIR, 'order_items.csv'), index=False)
    payments_df.to_csv(os.path.join(OUTPUT_DIR, 'payments.csv'), index=False)

if __name__ == "__main__":
    print("Starting Data Generation for Indian E-Commerce Project...")
    customers_df = generate_customers()
    generate_categories()
    generate_suppliers()
    generate_employees()
    products_df = generate_products()
    generate_orders_and_related(customers_df, products_df)
    print("Data Generation Complete. CSV files saved to Dataset/ directory.")
