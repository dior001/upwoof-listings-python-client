import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ResourceNotFoundError, ValidationError

@pytest.fixture
def client():
    return Client(api_key='test_key')

class TestReportCardsDSL:
    @responses.activate
    def test_get_reservation_report_cards(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/reservations/1/report_cards',
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
        responses.add(responses.POST, 'https://www.upwoof.com/api/v1/reservations/1/report_cards',
                      json={'ID': 1, 'PET_ID': 2, 'DATE': '2026-01-01', 'MOOD': 'happy'}, status=201)
        report_card = client.create_reservation_report_card(
            reservation_id='1', params={'pet_id': 2, 'date': '2026-01-01', 'mood': 'happy'}
        )
        assert report_card.id == 1
        assert report_card.pet_id == 2

    def test_create_reservation_report_card_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_reservation_report_card(reservation_id='', params={})


class TestListingReportCardsDSL:
    BASE = 'https://www.upwoof.com/api/v1/'

    @responses.activate
    def test_get_listing_report_cards(self, client):
        responses.add(responses.GET, f"{self.BASE}listings/1/report_cards", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'status': 'draft'})],
                      json=[{'id': 6, 'pet_id': 2, 'reservation_id': 4, 'published_at': None}])
        cards = client.get_listing_report_cards(listing_id='1', params={'status': 'draft'})
        assert cards[0].reservation_id == 4

    @responses.activate
    def test_start_listing_report_cards(self, client):
        responses.add(responses.POST, f"{self.BASE}listings/1/report_cards/start", status=201,
                      match=[matchers.json_params_matcher({'include_care_log': True})],
                      json={'created_count': 3, 'date': '2026-12-01', 'skipped_count': 1})
        result = client.start_listing_report_cards(listing_id='1', include_care_log=True)
        assert (result.created_count, result.skipped_count, result.date) == (3, 1, '2026-12-01')

    @responses.activate
    def test_start_listing_report_cards_turned_off(self, client):
        responses.add(responses.POST, f"{self.BASE}listings/1/report_cards/start", status=422,
                      json={'error': 'report_cards_disabled', 'message': 'Report cards are turned off'})
        with pytest.raises(ValidationError):
            client.start_listing_report_cards(listing_id='1')

    @responses.activate
    def test_publish_listing_report_cards(self, client):
        responses.add(responses.POST, f"{self.BASE}listings/1/report_cards/publish", status=201,
                      json={'date': '2026-12-01', 'published_count': 3})
        assert client.publish_listing_report_cards(listing_id='1').published_count == 3

    @responses.activate
    def test_get_report_card_photos(self, client):
        responses.add(responses.GET, f"{self.BASE}report_cards/6/photos", status=200,
                      json=[{'id': 12, 'shared': False, 'photo_share_id': None, 'url': 'https://example.test/p.jpg'}])
        photos = client.get_report_card_photos(report_card_id='6')
        assert photos[0].shared is False

    @responses.activate
    def test_share_and_unshare_report_card_photo(self, client):
        url = f"{self.BASE}report_cards/6/photos/12/share"
        responses.add(responses.POST, url, status=201, json={'id': 12, 'shared': True, 'photo_share_id': 30})
        responses.add(responses.DELETE, url, status=204)
        assert client.share_report_card_photo(report_card_id='6', photo_id='12').photo_share_id == 30
        assert client.unshare_report_card_photo(report_card_id='6', photo_id='12') is True

    @responses.activate
    def test_unshare_report_card_photo_not_shared(self, client):
        responses.add(responses.DELETE, f"{self.BASE}report_cards/6/photos/12/share", status=404, json={})
        with pytest.raises(ResourceNotFoundError):
            client.unshare_report_card_photo(report_card_id='6', photo_id='12')

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_report_cards(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.start_listing_report_cards(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.publish_listing_report_cards(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_report_card_photos(report_card_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.share_report_card_photo(report_card_id='6', photo_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.unshare_report_card_photo(report_card_id='', photo_id='12')
