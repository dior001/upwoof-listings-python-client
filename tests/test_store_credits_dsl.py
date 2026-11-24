import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError, ValidationError

BASE = "https://www.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestStoreCreditsDSL:
    @responses.activate
    def test_get_customer_store_credit(self, client):
        responses.add(responses.GET, f"{BASE}customers/2/store_credit", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'listing_id': '1'})],
                      json={'id': None, 'balance_cents': 0, 'currency': 'NZD', 'updated_at': None})
        account = client.get_customer_store_credit(customer_id='2', listing_id='1')
        assert account.balance_cents == 0
        assert account.id is None
        assert account.updated_at is None

    @responses.activate
    def test_get_customer_store_credit_transactions(self, client):
        responses.add(responses.GET, f"{BASE}customers/2/store_credit/transactions", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'listing_id': '1',
                                                           'page': '2'})],
                      json=[{'id': 9, 'amount_cents': -500, 'entry_type': 'redemption'}])
        transactions = client.get_customer_store_credit_transactions(customer_id='2', listing_id='1',
                                                                     params={'page': 2})
        assert transactions[0].entry_type == 'redemption'

    @pytest.mark.parametrize('entry_type', ['loyalty_conversion', 'deposit_overpayment', 'group_departure'])
    @responses.activate
    def test_get_customer_store_credit_transactions_new_entry_types(self, client, entry_type):
        responses.add(responses.GET, f"{BASE}customers/2/store_credit/transactions", status=200,
                      json=[{'id': 10, 'amount_cents': 500, 'entry_type': entry_type}])
        transactions = client.get_customer_store_credit_transactions(customer_id='2', listing_id='1')
        assert transactions[0].entry_type == entry_type

    @responses.activate
    def test_adjust_customer_store_credit(self, client):
        params = {'listing_id': 1, 'amount_cents': 1500, 'reason': 'Goodwill'}
        responses.add(responses.POST, f"{BASE}customers/2/store_credit/adjustments", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json={'id': 10, 'amount_cents': 1500, 'balance_after_cents': 1500,
                            'entry_type': 'manual_adjustment', 'created_at': '2026-11-18T01:00:00Z'})
        transaction = client.adjust_customer_store_credit(customer_id='2', params=params)
        assert transaction.balance_after_cents == 1500
        assert transaction.created_at.year == 2026

    @responses.activate
    def test_adjust_customer_store_credit_insufficient(self, client):
        responses.add(responses.POST, f"{BASE}customers/2/store_credit/adjustments", status=422,
                      json={'error': 'unprocessable entity', 'message': 'Insufficient store credit'})
        with pytest.raises(ValidationError) as raised:
            client.adjust_customer_store_credit(customer_id='2', params={'listing_id': 1, 'amount_cents': -99,
                                                                        'reason': 'Oops'})
        assert raised.value.errors == ['Insufficient store credit']

    @responses.activate
    def test_adjust_customer_store_credit_forbidden(self, client):
        responses.add(responses.POST, f"{BASE}customers/2/store_credit/adjustments", status=403,
                      json={'error': 'forbidden'})
        with pytest.raises(ClientError) as raised:
            client.adjust_customer_store_credit(customer_id='2', params={})
        assert raised.value.response.status_code == 403

    def test_blank_arguments(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_customer_store_credit(customer_id='', listing_id='1')
        with pytest.raises(ValueError, match="Listing ID cannot be blank"):
            client.get_customer_store_credit(customer_id='2', listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_customer_store_credit_transactions(customer_id='', listing_id='1')
        with pytest.raises(ValueError, match="Listing ID cannot be blank"):
            client.get_customer_store_credit_transactions(customer_id='2', listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.adjust_customer_store_credit(customer_id='', params={})
