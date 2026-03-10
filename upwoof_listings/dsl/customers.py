from typing import Any, Dict, List, Optional, Union
from .. import resources

class CustomersDSL:
    def get_customers(self) -> List[resources.Customer]:
        return resources.Customer.parse(self.request('get', 'customers/'))

    def get_customer(self, *, id: str) -> resources.Customer:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Customer.parse(self.request('get', f"customers/{id}"))

    def create_customer(self, *, params: Dict[str, Any]) -> resources.Customer:
        return resources.Customer.parse(self.request('post', 'customers/', query=params))

    def update_customer(self, *, id: str, params: Dict[str, Any]) -> resources.Customer:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Customer.parse(self.request('put', f"customers/{id}", query=params))

    def patch_customer(self, *, id: str, params: Dict[str, Any]) -> resources.Customer:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Customer.parse(self.request('patch', f"customers/{id}", query=params))

    def delete_customer(self, *, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"customers/{id}").status_code == 204
