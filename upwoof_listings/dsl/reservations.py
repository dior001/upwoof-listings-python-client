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
        """Book a confirmed stay, as a team member booking it would: the optional `accommodation_id`
        (else the best fit for the pet), the day's first drop-off and last pick-up window, and its order.
        A stay that can't be booked (an inactive pet, a full or closed unit, the daily dog or cat limit, a
        restricted breed, a missing evaluation, another listing's accommodation) raises ValidationError
        (HTTP 422, its error code and message say why) and nothing is created."""
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

    def update_reservation_unit_assignment(self, *, reservation_id: str, unit_assignment_id: str,
                                           accommodation_unit_id: Optional[str] = None
                                           ) -> resources.ReservationAccommodationAssignment:
        """Place one of a stay's `accommodation_assignments` in a physical unit (run or kennel) of its
        accommodation, or, with no `accommodation_unit_id`, take it out of its unit. Any team member of the
        stay's listing. Raises ResourceNotFoundError for a stay that isn't at the caller's listings, an assignment
        that isn't the stay's, or a unit that isn't an active unit of its accommodation, and ValidationError
        (HTTP 422, "The unit is taken by another stay on some of these nights") when another stay holds the unit
        on any of this stay's nights."""
        if not reservation_id or not unit_assignment_id:
            raise ValueError("ID cannot be blank")
        path = f"reservations/{reservation_id}/unit_assignments/{unit_assignment_id}"
        return resources.ReservationAccommodationAssignment.parse(
            self.request('patch', path, query={'accommodation_unit_id': accommodation_unit_id}))

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
