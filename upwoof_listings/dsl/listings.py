from typing import Any, Dict, List, Optional, Union
from .. import resources

class ListingsDSL:
    def get_listings(self) -> List[resources.Listing]:
        return resources.Listing.parse(self.request('get', 'listings/'))

    def get_listing(self, id: str) -> resources.Listing:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Listing.parse(self.request('get', f"listings/{id}"))

    def create_listing(self, params: Dict[str, Any]) -> resources.Listing:
        return resources.Listing.parse(self.request('post', 'listings/', query=params))

    def update_listing(self, id: str, params: Dict[str, Any]) -> resources.Listing:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Listing.parse(self.request('put', f"listings/{id}", query=params))

    def patch_listing(self, id: str, params: Dict[str, Any]) -> resources.Listing:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Listing.parse(self.request('patch', f"listings/{id}", query=params))

    def delete_listing(self, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"listings/{id}").status_code == 204
