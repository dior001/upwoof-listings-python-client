from typing import Any, Dict, List, Optional, Union
from .. import resources

class PetsDSL:
    def get_pets(self) -> List[resources.Pet]:
        return resources.Pet.parse(self.request('get', 'pets/'))

    def get_pet(self, *, id: str) -> resources.Pet:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Pet.parse(self.request('get', f"pets/{id}"))

    def create_pet(self, *, params: Dict[str, Any]) -> resources.Pet:
        return resources.Pet.parse(self.request('post', 'pets/', query=params))

    def update_pet(self, *, id: str, params: Dict[str, Any]) -> resources.Pet:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Pet.parse(self.request('put', f"pets/{id}", query=params))

    def patch_pet(self, *, id: str, params: Dict[str, Any]) -> resources.Pet:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Pet.parse(self.request('patch', f"pets/{id}", query=params))

    def delete_pet(self, *, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"pets/{id}").status_code == 204
