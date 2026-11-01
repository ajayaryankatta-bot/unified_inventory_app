"""
Unified Inventory Management System - Streamlit Dashboard Entry Point
"""
import streamlit as st
import pandas as pd
from inventory.database import SessionLocal
from inventory.models import InventoryBalance, SKU, Product, Location
from inventory.rules import calculate_atp
from inventory.generate import generate_synthetic_data

st.set_page_config(page_title="Unified Inventory Management System", layout="wide")

# Ensure data exists on startup
generate_synthetic_data()

st.title("📦 Unified Inventory Management System (UIMS)")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select View", ["Inventory Overview", "ATP Analysis"])

session = SessionLocal()

if page == "Inventory Overview":
    st.subheader("Live Inventory Balances & Stock Levels")
    data = session.query(InventoryBalance, SKU, Location).\
        join(SKU, InventoryBalance.sku_id == SKU.sku_id).\
        join(Location, InventoryBalance.location_id == Location.location_id).all()
        
    rows = []
    for bal, sku, loc in data:
        atp = calculate_atp(bal.on_hand, bal.reserved, bal.blocked, bal.inbound)
        rows.append({
            "SKU Code": sku.sku_code,
            "Location": loc.location_name,
            "On-Hand": bal.on_hand,
            "Reserved": bal.reserved,
            "Blocked": bal.blocked,
            "Inbound": bal.inbound,
            "ATP": atp
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

elif page == "ATP Analysis":
    st.subheader("Available-to-Promise (ATP) Formula Verification")
    st.latex(r"\text{ATP} = \text{On-Hand} - \text{Reserved} - \text{Blocked} + \text{Inbound}")
    st.info("ATP guardrails ensure values are strictly bounded at 0 and never drop into negative numbers.")

session.close()