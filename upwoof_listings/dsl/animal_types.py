from typing import List
from .. import resources

class AnimalTypesDSL:
    def get_animal_types(self) -> List[resources.AnimalType]:
        return resources.AnimalType.parse(self.request('get', 'animal_types/'))

    def get_animal_type(self, *, resource_id: str) -> resources.AnimalType:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.AnimalType.parse(self.request('get', f"animal_types/{resource_id}"))
