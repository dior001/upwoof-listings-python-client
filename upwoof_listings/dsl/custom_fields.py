from typing import Any, Dict, List, Optional
from .. import resources

class CustomFieldsDSL:
    def get_listing_custom_field_definitions(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                             ) -> List[resources.CustomFieldDefinition]:
        """A listing's own custom fields plus its listing group's group-wide ones. Optional `record_type`
        (customer, pet, reservation, incident_report), `page`, `per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/custom_field_definitions"
        return resources.CustomFieldDefinition.parse(self.request('get', path, query=params))

    def update_customer_custom_fields(self, *, resource_id: str, listing_id: str,
                                      custom_fields: List[Dict[str, Any]]) -> resources.Customer:
        """Answer a customer's custom fields at `listing_id`. See `_put_custom_fields`."""
        return resources.Customer.parse(self._put_custom_fields('customers', resource_id, listing_id, custom_fields))

    def update_pet_custom_fields(self, *, resource_id: str, listing_id: str,
                                 custom_fields: List[Dict[str, Any]]) -> resources.Pet:
        """Answer a pet's custom fields at `listing_id`. See `_put_custom_fields`."""
        return resources.Pet.parse(self._put_custom_fields('pets', resource_id, listing_id, custom_fields))

    def update_reservation_custom_fields(self, *, resource_id: str, listing_id: str,
                                         custom_fields: List[Dict[str, Any]]) -> resources.Reservation:
        """Answer a reservation's custom fields at `listing_id`. See `_put_custom_fields`."""
        return resources.Reservation.parse(
            self._put_custom_fields('reservations', resource_id, listing_id, custom_fields))

    def _put_custom_fields(self, collection: str, resource_id: str, listing_id: str,
                           custom_fields: List[Dict[str, Any]]):
        """`custom_fields` is a non-empty list of `{'custom_field_definition_id': id, 'value': ...}`: a
        string (text, select, ISO 8601 date), a number, a boolean (yes_no) or a list of strings
        (multi_select); None or "" clears the answer. Only the fields sent change. Answers the record with its
        updated `custom_fields`. Raises ValidationError (HTTP 422, nothing saved) when an id isn't one of the
        listing's fields for that record type (`body['unknown_custom_field_ids']`) or an answer is refused
        (`body['errors']`, keyed by definition id)."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        if not listing_id:
            raise ValueError("Listing ID cannot be blank")
        if not custom_fields:
            raise ValueError("Custom fields cannot be blank")
        query = {'listing_id': listing_id, 'custom_fields': custom_fields}
        return self.request('put', f"{collection}/{resource_id}/custom_fields", query=query)
