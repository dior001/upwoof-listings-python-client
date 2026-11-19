from typing import Any, Dict, List, Optional
from .. import resources

class InvoicePaymentsDSL:
    """The parts an invoice was paid in (split payments). Listing them is open to any team member of the invoice's
    listing; recording and refunding a part need owner/manager with two-factor authentication on (else ClientError,
    HTTP 403, as for an invoice that isn't open). An invoice or part that isn't reachable raises
    ResourceNotFoundError. A part's `tender` is `card_online`, `card_reader`, `cash`, `check` or `store_credit`."""

    def get_invoice_payments(self, *, invoice_id: str,
                             params: Optional[Dict[str, Any]] = None) -> List[resources.InvoicePayment]:
        """Oldest first; `page`/`per_page` in `params`."""
        if not invoice_id:
            raise ValueError("ID cannot be blank")
        return resources.InvoicePayment.parse(
            self.request('get', f"invoices/{invoice_id}/payments", query=params))

    def create_invoice_payment(self, *, invoice_id: str, params: Dict[str, Any]) -> resources.InvoicePayment:
        """Records part of an open invoice taken in cash or by check: `tender` required (`cash` or `check`),
        `amount_cents` optional (default: everything the invoice still owes). Raises ValidationError (HTTP 422) for
        a bad amount, or while a card payment is on a reader or the customer is paying online."""
        if not invoice_id:
            raise ValueError("ID cannot be blank")
        return resources.InvoicePayment.parse(
            self.request('post', f"invoices/{invoice_id}/payments", query=params))

    def refund_invoice_payment(self, *, invoice_id: str, payment_id: str,
                               params: Optional[Dict[str, Any]] = None) -> resources.InvoicePayment:
        """Refunds one part while the invoice is still open (cash or a check out of the till, a card reader part
        to its card, a store credit part given back whole); what is refunded is owed again. `amount_cents`
        optional (default: everything left to refund on the part). Returns the part after the refund. Raises
        ValidationError (HTTP 422) when the part isn't refundable, the amount is bad, a card payment is in
        progress, store credit isn't refunded whole or Stripe refused. Refund a paid invoice's part with
        `create_credit_note` and `invoice_payment_id` instead."""
        if not invoice_id or not payment_id:
            raise ValueError("ID cannot be blank")
        path = f"invoices/{invoice_id}/payments/{payment_id}/refund"
        return resources.InvoicePayment.parse(self.request('post', path, query=params))
