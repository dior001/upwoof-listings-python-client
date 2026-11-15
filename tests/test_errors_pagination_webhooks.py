import base64
import hashlib
import hmac
import pytest
import responses
from upwoof_listings import webhooks
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError, ResourceNotFoundError, ValidationError

BASE = 'https://pethotels.upwoof.com/api/v1/'

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key='test_key')


class TestValidationErrors:
    @responses.activate
    def test_refused_reservation_date_change_raises_validation_error_with_errors(self, client):
        responses.add(responses.PUT, f'{BASE}reservations/2', status=422,
                      json={'errors': ['Accommodation is not available for those dates']})
        with pytest.raises(ValidationError) as raised:
            client.update_reservation(resource_id='2', params={'when_reservation_finish': '2026-12-20'})
        assert isinstance(raised.value, ClientError)
        assert raised.value.errors == ['Accommodation is not available for those dates']
        assert raised.value.response.status_code == 422

    @responses.activate
    def test_refused_patch_raises_validation_error(self, client):
        responses.add(responses.PATCH, f'{BASE}reservations/2', status=422,
                      json={'errors': ['When reservation finish must be after the start']})
        with pytest.raises(ValidationError) as raised:
            client.patch_reservation(resource_id='2', params={'when_reservation_finish': '2026-01-01'})
        assert raised.value.errors == ['When reservation finish must be after the start']

    @responses.activate
    def test_unusable_gift_card_code_is_not_found(self, client):
        responses.add(responses.POST, f'{BASE}orders/2/redeem_gift_card', status=404,
                      json={'errors': ['Gift card not found']})
        with pytest.raises(ResourceNotFoundError) as raised:
            client.redeem_gift_card(resource_id='2', code='EXPIRED1')
        assert raised.value.errors == ['Gift card not found']

    @responses.activate
    def test_order_specific_gift_card_refusal_is_a_validation_error(self, client):
        responses.add(responses.POST, f'{BASE}orders/2/redeem_gift_card', status=422,
                      json={'errors': ['This gift card has already been applied to this order']})
        with pytest.raises(ValidationError):
            client.redeem_gift_card(resource_id='2', code='GIFT123')

    @responses.activate
    def test_errors_is_empty_for_a_non_json_body(self, client):
        responses.add(responses.GET, f'{BASE}listings/', status=500, body='oops')
        with pytest.raises(ClientError) as raised:
            client.request('get', 'listings/')
        assert raised.value.errors == []
        assert not isinstance(raised.value, ValidationError)
        assert '500' in str(raised.value)


class TestPagination:
    @responses.activate
    def test_per_page_above_the_api_cap_is_clamped_to_100(self, client):
        responses.add(responses.GET, f'{BASE}reservations/', json=[], status=200)
        client.get_reservations(params={'per_page': 1000, 'page': 2})
        url = responses.calls[0].request.url
        assert 'per_page=100' in url
        assert 'page=2' in url

    @responses.activate
    def test_per_page_within_the_cap_is_sent_as_given(self, client):
        responses.add(responses.GET, f'{BASE}reservations/', json=[], status=200)
        client.get_reservations(params={'per_page': 50})
        assert 'per_page=50' in responses.calls[0].request.url

    def test_max_per_page_matches_the_api(self):
        assert Client.MAX_PER_PAGE == 100


def _sign(secret, message):
    return base64.b64encode(hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()).decode()


class TestWebhookSignatures:
    SECRET = 'whsec_test'
    BODY = '{"event_type":"reservation.confirmed","webhook_delivery_id":7,"data":{}}'

    def test_verify_signature_accepts_the_body_signature(self):
        assert webhooks.verify_signature(self.BODY, _sign(self.SECRET, self.BODY), self.SECRET)
        assert webhooks.verify_signature(self.BODY.encode(), _sign(self.SECRET, self.BODY), self.SECRET.encode())

    def test_verify_signature_rejects_a_tampered_body_or_wrong_secret(self):
        signature = _sign(self.SECRET, self.BODY)
        assert not webhooks.verify_signature(self.BODY + ' ', signature, self.SECRET)
        assert not webhooks.verify_signature(self.BODY, signature, 'other')
        assert not webhooks.verify_signature(self.BODY, None, self.SECRET)

    def test_verify_timestamped_signature_accepts_a_fresh_delivery(self):
        timestamp = '1763190000'
        signature = _sign(self.SECRET, f'{timestamp}.{self.BODY}')
        assert webhooks.verify_timestamped_signature(self.BODY, timestamp, signature, self.SECRET,
                                                     now=1763190000 + 299)

    def test_verify_timestamped_signature_rejects_a_stale_or_future_delivery(self):
        timestamp = '1763190000'
        signature = _sign(self.SECRET, f'{timestamp}.{self.BODY}')
        assert not webhooks.verify_timestamped_signature(self.BODY, timestamp, signature, self.SECRET,
                                                         now=1763190000 + 301)
        assert not webhooks.verify_timestamped_signature(self.BODY, timestamp, signature, self.SECRET,
                                                         now=1763190000 - 301)
        assert webhooks.verify_timestamped_signature(self.BODY, timestamp, signature, self.SECRET,
                                                     now=1763190000 + 600, tolerance=900)

    def test_verify_timestamped_signature_rejects_a_replayed_timestamp_swap(self):
        signature = _sign(self.SECRET, f'1763190000.{self.BODY}')
        assert not webhooks.verify_timestamped_signature(self.BODY, '1763190200', signature, self.SECRET,
                                                         now=1763190200)

    def test_verify_timestamped_signature_rejects_a_missing_or_malformed_timestamp(self):
        signature = _sign(self.SECRET, f'1763190000.{self.BODY}')
        assert not webhooks.verify_timestamped_signature(self.BODY, None, signature, self.SECRET)
        assert not webhooks.verify_timestamped_signature(self.BODY, 'yesterday', signature, self.SECRET)

    def test_verify_timestamped_signature_uses_the_current_time_by_default(self):
        import time
        timestamp = str(int(time.time()))
        signature = _sign(self.SECRET, f'{timestamp}.{self.BODY}')
        assert webhooks.verify_timestamped_signature(self.BODY, timestamp, signature, self.SECRET)

    def test_header_names(self):
        assert webhooks.SIGNATURE_HEADER == 'X-Upwoof-Signature'
        assert webhooks.TIMESTAMP_HEADER == 'X-Upwoof-Timestamp'
        assert webhooks.TIMESTAMPED_SIGNATURE_HEADER == 'X-Upwoof-Timestamped-Signature'
        assert webhooks.DEFAULT_TOLERANCE_SECONDS == 300
