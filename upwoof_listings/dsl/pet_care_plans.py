from typing import Any, Dict, List, Optional
from .. import resources

class PetCarePlansDSL:
    """A pet's standing care plan: its meals (feeding plans) and medications (medication plans), copied onto each
    stay at check-in. Every method needs `listing_id`, one of the caller's team listings (any tier); the pet must be
    a pet of that listing's (or its group's) customers and the plan one the listing's group keeps, else
    ResourceNotFoundError. Times are wall-clock "HH:MM" in the listing's time zone; a badly formatted time raises
    ClientError (HTTP 400), and a refused plan ValidationError (HTTP 422)."""

    def _pet_plan_path(self, pet_id: str, kind: str, plan_id: Optional[str] = None) -> str:
        if not pet_id or (plan_id is not None and not plan_id):
            raise ValueError("ID cannot be blank")
        path = f"pets/{pet_id}/{kind}"
        return f"{path}/{plan_id}" if plan_id is not None else path

    @staticmethod
    def _with_listing(listing_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not listing_id:
            raise ValueError("ID cannot be blank")
        return {**(params or {}), 'listing_id': listing_id}

    # Feeding plans

    def get_pet_feeding_plans(self, *, pet_id: str, listing_id: str, params: Optional[Dict[str, Any]] = None
                              ) -> List[resources.PetFeedingPlan]:
        """By `time_of_day` (untimed last), then id; `page`/`per_page` in `params`."""
        return resources.PetFeedingPlan.parse(
            self.request('get', self._pet_plan_path(pet_id, 'feeding_plans'),
                         query=self._with_listing(listing_id, params)))

    def get_pet_feeding_plan(self, *, pet_id: str, plan_id: str, listing_id: str) -> resources.PetFeedingPlan:
        return resources.PetFeedingPlan.parse(
            self.request('get', self._pet_plan_path(pet_id, 'feeding_plans', plan_id),
                         query=self._with_listing(listing_id)))

    def create_pet_feeding_plan(self, *, pet_id: str, params: Dict[str, Any]) -> resources.PetFeedingPlan:
        """`listing_id` and `meal_label` required; `time_of_day` ("HH:MM", blank for untimed), `quantity`,
        `food_description` and `special_feeding` optional."""
        return resources.PetFeedingPlan.parse(
            self.request('post', self._pet_plan_path(pet_id, 'feeding_plans'), query=params))

    def patch_pet_feeding_plan(self, *, pet_id: str, plan_id: str,
                               params: Dict[str, Any]) -> resources.PetFeedingPlan:
        """`listing_id` required; changes only the other fields sent (a blank `time_of_day` makes it untimed)."""
        return resources.PetFeedingPlan.parse(
            self.request('patch', self._pet_plan_path(pet_id, 'feeding_plans', plan_id), query=params))

    def delete_pet_feeding_plan(self, *, pet_id: str, plan_id: str, listing_id: str) -> bool:
        return self.request('delete', self._pet_plan_path(pet_id, 'feeding_plans', plan_id),
                            query=self._with_listing(listing_id)).status_code == 204

    # Medication plans

    def get_pet_medication_plans(self, *, pet_id: str, listing_id: str, params: Optional[Dict[str, Any]] = None
                                 ) -> List[resources.PetMedicationPlan]:
        """By `medication_name`; `page`/`per_page` in `params`. `effective_dose_times` are the times doses fall
        due (the plan's own `dose_times`, else the frequency's usual times; empty when `as_needed`)."""
        return resources.PetMedicationPlan.parse(
            self.request('get', self._pet_plan_path(pet_id, 'medication_plans'),
                         query=self._with_listing(listing_id, params)))

    def get_pet_medication_plan(self, *, pet_id: str, plan_id: str, listing_id: str) -> resources.PetMedicationPlan:
        return resources.PetMedicationPlan.parse(
            self.request('get', self._pet_plan_path(pet_id, 'medication_plans', plan_id),
                         query=self._with_listing(listing_id)))

    def create_pet_medication_plan(self, *, pet_id: str, params: Dict[str, Any]) -> resources.PetMedicationPlan:
        """`listing_id` and `medication_name` required; `dosage`, `frequency` (`once_daily`, `twice_daily`,
        `three_times_daily`, `as_needed`), `dose_times` (a list of "HH:MM"; empty for the frequency's usual times)
        and `instructions` optional. Dose times it can't read raise ValidationError (HTTP 422)."""
        return resources.PetMedicationPlan.parse(
            self.request('post', self._pet_plan_path(pet_id, 'medication_plans'), query=params))

    def patch_pet_medication_plan(self, *, pet_id: str, plan_id: str,
                                  params: Dict[str, Any]) -> resources.PetMedicationPlan:
        """`listing_id` required; changes only the other fields sent."""
        return resources.PetMedicationPlan.parse(
            self.request('patch', self._pet_plan_path(pet_id, 'medication_plans', plan_id), query=params))

    def delete_pet_medication_plan(self, *, pet_id: str, plan_id: str, listing_id: str) -> bool:
        return self.request('delete', self._pet_plan_path(pet_id, 'medication_plans', plan_id),
                            query=self._with_listing(listing_id)).status_code == 204
