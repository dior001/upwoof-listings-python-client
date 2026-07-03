from typing import Any, Dict, List, Optional
from .. import resources

class ReviewsDSL:
    def get_listing_reviews(self, *, listing_id: str,
                            params: Optional[Dict[str, Any]] = None) -> List[resources.Review]:
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return resources.Review.parse(self.request('get', f"listings/{listing_id}/reviews", query=params))

    def create_reservation_review(self, *, reservation_id: str, params: Dict[str, Any]) -> resources.Review:
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        return resources.Review.parse(self.request('post', f"reservations/{reservation_id}/review", query=params))
