import os
import pytest
import vcr
from upwoof_listings.client import Client

# API Key for testing
API_KEY = os.environ.get('UPWOOF_API_KEY')

if not API_KEY:
    pytest.skip("UPWOOF_API_KEY environment variable not set", allow_module_level=True)

# Configure VCR
my_vcr = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    record_mode='once',
    filter_query_parameters=['access_token'],
    match_on=['method', 'scheme', 'host', 'port', 'path', 'query'],
)

@pytest.fixture
def client():
    return Client(api_key=API_KEY, url='https://staging.upwoof.com/api/v1/')

class TestIntegration:
    @my_vcr.use_cassette('get_listings.yaml')
    def test_get_listings(self, client):
        listings = client.get_listings()
        assert isinstance(listings, list)
        if len(listings) > 0:
            assert hasattr(listings[0], 'id')

    @my_vcr.use_cassette('get_pets.yaml')
    def test_get_pets(self, client):
        pets = client.get_pets()
        assert isinstance(pets, list)

    @my_vcr.use_cassette('get_accommodations.yaml')
    def test_get_accommodations(self, client):
        accommodations = client.get_accommodations()
        assert isinstance(accommodations, list)

    @my_vcr.use_cassette('get_customers.yaml')
    def test_get_customers(self, client):
        customers = client.get_customers()
        assert isinstance(customers, list)

    @my_vcr.use_cassette('get_invoices.yaml')
    def test_get_invoices(self, client):
        invoices = client.get_invoices()
        assert isinstance(invoices, list)

    @my_vcr.use_cassette('get_orders.yaml')
    def test_get_orders(self, client):
        orders = client.get_orders()
        assert isinstance(orders, list)

    @my_vcr.use_cassette('get_reservations.yaml')
    def test_get_reservations(self, client):
        reservations = client.get_reservations()
        assert isinstance(reservations, list)

    @my_vcr.use_cassette('get_users.yaml')
    def test_get_users(self, client):
        users = client.get_users()
        assert isinstance(users, list)

    @my_vcr.use_cassette('get_user_me.yaml')
    def test_get_user_me(self, client):
        user = client.get_user_me()
        assert hasattr(user, 'id')

    @my_vcr.use_cassette('get_animal_types.yaml')
    def test_get_animal_types(self, client):
        animal_types = client.get_animal_types()
        assert isinstance(animal_types, list)

    @my_vcr.use_cassette('get_accommodation_types.yaml')
    def test_get_accommodation_types(self, client):
        accommodation_types = client.get_accommodation_types()
        assert isinstance(accommodation_types, list)

    @my_vcr.use_cassette('get_breeds.yaml')
    def test_get_breeds(self, client):
        breeds = client.get_breeds()
        assert isinstance(breeds, list)
