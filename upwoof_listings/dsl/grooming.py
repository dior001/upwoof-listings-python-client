from typing import Any, Dict, List, Optional
from .. import resources

class GroomingDSL:
    """Booking a listing's appointments on a customer's behalf: grooms (`grooming`), private lessons (`lessons`),
    facility tours (`tours`) and pet transport trips (`transports`). Any team member of the listing; every
    method but the appointments lists raises ClientError (HTTP 403) when the listing doesn't offer that kind
    online, and every method raises ResourceNotFoundError when the caller isn't on the listing's team.

    Open times: `date` (YYYY-MM-DD, the listing's zone), `customer_id` and `service_type_ids` required, `pet_ids`
    required for every kind but tours (a tour has no pet), `groomer_id` optional (omit for any provider), and for
    grooms and lessons `pay_with_membership_credits` (pay with the customer's household's membership credits, one a
    groom or lesson, from plans whose `credit_uses` include `grooming` or `lessons`; no deposit is then taken). A
    `deposit_cents` above 0 means the booking will be held for a deposit.

    Booking: the open-times params without `date`, plus `starts_at` (ISO 8601, one of the open start times);
    optional `success_url`/`cancel_url` (full https addresses, at most 2000 characters; the success URL may carry
    Stripe's `{CHECKOUT_SESSION_ID}`) are where the customer returns from a deposit payment. A booking that takes
    a deposit comes back `pending_payment` (`deposit_status` `pending`) with a `checkout_url` to send the
    customer to; paying makes it `scheduled`, an expired or failed payment cancels it. Raises ValidationError
    (HTTP 422) for a bad pet, service or provider, too many appointments, a time that isn't open, a needed
    evaluation a pet hasn't passed, a transport pickup address missing, not enough membership credits (`no_credit`), or
    Stripe refusing to start the payment (nothing booked).

    Appointment lists: optional `customer_id`, `ids`, `status` (scheduled, confirmed, in_progress, completed,
    cancelled, pending_payment, no_show: a booked appointment the customer never came to), `page`, `per_page`;
    newest start first, `checkout_url` always None."""

    def _appointment_kind_request(self, method: str, listing_id: str, kind_path: str, action: str,
                                  params: Optional[Dict[str, Any]]):
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return self.request(method, f"listings/{listing_id}/{kind_path}/{action}", query=params)

    # Grooming

    def get_listing_grooming_services(self, *, listing_id: str,
                                      params: Optional[Dict[str, Any]] = None) -> List[resources.ServiceType]:
        """Active grooming services bookable online, by name; `page`/`per_page` in `params`."""
        return resources.ServiceType.parse(
            self._appointment_kind_request('get', listing_id, 'grooming', 'services', params))

    def get_listing_groomers(self, *, listing_id: str,
                             params: Optional[Dict[str, Any]] = None) -> List[resources.Groomer]:
        """Active groomers taking grooms, by name; `page`/`per_page` in `params`."""
        return resources.Groomer.parse(
            self._appointment_kind_request('get', listing_id, 'grooming', 'groomers', params))

    def get_listing_grooming_open_times(self, *, listing_id: str,
                                        params: Dict[str, Any]) -> resources.GroomingOpenTimes:
        """See the class docstring for the params (`pay_with_membership_credits` optional). Raises
        ResourceNotFoundError for a customer that isn't the listing's and ValidationError (HTTP 422) for a bad pet,
        service or groomer, too many grooms, a service needing an evaluation a pet hasn't passed, or not enough
        membership credits."""
        return resources.GroomingOpenTimes.parse(
            self._appointment_kind_request('get', listing_id, 'grooming', 'open_times', params))

    def create_listing_grooming_appointments(self, *, listing_id: str,
                                             params: Dict[str, Any]) -> List[resources.GroomingAppointment]:
        """Book one groom per pet per service; see the class docstring."""
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('post', listing_id, 'grooming', 'appointments', params))

    def get_listing_grooming_appointments(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                          ) -> List[resources.GroomingAppointment]:
        """The listing's grooms; see the class docstring for the filters."""
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('get', listing_id, 'grooming', 'appointments', params))

    # Private lessons

    def get_listing_lesson_services(self, *, listing_id: str,
                                    params: Optional[Dict[str, Any]] = None) -> List[resources.ServiceType]:
        """Active private lesson services bookable online, by name; `page`/`per_page` in `params`."""
        return resources.ServiceType.parse(
            self._appointment_kind_request('get', listing_id, 'lessons', 'services', params))

    def get_listing_trainers(self, *, listing_id: str,
                             params: Optional[Dict[str, Any]] = None) -> List[resources.Groomer]:
        """Active trainers taking private lessons, by name; `page`/`per_page` in `params`."""
        return resources.Groomer.parse(
            self._appointment_kind_request('get', listing_id, 'lessons', 'trainers', params))

    def get_listing_lesson_open_times(self, *, listing_id: str,
                                      params: Dict[str, Any]) -> resources.GroomingOpenTimes:
        """See the class docstring; `pay_with_membership_credits` optional."""
        return resources.GroomingOpenTimes.parse(
            self._appointment_kind_request('get', listing_id, 'lessons', 'open_times', params))

    def create_listing_lesson_appointments(self, *, listing_id: str,
                                           params: Dict[str, Any]) -> List[resources.GroomingAppointment]:
        """Book private lessons; see the class docstring."""
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('post', listing_id, 'lessons', 'appointments', params))

    def get_listing_lesson_appointments(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                        ) -> List[resources.GroomingAppointment]:
        """The listing's private lessons; see the class docstring for the filters."""
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('get', listing_id, 'lessons', 'appointments', params))

    # Facility tours (no pet)

    def get_listing_tour_services(self, *, listing_id: str,
                                  params: Optional[Dict[str, Any]] = None) -> List[resources.ServiceType]:
        """Active tour services bookable online, by name; `page`/`per_page` in `params`."""
        return resources.ServiceType.parse(
            self._appointment_kind_request('get', listing_id, 'tours', 'services', params))

    def get_listing_tour_hosts(self, *, listing_id: str,
                               params: Optional[Dict[str, Any]] = None) -> List[resources.Groomer]:
        """Active tour hosts, by name; `page`/`per_page` in `params`."""
        return resources.Groomer.parse(
            self._appointment_kind_request('get', listing_id, 'tours', 'hosts', params))

    def get_listing_tour_open_times(self, *, listing_id: str,
                                    params: Dict[str, Any]) -> resources.GroomingOpenTimes:
        """See the class docstring; no `pet_ids` (a tour has no pet)."""
        return resources.GroomingOpenTimes.parse(
            self._appointment_kind_request('get', listing_id, 'tours', 'open_times', params))

    def create_listing_tour_appointments(self, *, listing_id: str,
                                         params: Dict[str, Any]) -> List[resources.GroomingAppointment]:
        """Book facility tours (no `pet_ids`; the appointment's `pet_id` is None); see the class docstring."""
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('post', listing_id, 'tours', 'appointments', params))

    def get_listing_tour_appointments(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                      ) -> List[resources.GroomingAppointment]:
        """The listing's facility tours; see the class docstring for the filters."""
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('get', listing_id, 'tours', 'appointments', params))

    # Pet transport

    def get_listing_transport_services(self, *, listing_id: str,
                                       params: Optional[Dict[str, Any]] = None) -> List[resources.ServiceType]:
        """Active pet transport services bookable online, by name (with `per_km_surcharge_cents`)."""
        return resources.ServiceType.parse(
            self._appointment_kind_request('get', listing_id, 'transports', 'services', params))

    def get_listing_transport_drivers(self, *, listing_id: str,
                                      params: Optional[Dict[str, Any]] = None) -> List[resources.Groomer]:
        """Active drivers, by name; `page`/`per_page` in `params`."""
        return resources.Groomer.parse(
            self._appointment_kind_request('get', listing_id, 'transports', 'drivers', params))

    def get_listing_transport_open_times(self, *, listing_id: str,
                                         params: Dict[str, Any]) -> resources.GroomingOpenTimes:
        """See the class docstring."""
        return resources.GroomingOpenTimes.parse(
            self._appointment_kind_request('get', listing_id, 'transports', 'open_times', params))

    def create_listing_transport_appointments(self, *, listing_id: str,
                                              params: Dict[str, Any]) -> List[resources.GroomingAppointment]:
        """Book one pet transport trip; see the class docstring. Also takes a pickup (`pickup_address_id`, one of
        the customer's saved addresses, or typed `pickup_street_address`, `pickup_city`,
        `pickup_apartment_or_suite`, `pickup_state_or_province`, `pickup_zip_or_postal_code`,
        `pickup_country_code`; typed wins) and an optional drop-off (`dropoff_*`, the same six; blank means the
        listing)."""
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('post', listing_id, 'transports', 'appointments', params))

    def get_listing_transport_appointments(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                           ) -> List[resources.GroomingAppointment]:
        """The listing's pet transport trips; see the class docstring for the filters."""
        return resources.GroomingAppointment.parse(
            self._appointment_kind_request('get', listing_id, 'transports', 'appointments', params))
