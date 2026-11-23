from typing import Any, Dict, List, Optional
from .. import resources

class MembershipPlansDSL:
    """A listing's membership plans, read only (team members of the listing; else ClientError, HTTP 403).

    `credit_uses` lists what a credit pays for, any of `stays`, `classes` (training class enrollments), `lessons`
    (private lessons) and `grooming`; it is empty only on a discount-only plan. `credit_use` and
    `credits_cover_lessons` are deprecated (derived from `credit_uses`, and `credit_use` can't express grooming or
    lessons): read `credit_uses`."""

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
