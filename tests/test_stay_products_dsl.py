import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ValidationError

BASE = "https://pethotels.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestStayProductsDSL:
    @responses.activate
    def test_get_listing_stay_products(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/stay_products", status=200,
                      json=[{'id': 4, 'name': 'Chew toy', 'price_cents': 1200, 'currency': 'NZD',
                             'quantity_on_hand': 9}])
        products = client.get_listing_stay_products(listing_id='1')
        assert isinstance(products[0], client.resources.StayProduct)
        assert products[0].quantity_on_hand == 9

    @responses.activate
    def test_get_and_create_reservation_retail_items(self, client):
        responses.add(responses.GET, f"{BASE}reservations/3/retail_items", status=200,
                      json=[{'id': 6, 'retail_product_id': 4, 'quantity': 2, 'unit_price_cents': 1200}])
        responses.add(responses.POST, f"{BASE}reservations/3/retail_items", status=201,
                      match=[matchers.json_params_matcher({'retail_product_id': 4, 'quantity': 2})],
                      json={'id': 6, 'name': 'Chew toy', 'quantity': 2, 'stock_taken_quantity': 0})
        items = client.get_reservation_retail_items(reservation_id='3')
        assert isinstance(items[0], client.resources.ReservationRetailItem)
        item = client.create_reservation_retail_item(reservation_id='3',
                                                     params={'retail_product_id': 4, 'quantity': 2})
        assert item.name == 'Chew toy'

    @responses.activate
    def test_create_reservation_retail_item_refused(self, client):
        responses.add(responses.POST, f"{BASE}reservations/3/retail_items", status=422,
                      json={'errors': ['This product is already on the stay']})
        with pytest.raises(ValidationError) as raised:
            client.create_reservation_retail_item(reservation_id='3', params={'retail_product_id': 4})
        assert raised.value.errors == ['This product is already on the stay']

    @responses.activate
    def test_delete_reservation_retail_item(self, client):
        responses.add(responses.DELETE, f"{BASE}reservations/3/retail_items/6", status=204)
        assert client.delete_reservation_retail_item(reservation_id='3', retail_item_id='6')

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_stay_products(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_reservation_retail_items(reservation_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_reservation_retail_item(reservation_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_reservation_retail_item(reservation_id='3', retail_item_id='')
