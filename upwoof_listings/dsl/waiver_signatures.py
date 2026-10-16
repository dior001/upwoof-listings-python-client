from .. import resources

class WaiverSignaturesDSL:
    def get_reservation_waiver_signature(self, *, reservation_id: str) -> resources.WaiverSignature:
        if not reservation_id:
            raise ValueError("ID cannot be blank")
        return resources.WaiverSignature.parse(self.request('get', f"reservations/{reservation_id}/waiver_signature"))
