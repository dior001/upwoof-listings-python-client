from typing import Any, Dict, List, Optional
from .. import resources

class CustomersDSL:
    def get_customers(self, params: Optional[Dict[str, Any]] = None) -> List[resources.Customer]:
        return resources.Customer.parse(self.request('get', 'customers/', query=params))

    def get_customer(self, *, resource_id: str) -> resources.Customer:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Customer.parse(self.request('get', f"customers/{resource_id}"))

    def create_customer(self, *, params: Dict[str, Any]) -> resources.Customer:
        return resources.Customer.parse(self.request('post', 'customers/', query=params))

    def update_customer(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Customer:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Customer.parse(self.request('put', f"customers/{resource_id}", query=params))

    def patch_customer(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Customer:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Customer.parse(self.request('patch', f"customers/{resource_id}", query=params))

    def delete_customer(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"customers/{resource_id}").status_code == 204
