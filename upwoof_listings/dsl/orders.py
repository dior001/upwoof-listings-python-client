from typing import Any, Dict, List, Optional
from .. import resources

class OrdersDSL:
    def get_orders(self, params: Optional[Dict[str, Any]] = None) -> List[resources.Order]:
        return resources.Order.parse(self.request('get', 'orders/', query=params))

    def get_order(self, *, resource_id: str) -> resources.Order:
        """Get an order. This includes the order a standalone grooming appointment or private lesson (no
        reservation) is billed on, at one of the caller's listings; such an order can't be changed or deleted
        through the API (ClientError, HTTP 403)."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Order.parse(self.request('get', f"orders/{resource_id}"))

    def create_order(self, *, params: Dict[str, Any]) -> resources.Order:
        return resources.Order.parse(self.request('post', 'orders/', query=params))

    def update_order(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Order:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Order.parse(self.request('put', f"orders/{resource_id}", query=params))

    def patch_order(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Order:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Order.parse(self.request('patch', f"orders/{resource_id}", query=params))

    def apply_promo_code(self, *, resource_id: str, code: str) -> resources.Order:
        """Apply a promo code to an order as a discount line item, up to the order's
        remaining balance. Raises a ClientError (HTTP 404) for an unknown code, or a
        validation error (HTTP 422) if the code can't be applied to this order."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        if not code:
            raise ValueError("Code cannot be blank")
        path = f"orders/{resource_id}/apply_promo_code"
        return resources.Order.parse(self.request('post', path, query={'code': code}))

    def redeem_gift_card(self, *, resource_id: str, code: str) -> resources.Order:
        """Redeem a gift card against an order as a discount line item, up to whichever is
        smaller: the order's remaining balance or the gift card's remaining balance.

        Raises ResourceNotFoundError (HTTP 404) for an unknown order, and for any code that isn't a
        usable gift card here: unknown, expired, used up or another listing's all get the same 404,
        so the answer never reveals which codes exist. Raises ValidationError (HTTP 422, with the
        API's messages in `errors`) only for an order-specific refusal, such as an order past the
        "new" state or a card already applied to this order."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        if not code:
            raise ValueError("Code cannot be blank")
        path = f"orders/{resource_id}/redeem_gift_card"
        return resources.Order.parse(self.request('post', path, query={'code': code}))

    def delete_order(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"orders/{resource_id}").status_code == 204
