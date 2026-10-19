from typing import Any, Dict, List, Optional
from .. import resources

class OrdersDSL:
    def get_orders(self, params: Optional[Dict[str, Any]] = None) -> List[resources.Order]:
        return resources.Order.parse(self.request('get', 'orders/', query=params))

    def get_order(self, *, resource_id: str) -> resources.Order:
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
        smaller: the order's remaining balance or the gift card's remaining balance. Raises
        a ClientError (HTTP 404) for an unknown code, or a validation error (HTTP 422) if the
        card can't be redeemed against this order."""
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
