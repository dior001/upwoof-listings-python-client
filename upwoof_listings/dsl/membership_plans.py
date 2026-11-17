from typing import Any, Dict, List, Optional
from .. import resources

class MembershipPlansDSL:
    """A listing's membership plans, read only (team members of the listing; else ClientError, HTTP 403)."""

    def get_listing_membership_plans(self, *, listing_id: str,
                                     params: Optional[Dict[str, Any]] = None) -> List[resources.MembershipPlan]:
        """Active and inactive plans, by name then id; `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/membership_plans"
        return resources.MembershipPlan.parse(self.request('get', path, query=params))

    def get_listing_membership_plan(self, *, listing_id: str, membership_plan_id: str) -> resources.MembershipPlan:
        if not listing_id or not membership_plan_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/membership_plans/{membership_plan_id}"
        return resources.MembershipPlan.parse(self.request('get', path))
