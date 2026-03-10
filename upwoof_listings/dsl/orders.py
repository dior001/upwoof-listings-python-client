from typing import Any, Dict, List, Optional, Union
from .. import resources

class OrdersDSL:
    def get_orders(self) -> List[resources.Order]:
        return resources.Order.parse(self.request('get', 'orders/'))

    def get_order(self, *, id: str) -> resources.Order:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Order.parse(self.request('get', f"orders/{id}"))

    def create_order(self, *, params: Dict[str, Any]) -> resources.Order:
        return resources.Order.parse(self.request('post', 'orders/', query=params))

    def update_order(self, *, id: str, params: Dict[str, Any]) -> resources.Order:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Order.parse(self.request('put', f"orders/{id}", query=params))

    def patch_order(self, *, id: str, params: Dict[str, Any]) -> resources.Order:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Order.parse(self.request('patch', f"orders/{id}", query=params))

    def delete_order(self, *, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"orders/{id}").status_code == 204
