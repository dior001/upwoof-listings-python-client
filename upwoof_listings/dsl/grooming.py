from typing import Any, Dict, List, Optional
from .. import resources

class GroomingDSL:
    """Booking a listing's grooms online on a customer's behalf. Any team member of the listing; every method
    raises ClientError (HTTP 403) when the listing doesn't offer grooming online and ResourceNotFoundError when
    the caller isn't on the listing's team."""

    def get_listing_grooming_services(self, *, listing_id: str,
                                      params: Optional[Dict[str, Any]] = None) -> List[resources.ServiceType]:
        """Active grooming services bookable online, by name; `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/grooming/services"
        return resources.ServiceType.parse(self.request('get', path, query=params))

    def get_listing_groomers(self, *, listing_id: str,
                             params: Optional[Dict[str, Any]] = None) -> List[resources.Groomer]:
        """Active groomers taking grooms, by name; `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/grooming/groomers"
        return resources.Groomer.parse(self.request('get', path, query=params))

    def get_listing_grooming_open_times(self, *, listing_id: str,
                                        params: Dict[str, Any]) -> resources.GroomingOpenTimes:
        """`date` (YYYY-MM-DD, the listing's zone), `customer_id`, `pet_ids` and `service_type_ids` required;
        `groomer_id` optional (omit for any groomer). A `deposit_cents` above 0 means
        create_listing_grooming_appointments will refuse these grooms. Raises ResourceNotFoundError for a
        customer that isn't the listing's, ValidationError (HTTP 422) for a bad pet, service or groomer, more
        than 6 grooms, or a service needing an evaluation a pet hasn't passed."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/grooming/open_times"
        return resources.GroomingOpenTimes.parse(self.request('get', path, query=params))

    def create_listing_grooming_appointments(self, *, listing_id: str,
                                             params: Dict[str, Any]) -> List[resources.GroomingAppointment]:
        """Book one groom per pet per service at `starts_at` (ISO 8601, one of the open start times):
        `customer_id`, `pet_ids`, `service_type_ids`, `starts_at` required, `groomer_id` optional. Raises
        ValidationError (HTTP 422) as get_listing_grooming_open_times does, when the time isn't open, or when
        the grooms would take a deposit (the customer books those on the listing's UpWoof profile)."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/grooming/appointments"
        return resources.GroomingAppointment.parse(self.request('post', path, query=params))
