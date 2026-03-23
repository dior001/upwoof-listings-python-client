from typing import Any, Dict, List, Optional
from .. import resources

class AnimalTypesDSL:
    def get_animal_types(self, params: Optional[Dict[str, Any]] = None) -> List[resources.AnimalType]:
        return resources.AnimalType.parse(self.request('get', 'animal_types/', query=params))

    def get_animal_type(self, *, resource_id: str) -> resources.AnimalType:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.AnimalType.parse(self.request('get', f"animal_types/{resource_id}"))

    def create_animal_type(self, *, params: Dict[str, Any]) -> resources.AnimalType:
        return resources.AnimalType.parse(self.request('post', 'animal_types/', query=params))

    def update_animal_type(self, *, resource_id: str, params: Dict[str, Any]) -> resources.AnimalType:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.AnimalType.parse(self.request('put', f"animal_types/{resource_id}", query=params))

    def patch_animal_type(self, *, resource_id: str, params: Dict[str, Any]) -> resources.AnimalType:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.AnimalType.parse(self.request('patch', f"animal_types/{resource_id}", query=params))

    def delete_animal_type(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"animal_types/{resource_id}").status_code == 204
