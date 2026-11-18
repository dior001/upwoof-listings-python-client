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
    def test_create_listing_grooming_appointments_held_for_a_deposit(self, client):
        params = {'customer_id': 7, 'pet_ids': [3], 'service_type_ids': [2], 'starts_at': '2026-12-01T09:00:00+13:00',
                  'success_url': 'https://example.com/paid?session={CHECKOUT_SESSION_ID}',
                  'cancel_url': 'https://example.com/cancelled'}
        responses.add(responses.POST, f"{BASE}listings/1/grooming/appointments", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json=[{'id': 11, 'kind': 'grooming', 'status': 'pending_payment', 'deposit_cents': 2000,
                             'deposit_status': 'pending', 'checkout_url': 'https://checkout.stripe.com/c/pay/cs_1'}])
        appointment = client.create_listing_grooming_appointments(listing_id='1', params=params)[0]
        assert appointment.status == 'pending_payment'
        assert appointment.checkout_url == 'https://checkout.stripe.com/c/pay/cs_1'

    @responses.activate
    def test_create_listing_grooming_appointments_refused(self, client):
        message = "Stripe couldn't start the deposit payment; nothing was booked"
        responses.add(responses.POST, f"{BASE}listings/1/grooming/appointments", status=422,
                      json={'errors': [message]})
        with pytest.raises(ValidationError) as raised:
            client.create_listing_grooming_appointments(listing_id='1', params={})
        assert raised.value.errors == [message]

    @responses.activate
    def test_get_listing_grooming_appointments(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/grooming/appointments", status=200,
                      match=[matchers.query_string_matcher(
                          'access_token=test_key&status=pending_payment&ids%5B%5D=11&ids%5B%5D=12')],
                      json=[{'id': 12, 'kind': 'grooming', 'checkout_url': None}])
        appointments = client.get_listing_grooming_appointments(
            listing_id='1', params={'status': 'pending_payment', 'ids': [11, 12]})
        assert appointments[0].id == 12

    @pytest.mark.parametrize('kind_path,methods', [
        ('lessons', ('get_listing_lesson_services', 'get_listing_trainers', 'get_listing_lesson_open_times',
         'create_listing_lesson_appointments', 'get_listing_lesson_appointments')),
        ('tours', ('get_listing_tour_services', 'get_listing_tour_hosts', 'get_listing_tour_open_times',
         'create_listing_tour_appointments', 'get_listing_tour_appointments')),
        ('transports', ('get_listing_transport_services', 'get_listing_transport_drivers',
         'get_listing_transport_open_times', 'create_listing_transport_appointments',
         'get_listing_transport_appointments')),
    ])
    @responses.activate
    def test_other_appointment_kinds(self, client, kind_path, methods):
        services, providers, open_times, create, index = methods
        provider_path = {'lessons': 'trainers', 'tours': 'hosts', 'transports': 'drivers'}[kind_path]
        responses.add(responses.GET, f"{BASE}listings/1/{kind_path}/services", status=200,
                      json=[{'id': 2, 'kind': kind_path, 'per_km_surcharge_cents': None}])
        responses.add(responses.GET, f"{BASE}listings/1/{kind_path}/{provider_path}", status=200,
                      json=[{'id': 4, 'name': 'Sam'}])
        responses.add(responses.GET, f"{BASE}listings/1/{kind_path}/open_times", status=200,
                      json={'date': '2026-12-01', 'deposit_cents': 0, 'start_times': []})
        responses.add(responses.POST, f"{BASE}listings/1/{kind_path}/appointments", status=201,
                      json=[{'id': 11, 'status': 'scheduled'}])
        responses.add(responses.GET, f"{BASE}listings/1/{kind_path}/appointments", status=200,
                      json=[{'id': 11, 'status': 'scheduled'}])
        assert isinstance(getattr(client, services)(listing_id='1')[0], client.resources.ServiceType)
        assert isinstance(getattr(client, providers)(listing_id='1')[0], client.resources.Groomer)
        assert getattr(client, open_times)(listing_id='1', params={'date': '2026-12-01'}).deposit_cents == 0
        created = getattr(client, create)(listing_id='1', params={'customer_id': 7})
        assert isinstance(created[0], client.resources.GroomingAppointment)
        assert getattr(client, index)(listing_id='1')[0].status == 'scheduled'
        with pytest.raises(ValueError, match="ID cannot be blank"):
            getattr(client, index)(listing_id='')

    @responses.activate
    def test_create_listing_transport_appointments_sends_the_pickup(self, client):
        params = {'customer_id': 7, 'pet_ids': [3], 'service_type_ids': [5], 'starts_at': '2026-12-01T09:00:00+13:00',
                  'pickup_street_address': '1 Queen St', 'pickup_city': 'Auckland'}
        responses.add(responses.POST, f"{BASE}listings/1/transports/appointments", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json=[{'id': 11, 'kind': 'transport', 'pickup_city': 'Auckland', 'transport_distance_km': 12.5,
                             'transport_surcharge_cents': 1250}])
        trip = client.create_listing_transport_appointments(listing_id='1', params=params)[0]
        assert trip.transport_distance_km == 12.5

    @responses.activate
    def test_create_listing_tour_appointments_has_no_pet(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/tours/appointments", status=201,
                      json=[{'id': 11, 'kind': 'tour', 'pet_id': None}])
        tour = client.create_listing_tour_appointments(listing_id='1', params={'customer_id': 7})[0]
        assert tour.pet_id is None

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
