```markdown
# 📦 Unified Inventory Management System (UIMS)

An enterprise-grade, high-performance multi-channel stock orchestration and Available-to-Promise (ATP) engine built with **Python**, **SQLAlchemy**, and a modern **Streamlit** dark-mode dashboard. Designed and engineered for complex supply chain requirements, warehouse hierarchies, and rigorous technical evaluations.

---

## 📌 Project Overview & Business Architecture

The **Unified Inventory Management System (UIMS)** bridges physical brick-and-mortar stores, regional warehouses, and digital e-commerce channels into a single, cohesive orchestration layer. 

* **The Problem**: Traditional systems suffer from overselling, delayed reservation releases, and un-reconciled stock movements across distributed channels.
* **The Solution**: UIMS establishes an immutable ledger backbone combined with a zero-clamping Available-to-Promise (ATP) mathematical formula to guarantee absolute accuracy, data integrity, and real-time visibility.

---

## 📊 Core Features & Entities Breakdown

### Core Entities & Cardinality
1. **Product & SKU**: Master catalog definition (`SKU-000001` nomenclature). 1:N relationship with SKUs.
2. **Location**: Enterprise facility hierarchy spanning Central Warehouses, Fulfillment Centers, Dark Stores, and Retail Hubs (`LOC-000001`).
3. **InventoryBalance**: Real-time snapshot tracking On-Hand, Reserved, Blocked (quarantine), and Inbound stock.
4. **InventoryMovement**: Immutable ledger events (`MOV-2026-00000001`) tracking receipts, sales, returns, transfers, and adjustments.
5. **Reservation & Order**: Multi-channel customer orders (`ORD-2026-000001`) with timed reservations (`RES-<order-id>-01`).
6. **Shipment & ReplenishmentRule**: Inter-facility transfer tracking (`SHP-2026-000001`) and automated restocking logic.

### Core ATP Engine Formula
$$\text{ATP} = \max\left(0, \text{On-Hand} - \text{Reserved} - \text{Blocked} + \text{Inbound}\right)$$

---

## 📁 Project Folder Structure

```text
unified_inventory_management/
│
├── data/                       # Generated CSV datasets (Seed: 20261022)
│   ├── inventory_balances.csv
│   ├── movement_ledger.csv
│   ├── ground_truth_anomalies.csv
│   ├── in_transit_shipments.csv
│   └── multi_channel_orders.csv
│
├── tests/                      # Pytest verification test suite
│   └── test_uims_logic.py
│
├── generate_csv_data.py        # Deterministic synthetic data generator
├── unified_inventory_app.py    # Enterprise Streamlit dark-mode web application
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

```

---

## 🚀 Running Steps

Follow these instructions to set up, test, and run the application locally:

### 1. Clone repository

```cmd
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME

```

### 2. Create & activate virtual environment (`venv`)

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS / Linux)
source venv/bin/activate

```

### 3. Install dependencies (`pip install ...`)

```cmd
pip install streamlit pandas numpy plotly pytest sqlalchemy

```

### 4. Run data generation pipeline (`python generate_csv_data.py`)

```cmd
python generate_csv_data.py

```

*(This generates all required parent, child, movement, and ground-truth anomaly CSV datasets inside the `data/` directory).*

### 5. Run unit tests (`pytest -v`)

```cmd
pytest -v

```

### 6. Launch Streamlit UI (`streamlit run unified_inventory_app.py`)

```cmd
streamlit run unified_inventory_app.py

```



