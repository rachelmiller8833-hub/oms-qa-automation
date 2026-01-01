# Defines an abstraction for an external payment provider.
# Designed to be mocked in tests to simulate payment success or failure.
from dataclasses import dataclass

@dataclass
class PaymentResult:
    ok: bool
    transaction_id: str | None = None
    error: str | None = None


class PaymentClient:
    """
    Thin adapter for an external payment provider.
    In real life this would call a remote API (Stripe/PayPal/etc).
    """
    def charge(self, user_id: str, amount: float) -> PaymentResult:
        # Left unimplemented on purpose; tests are expected to mock this call.
        raise NotImplementedError("External payment provider call is not implemented")
