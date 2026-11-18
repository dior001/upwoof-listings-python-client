from typing import Any, Dict, List, Optional
from .. import resources

class PetsDSL:
    def get_pets(self, params: Optional[Dict[str, Any]] = None) -> List[resources.Pet]:
        return resources.Pet.parse(self.request('get', 'pets/', query=params))

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

    def deactivate_pet(self, *, resource_id: str, deactivation_reason: str) -> resources.Pet:
        """Mark a pet inactive (passed away, rehomed or other): `deactivation_reason` is one of passed_away,
        rehomed, other. Upcoming stays a recurring schedule booked for this pet alone that still await review
        are cancelled. Raises ValidationError (HTTP 422) when the pet is already inactive."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        if not deactivation_reason:
            raise ValueError("Deactivation reason cannot be blank")
        path = f"pets/{resource_id}/deactivation"
        return resources.Pet.parse(self.request('post', path, query={'deactivation_reason': deactivation_reason}))

    def reactivate_pet(self, *, resource_id: str) -> resources.Pet:
        """Make an inactive pet active again. Raises ValidationError (HTTP 422) when it is already active."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Pet.parse(self.request('delete', f"pets/{resource_id}/deactivation"))
