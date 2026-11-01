"""
SQLAlchemy ORM Models for Core Entities
"""
from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey
from inventory.database import Base

class Product(Base):
    __tablename__ = "Product"
    product_id = Column(String(64), primary_key=True)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    brand = Column(String(100))

class SKU(Base):
    __tablename__ = "SKU"
    sku_id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("Product.product_id"))
    sku_code = Column(String(100), unique=True, nullable=False)
    barcode = Column(String(100))
    size = Column(String(50))
    color = Column(String(50))
    unit_price = Column(Float, nullable=False)
    weight_kg = Column(Float)

class Location(Base):
    __tablename__ = "Location"
    location_id = Column(String(64), primary_key=True)
    location_name = Column(String(255), nullable=False)
    location_type = Column(String(50), nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    is_active = Column(Boolean, default=True)

class InventoryBalance(Base):
    __tablename__ = "InventoryBalance"
    balance_id = Column(String(64), primary_key=True)
    sku_id = Column(String(64), ForeignKey("SKU.sku_id"))
    location_id = Column(String(64), ForeignKey("Location.location_id"))
    on_hand = Column(Integer, default=0)
    reserved = Column(Integer, default=0)
    blocked = Column(Integer, default=0)
    inbound = Column(Integer, default=0)
    safety_stock = Column(Integer, default=0)