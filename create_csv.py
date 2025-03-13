import csv
import random
from datetime import datetime, timedelta

# Define parameters
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
total_records = 15000
product_categories = ['Electronics', 'Clothing', 'Home', 'Sports']
regions = ['North', 'South', 'East', 'West', 'Central']

# Function to generate a random date between start and end date
def random_date(start, end):
    delta = end - start
    random_days = random.randrange(delta.days + 1)
    return start + timedelta(days=random_days)

# Simulate a pool of customer IDs (e.g., 3000 unique customers)
customer_pool = [f"CUST{str(i).zfill(4)}" for i in range(1, 3000)]

# Dictionary to track purchase counts per customer (for repeat buyer logic)
customer_purchases = {}

with open('customer_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header row with additional column for exogenous data (inventory_index)
    writer.writerow([
        "purchase_id", 
        "customer_id", 
        "purchase_date", 
        "purchase_amount", 
        "product_category", 
        "repeat_buyer", 
        "customer_segment", 
        "promotion_flag", 
        "region",
        "inventory_index"
    ])
    
    for i in range(100001, 100001 + total_records):
        # Randomly select a customer
        customer_id = random.choice(customer_pool)
        purchase_date = random_date(start_date, end_date)
        
        # Simulate seasonal promotions (increased chance in November, December, and June)
        promotion_flag = 1 if purchase_date.month in [11, 12, 6] and random.random() < 0.7 else 0
        
        # Calculate a base purchase amount and apply a seasonal boost if promotion applies
        base_amount = random.uniform(20, 200)
        if promotion_flag:
            base_amount *= 1.1
        purchase_amount = round(base_amount, 2)
        
        # Randomly select a product category
        product_category = random.choice(product_categories)
        
        # Update repeat buyer count for the customer
        if customer_id in customer_purchases:
            customer_purchases[customer_id] += 1
        else:
            customer_purchases[customer_id] = 0
        repeat_buyer = customer_purchases[customer_id]
        
        # Determine customer segment based on purchase count and amount
        if repeat_buyer >= 3 or purchase_amount > 150:
            customer_segment = 'High Value'
        elif repeat_buyer > 0:
            customer_segment = 'Occasional'
        else:
            customer_segment = 'New'
        
        # Randomly assign a region
        region = random.choice(regions)
        
        # Simulate an inventory_index as an exogenous factor.
        # This could represent the available inventory or a related metric.
        # Here, we simulate it as a random float that may also be used to analyze
        # trends when aggregated over time.
        inventory_index = round(random.uniform(50, 200), 2)
        
        # Write the record row including the inventory_index
        writer.writerow([
            i,
            customer_id,
            purchase_date.strftime('%Y-%m-%d'),
            purchase_amount,
            product_category,
            repeat_buyer,
            customer_segment,
            promotion_flag,
            region,
            inventory_index
        ])

print("CSV file 'customer_data.csv' has been generated successfully.")
