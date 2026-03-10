from typing import Any, Dict, List, Optional, Union
from .. import resources

class CreditNotesDSL:
    def get_credit_notes(self) -> List[resources.CreditNote]:
        return resources.CreditNote.parse(self.request('get', 'credit_notes/'))

    def get_credit_note(self, *, id: str) -> resources.CreditNote:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.CreditNote.parse(self.request('get', f"credit_notes/{id}"))

    def void_credit_note(self, *, id: str) -> resources.CreditNote:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.CreditNote.parse(self.request('post', f"credit_notes/{id}/void"))

    def create_credit_note(self, *, params: Dict[str, Any]) -> resources.CreditNote:
        return resources.CreditNote.parse(self.request('post', 'credit_notes/', query=params))

    def update_credit_note(self, *, id: str, params: Dict[str, Any]) -> resources.CreditNote:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.CreditNote.parse(self.request('put', f"credit_notes/{id}", query=params))

    def patch_credit_note(self, *, id: str, params: Dict[str, Any]) -> resources.CreditNote:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.CreditNote.parse(self.request('patch', f"credit_notes/{id}", query=params))

    def delete_credit_note(self, *, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"credit_notes/{id}").status_code == 204
