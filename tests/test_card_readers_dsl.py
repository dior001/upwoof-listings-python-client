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


class TestCardReadersDSL:
    @responses.activate
    def test_get_listing_card_readers(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/card_readers", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'page': '2'})],
                      json=[{'id': 5, 'label': 'Front desk', 'online': True, 'status': 'online'}])
        readers = client.get_listing_card_readers(listing_id='1', params={'page': 2})
        assert readers[0].label == 'Front desk'
        assert readers[0].online is True

    @responses.activate
    def test_create_listing_card_reader(self, client):
        params = {'label': 'Front desk', 'registration_code': 'simulated-wpe'}
        responses.add(responses.POST, f"{BASE}listings/1/card_readers", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json={'id': 5, 'label': 'Front desk', 'device_type': 'bbpos_wisepos_e'})
        assert client.create_listing_card_reader(listing_id='1', params=params).device_type == 'bbpos_wisepos_e'

    @responses.activate
    def test_create_listing_card_reader_needs_two_factor(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/card_readers", status=403, json={'error': 'Forbidden'})
        with pytest.raises(ClientError):
            client.create_listing_card_reader(listing_id='1', params={'label': 'x', 'registration_code': 'y'})

    @responses.activate
    def test_create_listing_card_reader_refused_by_stripe(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/card_readers", status=422,
                      json={'error': 'card_reader_not_registered', 'message': 'Stripe refused the code'})
        with pytest.raises(ValidationError) as raised:
            client.create_listing_card_reader(listing_id='1', params={'label': 'x', 'registration_code': 'y'})
        assert raised.value.errors == ['Stripe refused the code']

    @responses.activate
    def test_delete_listing_card_reader(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/card_readers/5", status=204)
        assert client.delete_listing_card_reader(listing_id='1', card_reader_id='5') is True

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_card_readers(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_listing_card_reader(listing_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_listing_card_reader(listing_id='1', card_reader_id='')


class TestTerminalPaymentsDSL:
    @pytest.mark.parametrize('payables,kwarg,kind', [('invoices', 'invoice_id', 'invoice'),
                                                      ('retail_sales', 'retail_sale_id', 'retail_sale')])
    @responses.activate
    def test_create_get_and_cancel(self, client, payables, kwarg, kind):
        url = f"{BASE}listings/1/{payables}/9/terminal_payment"
        responses.add(responses.POST, url, status=201, match=[matchers.json_params_matcher({'card_reader_id': 5})],
                      json={'id': 3, 'status': 'processing', 'payable_id': 9, 'amount_cents': 4500})
        responses.add(responses.GET, url, status=200, json={'id': 3, 'status': 'succeeded'})
        responses.add(responses.POST, f"{url}/cancel", status=200, json={'id': 3, 'status': 'canceled'})
        ids = {'listing_id': '1', kwarg: '9'}
        assert getattr(client, f"create_{kind}_terminal_payment")(**ids, card_reader_id=5).status == 'processing'
        assert getattr(client, f"get_{kind}_terminal_payment")(**ids).status == 'succeeded'
        assert getattr(client, f"cancel_{kind}_terminal_payment")(**ids).status == 'canceled'

    @responses.activate
    def test_get_invoice_terminal_payment_none_started(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/invoices/9/terminal_payment", status=404, json={})
        with pytest.raises(ResourceNotFoundError):
            client.get_invoice_terminal_payment(listing_id='1', invoice_id='9')

    @responses.activate
    def test_create_invoice_terminal_payment_nothing_to_collect(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/invoices/9/terminal_payment", status=422,
                      json={'error': 'not_collectable', 'message': 'Nothing to collect'})
        with pytest.raises(ValidationError):
            client.create_invoice_terminal_payment(listing_id='1', invoice_id='9', card_reader_id=5)

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_invoice_terminal_payment(listing_id='1', invoice_id='9', card_reader_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_retail_sale_terminal_payment(listing_id='1', retail_sale_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.cancel_invoice_terminal_payment(listing_id='', invoice_id='9')
