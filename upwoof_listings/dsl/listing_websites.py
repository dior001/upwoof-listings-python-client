from typing import Any, Dict
from .. import resources

class ListingWebsitesDSL:
    """A listing's UpWoof website (owner/manager only): its address, theme, palette, booking switch, own domain
    and billing status. Subscribing and cancelling happen in the listings manager."""

    def get_listing_website(self, *, listing_id: str) -> resources.ListingWebsite:
        """Raises ResourceNotFoundError when the listing has no website."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.ListingWebsite.parse(self.request('get', f"listings/{listing_id}/website"))

    def update_listing_website(self, *, listing_id: str, params: Dict[str, Any]) -> resources.ListingWebsite:
        """Changes only the fields sent: `theme` (classic, modern, playful), `palette` (`primary`, `secondary`,
        `accent` as #rrggbb; a colour sent blank goes back to the theme's own), `bookings_enabled` and
        `custom_domain` (blank detaches it). Raises ValidationError when a value is refused (or the domain,
        `custom_domain_refused`)."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.ListingWebsite.parse(self.request('patch', f"listings/{listing_id}/website", query=params))
