from typing import Any, Dict, List, Optional, Union
from .. import resources

class ReservationsDSL:
    def get_reservations(self) -> List[resources.Reservation]:
        return resources.Reservation.parse(self.request('get', 'reservations/'))

    def get_reservation(self, *, id: str) -> resources.Reservation:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('get', f"reservations/{id}"))

    def create_reservation(self, *, params: Dict[str, Any]) -> resources.Reservation:
        return resources.Reservation.parse(self.request('post', 'reservations/', query=params))

    def update_reservation(self, *, id: str, params: Dict[str, Any]) -> resources.Reservation:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('put', f"reservations/{id}", query=params))

    def patch_reservation(self, *, id: str, params: Dict[str, Any]) -> resources.Reservation:
        if not id:
            raise ValueError("ID cannot be blank")
        return resources.Reservation.parse(self.request('patch', f"reservations/{id}", query=params))

    def delete_reservation(self, *, id: str) -> bool:
        if not id:
            raise ValueError("ID cannot be blank")
        return self.request('delete', f"reservations/{id}").status_code == 204
