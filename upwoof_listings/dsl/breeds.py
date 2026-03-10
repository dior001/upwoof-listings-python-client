from typing import List
from .. import resources

class BreedsDSL:
    def get_breeds(self) -> List[resources.Breed]:
        return resources.Breed.parse(self.request('get', 'breeds/'))

    def get_breed(self, *, resource_id: str) -> resources.Breed:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Breed.parse(self.request('get', f"breeds/{resource_id}"))
