from typing import Any, Dict, List, Optional
from .. import resources

class BreedsDSL:
    def get_breeds(self, params: Optional[Dict[str, Any]] = None) -> List[resources.Breed]:
        return resources.Breed.parse(self.request('get', 'breeds/', query=params))

    def get_breed(self, *, resource_id: str) -> resources.Breed:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Breed.parse(self.request('get', f"breeds/{resource_id}"))

    def create_breed(self, *, params: Dict[str, Any]) -> resources.Breed:
        return resources.Breed.parse(self.request('post', 'breeds/', query=params))

    def update_breed(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Breed:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Breed.parse(self.request('put', f"breeds/{resource_id}", query=params))

    def patch_breed(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Breed:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Breed.parse(self.request('patch', f"breeds/{resource_id}", query=params))

    def delete_breed(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"breeds/{resource_id}").status_code == 204
