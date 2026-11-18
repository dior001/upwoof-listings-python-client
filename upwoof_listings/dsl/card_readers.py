from typing import Any, Dict, List, Optional
from .. import resources

class CardReadersDSL:
    """A listing's Stripe Terminal card readers and the in-person payments taken on them. Any team member of
    the listing lists readers and takes payments; registering or removing a reader needs the owner/manager
    tier with two-factor authentication on (ClientError, HTTP 403, otherwise)."""

    def get_listing_card_readers(self, *, listing_id: str,
                                 params: Optional[Dict[str, Any]] = None) -> List[resources.CardReader]:
        """By label; `page`/`per_page` in `params`. `status`/`online` are as Stripe last reported them."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/card_readers"
        return resources.CardReader.parse(self.request('get', path, query=params))

    def create_listing_card_reader(self, *, listing_id: str, params: Dict[str, Any]) -> resources.CardReader:
        """Register a reader: `label` and `registration_code` (shown on the reader) required. Raises
        ValidationError (HTTP 422) when Stripe refuses the code or the listing can't take card payments."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/card_readers"
        return resources.CardReader.parse(self.request('post', path, query=params))

    def delete_listing_card_reader(self, *, listing_id: str, card_reader_id: str) -> bool:
        """Raises ResourceNotFoundError for an unknown reader, ValidationError (HTTP 422) when Stripe fails."""
        if not listing_id or not card_reader_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"listings/{listing_id}/card_readers/{card_reader_id}").status_code == 204

    def create_invoice_terminal_payment(self, *, listing_id: str, invoice_id: str,
                                        card_reader_id: str) -> resources.TerminalPayment:
        """Send an open invoice's balance to one of the listing's readers (status `processing`). Raises
        ResourceNotFoundError when the invoice or reader isn't the listing's, ValidationError (HTTP 422) when
        there's nothing to collect, it's already on a reader or paid, or Stripe refuses."""
        return self._create_terminal_payment(listing_id, 'invoices', invoice_id, card_reader_id)

    def get_invoice_terminal_payment(self, *, listing_id: str, invoice_id: str) -> resources.TerminalPayment:
        """The invoice's reader payment, refreshed from Stripe while `processing`; ResourceNotFoundError when
        none was started."""
        return self._get_terminal_payment(listing_id, 'invoices', invoice_id)

    def cancel_invoice_terminal_payment(self, *, listing_id: str, invoice_id: str) -> resources.TerminalPayment:
        """Take the payment off the reader; ValidationError (HTTP 422) when Stripe can't cancel it."""
        return self._cancel_terminal_payment(listing_id, 'invoices', invoice_id)

    def create_retail_sale_terminal_payment(self, *, listing_id: str, retail_sale_id: str,
                                            card_reader_id: str) -> resources.TerminalPayment:
        """As create_invoice_terminal_payment, for a shop sale rung up as `card_present`."""
        return self._create_terminal_payment(listing_id, 'retail_sales', retail_sale_id, card_reader_id)

    def get_retail_sale_terminal_payment(self, *, listing_id: str,
                                         retail_sale_id: str) -> resources.TerminalPayment:
        return self._get_terminal_payment(listing_id, 'retail_sales', retail_sale_id)

    def cancel_retail_sale_terminal_payment(self, *, listing_id: str,
                                            retail_sale_id: str) -> resources.TerminalPayment:
        return self._cancel_terminal_payment(listing_id, 'retail_sales', retail_sale_id)

    def _create_terminal_payment(self, listing_id, payables, payable_id, card_reader_id):
        if not listing_id or not payable_id or not card_reader_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/{payables}/{payable_id}/terminal_payment"
        return resources.TerminalPayment.parse(self.request('post', path, query={'card_reader_id': card_reader_id}))

    def _get_terminal_payment(self, listing_id, payables, payable_id):
        if not listing_id or not payable_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/{payables}/{payable_id}/terminal_payment"
        return resources.TerminalPayment.parse(self.request('get', path))

    def _cancel_terminal_payment(self, listing_id, payables, payable_id):
        if not listing_id or not payable_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/{payables}/{payable_id}/terminal_payment/cancel"
        return resources.TerminalPayment.parse(self.request('post', path))
