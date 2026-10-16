import pytest
import responses
from upwoof_listings.client import Client

@pytest.fixture
def client():
    return Client(api_key='test_key')

class TestWaiverSignaturesDSL:
    @responses.activate
    def test_get_reservation_waiver_signature(self, client):
        responses.add(responses.GET, 'https://pethotels.upwoof.com/api/v1/reservations/1/waiver_signature',
                      json={'ID': 1, 'SIGNATURE_DATA': 'Jane Doe', 'RESERVATION_ID': 1}, status=200)
        signature = client.get_reservation_waiver_signature(reservation_id='1')
        assert signature.id == 1
        assert signature.signature_data == 'Jane Doe'
        assert signature.reservation_id == 1

    def test_get_reservation_waiver_signature_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_reservation_waiver_signature(reservation_id='')
