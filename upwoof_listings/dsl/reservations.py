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
        """Create a reservation. An inactive (deactivated) `pet_id` raises ValidationError (HTTP 422,
        "Inactive pets can't be booked: <name>") and nothing is created."""
        return resources.Reservation.parse(self.request('post', 'reservations/', query=params))

    def update_reservation(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Reservation:
        """Update a reservation. Changing `when_reservation_start`/`when_reservation_finish` runs the
        same availability check as the listing manager, rebuilds the order and fires
        `reservation.duration_changed` (and its webhook). A refused change raises ValidationError
        (HTTP 422) with the API's reasons in `errors`. So does a reservation whose every pet is inactive
        (deactivated); its dates are left unchanged."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('put', f"reservations/{resource_id}", query=params))

    def patch_reservation(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Reservation:
        """Partially update a reservation. Changing `when_reservation_start`/`when_reservation_finish` runs the
        same availability check as the listing manager, rebuilds the order and fires
        `reservation.duration_changed` (and its webhook). A refused change raises ValidationError
        (HTTP 422) with the API's reasons in `errors`. So does a reservation whose every pet is inactive
        (deactivated); its dates are left unchanged."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('patch', f"reservations/{resource_id}", query=params))

    def cancel_reservation(self, *, resource_id: str, reason: str, mode: Optional[str] = None) -> resources.Reservation:
        """Cancel an awaiting_review or confirmed reservation on the listing's own behalf: a phone
        cancellation, or an off-platform booking with no customer login to cancel it themselves. `mode`
        apply_policy (the default) applies the listing's own cancellation policy, exactly as a customer
        self-cancelling would; `mode` full_refund (owner/manager only) overrides it and refunds any
        deposit paid in full, regardless of the cancellation window. Raises ValidationError (HTTP 422) if
        the cancellation itself is refused (e.g. an unrefunded payment blocks it), with the API's reasons
        in `errors`."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        if not reason:
            raise ValueError("Reason cannot be blank")
        params: Dict[str, Any] = {'reason': reason}
        if mode:
            params['mode'] = mode
        return resources.Reservation.parse(self.request('post', f"reservations/{resource_id}/cancel", query=params))
