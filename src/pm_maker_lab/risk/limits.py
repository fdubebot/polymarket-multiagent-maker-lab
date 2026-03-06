from dataclasses import dataclass


@dataclass
class RiskLimits:
    max_inventory: int = 25
    max_notional: float = 10.0

    def approve(self, inventory: int, quote_mid: float, order_size: int = 1) -> bool:
        next_inv = inventory + order_size
        if abs(next_inv) > self.max_inventory:
            return False
        next_notional = abs(next_inv) * quote_mid
        return next_notional <= self.max_notional
