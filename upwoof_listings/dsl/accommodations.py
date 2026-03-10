from typing import Any, Dict, List, Optional, Union
from .. import resources

class AccommodationsDSL:
    def get_accommodations(self) -> List[resources.Accommodation]:
        return resources.Accommodation.parse(self.request('get', 'accommodations/'))

    def get_accommodation(self, *, id: str) -> resources.Accommodation:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Accommodation.parse(self.request('get', f"accommodations/{id}"))

    def create_accommodation(self, *, params: Dict[str, Any]) -> resources.Accommodation:
        return resources.Accommodation.parse(self.request('post', 'accommodations/', query=params))

    def update_accommodation(self, *, id: str, params: Dict[str, Any]) -> resources.Accommodation:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Accommodation.parse(self.request('put', f"accommodations/{id}", query=params))

    def patch_accommodation(self, *, id: str, params: Dict[str, Any]) -> resources.Accommodation:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Accommodation.parse(self.request('patch', f"accommodations/{id}", query=params))

    def delete_accommodation(self, *, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"accommodations/{id}").status_code == 204
