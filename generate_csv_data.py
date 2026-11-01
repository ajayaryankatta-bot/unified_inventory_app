"""
CSV Data Generator for UIMS Dashboard (Seed: 20261022)
Creates files inside data/ folder.
"""
import os
import random
import numpy as np
import pandas as pd

# Set deterministic seed
random.seed(20261022)
np.random.seed(20261022)

os.makedirs("data", exist_ok=True)

# 1. Inventory Balances & Stock Levels
skus = [f"SKU-{i:06d}" for i in range(1, 101)]
locations = ["Central Warehouse A", "Asia-Pacific Hub", "European DC", "West Coast Hub", "Retail Store #12"]
loc_types = ["Warehouse", "Fulfillment Center", "Distribution Center", "Warehouse", "Retail"]

balance_data = []
for sku in skus:
    loc_idx = random.randint(0, len(locations) - 1)
    on_hand = random.randint(50, 500)
    reserved = random.randint(0, 50)
    blocked = random.randint(0, 15)
    inbound = random.randint(0, 100)
    atp = max(0, on_hand - reserved - blocked + inbound)
    balance_data.append({
        "SKU Code": sku,
        "Product ID": f"PROD-{random.randint(1000, 9999)}",
        "Location Name": locations[loc_idx],
        "Location Type": loc_types[loc_idx],
        "On-Hand Stock": on_hand,
        "Reserved Stock": reserved,
        "Blocked Stock": blocked,
        "Inbound Stock": inbound,
        "ATP": atp
    })
df_balances = pd.DataFrame(balance_data)
df_balances.to_csv("data/inventory_balances.csv", index=False)

# 2. Movement Ledger (Sample View)
m_types = ["RECEIPT", "SALE", "RETURN", "ADJUSTMENT", "TRANSFER_OUT", "TRANSFER_IN"]
ledger_data = []
for i in range(1, 1001):
    m_type = random.choice(m_types)
    delta = random.randint(1, 50) if m_type in ["RECEIPT", "RETURN", "TRANSFER_IN"] else -random.randint(1, 50)
    ledger_data.append({
        "Movement ID": f"MOV-{i:07d}",
        "Timestamp": pd.Timestamp("2026-10-22") - pd.Timedelta(minutes=random.randint(0, 10000)),
        "SKU Code": random.choice(skus),
        "Location ID": f"LOC-{random.randint(1, 10):03d}",
        "Movement Type": m_type,
        "Quantity Delta": delta,
        "Reference Document / Order ID": f"ORD-{random.randint(10000, 99999)}"
    })
df_ledger = pd.DataFrame(ledger_data)
df_ledger.to_csv("data/movement_ledger.csv", index=False)

# 3. Ground Truth Anomalies
anomaly_types = ["Negative ATP Clamped", "Expired Reservation Hold", "Dual-Counting Risk", "Stock Discrepancy"]
anomaly_data = []
for i in range(1, 126):
    anomaly_data.append({
        "Anomaly ID": f"ANO-{i:04d}",
        "SKU Code": random.choice(skus),
        "Location": random.choice(locations),
        "Anomaly Type": random.choice(anomaly_types),
        "Severity": random.choice(["HIGH", "MEDIUM", "LOW"]),
        "Detected Timestamp": pd.Timestamp("2026-10-22") - pd.Timedelta(hours=random.randint(1, 72)),
        "Status": random.choice(["UNRESOLVED", "UNDER_REVIEW", "RESOLVED"])
    })
df_anomalies = pd.DataFrame(anomaly_data)
df_anomalies.to_csv("data/ground_truth_anomalies.csv", index=False)

# 4. In-Transit Shipments
shipment_data = []
statuses = ["IN_TRANSIT", "DISPATCHED", "CUSTOMS_HOLD", "DELIVERED"]
for i in range(1, 151):
    shipment_data.append({
        "Shipment ID": f"SHP-{i:05d}",
        "Origin Facility": random.choice(locations),
        "Destination Facility": random.choice(locations),
        "SKU Code": random.choice(skus),
        "Transfer Quantity": random.randint(50, 500),
        "Dispatch Date": "2026-10-20",
        "Estimated Delivery": "2026-10-25",
        "Status": random.choice(statuses)
    })
df_shipments = pd.DataFrame(shipment_data)
df_shipments.to_csv("data/in_transit_shipments.csv", index=False)

# 5. Multi-Channel Orders
channels = ["Web Shop", "Mobile App", "B2B Wholesale", "Marketplace"]
order_statuses = ["ALLOCATED", "RESERVED", "SHIPPED", "BACKORDERED"]
order_data = []
for i in range(1, 501):
    order_data.append({
        "Order ID": f"ORD-2026-{i:05d}",
        "Channel": random.choice(channels),
        "Customer ID": f"CUST-{random.randint(1000, 9999)}",
        "SKU Code": random.choice(skus),
        "Quantity Requested": random.randint(1, 20),
        "Fulfillment Location": random.choice(locations),
        "Order Status": random.choice(order_statuses),
        "Order Timestamp": pd.Timestamp("2026-10-22") - pd.Timedelta(minutes=random.randint(0, 5000))
    })
df_orders = pd.DataFrame(order_data)
df_orders.to_csv("data/multi_channel_orders.csv", index=False)

print("Data generation complete. All 5 CSV files created in data/ directory.")