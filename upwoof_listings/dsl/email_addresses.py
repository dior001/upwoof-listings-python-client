from typing import Any, Dict, List, Optional
from .. import resources

class EmailAddressesDSL:
    """A listing's role email addresses (`<role_key>+<listing id>@upwoof.net`) and the emails received at them.
    Reading is any team member of the listing; creating, changing and deleting need owner/manager. An id that
    isn't the listing's raises ResourceNotFoundError."""

    def get_listing_email_addresses(self, *, listing_id: str,
                                    params: Optional[Dict[str, Any]] = None) -> List[resources.ListingEmailAddress]:
        """Ordered by `role_key`; always includes the `bookings` address. `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/email_addresses"
        return resources.ListingEmailAddress.parse(self.request('get', path, query=params))

    def get_listing_email_address(self, *, listing_id: str,
                                  listing_email_address_id: str) -> resources.ListingEmailAddress:
        if not listing_id or not listing_email_address_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/email_addresses/{listing_email_address_id}"
        return resources.ListingEmailAddress.parse(self.request('get', path))

    def create_listing_email_address(self, *, listing_id: str,
                                     params: Dict[str, Any]) -> resources.ListingEmailAddress:
        """`name` and `role_key` (`[a-z][a-z0-9-]{1,29}`, unique at the listing, not reserved) required; optional
        `active` (default True), `recipient_scope` (`owners_and_managers`, the default, `all_team` or
        `selected`), `selected_user_ids` (team members, required when `selected`), `show_on_profile`, and the AI
        assistant's `ai_role`, `ai_instructions` and `ai_review_required` (False also needs
        `ai_automatic_confirmation: True`; see AiTasksDSL). Raises ValidationError (HTTP 422) for a taken or
        reserved role key."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/email_addresses"
        return resources.ListingEmailAddress.parse(self.request('post', path, query=params))

    def patch_listing_email_address(self, *, listing_id: str, listing_email_address_id: str,
                                    params: Dict[str, Any]) -> resources.ListingEmailAddress:
        """Changes only the fields sent (the AI fields as for create; `ai_role: None` switches the assistant
        off). Raises ValidationError (HTTP 422, error `bookings_role_key`) when
        changing the bookings address's `role_key`."""
        if not listing_id or not listing_email_address_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/email_addresses/{listing_email_address_id}"
        return resources.ListingEmailAddress.parse(self.request('patch', path, query=params))

    def delete_listing_email_address(self, *, listing_id: str, listing_email_address_id: str) -> bool:
        """Raises ValidationError (HTTP 422, error `bookings_address`) for the bookings address."""
        if not listing_id or not listing_email_address_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/email_addresses/{listing_email_address_id}"
        return self.request('delete', path).status_code == 204

    def get_listing_inbound_emails(self, *, listing_id: str,
                                   params: Optional[Dict[str, Any]] = None) -> List[resources.InboundEmailRecord]:
        """Emails received at the listing's addresses, newest first. Optional `outcome` (posted, lead_created,
        lead_appended, ignored_automatic, ignored_own_team, rejected_unknown_address, rejected_sender,
        rejected_ambiguous, throttled, failed), `since` (ISO 8601), `page`, `per_page`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/inbound_emails"
        return resources.InboundEmailRecord.parse(self.request('get', path, query=params))
