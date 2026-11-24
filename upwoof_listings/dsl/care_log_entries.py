from typing import Any, Dict, List, Optional
from .. import resources

class CareLogEntriesDSL:
    """A stay's care log: its feeding, medication, potty and note tasks. Any team member of the stay's listing (a
    stay or task elsewhere raises ResourceNotFoundError). A task's `outcome` is `ate_all`, `ate_some` or `ate_none`
    for a feeding and `given` or `refused` for a dose (None while to do, or not recorded)."""

    def get_reservation_care_log_entries(self, *, reservation_id: str, params: Optional[Dict[str, Any]] = None
                                         ) -> List[resources.CareLogEntry]:
        """By `scheduled_at`, then id. `params`: `date` (YYYY-MM-DD, the listing's own day), `entry_type`
        (`feeding`, `medication`, `potty`, `note`), `status` (`pending`, `completed`), `page`, `per_page`."""
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        return resources.CareLogEntry.parse(
            self.request('get', f"reservations/{reservation_id}/care_log_entries", query=params))

    def complete_care_log_entry(self, *, resource_id: str,
                                params: Optional[Dict[str, Any]] = None) -> resources.CareLogEntry:
        """Mark a task done. `params` (all optional): `outcome`, and for a medication `dose_given` and
        `administration_notes` (required when the outcome is `refused`). Raises ValidationError (HTTP 422) when the
        task is already done, the outcome doesn't fit its kind, or a refusal has no reason."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.CareLogEntry.parse(
            self.request('post', f"care_log_entries/{resource_id}/complete", query=params or {}))
