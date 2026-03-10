from typing import Any, Dict, List
from .. import resources

class PetsDSL:
    def get_pets(self) -> List[resources.Pet]:
        return resources.Pet.parse(self.request('get', 'pets/'))

    def get_pet(self, *, resource_id: str) -> resources.Pet:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Pet.parse(self.request('get', f"pets/{resource_id}"))

    def create_pet(self, *, params: Dict[str, Any]) -> resources.Pet:
        return resources.Pet.parse(self.request('post', 'pets/', query=params))

    def update_pet(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Pet:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Pet.parse(self.request('put', f"pets/{resource_id}", query=params))

    def patch_pet(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Pet:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Pet.parse(self.request('patch', f"pets/{resource_id}", query=params))

    def delete_pet(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"pets/{resource_id}").status_code == 204
