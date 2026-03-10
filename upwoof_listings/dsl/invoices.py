from typing import Any, Dict, List, Optional, Union
from .. import resources

class InvoicesDSL:
    def get_invoices(self) -> List[resources.Invoice]:
        return resources.Invoice.parse(self.request('get', 'invoices/'))

    def get_invoice(self, *, id: str) -> resources.Invoice:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Invoice.parse(self.request('get', f"invoices/{id}"))

    def pay_invoice_out_of_band(self, *, id: str) -> resources.Invoice:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Invoice.parse(self.request('post', f"invoices/{id}/pay_out_of_band"))

    def create_invoice(self, *, params: Dict[str, Any]) -> resources.Invoice:
        return resources.Invoice.parse(self.request('post', 'invoices/', query=params))

    def update_invoice(self, *, id: str, params: Dict[str, Any]) -> resources.Invoice:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Invoice.parse(self.request('put', f"invoices/{id}", query=params))

    def patch_invoice(self, *, id: str, params: Dict[str, Any]) -> resources.Invoice:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Invoice.parse(self.request('patch', f"invoices/{id}", query=params))

    def delete_invoice(self, *, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"invoices/{id}").status_code == 204
