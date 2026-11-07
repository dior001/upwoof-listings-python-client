from typing import Any, Dict, List, Optional
from .. import resources

class ListingsDSL:
    def get_listings(self, params: Optional[Dict[str, Any]] = None) -> List[resources.Listing]:
        return resources.Listing.parse(self.request('get', 'listings/', query=params))

    def get_listing(self, *, resource_id: str) -> resources.Listing:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Listing.parse(self.request('get', f"listings/{resource_id}"))

    def create_listing(self, *, params: Dict[str, Any]) -> resources.Listing:
        return resources.Listing.parse(self.request('post', 'listings/', query=params))

    def update_listing(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Listing:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Listing.parse(self.request('put', f"listings/{resource_id}", query=params))

    def patch_listing(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Listing:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Listing.parse(self.request('patch', f"listings/{resource_id}", query=params))

    def delete_listing(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"listings/{resource_id}").status_code == 204

    def get_listing_capacity(self, *, listing_id: str,
                             date: Optional[str] = None) -> resources.ResourceObject:
        """Return current pet counts vs. configured capacity limits for a listing, optionally
        for a specific date (defaults to today on the server side)."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        query = {'date': date} if date else None
        return resources.ResourceObject.parse(self.request('get', f"listings/{listing_id}/capacity", query=query))
