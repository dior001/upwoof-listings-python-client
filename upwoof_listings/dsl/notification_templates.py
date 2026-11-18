from typing import Any, Dict, List, Optional
from .. import resources

class NotificationTemplatesDSL:
    """A listing's own notification wording. Owner/manager of the listing only (else ClientError, HTTP 403)."""

    def get_listing_notification_templates(self, *, listing_id: str, params: Optional[Dict[str, Any]] = None
                                           ) -> List[resources.NotificationTemplateOverride]:
        """Only the rows the listing has written (anything absent uses the default wording), ordered by
        notification_key, channel, reservation_type; `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/notification_templates"
        return resources.NotificationTemplateOverride.parse(self.request('get', path, query=params))

    def update_listing_notification_template(self, *, listing_id: str,
                                             params: Dict[str, Any]) -> resources.NotificationTemplateOverride:
        """Create or update one row: `notification_key` and `channel` (email, sms) required;
        `reservation_type` (any_type default, boarding, daycare, grooming), `subject`, `body`, `enabled`
        optional, and fields not sent are left unchanged. Raises ResourceNotFoundError for a pair the listing
        isn't offered (sms only for reservation_confirmed/upcoming_stay_reminder; grooming only for
        invoice_finalized/payment_received) and ValidationError (HTTP 422) for an unknown {{tag}}, a length
        over the limit, or switching off a notification that can't be."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/notification_templates"
        return resources.NotificationTemplateOverride.parse(self.request('put', path, query=params))

    def delete_listing_notification_template(self, *, listing_id: str, notification_key: str, channel: str,
                                             reservation_type: Optional[str] = None) -> bool:
        """Go back to the default wording. Raises ResourceNotFoundError when there is no such row."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        if not notification_key or not channel:
            raise ValueError("Notification key and channel cannot be blank")
        query = {'notification_key': notification_key, 'channel': channel}
        if reservation_type:
            query['reservation_type'] = reservation_type
        path = f"listings/{listing_id}/notification_templates"
        return self.request('delete', path, query=query).status_code == 204
