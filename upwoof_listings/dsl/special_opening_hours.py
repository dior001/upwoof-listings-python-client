from typing import Any, Dict, List, Optional
from .. import resources

class SpecialOpeningHoursDSL:
    def get_listing_special_opening_hours(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                          ) -> List[resources.SpecialOpeningHour]:
        """A listing's special-date opening hours, by date, from `from` (YYYY-MM-DD; default today in the
        listing's time zone). Times are "HH:MM" wall clock in the listing's time zone; an empty
        `pick_up_and_drop_off_windows` means the weekday's windows that fit inside the hours are offered.
        `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/special_opening_hours"
        return resources.SpecialOpeningHour.parse(self.request('get', path, query=params))
