from typing import Any, Dict, List, Optional
from .. import resources

class CreditNotesDSL:
    def get_credit_notes(self, params: Optional[Dict[str, Any]] = None) -> List[resources.CreditNote]:
        return resources.CreditNote.parse(self.request('get', 'credit_notes/', query=params))

    def get_credit_note(self, *, resource_id: str) -> resources.CreditNote:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.CreditNote.parse(self.request('get', f"credit_notes/{resource_id}"))

    def void_credit_note(self, *, resource_id: str) -> resources.CreditNote:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.CreditNote.parse(self.request('post', f"credit_notes/{resource_id}/void"))

    def create_credit_note(self, *, params: Dict[str, Any]) -> resources.CreditNote:
        """For a paid invoice taken in parts (cash, check or card reader parts), `invoice_payment_id` is required:
        the part (from `get_invoice_payments`) the refund goes back through. Omitting it, or naming more than the
        part has left to refund, raises ValidationError (HTTP 422); a part that isn't the invoice's own raises
        ResourceNotFoundError."""
        return resources.CreditNote.parse(self.request('post', 'credit_notes/', query=params))

    def delete_credit_note(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"credit_notes/{resource_id}").status_code == 204
