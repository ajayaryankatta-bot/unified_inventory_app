"""
Available-to-Promise (ATP) Formula Calculation Rules
"""

def calculate_atp(on_hand: int, reserved: int, blocked: int, inbound: int) -> int:
    """
    Calculates Available-to-Promise (ATP) inventory.
    Formula: On-hand - Reserved - Blocked + Inbound
    Guardrail: Clamps at a minimum of 0.
    """
    atp = on_hand - reserved - blocked + inbound
    return max(0, atp)