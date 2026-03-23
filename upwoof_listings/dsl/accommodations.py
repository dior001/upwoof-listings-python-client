from typing import Any, Dict, List, Optional
from .. import resources

class AccommodationsDSL:
    def get_accommodations(self, params: Optional[Dict[str, Any]] = None) -> List[resources.Accommodation]:
        return resources.Accommodation.parse(self.request('get', 'accommodations/', query=params))

    def get_accommodation(self, *, resource_id: str) -> resources.Accommodation:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Accommodation.parse(self.request('get', f"accommodations/{resource_id}"))

    def create_accommodation(self, *, params: Dict[str, Any]) -> resources.Accommodation:
        return resources.Accommodation.parse(self.request('post', 'accommodations/', query=params))

    def update_accommodation(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Accommodation:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Accommodation.parse(self.request('put', f"accommodations/{resource_id}", query=params))

    def patch_accommodation(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Accommodation:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Accommodation.parse(self.request('patch', f"accommodations/{resource_id}", query=params))

    def delete_accommodation(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"accommodations/{resource_id}").status_code == 204
