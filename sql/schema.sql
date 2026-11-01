-- Unified Inventory Management System - Complete MySQL DDL Schema
-- Ensure database is selected
USE inventory_db;

-- Drop existing tables in reverse order of foreign key dependencies if re-running
DROP TABLE IF EXISTS ReplenishmentRule;
DROP TABLE IF EXISTS Shipment;
DROP TABLE IF EXISTS OrderLine;
DROP TABLE IF EXISTS `Order`;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS InventoryMovement;
DROP TABLE IF EXISTS InventoryBalance;
DROP TABLE IF EXISTS SKU;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Product;

-- 1. Product Table
CREATE TABLE Product (
    product_id VARCHAR(64) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. SKU Table
CREATE TABLE SKU (
    sku_id VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(64) NOT NULL,
    sku_code VARCHAR(100) UNIQUE NOT NULL,
    barcode VARCHAR(100),
    size VARCHAR(50),
    color VARCHAR(50),
    unit_price DECIMAL(10,2) NOT NULL,
    weight_kg DECIMAL(8,3),
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Location Table
CREATE TABLE Location (
    location_id VARCHAR(64) PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    location_type VARCHAR(50) NOT NULL, -- e.g., 'Warehouse', 'Retail Store', 'Dark Store', 'Online Channel'
    city VARCHAR(100),
    country VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. InventoryBalance Table
CREATE TABLE InventoryBalance (
    balance_id VARCHAR(64) PRIMARY KEY,
    sku_id VARCHAR(64) NOT NULL,
    location_id VARCHAR(64) NOT NULL,
    on_hand INT NOT NULL DEFAULT 0,
    reserved INT NOT NULL DEFAULT 0,
    blocked INT NOT NULL DEFAULT 0,
    inbound INT NOT NULL DEFAULT 0,
    safety_stock INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_sku_location (sku_id, location_id),
    FOREIGN KEY (sku_id) REFERENCES SKU(sku_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. InventoryMovement Table
CREATE TABLE InventoryMovement (
    movement_id VARCHAR(64) PRIMARY KEY,
    sku_id VARCHAR(64) NOT NULL,
    location_id VARCHAR(64) NOT NULL,
    movement_type VARCHAR(50) NOT NULL, -- e.g., 'RECEIPT', 'SALE', 'RETURN', 'TRANSFER', 'ADJUSTMENT', 'DAMAGE'
    quantity_change INT NOT NULL,
    reference_id VARCHAR(64), -- Order ID, Transfer ID, etc.
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku_id) REFERENCES SKU(sku_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Reservation Table
CREATE TABLE Reservation (
    reservation_id VARCHAR(64) PRIMARY KEY,
    sku_id VARCHAR(64) NOT NULL,
    location_id VARCHAR(64) NOT NULL,
    order_id VARCHAR(64),
    quantity INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE', -- 'ACTIVE', 'EXPIRED', 'RELEASED', 'FULFILLED'
    expires_at DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku_id) REFERENCES SKU(sku_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Order Table
CREATE TABLE `Order` (
    order_id VARCHAR(64) PRIMARY KEY,
    channel VARCHAR(50) NOT NULL, -- 'Online', 'Store', 'Marketplace'
    customer_id VARCHAR(64),
    order_status VARCHAR(50) NOT NULL DEFAULT 'CREATED', -- 'CREATED', 'ALLOCATED', 'SHIPPED', 'CANCELLED'
    shipping_location_id VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shipping_location_id) REFERENCES Location(location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. OrderLine Table
CREATE TABLE OrderLine (
    order_line_id VARCHAR(64) PRIMARY KEY,
    order_id VARCHAR(64) NOT NULL,
    sku_id VARCHAR(64) NOT NULL,
    quantity INT NOT NULL,
    allocated_quantity INT NOT NULL DEFAULT 0,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE,
    FOREIGN KEY (sku_id) REFERENCES SKU(sku_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Shipment Table
CREATE TABLE Shipment (
    shipment_id VARCHAR(64) PRIMARY KEY,
    order_id VARCHAR(64) NOT NULL,
    source_location_id VARCHAR(64) NOT NULL,
    destination_address VARCHAR(255),
    shipment_status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'IN_TRANSIT', 'DELIVERED'
    shipped_at DATETIME,
    delivered_at DATETIME,
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
    FOREIGN KEY (source_location_id) REFERENCES Location(location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. ReplenishmentRule Table
CREATE TABLE ReplenishmentRule (
    rule_id VARCHAR(64) PRIMARY KEY,
    sku_id VARCHAR(64) NOT NULL,
    location_id VARCHAR(64) NOT NULL,
    reorder_point INT NOT NULL,
    reorder_quantity INT NOT NULL,
    safety_stock INT NOT NULL,
    FOREIGN KEY (sku_id) REFERENCES SKU(sku_id),
    FOREIGN KEY (location_id) REFERENCES Location(location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;