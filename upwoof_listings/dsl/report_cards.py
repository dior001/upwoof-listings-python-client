from typing import Any, Dict, List, Optional
from .. import resources

class ReportCardsDSL:
    def get_reservation_report_cards(self, *, reservation_id: str) -> List[resources.ReportCard]:
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        return resources.ReportCard.parse(self.request('get', f"reservations/{reservation_id}/report_cards"))

    def create_reservation_report_card(self, *, reservation_id: str, params: Dict[str, Any]) -> resources.ReportCard:
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        path = f"reservations/{reservation_id}/report_cards"
        return resources.ReportCard.parse(self.request('post', path, query=params))

    def get_listing_report_cards(self, *, listing_id: str,
                                 params: Optional[Dict[str, Any]] = None) -> List[resources.ReportCard]:
        """The cards on the listing's stays for one day, by stay then pet: optional `date` (YYYY-MM-DD, default
        today in the listing's zone), `status` (draft or published), `page`, `per_page`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.ReportCard.parse(self.request('get', f"listings/{listing_id}/report_cards", query=params))

    def start_listing_report_cards(self, *, listing_id: str,
                                   include_care_log: bool = False) -> resources.ResourceObject:
        """Start today's draft for every active pet on every checked-in stay without one (`include_care_log`
        fills them from the care log). Returns `created_count`, `skipped_count` and `date`. Raises
        ValidationError (HTTP 422) when the listing has report cards turned off."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/report_cards/start"
        return resources.ResourceObject.parse(self.request('post', path, query={'include_care_log': include_care_log}))

    def publish_listing_report_cards(self, *, listing_id: str) -> resources.ResourceObject:
        """Send every draft for today (each customer is told once). Returns `published_count` and `date`.
        Raises ValidationError (HTTP 422) when the listing has report cards turned off."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.ResourceObject.parse(self.request('post', f"listings/{listing_id}/report_cards/publish"))

    def get_report_card_photos(self, *, report_card_id: str,
                               params: Optional[Dict[str, Any]] = None) -> List[resources.ReportCardPhoto]:
        """Oldest first; `page`/`per_page` in `params`. Each `url` is valid for 15 minutes."""
        if not report_card_id:
            raise ValueError("ID cannot be blank")
        path = f"report_cards/{report_card_id}/photos"
        return resources.ReportCardPhoto.parse(self.request('get', path, query=params))

    def share_report_card_photo(self, *, report_card_id: str, photo_id: str) -> resources.ReportCardPhoto:
        """Share the photo in the listing's website photo stream (idempotent). Raises ValidationError (HTTP
        422) when the listing's photo stream is off."""
        if not report_card_id or not photo_id:
            raise ValueError("ID cannot be blank")
        path = f"report_cards/{report_card_id}/photos/{photo_id}/share"
        return resources.ReportCardPhoto.parse(self.request('post', path))

    def unshare_report_card_photo(self, *, report_card_id: str, photo_id: str) -> bool:
        """Raises ResourceNotFoundError when the photo isn't shared."""
        if not report_card_id or not photo_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"report_cards/{report_card_id}/photos/{photo_id}/share").status_code == 204
