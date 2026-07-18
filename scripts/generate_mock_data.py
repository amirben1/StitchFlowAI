import json
import random
from datetime import datetime, timedelta

def generate_erp_data():
    categories = ["Linen Shirts", "Oversized Hoodies", "Cargo Pants", "Cashmere Sweaters", "Tailored Trousers", "Sneakers"]
    colors = ["Black", "White", "Navy", "Olive", "Beige", "Grey"]
    sizes = ["S", "M", "L", "XL"]
    
    inventory = []
    
    # Generate 200 SKUs
    for i in range(200):
        cat = random.choice(categories)
        col = random.choice(colors)
        sz = random.choice(sizes)
        
        # Base stats
        base_cost = random.randint(20, 120)
        volume = round(random.uniform(0.005, 0.03), 4)
        
        # Historical sales (last 6 months)
        if cat == "Linen Shirts":
            sales_history = [10, 20, 50, 150, 400, 1200]
        elif cat == "Cargo Pants":
            sales_history = [50, 70, 100, 150, 220, 300]
        elif cat == "Oversized Hoodies":
            sales_history = [800, 600, 400, 200, 100, 20]
        elif cat in ["Cashmere Sweaters", "Tailored Trousers"]:
            sales_history = [100, 105, 95, 110, 100, 98]
        else:
            sales_history = [random.randint(5, 100) for _ in range(6)]
            
        inventory.append({
            "sku": f"{cat[:3].upper()}-{col[:3].upper()}-{sz}-{i}",
            "category": cat,
            "color": col,
            "size": sz,
            "current_stock": random.randint(0, 500),
            "reorder_point": random.randint(50, 200),
            "unit_cost_tnd": base_cost,
            "volume_m3": volume,
            "sales_last_6_months": sales_history,
            "supplier_lead_time_days": random.randint(7, 45)
        })

    data = {
        "budget_tnd": 250000,
        "warehouse_capacity_m3": 1000,
        "used_capacity_m3": sum(item["current_stock"] * item["volume_m3"] for item in inventory),
        "inventory": inventory
    }
    
    with open("data/mock_erp.json", "w") as f:
        json.dump(data, f, indent=2)

def generate_market_data():
    competitors = ["Zara Tunis", "Pull&Bear Sousse", "Bershka Sfax", "Local Boutique"]
    
    market_intel = []
    for _ in range(50):
        comp = random.choice(competitors)
        product = random.choice(["Linen Shirt", "Oversized Hoodie", "Cargo Pants", "Cashmere Sweater"])
        
        if product == "Linen Shirt" or product == "Cargo Pants":
            stock = random.choice(["Low Stock", "Out of Stock", "Out of Stock"])
        elif product == "Oversized Hoodie":
            stock = random.choice(["In Stock", "In Stock", "Overstocked"])
        else:
            stock = random.choice(["In Stock", "Low Stock", "Out of Stock"])

        market_intel.append({
            "competitor": comp,
            "observed_product": product,
            "price_tnd": random.randint(40, 250),
            "stock_status": stock,
            "promotion_active": product == "Oversized Hoodie",
            "date_observed": (datetime.now() - timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")
        })
        
    data = {
        "competitor_pricing": market_intel,
        "customer_sentiment": [
            {"keyword": "Linen Shirt", "sentiment_score": 0.97, "mentions": 3450},
            {"keyword": "Cargo Pants", "sentiment_score": 0.87, "mentions": 2120},
            {"keyword": "Quiet Luxury", "sentiment_score": 0.65, "mentions": 1890},
            {"keyword": "Oversized Hoodie", "sentiment_score": -0.45, "mentions": 120}
        ]
    }
    
    with open("data/mock_local_market.json", "w") as f:
        json.dump(data, f, indent=2)

def generate_trends_data():
    data = {
        "global_trends": [
            {"style": "Gorpcore", "key_items": ["Olive Cargo Pants", "Technical Jackets"], "yoy_growth_percent": 340, "projected_peak_month": "October"},
            {"style": "Y2K Nostalgia", "key_items": ["Low-rise Jeans", "Baby Tees"], "yoy_growth_percent": 120, "projected_peak_month": "July"},
            {"style": "Quiet Luxury", "key_items": ["Cashmere Sweaters", "Tailored Trousers"], "yoy_growth_percent": 45, "projected_peak_month": "December"}
        ],
        "social_media_virality": [
            {"hashtag": "#cargopants", "views_last_7_days": "45M", "trend_vector": "up"},
            {"hashtag": "#skinnyjeans", "views_last_7_days": "1.2M", "trend_vector": "down"}
        ]
    }
    
    with open("data/mock_digital_trends.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    generate_erp_data()
    generate_market_data()
    generate_trends_data()
    print("Generated realistic mock datasets.")
