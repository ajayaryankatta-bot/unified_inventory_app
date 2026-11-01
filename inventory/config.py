"""
System Configurations, Database Credentials, and Seed Defaults
"""
import os

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "leela0708")  # Update with your MySQL password
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "inventory_db")

SEED_VALUE = 20261022