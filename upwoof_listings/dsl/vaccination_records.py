from typing import Any, Dict, List
from .. import resources

class VaccinationRecordsDSL:
    def get_pet_vaccination_records(self, *, pet_id: str) -> List[resources.VaccinationRecord]:
        if not pet_id:
            raise ValueError("ID cannot be blank")
        return resources.VaccinationRecord.parse(self.request('get', f"pets/{pet_id}/vaccination_records"))

    def create_pet_vaccination_record(self, *, pet_id: str, params: Dict[str, Any]) -> resources.VaccinationRecord:
        if not pet_id:
            raise ValueError("ID cannot be blank")
        path = f"pets/{pet_id}/vaccination_records"
        return resources.VaccinationRecord.parse(self.request('post', path, query=params))
