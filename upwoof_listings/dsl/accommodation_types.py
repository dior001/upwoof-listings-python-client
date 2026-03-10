from typing import List
from .. import resources

class AccommodationTypesDSL:
    def get_accommodation_types(self) -> List[resources.AccommodationType]:
        return resources.AccommodationType.parse(self.request('get', 'accommodation_types/'))

    def get_accommodation_type(self, *, id: str) -> resources.AccommodationType:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.AccommodationType.parse(self.request('get', f"accommodation_types/{id}"))
