from typing import Any, Dict, List
from .. import resources

class ReportCardsDSL:
    def get_reservation_report_cards(self, *, reservation_id: str) -> List[resources.ReportCard]:
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        return resources.ReportCard.parse(self.request('get', f"reservations/{reservation_id}/report_cards"))

    def create_reservation_report_card(self, *, reservation_id: str, params: Dict[str, Any]) -> resources.ReportCard:
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        path = f"reservations/{reservation_id}/report_cards"
        return resources.ReportCard.parse(self.request('post', path, query=params))
