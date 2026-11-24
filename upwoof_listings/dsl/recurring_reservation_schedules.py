from typing import Any, Dict, List, Optional
from .. import resources

class RecurringReservationSchedulesDSL:
    """Recurring bookings: a customer's pets booked into one unit on the same weekdays every 1 to 4 weeks. Reading
    needs a team member of the schedule's listing (a schedule elsewhere raises ResourceNotFoundError); creating and
    changing, stopping or skipping dates needs a team member allowed to manage the listing's recurring bookings (else
    ClientError, HTTP 403). A schedule set up over the API confirms its dates itself when they fit. `weekdays` are
    `monday` to `sunday`; `interval` is 1, 2, 3 or 4 (weeks). A bad weekday or interval raises ClientError
    (HTTP 400)."""

    def get_recurring_reservation_schedules(self, params: Optional[Dict[str, Any]] = None
                                            ) -> List[resources.RecurringReservationSchedule]:
        """Schedules at the caller's listings, by id. `params`: `active`, `customer_id`, `listing_id`, `page`,
        `per_page`."""
        return resources.RecurringReservationSchedule.parse(
            self.request('get', 'recurring_reservation_schedules', query=params))

    def get_recurring_reservation_schedule(self, *, resource_id: str) -> resources.RecurringReservationSchedule:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.RecurringReservationSchedule.parse(
            self.request('get', f"recurring_reservation_schedules/{resource_id}"))

    def create_recurring_reservation_schedule(self, *, params: Dict[str, Any]
                                              ) -> resources.RecurringReservationSchedule:
        """`listing_id`, `customer_id`, `accommodation_id`, `pet_ids`, `weekdays` and `start_date` (YYYY-MM-DD,
        today or later in the listing's zone) required; `interval` (default 1) and `end_date` optional. The first
        four weeks of dates are booked at once as reservations awaiting review, and the customer is emailed one
        confirmation. Raises ResourceNotFoundError for a listing, customer or unit that isn't among the caller's
        listings and ValidationError (HTTP 422) for pets that aren't the customer household's active pets, a start
        in the past, and other refusals."""
        return resources.RecurringReservationSchedule.parse(
            self.request('post', 'recurring_reservation_schedules', query=params))

    def patch_recurring_reservation_schedule(self, *, resource_id: str, params: Dict[str, Any]
                                             ) -> resources.RecurringReservationSchedule:
        """Changes only the fields sent: `weekdays`, `interval`, `pet_ids`, `end_date` (None or blank clears it).
        Upcoming dates the schedule no longer books that are awaiting review, or confirmed themselves and haven't
        started, are cancelled, and new dates are
        booked at once. Raises ValidationError (HTTP 422) for a refused change or a stopped schedule ("This
        recurring booking has been stopped")."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.RecurringReservationSchedule.parse(
            self.request('patch', f"recurring_reservation_schedules/{resource_id}", query=params))

    def deactivate_recurring_reservation_schedule(self, *, resource_id: str
                                                  ) -> resources.RecurringReservationSchedule:
        """Stop the schedule (`active` False). Its stays still awaiting review, and those that confirmed
        themselves and haven't started, are cancelled free of charge; stays someone confirmed by hand are left.
        The customer is told. Raises ValidationError (HTTP 422) when it is already stopped."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.RecurringReservationSchedule.parse(
            self.request('post', f"recurring_reservation_schedules/{resource_id}/deactivate", query={}))

    def skip_recurring_reservation_schedule_date(self, *, resource_id: str, date: str
                                                 ) -> resources.RecurringReservationSchedule:
        """Skip one date (YYYY-MM-DD) the schedule books within the next 90 days (the listing's zone); it is added
        to `skipped_dates`, and a stay booked on it that is still awaiting review or confirmed itself is cancelled
        free of charge. Raises ValidationError (HTTP 422) for any other date or a stopped schedule."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        if not date:
            raise ValueError("Date cannot be blank")
        return resources.RecurringReservationSchedule.parse(
            self.request('post', f"recurring_reservation_schedules/{resource_id}/skipped_dates",
                         query={'date': str(date)}))

    def restore_recurring_reservation_schedule_date(self, *, resource_id: str, date: str
                                                    ) -> resources.RecurringReservationSchedule:
        """Restore a skipped date (YYYY-MM-DD); it is booked again straight away when within the next four weeks.
        Raises ValidationError (HTTP 422) when the date isn't skipped or the schedule is stopped."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        if not date:
            raise ValueError("Date cannot be blank")
        return resources.RecurringReservationSchedule.parse(
            self.request('delete', f"recurring_reservation_schedules/{resource_id}/skipped_dates/{date}"))
