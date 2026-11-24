import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError, ResourceNotFoundError, ValidationError

BASE = "https://www.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestAuthorizedPickupsDSL:
    @responses.activate
    def test_get_customer_authorized_pickups_sends_the_listing(self, client):
        responses.add(responses.GET, f"{BASE}customers/7/authorized_pickups", status=200,
                      match=[matchers.query_string_matcher('access_token=test_key&page=2&listing_id=1')],
                      json=[{'id': 3, 'name': 'Aunt Jo', 'relationship': 'Aunt', 'customer_id': 7, 'listing_id': 1}])
        pickups = client.get_customer_authorized_pickups(customer_id='7', listing_id='1', params={'page': 2})
        assert isinstance(pickups[0], client.resources.AuthorizedPickup)
        assert pickups[0].relationship == 'Aunt'

    @responses.activate
    def test_get_customer_authorized_pickup(self, client):
        responses.add(responses.GET, f"{BASE}customers/7/authorized_pickups/3", status=200,
                      match=[matchers.query_string_matcher('access_token=test_key&listing_id=1')],
                      json={'id': 3, 'name': 'Aunt Jo', 'notes': None})
        assert client.get_customer_authorized_pickup(customer_id='7', authorized_pickup_id='3',
                                                     listing_id='1').name == 'Aunt Jo'

    @responses.activate
    def test_create_and_patch_customer_authorized_pickup(self, client):
        params = {'listing_id': 1, 'name': 'Aunt Jo', 'phone': '+64211234567'}
        responses.add(responses.POST, f"{BASE}customers/7/authorized_pickups", status=201,
                      match=[matchers.json_params_matcher(params)], json={'id': 3, 'name': 'Aunt Jo'})
        responses.add(responses.PATCH, f"{BASE}customers/7/authorized_pickups/3", status=200,
                      match=[matchers.json_params_matcher({'listing_id': 1, 'notes': 'Bring ID'})],
                      json={'id': 3, 'notes': 'Bring ID'})
        assert client.create_customer_authorized_pickup(customer_id='7', params=params).id == 3
        patched = client.patch_customer_authorized_pickup(customer_id='7', authorized_pickup_id='3',
                                                          params={'listing_id': 1, 'notes': 'Bring ID'})
        assert patched.notes == 'Bring ID'

    @responses.activate
    def test_create_customer_authorized_pickup_refused(self, client):
        responses.add(responses.POST, f"{BASE}customers/7/authorized_pickups", status=422,
                      json={'error': 'unprocessable entity', 'message': "Name can't be blank"})
        with pytest.raises(ValidationError):
            client.create_customer_authorized_pickup(customer_id='7', params={'listing_id': 1, 'name': ''})

    @responses.activate
    def test_delete_customer_authorized_pickup(self, client):
        responses.add(responses.DELETE, f"{BASE}customers/7/authorized_pickups/3", status=204,
                      match=[matchers.query_string_matcher('access_token=test_key&listing_id=1')])
        assert client.delete_customer_authorized_pickup(customer_id='7', authorized_pickup_id='3', listing_id='1')

    @responses.activate
    def test_customer_outside_the_directory(self, client):
        responses.add(responses.GET, f"{BASE}customers/9/authorized_pickups", status=404, json={'error': 'Not found'})
        with pytest.raises(ResourceNotFoundError):
            client.get_customer_authorized_pickups(customer_id='9', listing_id='1')

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_customer_authorized_pickups(customer_id='7', listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_customer_authorized_pickup(customer_id='7', authorized_pickup_id='', listing_id='1')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_customer_authorized_pickup(customer_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_customer_authorized_pickup(customer_id='7', authorized_pickup_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_customer_authorized_pickup(customer_id='7', authorized_pickup_id='3', listing_id='')


class TestCustomerTagsDSL:
    @responses.activate
    def test_get_listing_customer_tags(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/customer_tags", status=200,
                      json=[{'id': 5, 'name': 'VIP', 'colour': 'warning', 'listing_id': 1}])
        tags = client.get_listing_customer_tags(listing_id='1')
        assert isinstance(tags[0], client.resources.CustomerTag)
        assert tags[0].colour == 'warning'

    @responses.activate
    def test_create_patch_and_delete_listing_customer_tag(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/customer_tags", status=201,
                      match=[matchers.json_params_matcher({'name': 'VIP', 'colour': 'warning'})],
                      json={'id': 5, 'name': 'VIP'})
        responses.add(responses.PATCH, f"{BASE}listings/1/customer_tags/5", status=200,
                      match=[matchers.json_params_matcher({'colour': 'danger'})], json={'id': 5, 'colour': 'danger'})
        responses.add(responses.DELETE, f"{BASE}listings/1/customer_tags/5", status=204)
        assert client.create_listing_customer_tag(listing_id='1', params={'name': 'VIP', 'colour': 'warning'}).id == 5
        assert client.patch_listing_customer_tag(listing_id='1', tag_id='5',
                                                 params={'colour': 'danger'}).colour == 'danger'
        assert client.delete_listing_customer_tag(listing_id='1', tag_id='5')

    @responses.activate
    def test_delete_listing_customer_tag_used_by_a_pricing_rule(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/customer_tags/5", status=422,
                      json={'error': 'unprocessable entity', 'message': 'Pricing rules use this tag: VIP rate'})
        with pytest.raises(ValidationError):
            client.delete_listing_customer_tag(listing_id='1', tag_id='5')

    @responses.activate
    def test_tag_and_untag_listing_customer(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/customer_tags/5/customers", status=201,
                      match=[matchers.json_params_matcher({'customer_id': '7'})],
                      json={'id': 8, 'customer_id': 7, 'customer_tag_id': 5, 'assigned_by_user_id': 2})
        responses.add(responses.DELETE, f"{BASE}listings/1/customer_tags/5/customers", status=204,
                      match=[matchers.query_string_matcher('access_token=test_key&customer_id=7')])
        tagging = client.tag_listing_customer(listing_id='1', tag_id='5', customer_id='7')
        assert isinstance(tagging, client.resources.CustomerTagging)
        assert tagging.customer_tag_id == 5
        assert client.untag_listing_customer(listing_id='1', tag_id='5', customer_id='7')

    @responses.activate
    def test_staff_member_refused(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/customer_tags", status=403, json={'error': 'Forbidden'})
        with pytest.raises(ClientError):
            client.get_listing_customer_tags(listing_id='1')

    @responses.activate
    def test_get_customers_by_tag(self, client):
        responses.add(responses.GET, f"{BASE}customers/", status=200,
                      match=[matchers.query_string_matcher('access_token=test_key&customer_tag_id=5')],
                      json=[{'id': 7, 'customer_tags': [{'id': 5, 'name': 'VIP'}]}])
        customers = client.get_customers(params={'customer_tag_id': 5})
        assert customers[0].customer_tags[0]['name'] == 'VIP'

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_customer_tags(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_listing_customer_tag(listing_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_listing_customer_tag(listing_id='1', tag_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_listing_customer_tag(listing_id='1', tag_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.tag_listing_customer(listing_id='1', tag_id='5', customer_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.untag_listing_customer(listing_id='1', tag_id='', customer_id='7')
