from typing import Any, Dict, List
from .. import resources

class OrdersDSL:
    def get_orders(self) -> List[resources.Order]:
        return resources.Order.parse(self.request('get', 'orders/'))

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

    def delete_order(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"orders/{resource_id}").status_code == 204
