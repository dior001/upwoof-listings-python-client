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


class TestConversationsDSL:
    @responses.activate
    def test_get_listing_conversations(self, client):
        query = {'access_token': 'test_key', 'customer_id': '4', 'updated_since': '2026-11-25T00:00:00Z'}
        responses.add(responses.GET, f"{BASE}listings/1/conversations", status=200,
                      match=[matchers.query_param_matcher(query)],
                      json=[{'id': 7, 'subject': 'Room next week?',
                             'participants': [{'customer_id': 4, 'kind': 'customer', 'name': 'Ana Ruiz'}]}])
        conversations = client.get_listing_conversations(
            listing_id='1', params={'customer_id': 4, 'updated_since': '2026-11-25T00:00:00Z'})
        assert conversations[0].subject == 'Room next week?'
        assert conversations[0].participants[0]['kind'] == 'customer'

    @responses.activate
    def test_get_listing_conversation(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/conversations/7", status=200,
                      json={'id': 7, 'messages': [{'id': 9, 'body': 'Room for Rex?', 'origin': 'email'}]})
        conversation = client.get_listing_conversation(listing_id='1', conversation_id='7')
        assert conversation.messages[0]['origin'] == 'email'

    @responses.activate
    def test_get_listing_conversation_not_found(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/conversations/8", status=404, json={'error': 'not_found'})
        with pytest.raises(ResourceNotFoundError):
            client.get_listing_conversation(listing_id='1', conversation_id='8')

    @responses.activate
    def test_create_listing_conversation_message(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/conversations/7/messages", status=201,
                      match=[matchers.json_params_matcher({'body': 'Yes, from Monday.'})],
                      json={'id': 10, 'body': 'Yes, from Monday.', 'origin': 'api', 'sender_kind': 'team_member'})
        message = client.create_listing_conversation_message(listing_id='1', conversation_id='7',
                                                             params={'body': 'Yes, from Monday.'})
        assert message.origin == 'api'
        assert message.sender_kind == 'team_member'

    @responses.activate
    def test_create_listing_conversation_message_not_a_participant(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/conversations/7/messages", status=403,
                      json={'error': 'not_a_participant'})
        with pytest.raises(ClientError):
            client.create_listing_conversation_message(listing_id='1', conversation_id='7', params={'body': 'Hi'})

    @responses.activate
    def test_create_listing_conversation_message_not_sent(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/conversations/7/messages", status=422,
                      json={'error': 'message_not_sent'})
        with pytest.raises(ValidationError):
            client.create_listing_conversation_message(listing_id='1', conversation_id='7', params={'body': 'Hi'})

    def test_blank_arguments(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_conversations(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_conversation(listing_id='1', conversation_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_listing_conversation_message(listing_id='', conversation_id='7', params={'body': 'Hi'})
        with pytest.raises(ValueError, match="Params cannot be blank"):
            client.create_listing_conversation_message(listing_id='1', conversation_id='7', params={})
