import pytest
import responses
from upwoof_listings.client import Client

@pytest.fixture
def client():
    return Client(api_key='test_key')

class TestReportCardsDSL:
    @responses.activate
    def test_get_reservation_report_cards(self, client):
        responses.add(responses.GET, 'https://pethotels.upwoof.com/api/v1/reservations/1/report_cards',
                      json=[{'ID': 1, 'PET_ID': 2, 'DATE': '2026-01-01'}], status=200)
        report_cards = client.get_reservation_report_cards(reservation_id='1')
        assert isinstance(report_cards, list)
        assert report_cards[0].id == 1
        assert report_cards[0].pet_id == 2

    def test_get_reservation_report_cards_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_reservation_report_cards(reservation_id='')

    @responses.activate
    def test_create_reservation_report_card(self, client):
        responses.add(responses.POST, 'https://pethotels.upwoof.com/api/v1/reservations/1/report_cards',
                      json={'ID': 1, 'PET_ID': 2, 'DATE': '2026-01-01', 'MOOD': 'happy'}, status=201)
        report_card = client.create_reservation_report_card(
            reservation_id='1', params={'pet_id': 2, 'date': '2026-01-01', 'mood': 'happy'}
        )
        assert report_card.id == 1
        assert report_card.pet_id == 2

    def test_create_reservation_report_card_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_reservation_report_card(reservation_id='', params={})
