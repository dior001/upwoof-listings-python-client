from typing import Any, Dict, List, Optional
from .. import resources

class PlayYardsDSL:
    """A listing's play yards and the dogs placed in them (the playgroups board). Any team member of the
    listing; an id that isn't the listing's raises ResourceNotFoundError."""

    def get_listing_play_yards(self, *, listing_id: str,
                               params: Optional[Dict[str, Any]] = None) -> List[resources.PlayYard]:
        """Board order (sort, name); `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.PlayYard.parse(self.request('get', f"listings/{listing_id}/play_yards", query=params))

    def get_listing_play_yard(self, *, listing_id: str, play_yard_id: str) -> resources.PlayYard:
        if not listing_id or not play_yard_id:
            raise ValueError("ID cannot be blank")
        return resources.PlayYard.parse(self.request('get', f"listings/{listing_id}/play_yards/{play_yard_id}"))

    def create_listing_play_yard(self, *, listing_id: str, params: Dict[str, Any]) -> resources.PlayYard:
        """`name` and `capacity` (1-500) required; optional `calm_dogs_only`, `min_weight_lbs`,
        `max_weight_lbs`, `sort`. Raises ValidationError (HTTP 422) for a duplicate name, a bad capacity or a
        minimum weight above the maximum."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.PlayYard.parse(self.request('post', f"listings/{listing_id}/play_yards", query=params))

    def patch_listing_play_yard(self, *, listing_id: str, play_yard_id: str,
                                params: Dict[str, Any]) -> resources.PlayYard:
        """Changes only the fields sent."""
        if not listing_id or not play_yard_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/play_yards/{play_yard_id}"
        return resources.PlayYard.parse(self.request('patch', path, query=params))

    def delete_listing_play_yard(self, *, listing_id: str, play_yard_id: str) -> bool:
        """Also removes the placements in the yard."""
        if not listing_id or not play_yard_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"listings/{listing_id}/play_yards/{play_yard_id}").status_code == 204

    def get_listing_playgroup_assignments(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                          ) -> List[resources.PlaygroupAssignment]:
        """Placements overlapping a day, earliest first: optional `date` (YYYY-MM-DD, default today in the
        listing's zone), `from`/`to` ("HH:MM", both or neither) for one rotation, `pet_id`, `play_yard_id`,
        `page`, `per_page`. Each carries the board's `warnings` for the window (over_capacity, incompatible,
        isolation, temperament, size, evaluation_failed, evaluation_pending, evaluation_expired)."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/playgroup_assignments"
        return resources.PlaygroupAssignment.parse(self.request('get', path, query=params))

    def create_listing_playgroup_assignment(self, *, listing_id: str,
                                            params: Dict[str, Any]) -> resources.PlaygroupAssignment:
        """Place a dog: `reservation_id` (a checked-in stay), `pet_id` (one of its pets), `play_yard_id`,
        `starts_at` and `ends_at` (ISO 8601, within one listing-local day) required. Raises
        ResourceNotFoundError for a stay, pet or yard that isn't the listing's, ValidationError (HTTP 422)
        when the dog is already in a yard then or the times don't fit."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/playgroup_assignments"
        return resources.PlaygroupAssignment.parse(self.request('post', path, query=params))

    def patch_listing_playgroup_assignment(self, *, listing_id: str, playgroup_assignment_id: str,
                                           play_yard_id: str) -> resources.PlaygroupAssignment:
        """Move a placement to another of the listing's yards."""
        if not listing_id or not playgroup_assignment_id or not play_yard_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/playgroup_assignments/{playgroup_assignment_id}"
        return resources.PlaygroupAssignment.parse(
            self.request('patch', path, query={'play_yard_id': play_yard_id}))

    def delete_listing_playgroup_assignment(self, *, listing_id: str, playgroup_assignment_id: str) -> bool:
        if not listing_id or not playgroup_assignment_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/playgroup_assignments/{playgroup_assignment_id}"
        return self.request('delete', path).status_code == 204
