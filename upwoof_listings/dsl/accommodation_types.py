from typing import Any, Dict, List, Optional
from .. import resources

class AccommodationTypesDSL:
    def get_accommodation_types(self, params: Optional[Dict[str, Any]] = None) -> List[resources.AccommodationType]:
        return resources.AccommodationType.parse(self.request('get', 'accommodation_types/', query=params))

    def get_accommodation_type(self, *, resource_id: str) -> resources.AccommodationType:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.AccommodationType.parse(self.request('get', f"accommodation_types/{resource_id}"))

    def create_accommodation_type(self, *, params: Dict[str, Any]) -> resources.AccommodationType:
        return resources.AccommodationType.parse(self.request('post', 'accommodation_types/', query=params))

    def update_accommodation_type(self, *, resource_id: str, params: Dict[str, Any]) -> resources.AccommodationType:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.AccommodationType.parse(self.request('put', f"accommodation_types/{resource_id}", query=params))

    def patch_accommodation_type(self, *, resource_id: str, params: Dict[str, Any]) -> resources.AccommodationType:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.AccommodationType.parse(self.request('patch', f"accommodation_types/{resource_id}", query=params))

    def delete_accommodation_type(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"accommodation_types/{resource_id}").status_code == 204
