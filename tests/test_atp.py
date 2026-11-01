"""
Automated Unit Tests for Available-to-Promise (ATP) Engine & Constraints
"""
import pytest
import sys
import os

# Add root directory to path to import unified_inventory_app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unified_inventory_app import calculate_atp

def test_atp_standard_calculation():
    """Test standard ATP formula: On-hand - Reserved - Blocked + Inbound"""
    assert calculate_atp(100, 20, 10, 50) == 120

def test_atp_negative_guardrail():
    """Ensure ATP never drops below zero even when commitments exceed stock"""
    assert calculate_atp(10, 20, 5, 0) == 0

def test_atp_zero_stock():
    """Test ATP calculation with zero inventory across all parameters"""
    assert calculate_atp(0, 0, 0, 0) == 0

def test_atp_high_inbound():
    """Test ATP calculation with high incoming stock and active reservations"""
    assert calculate_atp(50, 10, 5, 200) == 235