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


class TestAiTasksDSL:
    @responses.activate
    def test_get_listing_ai_tasks(self, client):
        query = {'access_token': 'test_key', 'status': 'awaiting_review', 'listing_email_address_id': '2'}
        responses.add(responses.GET, f"{BASE}listings/1/ai_tasks", status=200,
                      match=[matchers.query_param_matcher(query)],
                      json=[{'id': 9, 'status': 'awaiting_review', 'recommended_action': 'reply',
                             'recommended_params': {'message': 'Yes, we have room'}, 'held_reason': 'review_required'}])
        tasks = client.get_listing_ai_tasks(listing_id='1',
                                            params={'status': 'awaiting_review', 'listing_email_address_id': 2})
        assert tasks[0].recommended_action == 'reply'
        assert tasks[0].recommended_params['message'] == 'Yes, we have room'

    @responses.activate
    def test_get_listing_ai_task(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/ai_tasks/9", status=200,
                      json={'id': 9, 'body_text': 'Room for Rex?', 'recommendation': 'Reply to say yes'})
        task = client.get_listing_ai_task(listing_id='1', task_id='9')
        assert task.body_text == 'Room for Rex?'

    @responses.activate
    def test_get_listing_ai_task_not_found(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/ai_tasks/8", status=404, json={'error': 'not_found'})
        with pytest.raises(ResourceNotFoundError):
            client.get_listing_ai_task(listing_id='1', task_id='8')

    @responses.activate
    def test_approve_listing_ai_task(self, client):
        body = {'params': {'message': 'Yes, see you then', 'pet_ids': [3]}}
        responses.add(responses.POST, f"{BASE}listings/1/ai_tasks/9/approve", status=201,
                      match=[matchers.json_params_matcher(body)],
                      json={'id': 9, 'status': 'completed', 'amended': True, 'executed_action': 'reply'})
        task = client.approve_listing_ai_task(listing_id='1', task_id='9', params=body)
        assert task.status == 'completed'
        assert task.amended is True

    @responses.activate
    def test_approve_listing_ai_task_refused(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/ai_tasks/9/approve", status=422,
                      json={'error': 'ai_task_refused', 'message': 'This task is no longer waiting for review'})
        with pytest.raises(ValidationError):
            client.approve_listing_ai_task(listing_id='1', task_id='9')

    @responses.activate
    def test_decline_listing_ai_task(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/ai_tasks/9/decline", status=201,
                      match=[matchers.json_params_matcher({'note': 'Already called them'})],
                      json={'id': 9, 'status': 'declined', 'decline_note': 'Already called them'})
        task = client.decline_listing_ai_task(listing_id='1', task_id='9', params={'note': 'Already called them'})
        assert task.decline_note == 'Already called them'

    @responses.activate
    def test_handle_listing_ai_task(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/ai_tasks/9/handled", status=201,
                      json={'id': 9, 'status': 'completed', 'reviewed_by_user_id': 4})
        assert client.handle_listing_ai_task(listing_id='1', task_id='9').reviewed_by_user_id == 4

    @responses.activate
    def test_listing_email_address_ai_role(self, client):
        body = {'ai_role': 'bookings', 'ai_review_required': False, 'ai_automatic_confirmation': True,
                'ai_instructions': 'Never book cats'}
        responses.add(responses.PATCH, f"{BASE}listings/1/email_addresses/2", status=200,
                      match=[matchers.json_params_matcher(body)],
                      json={'id': 2, 'ai_role': 'bookings', 'ai_active': True, 'ai_review_required': False,
                            'ai_automatic_since': '2026-11-25T01:00:00Z', 'ai_automatic_enabled_by_user_id': 4})
        address = client.patch_listing_email_address(listing_id='1', listing_email_address_id='2', params=body)
        assert address.ai_role == 'bookings'
        assert address.ai_review_required is False

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_ai_tasks(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_ai_task(listing_id='1', task_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.approve_listing_ai_task(listing_id='', task_id='9')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.decline_listing_ai_task(listing_id='1', task_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.handle_listing_ai_task(listing_id='', task_id='9')
