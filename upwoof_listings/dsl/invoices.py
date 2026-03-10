from typing import Any, Dict, List
from .. import resources

class InvoicesDSL:
    def get_invoices(self) -> List[resources.Invoice]:
        return resources.Invoice.parse(self.request('get', 'invoices/'))

    def get_invoice(self, *, resource_id: str) -> resources.Invoice:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Invoice.parse(self.request('get', f"invoices/{resource_id}"))

    def pay_invoice_out_of_band(self, *, resource_id: str) -> resources.Invoice:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Invoice.parse(self.request('post', f"invoices/{resource_id}/pay_out_of_band"))

    def create_invoice(self, *, params: Dict[str, Any]) -> resources.Invoice:
        return resources.Invoice.parse(self.request('post', 'invoices/', query=params))

    def update_invoice(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Invoice:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Invoice.parse(self.request('put', f"invoices/{resource_id}", query=params))

    def patch_invoice(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Invoice:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Invoice.parse(self.request('patch', f"invoices/{resource_id}", query=params))

    def delete_invoice(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"invoices/{resource_id}").status_code == 204
