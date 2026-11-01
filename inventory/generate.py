"""
Deterministic Synthetic Data Generator
"""
import random
from inventory.database import SessionLocal, engine, Base
from inventory.models import Product, SKU, Location, InventoryBalance
from inventory.config import SEED_VALUE

def generate_synthetic_data():
    """Generates starter data if the database is empty."""
    random.seed(SEED_VALUE)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    if session.query(Product).count() > 0:
        session.close()
        return "Database already populated!"

    # Create dummy sample products & locations
    loc = Location(location_id="loc_wh_01", location_name="Chicago Hub", location_type="Warehouse", city="Chicago", country="USA")
    session.add(loc)

    for i in range(1, 11):
        prod = Product(product_id=f"prod_{i:03d}", product_name=f"Product Item {i}", category="Electronics", brand="BrandX")
        session.add(prod)
        sku = SKU(sku_id=f"sku_{i:03d}", product_id=prod.product_id, sku_code=f"SKU-CODE-{i:03d}", unit_price=99.99)
        session.add(sku)
        
        balance = InventoryBalance(
            balance_id=f"bal_{i:03d}",
            sku_id=sku.sku_id,
            location_id=loc.location_id,
            on_hand=random.randint(50, 200),
            reserved=random.randint(5, 20),
            blocked=random.randint(0, 5),
            inbound=random.randint(20, 50)
        )
        session.add(balance)

    session.commit()
    session.close()
    return "Modular synthetic dataset generated successfully!"