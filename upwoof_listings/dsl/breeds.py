from typing import List
from .. import resources

class BreedsDSL:
    def get_breeds(self) -> List[resources.Breed]:
        return resources.Breed.parse(self.request('get', 'breeds/'))

    def get_breed(self, *, id: str) -> resources.Breed:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Breed.parse(self.request('get', f"breeds/{id}"))
