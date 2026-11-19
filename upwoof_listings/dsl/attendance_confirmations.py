from typing import Any, Dict, List, Optional
from .. import resources

class AttendanceConfirmationsDSL:
    """"Still coming?" requests sent to customers (read only). Any team member of the stay's listing. A request's
    `status` is `pending` (no answer), `confirmed` (coming) or `declined` (can't make it); `visit_on` is the day
    asked about for a multi-day daycare stay (one request per day), None for the whole stay, and `visit_date` is
    `visit_on` else the stay's first day."""

    def get_reservation_attendance_confirmations(self, *, reservation_id: str, params: Optional[Dict[str, Any]] = None
                                                 ) -> List[resources.AttendanceConfirmation]:
        """A stay's requests, by id; `page`/`per_page` in `params`."""
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        return resources.AttendanceConfirmation.parse(
            self.request('get', f"reservations/{reservation_id}/attendance_confirmations", query=params))

    def get_listing_attendance_confirmations(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                             ) -> List[resources.AttendanceConfirmation]:
        """A listing's requests, by id. `params`: `date` (YYYY-MM-DD: requests asking about that day, i.e.
        `visit_on` that day or a whole-stay request whose stay starts that day), `status` (`pending`, `confirmed`,
        `declined`), `page`, `per_page`. A bad date or status raises ClientError (HTTP 400)."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.AttendanceConfirmation.parse(
            self.request('get', f"listings/{listing_id}/attendance_confirmations", query=params))
