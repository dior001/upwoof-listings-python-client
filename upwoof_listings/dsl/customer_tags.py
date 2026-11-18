from typing import Any, Dict, List, Optional
from .. import resources

class CustomerTagsDSL:
    """A listing's customer tags. Owner/manager of the listing only (a staff member gets ClientError, HTTP 403);
    a tag that isn't the listing's raises ResourceNotFoundError. Filter `get_customers` by a tag with
    `customer_tag_id`, and limit a pricing rule to tags with `customer_tag_ids`."""

    def get_listing_customer_tags(self, *, listing_id: str,
                                  params: Optional[Dict[str, Any]] = None) -> List[resources.CustomerTag]:
        """By name; `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.CustomerTag.parse(
            self.request('get', f"listings/{listing_id}/customer_tags", query=params))

    def create_listing_customer_tag(self, *, listing_id: str, params: Dict[str, Any]) -> resources.CustomerTag:
        """`name` required (at most 40, unique per listing ignoring case); `colour` optional (secondary, primary,
        info, success, warning, danger, dark; default secondary). Raises ValidationError (HTTP 422) for a blank,
        too-long or duplicate name."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.CustomerTag.parse(
            self.request('post', f"listings/{listing_id}/customer_tags", query=params))

    def patch_listing_customer_tag(self, *, listing_id: str, tag_id: str,
                                   params: Dict[str, Any]) -> resources.CustomerTag:
        """Changes only `name`/`colour` sent."""
        if not listing_id or not tag_id:
            raise ValueError("ID cannot be blank")
        return resources.CustomerTag.parse(
            self.request('patch', f"listings/{listing_id}/customer_tags/{tag_id}", query=params))

    def delete_listing_customer_tag(self, *, listing_id: str, tag_id: str) -> bool:
        """Takes the tag off every customer. Raises ValidationError (HTTP 422) while a pricing rule is limited to
        it."""
        if not listing_id or not tag_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"listings/{listing_id}/customer_tags/{tag_id}").status_code == 204

    def tag_listing_customer(self, *, listing_id: str, tag_id: str,
                             customer_id: str) -> resources.CustomerTagging:
        """Put the tag on a customer of the listing's group. Raises ValidationError (HTTP 422) when the customer
        already carries it."""
        if not listing_id or not tag_id or not customer_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/customer_tags/{tag_id}/customers"
        return resources.CustomerTagging.parse(self.request('post', path, query={'customer_id': customer_id}))

    def untag_listing_customer(self, *, listing_id: str, tag_id: str, customer_id: str) -> bool:
        """Take the tag off a customer; ResourceNotFoundError when the customer doesn't carry it."""
        if not listing_id or not tag_id or not customer_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/customer_tags/{tag_id}/customers"
        return self.request('delete', path, query={'customer_id': customer_id}).status_code == 204
