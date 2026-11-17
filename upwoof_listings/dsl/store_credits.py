from typing import Any, Dict, List, Optional
from .. import resources

class StoreCreditsDSL:
    def get_customer_store_credit(self, *, customer_id: str, listing_id: str) -> resources.StoreCreditAccount:
        """A customer's store credit balance usable at one of the caller's listings (or its listing group,
        when the group shares credit). A customer with no credit there yet answers a zero balance with
        `id` None. Raises ResourceNotFoundError when the listing isn't the caller's or the customer isn't
        one of its customers."""
        if not customer_id:
            raise ValueError("ID cannot be blank")
        if not listing_id:
            raise ValueError("Listing ID cannot be blank")
        path = f"customers/{customer_id}/store_credit"
        return resources.StoreCreditAccount.parse(self.request('get', path, query={'listing_id': listing_id}))

    def get_customer_store_credit_transactions(self, *, customer_id: str, listing_id: str,
                                               params: Optional[Dict[str, Any]] = None
                                               ) -> List[resources.StoreCreditTransaction]:
        """The store credit ledger behind that balance, newest first (`page`/`per_page` in `params`)."""
        if not customer_id:
            raise ValueError("ID cannot be blank")
        if not listing_id:
            raise ValueError("Listing ID cannot be blank")
        path = f"customers/{customer_id}/store_credit/transactions"
        query = {**(params or {}), 'listing_id': listing_id}
        return resources.StoreCreditTransaction.parse(self.request('get', path, query=query))

    def adjust_customer_store_credit(self, *, customer_id: str,
                                     params: Dict[str, Any]) -> resources.StoreCreditTransaction:
        """Add (positive `amount_cents`) or take back (negative) store credit, with a `reason`, at
        `listing_id`. Owner/manager with two-factor authentication on only (else ClientError, HTTP 403).
        Raises ValidationError (HTTP 422) for a zero or too-large amount, a blank or too-long reason, or
        taking back more than the balance. The customer is notified and a
        `store_credit.balance_changed` webhook is sent."""
        if not customer_id:
            raise ValueError("ID cannot be blank")
        path = f"customers/{customer_id}/store_credit/adjustments"
        return resources.StoreCreditTransaction.parse(self.request('post', path, query=params))
