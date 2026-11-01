-- Unified Inventory Management System - Performance Indexes
-- Ensure database is selected
USE inventory_db;

-- 1. SKU Indexes
CREATE INDEX idx_sku_product_id ON SKU(product_id);
CREATE INDEX idx_sku_code ON SKU(sku_code);

-- 2. Inventory Balance Indexes (Critical for fast ATP and stock lookups)
CREATE INDEX idx_balance_sku_id ON InventoryBalance(sku_id);
CREATE INDEX idx_balance_location_id ON InventoryBalance(location_id);

-- 3. Inventory Movement Indexes (Optimizes audit trails and ledger queries)
CREATE INDEX idx_movement_sku_location ON InventoryMovement(sku_id, location_id);
CREATE INDEX idx_movement_timestamp ON InventoryMovement(timestamp);
CREATE INDEX idx_movement_reference ON InventoryMovement(reference_id);

-- 4. Reservation Indexes (Optimizes active hold checks and expiration cleanup)
CREATE INDEX idx_reservation_sku_location ON Reservation(sku_id, location_id);
CREATE INDEX idx_reservation_status ON Reservation(status);
CREATE INDEX idx_reservation_expiry ON Reservation(expires_at);

-- 5. Order & OrderLine Indexes (Optimizes fulfillment and allocation tracking)
CREATE INDEX idx_order_channel ON `Order`(channel);
CREATE INDEX idx_order_status ON `Order`(order_status);
CREATE INDEX idx_order_shipping_loc ON `Order`(shipping_location_id);
CREATE INDEX idx_orderline_order_id ON OrderLine(order_id);
CREATE INDEX idx_orderline_sku_id ON OrderLine(sku_id);

-- 6. Shipment Indexes (Optimizes in-transit and transfer tracking)
CREATE INDEX idx_shipment_order_id ON Shipment(order_id);
CREATE INDEX idx_shipment_source_loc ON Shipment(source_location_id);
CREATE INDEX idx_shipment_status ON Shipment(shipment_status);

-- 7. Replenishment Rule Indexes (Optimizes low-stock and reorder point detection)
CREATE INDEX idx_replenishment_sku_loc ON ReplenishmentRule(sku_id, location_id);