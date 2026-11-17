from typing import Any, Dict, List, Optional
from .. import resources

class PricingRulesDSL:
    """A listing's pricing rules. Owner/manager of the listing only (a staff member gets ClientError, HTTP
    403); a rule id that isn't the listing's raises ResourceNotFoundError."""

    def get_listing_pricing_rules(self, *, listing_id: str,
                                  params: Optional[Dict[str, Any]] = None) -> List[resources.PricingRule]:
        """Highest priority first (priority desc, id asc); `page`/`per_page` in `params`."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/pricing_rules"
        return resources.PricingRule.parse(self.request('get', path, query=params))

    def get_listing_pricing_rule(self, *, listing_id: str, pricing_rule_id: str) -> resources.PricingRule:
        if not listing_id or not pricing_rule_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/pricing_rules/{pricing_rule_id}"
        return resources.PricingRule.parse(self.request('get', path))

    def create_listing_pricing_rule(self, *, listing_id: str, params: Dict[str, Any]) -> resources.PricingRule:
        """`name` required. A rule needs at least one condition (animal_type_id, breed_ids, min_age_months,
        max_age_months, customer_id, or neuter_status other than any_status); a refused rule raises
        ValidationError (HTTP 422)."""
        if not listing_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/pricing_rules"
        return resources.PricingRule.parse(self.request('post', path, query=params))

    def patch_listing_pricing_rule(self, *, listing_id: str, pricing_rule_id: str,
                                   params: Dict[str, Any]) -> resources.PricingRule:
        """Changes only the fields sent; send None to clear an optional one."""
        if not listing_id or not pricing_rule_id:
            raise ValueError("ID cannot be blank")
        path = f"listings/{listing_id}/pricing_rules/{pricing_rule_id}"
        return resources.PricingRule.parse(self.request('patch', path, query=params))

    def delete_listing_pricing_rule(self, *, listing_id: str, pricing_rule_id: str) -> bool:
        if not listing_id or not pricing_rule_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"listings/{listing_id}/pricing_rules/{pricing_rule_id}").status_code == 204
