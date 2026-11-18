import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ResourceNotFoundError, ValidationError

BASE = "https://pethotels.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


ANSWERS = [{'custom_field_definition_id': 7, 'value': 'Chip 123'}]


class TestCustomFieldsDSL:
    @responses.activate
    def test_get_listing_custom_field_definitions(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/custom_field_definitions", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'record_type': 'pet'})],
                      json=[{'id': 7, 'label': 'Microchip', 'field_type': 'text', 'group_wide': False}])
        definitions = client.get_listing_custom_field_definitions(listing_id='1', params={'record_type': 'pet'})
        assert definitions[0].label == 'Microchip'

    @pytest.mark.parametrize('method, collection', [
        ('update_customer_custom_fields', 'customers'),
        ('update_pet_custom_fields', 'pets'),
        ('update_reservation_custom_fields', 'reservations'),
    ])
    @responses.activate
    def test_update_custom_fields(self, client, method, collection):
        responses.add(responses.PUT, f"{BASE}{collection}/5/custom_fields", status=200,
                      match=[matchers.json_params_matcher({'listing_id': '1', 'custom_fields': ANSWERS})],
                      json={'id': 5, 'custom_fields': [{'custom_field_definition_id': 7, 'value': 'Chip 123',
                                                        'display_value': 'Chip 123'}]})
        record = getattr(client, method)(resource_id='5', listing_id='1', custom_fields=ANSWERS)
        assert record.custom_fields[0]['display_value'] == 'Chip 123'

    @responses.activate
    def test_unknown_custom_field_ids(self, client):
        responses.add(responses.PUT, f"{BASE}pets/5/custom_fields", status=422,
                      json={'error': 'unprocessable entity', 'unknown_custom_field_ids': ['99'], 'errors': {}})
        with pytest.raises(ValidationError) as raised:
            client.update_pet_custom_fields(resource_id='5', listing_id='1',
                                            custom_fields=[{'custom_field_definition_id': 99, 'value': 'x'}])
        assert raised.value.body['unknown_custom_field_ids'] == ['99']
        assert raised.value.errors == []

    @responses.activate
    def test_refused_answer(self, client):
        responses.add(responses.PUT, f"{BASE}pets/5/custom_fields", status=422,
                      json={'error': 'unprocessable entity', 'unknown_custom_field_ids': [],
                            'errors': {'7': 'is not a number'}})
        with pytest.raises(ValidationError) as raised:
            client.update_pet_custom_fields(resource_id='5', listing_id='1', custom_fields=ANSWERS)
        assert raised.value.errors == ['is not a number']
        assert raised.value.body['errors'] == {'7': 'is not a number'}

    def test_blank_arguments(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_custom_field_definitions(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.update_pet_custom_fields(resource_id='', listing_id='1', custom_fields=ANSWERS)
        with pytest.raises(ValueError, match="Listing ID cannot be blank"):
            client.update_pet_custom_fields(resource_id='5', listing_id='', custom_fields=ANSWERS)
        with pytest.raises(ValueError, match="Custom fields cannot be blank"):
            client.update_pet_custom_fields(resource_id='5', listing_id='1', custom_fields=[])


class TestSpecialOpeningHoursDSL:
    @responses.activate
    def test_get_listing_special_opening_hours(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/special_opening_hours", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'from': '2026-12-01'})],
                      json=[{'id': 3, 'date': '2026-12-24', 'when_open': '09:00', 'when_close': '12:00',
                             'pick_up_and_drop_off_windows': []}])
        hours = client.get_listing_special_opening_hours(listing_id='1', params={'from': '2026-12-01'})
        assert hours[0].when_close == '12:00'

    def test_blank_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_special_opening_hours(listing_id='')


class TestNotificationTemplatesDSL:
    @responses.activate
    def test_get_listing_notification_templates(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/notification_templates", status=200,
                      json=[{'id': 1, 'notification_key': 'reservation_confirmed', 'channel': 'email'}])
        templates = client.get_listing_notification_templates(listing_id='1')
        assert templates[0].channel == 'email'

    @responses.activate
    def test_update_listing_notification_template(self, client):
        params = {'notification_key': 'upcoming_stay_reminder', 'channel': 'sms', 'enabled': False}
        responses.add(responses.PUT, f"{BASE}listings/1/notification_templates", status=200,
                      match=[matchers.json_params_matcher(params)], json={'id': 2, 'enabled': False})
        assert client.update_listing_notification_template(listing_id='1', params=params).enabled is False

    @responses.activate
    def test_delete_listing_notification_template_sends_the_key_in_the_query(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/notification_templates", status=204,
                      match=[matchers.query_param_matcher({'access_token': 'test_key',
                                                           'notification_key': 'invoice_finalized',
                                                           'channel': 'email', 'reservation_type': 'grooming'})])
        assert client.delete_listing_notification_template(listing_id='1', notification_key='invoice_finalized',
                                                           channel='email', reservation_type='grooming') is True

    @responses.activate
    def test_delete_listing_notification_template_without_a_type(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/notification_templates", status=404,
                      match=[matchers.query_param_matcher({'access_token': 'test_key',
                                                           'notification_key': 'reservation_confirmed',
                                                           'channel': 'sms'})])
        with pytest.raises(ResourceNotFoundError):
            client.delete_listing_notification_template(listing_id='1', notification_key='reservation_confirmed',
                                                        channel='sms')

    def test_blank_arguments(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_notification_templates(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.update_listing_notification_template(listing_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_listing_notification_template(listing_id='', notification_key='k', channel='email')
        with pytest.raises(ValueError, match="cannot be blank"):
            client.delete_listing_notification_template(listing_id='1', notification_key='', channel='email')
