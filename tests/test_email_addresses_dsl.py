import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ResourceNotFoundError, ValidationError

BASE = "https://www.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestEmailAddressesDSL:
    @responses.activate
    def test_get_listing_email_addresses(self, client):
        query = {'access_token': 'test_key', 'page': '2'}
        responses.add(responses.GET, f"{BASE}listings/1/email_addresses", status=200,
                      match=[matchers.query_param_matcher(query)],
                      json=[{'id': 2, 'role_key': 'bookings', 'email_address': 'bookings+1@upwoof.net',
                             'selected_user_ids': []}])
        addresses = client.get_listing_email_addresses(listing_id='1', params={'page': 2})
        assert addresses[0].email_address == 'bookings+1@upwoof.net'

    @responses.activate
    def test_get_listing_email_address(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/email_addresses/2", status=200,
                      json={'id': 2, 'recipient_scope': 'owners_and_managers'})
        address = client.get_listing_email_address(listing_id='1', listing_email_address_id='2')
        assert address.recipient_scope == 'owners_and_managers'

    @responses.activate
    def test_get_listing_email_address_not_found(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/email_addresses/9", status=404, json={'error': 'not_found'})
        with pytest.raises(ResourceNotFoundError):
            client.get_listing_email_address(listing_id='1', listing_email_address_id='9')

    @responses.activate
    def test_create_listing_email_address(self, client):
        params = {'name': 'Grooming', 'role_key': 'grooming', 'recipient_scope': 'selected',
                  'selected_user_ids': [5], 'show_on_profile': True}
        responses.add(responses.POST, f"{BASE}listings/1/email_addresses", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json={'id': 3, 'role_key': 'grooming', 'selected_user_ids': [5]})
        address = client.create_listing_email_address(listing_id='1', params=params)
        assert address.selected_user_ids == [5]

    @responses.activate
    def test_create_listing_email_address_reserved_role_key(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/email_addresses", status=422,
                      json={'errors': ['Role key is reserved']})
        with pytest.raises(ValidationError):
            client.create_listing_email_address(listing_id='1', params={'name': 'Admin', 'role_key': 'admin'})

    @responses.activate
    def test_patch_listing_email_address(self, client):
        responses.add(responses.PATCH, f"{BASE}listings/1/email_addresses/3", status=200,
                      match=[matchers.json_params_matcher({'active': False})], json={'id': 3, 'active': False})
        address = client.patch_listing_email_address(listing_id='1', listing_email_address_id='3',
                                                     params={'active': False})
        assert address.active is False

    @responses.activate
    def test_patch_bookings_role_key_refused(self, client):
        responses.add(responses.PATCH, f"{BASE}listings/1/email_addresses/2", status=422,
                      json={'error': 'bookings_role_key', 'message': "The bookings address's role key can't change"})
        with pytest.raises(ValidationError):
            client.patch_listing_email_address(listing_id='1', listing_email_address_id='2',
                                               params={'role_key': 'stays'})

    @responses.activate
    def test_delete_listing_email_address(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/email_addresses/3", status=204)
        assert client.delete_listing_email_address(listing_id='1', listing_email_address_id='3') is True

    @responses.activate
    def test_delete_bookings_address_refused(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/email_addresses/2", status=422,
                      json={'error': 'bookings_address', 'message': "The bookings address can't be deleted"})
        with pytest.raises(ValidationError):
            client.delete_listing_email_address(listing_id='1', listing_email_address_id='2')

    @responses.activate
    def test_get_listing_inbound_emails(self, client):
        query = {'access_token': 'test_key', 'outcome': 'lead_created', 'since': '2026-11-01T00:00:00Z'}
        responses.add(responses.GET, f"{BASE}listings/1/inbound_emails", status=200,
                      match=[matchers.query_param_matcher(query)],
                      json=[{'id': 7, 'outcome': 'lead_created', 'lead_id': 4, 'reason': None,
                             'sender_email': 'jo@example.com', 'sender_verified': True}])
        emails = client.get_listing_inbound_emails(
            listing_id='1', params={'outcome': 'lead_created', 'since': '2026-11-01T00:00:00Z'})
        assert emails[0].lead_id == 4
        assert emails[0].reason is None

    @responses.activate
    def test_customer_upwoof_email_address(self, client):
        responses.add(responses.GET, f"{BASE}customers/5", status=200,
                      json={'id': 5, 'upwoof_email_address': 'jo+abc123@upwoof.net'})
        assert client.get_customer(resource_id='5').upwoof_email_address == 'jo+abc123@upwoof.net'

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_email_addresses(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_email_address(listing_id='1', listing_email_address_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_listing_email_address(listing_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_listing_email_address(listing_id='1', listing_email_address_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_listing_email_address(listing_id='', listing_email_address_id='2')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_inbound_emails(listing_id='')
