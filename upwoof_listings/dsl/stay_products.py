from typing import Any, Dict, List, Optional
from .. import resources

class StayProductsDSL:
    """Shop products added to a stay's bill. Any team member of the listing; a reservation, product or item that
    isn't reachable raises ResourceNotFoundError."""

    def get_listing_stay_products(self, *, listing_id: str,
                                  params: Optional[Dict[str, Any]] = None) -> List[resources.StayProduct]:
        """Active products priced in the listing's currency, by name; `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.StayProduct.parse(
            self.request('get', f"listings/{listing_id}/stay_products", query=params))

    def get_reservation_retail_items(self, *, reservation_id: str, params: Optional[Dict[str, Any]] = None
                                     ) -> List[resources.ReservationRetailItem]:
        """In the order added; `page`/`per_page` in `params`."""
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        return resources.ReservationRetailItem.parse(
            self.request('get', f"reservations/{reservation_id}/retail_items", query=params))

    def create_reservation_retail_item(self, *, reservation_id: str,
                                       params: Dict[str, Any]) -> resources.ReservationRetailItem:
        """`retail_product_id` required (one of the stay's listing's products), `quantity` optional (1-99,
        default 1). Raises ValidationError (HTTP 422) when the stay's order isn't open, the product isn't offered,
        is already on the stay (change its quantity with `patch_reservation_retail_item` instead), the quantity is
        invalid or not in stock. The customer is told, as on the web."""
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        return resources.ReservationRetailItem.parse(
            self.request('post', f"reservations/{reservation_id}/retail_items", query=params))

    def patch_reservation_retail_item(self, *, reservation_id: str, retail_item_id: str,
                                      params: Dict[str, Any]) -> resources.ReservationRetailItem:
        """Changes how many of the product the stay carries, at the price it was added at: `quantity` required
        (1-99). The same quantity again changes nothing; the customer isn't told. Raises ValidationError (HTTP 422)
        once the stay's order is invoiced, or for a bad quantity or not enough in stock."""
        if not reservation_id or not retail_item_id:
            raise ValueError("ID cannot be blank")
        path = f"reservations/{reservation_id}/retail_items/{retail_item_id}"
        return resources.ReservationRetailItem.parse(self.request('patch', path, query=params))

    def delete_reservation_retail_item(self, *, reservation_id: str, retail_item_id: str) -> bool:
        """Raises ValidationError (HTTP 422) once the stay's order is invoiced."""
        if not reservation_id or not retail_item_id:
            raise ValueError("ID cannot be blank")
        path = f"reservations/{reservation_id}/retail_items/{retail_item_id}"
        return self.request('delete', path).status_code == 204
