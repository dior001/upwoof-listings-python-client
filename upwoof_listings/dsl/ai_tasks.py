from typing import Any, Dict, List, Optional
from .. import resources

class AiTasksDSL:
    """Emails an address's AI assistant has read and what it recommends doing about them. Any team member of
    the listing; a caller sees only tasks of the role addresses they receive unless they are an owner/manager.
    A task the caller can't see raises ResourceNotFoundError. Lists leave out `body_text` and
    `recommendation`; the single task and the review methods include them."""

    def get_listing_ai_tasks(self, *, listing_id: str,
                             params: Optional[Dict[str, Any]] = None) -> List[resources.AiTask]:
        """Newest first. Optional `listing_email_address_id`, `status` (queued, awaiting_review, executing,
        needs_attention, completed, declined, superseded), `page`, `per_page`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/ai_tasks"
        return resources.AiTask.parse(self.request('get', path, query=params))

    def get_listing_ai_task(self, *, listing_id: str, task_id: str) -> resources.AiTask:
        if not listing_id or not task_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/ai_tasks/{task_id}"
        return resources.AiTask.parse(self.request('get', path))

    def approve_listing_ai_task(self, *, listing_id: str, task_id: str,
                                params: Optional[Dict[str, Any]] = None) -> resources.AiTask:
        """Runs the recommended action. The body's optional `params` key amends it: a dict of the recommended
        action's param names to values (e.g. `params={'params': {'message': '...'}}`); a key left out keeps the
        recommended value, None clears an optional one; ids for records, lists of ids, `YYYY-MM-DD` dates,
        `YYYY-MM-DDTHH:MM` listing-local times, text. Raises ValidationError (HTTP 422, error `unknown_params`
        for a key the action doesn't have, `ai_task_refused` when the task isn't awaiting review, the params
        don't validate, the caller's permission group doesn't allow the action, or the action failed)."""
        if not listing_id or not task_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/ai_tasks/{task_id}/approve"
        return resources.AiTask.parse(self.request('post', path, query=params))

    def decline_listing_ai_task(self, *, listing_id: str, task_id: str,
                                params: Optional[Dict[str, Any]] = None) -> resources.AiTask:
        """Optional `note` (at most 1,000 characters, never sent to the sender). Raises ValidationError (HTTP
        422, error `ai_task_refused`) once the task has moved on."""
        if not listing_id or not task_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/ai_tasks/{task_id}/decline"
        return resources.AiTask.parse(self.request('post', path, query=params))

    def handle_listing_ai_task(self, *, listing_id: str, task_id: str) -> resources.AiTask:
        """Marks a task that needs a person (or was interrupted) handled. Raises ValidationError (HTTP 422,
        error `ai_task_refused`) otherwise."""
        if not listing_id or not task_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/ai_tasks/{task_id}/handled"
        return resources.AiTask.parse(self.request('post', path))
