from typing import Any, Dict, List, Optional
from .. import resources

class ReservationsDSL:
    def get_reservations(self, params: Optional[Dict[str, Any]] = None) -> List[resources.Reservation]:
        return resources.Reservation.parse(self.request('get', 'reservations/', query=params))

    def get_reservation(self, *, resource_id: str) -> resources.Reservation:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('get', f"reservations/{resource_id}"))

    def create_reservation(self, *, params: Dict[str, Any]) -> resources.Reservation:
        return resources.Reservation.parse(self.request('post', 'reservations/', query=params))

    def update_reservation(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Reservation:
        """Update a reservation. Changing `when_reservation_start`/`when_reservation_finish` runs the
        same availability check as the listing manager, rebuilds the order and fires
        `reservation.duration_changed` (and its webhook). A refused change raises ValidationError
        (HTTP 422) with the API's reasons in `errors`."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('put', f"reservations/{resource_id}", query=params))

    def patch_reservation(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Reservation:
        """Partially update a reservation. Changing `when_reservation_start`/`when_reservation_finish` runs the
        same availability check as the listing manager, rebuilds the order and fires
        `reservation.duration_changed` (and its webhook). A refused change raises ValidationError
        (HTTP 422) with the API's reasons in `errors`."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('patch', f"reservations/{resource_id}", query=params))
