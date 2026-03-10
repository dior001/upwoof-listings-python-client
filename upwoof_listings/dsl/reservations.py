from typing import Any, Dict, List
from .. import resources

class ReservationsDSL:
    def get_reservations(self) -> List[resources.Reservation]:
        return resources.Reservation.parse(self.request('get', 'reservations/'))

    def get_reservation(self, *, resource_id: str) -> resources.Reservation:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('get', f"reservations/{resource_id}"))

    def create_reservation(self, *, params: Dict[str, Any]) -> resources.Reservation:
        return resources.Reservation.parse(self.request('post', 'reservations/', query=params))

    def update_reservation(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Reservation:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('put', f"reservations/{resource_id}", query=params))

    def patch_reservation(self, *, resource_id: str, params: Dict[str, Any]) -> resources.Reservation:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('patch', f"reservations/{resource_id}", query=params))

    def delete_reservation(self, *, resource_id: str) -> bool:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"reservations/{resource_id}").status_code == 204
