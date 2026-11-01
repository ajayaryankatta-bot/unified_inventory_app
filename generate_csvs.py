"""
Utility script to export database tables into physical CSV files for GitHub
"""
import os
import pandas as pd
from inventory.database import SessionLocal, engine
from inventory.models import Product, SKU, Location, InventoryBalance

def export_to_csv():
    # Ensure directories exist
    os.makedirs("data/starter", exist_ok=True)
    
    session = SessionLocal()
    
    # Export Products
    df_products = pd.read_sql(session.query(Product).statement, engine)
    df_products.to_csv("data/starter/products.csv", index=False)
    
    # Export SKUs
    df_skus = pd.read_sql(session.query(SKU).statement, engine)
    df_skus.to_csv("data/starter/skus.csv", index=False)
    
    # Export Locations
    df_locs = pd.read_sql(session.query(Location).statement, engine)
    df_locs.to_csv("data/starter/locations.csv", index=False)
    
    # Export Inventory Balances
    df_bal = pd.read_sql(session.query(InventoryBalance).statement, engine)
    df_bal.to_csv("data/starter/inventory_balances.csv", index=False)
    
    session.close()
    print("Successfully generated CSV files in data/starter/!")

if __name__ == "__main__":
    export_to_csv()