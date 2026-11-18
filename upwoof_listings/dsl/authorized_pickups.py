from typing import Any, Dict, List, Optional
from .. import resources

class AuthorizedPickupsDSL:
    """The people a customer has authorised to collect their pets. Any team member (admin or staff) of
    `listing_id`, which every method needs; the customer must be in that listing's (group's) customer directory,
    else ResourceNotFoundError."""

    def get_customer_authorized_pickups(self, *, customer_id: str, listing_id: str,
                                        params: Optional[Dict[str, Any]] = None
                                        ) -> List[resources.AuthorizedPickup]:
        """By name, every pickup the listing's group holds for the same person; `page`/`per_page` in `params`."""
        if not customer_id or not listing_id:
            raise ValueError("ID cannot be blank")
        query = {**(params or {}), 'listing_id': listing_id}
        return resources.AuthorizedPickup.parse(
            self.request('get', f"customers/{customer_id}/authorized_pickups", query=query))

    def get_customer_authorized_pickup(self, *, customer_id: str, authorized_pickup_id: str,
                                       listing_id: str) -> resources.AuthorizedPickup:
        if not customer_id or not authorized_pickup_id or not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"customers/{customer_id}/authorized_pickups/{authorized_pickup_id}"
        return resources.AuthorizedPickup.parse(self.request('get', path, query={'listing_id': listing_id}))

    def create_customer_authorized_pickup(self, *, customer_id: str,
                                          params: Dict[str, Any]) -> resources.AuthorizedPickup:
        """`listing_id` and `name` (at most 100) required; `relationship` (60), `phone` (40), `notes` (500)
        optional. Raises ValidationError (HTTP 422) for a blank or too-long value."""
        if not customer_id:
            raise ValueError("ID cannot be blank")
        return resources.AuthorizedPickup.parse(
            self.request('post', f"customers/{customer_id}/authorized_pickups", query=params))

    def patch_customer_authorized_pickup(self, *, customer_id: str, authorized_pickup_id: str,
                                         params: Dict[str, Any]) -> resources.AuthorizedPickup:
        """`listing_id` required; changes only the other fields sent (`name`, `relationship`, `phone`,
        `notes`)."""
        if not customer_id or not authorized_pickup_id:
            raise ValueError("ID cannot be blank")
        path = f"customers/{customer_id}/authorized_pickups/{authorized_pickup_id}"
        return resources.AuthorizedPickup.parse(self.request('patch', path, query=params))

    def delete_customer_authorized_pickup(self, *, customer_id: str, authorized_pickup_id: str,
                                          listing_id: str) -> bool:
        if not customer_id or not authorized_pickup_id or not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"customers/{customer_id}/authorized_pickups/{authorized_pickup_id}"
        return self.request('delete', path, query={'listing_id': listing_id}).status_code == 204
