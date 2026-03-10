from datetime import datetime
import pytest
import responses
import upwoof_listings
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError, ResourceNotFoundError
from upwoof_listings.resources import Listing

# pylint: disable=redefined-outer-name

@pytest.fixture
def client():
    return Client(api_key='test_key')

class TestClient:
    @responses.activate
    def test_request_success(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/listings/',
                      json={'ID': '1'}, status=200)
        response = client.request('get', 'listings/')
        assert response.status_code == 200
        assert response.json() == {'ID': '1'}
        assert 'access_token=test_key' in responses.calls[0].request.url

    @responses.activate
    def test_request_not_found(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/listings/999',
                      status=404)
        with pytest.raises(ResourceNotFoundError):
            client.request('get', 'listings/999')

    @responses.activate
    def test_request_custom_headers(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/listings/',
                      json={}, status=200)
        client.request('get', 'listings/', headers={'X-Custom': 'Value'})
        assert responses.calls[0].request.headers['X-Custom'] == 'Value'

    @responses.activate
    def test_request_post_data(self, client):
        responses.add(responses.POST, 'https://www.upwoof.com/api/v1/listings/',
                      json={}, status=201)
        client.request('post', 'listings/', query={'foo': 'bar'}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        assert responses.calls[0].request.body == 'foo=bar'

    @responses.activate
    def test_request_get_query(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/listings/',
                      json={}, status=200)
        client.request('get', 'listings/', query={'foo': 'bar'})
        assert 'foo=bar' in responses.calls[0].request.url

    def test_unsupported_method(self, client):
        with pytest.raises(ValueError, match="Unsupported method"):
            client.request('invalid', 'listings/')

    @responses.activate
    def test_request_client_error(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/listings/',
                      status=400)
        with pytest.raises(ClientError):
            client.request('get', 'listings/')

class TestResources:
    def test_resource_object_parsing(self):
        class MockResponse:
            def json(self): return {'ID': '1', 'DATE_CREATED_UTC': '2023-01-01T00:00:00Z'}
        
        listing = Listing.parse(MockResponse())
        assert listing.id == '1'
        assert isinstance(listing.date_created_utc, datetime)

    def test_resource_object_list_parsing(self):
        class MockResponse:
            def json(self): return [{'ID': '1'}, {'ID': '2'}]
        
        listings = Listing.parse(MockResponse())
        assert len(listings) == 2
        assert listings[0].id == '1'
        assert listings[1].id == '2'

    def test_resource_object_getattr_error(self):
        listing = Listing({'ID': '1'})
        with pytest.raises(AttributeError):
            _ = listing.non_existent

    def test_resource_object_repr(self):
        listing = Listing({'ID': '1', 'DATE_CREATED_UTC': '2023-01-01T00:00:00Z'})
        # Should contain class name and some attributes
        rep = repr(listing)
        assert 'Listing' in rep
        assert 'date_created_utc' in rep

    def test_resource_object_serialize(self):
        listing = Listing({'ID': '1', 'DATE_CREATED_UTC': '2023-01-01T00:00:00Z'})
        serialized = listing.serialize()
        assert serialized['DATE_CREATED_UTC'] == '2023-01-01T00:00:00+00:00'

    def test_resource_object_parse_blank(self):
        with pytest.raises(ValueError, match="Response cannot be blank"):
            Listing.parse(None)

    def test_resource_object_parse_none_json(self):
        class MockResponse:
            def json(self): return "not a dict or list"
        assert Listing.parse(MockResponse()) is None

class TestDSL:
    @responses.activate
    def test_get_listings(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/listings/',
                      json=[{'ID': '1'}], status=200)
        listings = client.get_listings()
        assert len(listings) == 1
        assert listings[0].id == '1'

    @responses.activate
    def test_get_listing(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/listings/1',
                      json={'ID': '1'}, status=200)
        listing = client.get_listing(resource_id='1')
        assert listing.id == '1'

    def test_get_listing_blank_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing(resource_id='')

    @responses.activate
    def test_update_listing_blank_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.update_listing(resource_id='', params={})

    @responses.activate
    def test_patch_listing_blank_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_listing(resource_id='', params={})

    @responses.activate
    def test_delete_listing_blank_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_listing(resource_id='')

    @responses.activate
    def test_create_listing(self, client):
        responses.add(responses.POST, 'https://www.upwoof.com/api/v1/listings/',
                      json={'ID': '2'}, status=201)
        listing = client.create_listing(params={'NAME': 'New Listing'})
        assert listing.id == '2'
        assert responses.calls[0].request.body == b'{"NAME": "New Listing"}'

    @responses.activate
    def test_update_listing(self, client):
        responses.add(responses.PUT, 'https://www.upwoof.com/api/v1/listings/1',
                      json={'ID': '1'}, status=200)
        listing = client.update_listing(resource_id='1', params={'NAME': 'Updated'})
        assert listing.id == '1'

    @responses.activate
    def test_patch_listing(self, client):
        responses.add(responses.PATCH, 'https://www.upwoof.com/api/v1/listings/1',
                      json={'ID': '1'}, status=200)
        listing = client.patch_listing(resource_id='1', params={'NAME': 'Patched'})
        assert listing.id == '1'

    @responses.activate
    def test_delete_listing(self, client):
        responses.add(responses.DELETE, 'https://www.upwoof.com/api/v1/listings/1',
                      status=204)
        assert client.delete_listing(resource_id='1') is True

class TestGlobalClient:
    def test_global_client_init(self):
        upwoof_listings.api_key = 'global_key'
        c = upwoof_listings.get_client()
        assert c.api_key == 'global_key'
        assert upwoof_listings.get_client() is c # Singleton-ish

class TestAllDSL:
    @responses.activate
    def test_all_dsl_methods(self, client):
        # We'll just test one method from each to ensure coverage of the dsl/__init__.py
        methods = [
            ('get_pets', 'pets/'),
            ('get_accommodations', 'accommodations/'),
            ('get_credit_notes', 'credit_notes/'),
            ('get_customers', 'customers/'),
            ('get_invoices', 'invoices/'),
            ('get_orders', 'orders/'),
            ('get_reservations', 'reservations/'),
            ('get_users', 'users/'),
            ('get_accommodation_types', 'accommodation_types/'),
            ('get_animal_types', 'animal_types/'),
            ('get_breeds', 'breeds/'),
        ]
        for method_name, path in methods:
            responses.add(responses.GET, f'https://www.upwoof.com/api/v1/{path}',
                          json=[], status=200)
            getattr(client, method_name)()
        
        # Test all types of methods for one resource to cover the boilerplate
        res_types = [
            ('pet', 'pets'),
            ('accommodation', 'accommodations'),
            ('credit_note', 'credit_notes'),
            ('customer', 'customers'),
            ('invoice', 'invoices'),
            ('order', 'orders'),
            ('reservation', 'reservations'),
            ('user', 'users'),
            ('listing', 'listings'),
        ]
        for single, plural in res_types:
            # get single
            responses.add(responses.GET, f'https://www.upwoof.com/api/v1/{plural}/1', json={}, status=200)
            getattr(client, f'get_{single}')(resource_id='1')
            # create
            responses.add(responses.POST, f'https://www.upwoof.com/api/v1/{plural}/', json={}, status=201)
            getattr(client, f'create_{single}')(params={})
            # update
            responses.add(responses.PUT, f'https://www.upwoof.com/api/v1/{plural}/1', json={}, status=200)
            getattr(client, f'update_{single}')(resource_id='1', params={})
            # patch
            responses.add(responses.PATCH, f'https://www.upwoof.com/api/v1/{plural}/1', json={}, status=200)
            getattr(client, f'patch_{single}')(resource_id='1', params={})
            # delete
            responses.add(responses.DELETE, f'https://www.upwoof.com/api/v1/{plural}/1', status=204)
            getattr(client, f'delete_{single}')(resource_id='1')

        # Resource specific singletons
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/accommodation_types/1', json={}, status=200)
        client.get_accommodation_type(resource_id='1')
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/animal_types/1', json={}, status=200)
        client.get_animal_type(resource_id='1')
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/breeds/1', json={}, status=200)
        client.get_breed(resource_id='1')

        # New endpoints
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/users/me', json={}, status=200)
        client.get_user_me()

        responses.add(responses.POST, 'https://www.upwoof.com/api/v1/credit_notes/1/void', json={}, status=200)
        client.void_credit_note(resource_id='1')

        responses.add(responses.POST, 'https://www.upwoof.com/api/v1/invoices/1/pay_out_of_band', json={}, status=200)
        client.pay_invoice_out_of_band(resource_id='1')

    def test_resources_property(self, client):
        from upwoof_listings import resources
        assert client.resources == resources

    def test_dsl_blank_id_errors(self, client):
        with pytest.raises(ValueError):
            client.get_pet(resource_id='')
        with pytest.raises(ValueError):
            client.update_pet(resource_id='', params={})
        with pytest.raises(ValueError):
            client.patch_pet(resource_id='', params={})
        with pytest.raises(ValueError):
            client.delete_pet(resource_id='')
        
        with pytest.raises(ValueError):
            client.void_credit_note(resource_id='')
        with pytest.raises(ValueError):
            client.pay_invoice_out_of_band(resource_id='')

        with pytest.raises(ValueError):
            client.get_accommodation(resource_id='')
        with pytest.raises(ValueError):
            client.update_accommodation(resource_id='', params={})
        with pytest.raises(ValueError):
            client.patch_accommodation(resource_id='', params={})
        with pytest.raises(ValueError):
            client.delete_accommodation(resource_id='')

        with pytest.raises(ValueError):
            client.get_credit_note(resource_id='')
        with pytest.raises(ValueError):
            client.update_credit_note(resource_id='', params={})
        with pytest.raises(ValueError):
            client.patch_credit_note(resource_id='', params={})
        with pytest.raises(ValueError):
            client.delete_credit_note(resource_id='')

        with pytest.raises(ValueError):
            client.get_customer(resource_id='')
        with pytest.raises(ValueError):
            client.update_customer(resource_id='', params={})
        with pytest.raises(ValueError):
            client.patch_customer(resource_id='', params={})
        with pytest.raises(ValueError):
            client.delete_customer(resource_id='')

        with pytest.raises(ValueError):
            client.get_invoice(resource_id='')
        with pytest.raises(ValueError):
            client.update_invoice(resource_id='', params={})
        with pytest.raises(ValueError):
            client.patch_invoice(resource_id='', params={})
        with pytest.raises(ValueError):
            client.delete_invoice(resource_id='')

        with pytest.raises(ValueError):
            client.get_order(resource_id='')
        with pytest.raises(ValueError):
            client.update_order(resource_id='', params={})
        with pytest.raises(ValueError):
            client.patch_order(resource_id='', params={})
        with pytest.raises(ValueError):
            client.delete_order(resource_id='')

        with pytest.raises(ValueError):
            client.get_reservation(resource_id='')
        with pytest.raises(ValueError):
            client.update_reservation(resource_id='', params={})
        with pytest.raises(ValueError):
            client.patch_reservation(resource_id='', params={})
        with pytest.raises(ValueError):
            client.delete_reservation(resource_id='')

        with pytest.raises(ValueError):
            client.get_user(resource_id='')
        with pytest.raises(ValueError):
            client.update_user(resource_id='', params={})
        with pytest.raises(ValueError):
            client.patch_user(resource_id='', params={})
        with pytest.raises(ValueError):
            client.delete_user(resource_id='')

        with pytest.raises(ValueError):
            client.get_accommodation_type(resource_id='')
        with pytest.raises(ValueError):
            client.get_animal_type(resource_id='')
        with pytest.raises(ValueError):
            client.get_breed(resource_id='')

def test_serializer_basic():
    from upwoof_listings.resources.object import Serializer
    assert Serializer.serialize(123) == '123'
    assert Serializer.deserialize({'KEY': 'VAL', 'NESTED': {'K': 'V'}}) == {'key': 'VAL', 'nested': {'k': 'V'}}
    assert Serializer.deserialize(['A', {'K': 'V'}]) == ['A', {'k': 'V'}]
    assert Serializer.deserialize('plain') == 'plain'
