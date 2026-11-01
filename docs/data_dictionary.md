# Unified Inventory Management System (UIMS) - Data Dictionary

This document outlines the relational database schema, tables, columns, and data types for the Unified Inventory Management System.

## Core Entities

### 1. Product
* **`product_id`** (VARCHAR(64), Primary Key): Unique product identifier.
* **`product_name`** (VARCHAR(255), Not Null): Commercial name of the product.
* **`category`** (VARCHAR(100), Not Null): Product category (e.g., Electronics, Apparel).
* **`brand`** (VARCHAR(100)): Brand or manufacturer name.

### 2. SKU (Stock Keeping Unit)
* **`sku_id`** (VARCHAR(64), Primary Key): Unique SKU identifier.
* **`product_id`** (VARCHAR(64), Foreign Key): References `Product(product_id)`.
* **`sku_code`** (VARCHAR(100), Unique, Not Null): Stock keeping unit merchant code.
* **`barcode`** (VARCHAR(100)): EAN/UPC barcode.
* **`size`** / **`color`** (VARCHAR(50)): Variant attributes.
* **`unit_price`** (FLOAT, Not Null): Base retail unit price.
* **`weight_kg`** (FLOAT): Physical unit weight.

### 3. Location
* **`location_id`** (VARCHAR(64), Primary Key): Unique facility identifier.
* **`location_name`** (VARCHAR(255), Not Null): Facility display name.
* **`location_type`** (VARCHAR(50), Not Null): Facility classification (Warehouse, Retail Store, Dark Store, Online Channel).
* **`city`** / **`country`** (VARCHAR(100)): Geographical location.
* **`is_active`** (BOOLEAN): Operational status flag.

### 4. InventoryBalance
* **`balance_id`** (VARCHAR(64), Primary Key): Unique balance record identifier.
* **`sku_id`** (VARCHAR(64), Foreign Key): References `SKU(sku_id)`.
* **`location_id`** (VARCHAR(64), Foreign Key): References `Location(location_id)`.
* **`on_hand`** (INT): Physical stock currently inside the facility.
* **`reserved`** (INT): Stock allocated to active customer orders.
* **`blocked`** (INT): Stock quarantined for quality or damage inspection.
* **`inbound`** (INT): Stock confirmed on incoming purchase orders/transfers.
* **`safety_stock`** (INT): Minimum buffer threshold.

### 5. InventoryMovement (Immutable Ledger)
* **`movement_id`** (VARCHAR(64), Primary Key): Unique movement transaction ID.
* **`sku_id`** (VARCHAR(64), Foreign Key): References `SKU(sku_id)`.
* **`location_id`** (VARCHAR(64), Foreign Key): References `Location(location_id)`.
* **`movement_type`** (VARCHAR(50)): Transaction type (`RECEIPT`, `SALE`, `RETURN`, `TRANSFER`, `ADJUSTMENT`).
* **`quantity_change`** (INT): Delta quantity (+/-).
* **`reference_id`** (VARCHAR(64)): Source document reference (Order ID, PO ID).
* **`timestamp`** (TIMESTAMP): UTC event timestamp.