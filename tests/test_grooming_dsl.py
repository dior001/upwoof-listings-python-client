import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError, ValidationError

BASE = "https://pethotels.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestGroomingDSL:
    @responses.activate
    def test_get_listing_grooming_services(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/grooming/services", status=200,
                      json=[{'id': 2, 'name': 'Bath', 'duration_minutes': 60, 'animal_types': ['Dog']}])
        services = client.get_listing_grooming_services(listing_id='1')
        assert services[0].animal_types == ['Dog']

    @responses.activate
    def test_get_listing_groomers(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/grooming/groomers", status=200,
                      json=[{'id': 4, 'name': 'Sam', 'specialties': ['Poodles']}])
        assert client.get_listing_groomers(listing_id='1')[0].specialties == ['Poodles']

    @responses.activate
    def test_get_listing_grooming_open_times_sends_lists_as_brackets(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/grooming/open_times", status=200,
                      match=[matchers.query_string_matcher(
                          'access_token=test_key&date=2026-12-01&customer_id=7'
                          '&pet_ids%5B%5D=3&pet_ids%5B%5D=4&service_type_ids%5B%5D=2')],
                      json={'date': '2026-12-01', 'deposit_cents': 0, 'currency': 'NZD',
                            'start_times': ['2026-12-01T09:00:00+13:00']})
        times = client.get_listing_grooming_open_times(listing_id='1', params={
            'date': '2026-12-01', 'customer_id': 7, 'pet_ids': [3, 4], 'service_type_ids': [2]})
        assert times.start_times == ['2026-12-01T09:00:00+13:00']
        assert times.deposit_cents == 0

    @responses.activate
    def test_create_listing_grooming_appointments(self, client):
        params = {'customer_id': 7, 'pet_ids': [3], 'service_type_ids': [2], 'starts_at': '2026-12-01T09:00:00+13:00'}
        responses.add(responses.POST, f"{BASE}listings/1/grooming/appointments", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json=[{'id': 11, 'status': 'scheduled', 'pet_id': 3, 'reservation_id': None}])
        appointments = client.create_listing_grooming_appointments(listing_id='1', params=params)
        assert appointments[0].status == 'scheduled'
        assert appointments[0].reservation_id is None

    @responses.activate
    def test_create_listing_grooming_appointments_with_a_deposit(self, client):
        message = "The listing takes a deposit on these grooms; the customer books them on the listing's UpWoof profile"
        responses.add(responses.POST, f"{BASE}listings/1/grooming/appointments", status=422,
                      json={'errors': [message]})
        with pytest.raises(ValidationError) as raised:
            client.create_listing_grooming_appointments(listing_id='1', params={})
        assert raised.value.errors == [message]

    @responses.activate
    def test_grooming_not_offered_online(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/grooming/services", status=403, json={'error': 'Forbidden'})
        with pytest.raises(ClientError):
            client.get_listing_grooming_services(listing_id='1')

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_grooming_services(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_groomers(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_grooming_open_times(listing_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_listing_grooming_appointments(listing_id='', params={})
