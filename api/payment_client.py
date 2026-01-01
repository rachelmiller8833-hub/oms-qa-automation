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
        # Real implementation would be an HTTP request.
        # We keep it unimplemented on purpose; tests will mock it.
        raise NotImplementedError("External payment provider call is not implemented")
