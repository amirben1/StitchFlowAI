import json
import random
from datetime import datetime, timedelta

def generate_erp_data():
    categories = ["Hoodies", "T-Shirts", "Cargo Pants", "Jeans", "Jackets", "Sneakers"]
    colors = ["Black", "White", "Red", "Blue", "Olive", "Grey"]
    sizes = ["S", "M", "L", "XL"]
    
    inventory = []
    
    # Generate 200 SKUs
    for i in range(200):
        cat = random.choice(categories)
        col = random.choice(colors)
        sz = random.choice(sizes)
        
        # Base stats
        base_cost = random.randint(10, 50)
        volume = round(random.uniform(0.005, 0.03), 4)
        
        # Historical sales (last 6 months)
        sales_history = [random.randint(5, 100) for _ in range(6)]
        
        # If it's an Olive Cargo Pant, make it trend upwards rapidly
        if cat == "Cargo Pants" and col == "Olive":
            sales_history = [10, 25, 50, 120, 300, 800]
            
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
        market_intel.append({
            "competitor": comp,
            "observed_product": random.choice(["Oversized Hoodie", "Parachute Pants", "Olive Cargo Pants", "Graphic Tees"]),
            "price_tnd": random.randint(40, 150),
            "stock_status": random.choice(["In Stock", "Low Stock", "Out of Stock", "Out of Stock"]),
            "promotion_active": random.choice([True, False, False]),
            "date_observed": (datetime.now() - timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")
        })
        
    data = {
        "competitor_pricing": market_intel,
        "customer_sentiment": [
            {"keyword": "Olive Cargo", "sentiment_score": 0.95, "mentions": 1450},
            {"keyword": "Skinny Jeans", "sentiment_score": -0.4, "mentions": 120},
            {"keyword": "Heavyweight Hoodie", "sentiment_score": 0.8, "mentions": 890}
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
