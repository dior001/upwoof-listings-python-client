from typing import Any, Dict, List, Optional
from .. import resources

class PetEvaluationsDSL:
    def get_pet_evaluations(self, params: Optional[Dict[str, Any]] = None) -> List[resources.PetEvaluation]:
        """List the temperament evaluations and meet-and-greets recorded at the caller's listings, newest
        first (evaluated_on desc, id desc). Optional filters: evaluation_type (temperament, meet_and_greet),
        listing_id, pet_id, reservation_id, result (pending, passed, partial, failed), page, per_page."""
        return resources.PetEvaluation.parse(self.request('get', 'pet_evaluations', query=params))

    def get_pet_evaluation(self, *, resource_id: str) -> resources.PetEvaluation:
        """Get one evaluation. Raises ResourceNotFoundError unless it was recorded at one of the caller's
        listings."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.PetEvaluation.parse(self.request('get', f"pet_evaluations/{resource_id}"))

    def create_reservation_pet_evaluation(self, *, reservation_id: str,
                                          params: Dict[str, Any]) -> resources.PetEvaluation:
        """Record an evaluation result for one of a reservation's pets. `params`: pet_id and result
        (pending, passed, partial, failed) required; evaluation_type (temperament, meet_and_greet; defaults to
        the stay's evaluation-visit type, else temperament), evaluated_on (defaults to today in the listing's
        time zone), expires_on (on/after evaluated_on, else 422) and notes optional. A pending evaluation the
        pet already has on that stay is filled in and returned (same id). Raises ResourceNotFoundError for a
        reservation not at the caller's listings or a pet not on it."""
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        path = f"reservations/{reservation_id}/pet_evaluations"
        return resources.PetEvaluation.parse(self.request('post', path, query=params))
