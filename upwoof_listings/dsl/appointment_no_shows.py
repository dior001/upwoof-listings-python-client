from .. import resources

class AppointmentNoShowsDSL:
    """Marking a listing's appointment (groom, private lesson, facility tour, pet transport trip) a no-show, as the
    listing's board does: a scheduled or confirmed appointment whose start has passed. A deposit held for it is kept
    (`deposit_status` `forfeited`; owner/manager only, else ClientError, HTTP 403); with none held, the listing's
    no-show fee for that kind (if set) is billed on its own invoice. The customer is told. Raises
    ResourceNotFoundError for an appointment that isn't the listing's of that kind and ValidationError (HTTP 422)
    for one that can't be marked."""

    def _mark_no_show(self, listing_id: str, kind_path: str, appointment_id: str) -> resources.GroomingAppointment:
        if not appointment_id:
            raise ValueError("ID cannot be blank")
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('post', listing_id, kind_path,
                                           f"appointments/{appointment_id}/no_show", {}))

    def mark_grooming_appointment_no_show(self, *, listing_id: str,
                                          appointment_id: str) -> resources.GroomingAppointment:
        """See the class docstring."""
        return self._mark_no_show(listing_id, 'grooming', appointment_id)

    def mark_lesson_no_show(self, *, listing_id: str, appointment_id: str) -> resources.GroomingAppointment:
        """See the class docstring."""
        return self._mark_no_show(listing_id, 'lessons', appointment_id)

    def mark_tour_no_show(self, *, listing_id: str, appointment_id: str) -> resources.GroomingAppointment:
        """See the class docstring."""
        return self._mark_no_show(listing_id, 'tours', appointment_id)

    def mark_transport_no_show(self, *, listing_id: str, appointment_id: str) -> resources.GroomingAppointment:
        """See the class docstring."""
        return self._mark_no_show(listing_id, 'transports', appointment_id)
