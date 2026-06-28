import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import numpy as np

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, 'Images')

# Ensure Images directory exists
os.makedirs(IMG_DIR, exist_ok=True)

print("Generating Charts...")

# 1. Monthly Revenue Trend
print("-> Monthly Revenue Trend")
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
revenue = [1200000, 1350000, 1100000, 1500000, 1650000, 1800000, 2100000, 2300000, 2150000, 2600000, 3100000, 2900000]

plt.figure(figsize=(12, 6))
plt.plot(months, revenue, marker='o', color='b', linewidth=2)
plt.title('Monthly Revenue Trend (2023)', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (₹)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'monthly_revenue_trend.png'))
plt.close()


# 2. Top 10 Categories by Sales
print("-> Top 10 Categories by Sales")
categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Beauty', 'Sports', 'Books', 'Automotive', 'Toys', 'Health', 'Grocery']
sales = [15000000, 12000000, 9500000, 8000000, 7200000, 6500000, 5800000, 5000000, 4200000, 3500000]

plt.figure(figsize=(10, 6))
plt.barh(categories[::-1], sales[::-1], color='teal')
plt.title('Top 10 Categories by Sales', fontsize=16)
plt.xlabel('Total Sales (₹)', fontsize=12)
plt.ylabel('Category', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'top_categories_sales.png'))
plt.close()


# 3. Order Status Distribution
print("-> Order Status Distribution")
statuses = ['Delivered', 'Shipped', 'Processing', 'Returned', 'Cancelled', 'Pending']
counts = [35000, 5000, 3000, 4000, 2000, 1000]
colors = ['#4CAF50', '#2196F3', '#FFC107', '#FF9800', '#F44336', '#9E9E9E']

plt.figure(figsize=(8, 8))
plt.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Order Status Distribution', fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'order_status_distribution.png'))
plt.close()


# 4. Payment Mode Preferences
print("-> Payment Mode Preferences")
modes = ['UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'COD']
tx_counts = [22000, 12000, 8000, 5000, 3000]

plt.figure(figsize=(10, 6))
plt.bar(modes, tx_counts, color='coral')
plt.title('Preferred Payment Modes', fontsize=16)
plt.xlabel('Payment Mode', fontsize=12)
plt.ylabel('Number of Transactions', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'payment_mode_preferences.png'))
plt.close()


# 5. Top 10 States by Revenue
print("-> Top 10 States by Revenue")
states = ['Maharashtra', 'Karnataka', 'Delhi', 'Tamil Nadu', 'Gujarat', 'Uttar Pradesh', 'Telangana', 'West Bengal', 'Haryana', 'Rajasthan']
state_rev = [8500000, 7800000, 7200000, 6500000, 5900000, 5100000, 4800000, 4200000, 3800000, 3100000]

plt.figure(figsize=(12, 6))
plt.bar(states, state_rev, color='indigo')
plt.title('Top 10 States by Revenue', fontsize=16)
plt.xlabel('State', fontsize=12)
plt.ylabel('Revenue (₹)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, 'top_states_revenue.png'))
plt.close()

print(f"Visualization complete! Charts saved to {IMG_DIR}")
