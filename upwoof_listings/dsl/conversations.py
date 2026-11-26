from typing import Any, Dict, List, Optional
from .. import resources

class ConversationsDSL:
    """A listing's conversations (in-app messages, and email replies to them), their messages and a reply. Only
    conversations with the listing are reachable; any other raises ResourceNotFoundError. Any team member may
    read them; to reply the caller must take part in the conversation. A conversation's id is an
    inbound_email.received webhook's `conversation_id`."""

    def get_listing_conversations(self, *, listing_id: str,
                                  params: Optional[Dict[str, Any]] = None) -> List[resources.Conversation]:
        """Most recently active first, without their messages. Optional `customer_id` (a customer of the
        listing), `updated_since` (ISO 8601), `page`, `per_page`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/conversations"
        return resources.Conversation.parse(self.request('get', path, query=params))

    def get_listing_conversation(self, *, listing_id: str, conversation_id: str) -> resources.Conversation:
        """Every message, oldest first, each with its `origin` (web, email, automated, ai or api) and sender."""
        if not listing_id or not conversation_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/conversations/{conversation_id}"
        return resources.Conversation.parse(self.request('get', path))

    def create_listing_conversation_message(self, *, listing_id: str, conversation_id: str,
                                            params: Dict[str, Any]) -> resources.ConversationMessage:
        """Replies to everyone in the conversation as the caller (origin `api`); anyone with no UpWoof login is
        emailed it. `body` is required (at most 20,000 characters). Raises ClientError (HTTP 403, error
        `not_a_participant`) when the caller doesn't take part, ValidationError (HTTP 422, `message_not_sent`)
        when it can't be posted, and ClientError (HTTP 429) past 30 replies in 10 minutes with one token."""
        if not listing_id or not conversation_id:
            raise ValueError("ID cannot be blank")
        if not params:
            raise ValueError("Params cannot be blank")
        path = f"listings/{listing_id}/conversations/{conversation_id}/messages"
        return resources.ConversationMessage.parse(self.request('post', path, query=params))
