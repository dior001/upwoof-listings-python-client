import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError, ResourceNotFoundError, ValidationError

BASE = "https://www.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name

SCHEDULE = {'id': 4, 'listing_id': 1, 'customer_id': 7, 'accommodation_id': 9, 'pet_ids': [3], 'active': True,
            'weekdays': ['monday', 'friday'], 'interval': 1, 'start_date': '2026-12-01', 'end_date': None,
            'skipped_dates': [], 'recurrence_description': 'Weekly on Mondays and Fridays',
            'created_at': '2026-11-23T08:00:00Z', 'updated_at': '2026-11-23T08:00:00Z'}


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestRecurringReservationSchedulesDSL:
    @responses.activate
    def test_get_recurring_reservation_schedules(self, client):
        responses.add(responses.GET, f"{BASE}recurring_reservation_schedules", status=200, json=[SCHEDULE],
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'listing_id': '1',
                                                           'active': 'True'})])
        schedules = client.get_recurring_reservation_schedules(params={'listing_id': 1, 'active': True})
        assert isinstance(schedules[0], client.resources.RecurringReservationSchedule)
        assert schedules[0].weekdays == ['monday', 'friday']

    @responses.activate
    def test_get_recurring_reservation_schedule(self, client):
        responses.add(responses.GET, f"{BASE}recurring_reservation_schedules/4", status=200, json=SCHEDULE)
        schedule = client.get_recurring_reservation_schedule(resource_id='4')
        assert schedule.recurrence_description == 'Weekly on Mondays and Fridays'

    @responses.activate
    def test_get_recurring_reservation_schedule_elsewhere(self, client):
        responses.add(responses.GET, f"{BASE}recurring_reservation_schedules/5", status=404, json={'error': 'x'})
        with pytest.raises(ResourceNotFoundError):
            client.get_recurring_reservation_schedule(resource_id='5')

    @responses.activate
    def test_create_recurring_reservation_schedule(self, client):
        params = {'listing_id': 1, 'customer_id': 7, 'accommodation_id': 9, 'pet_ids': [3],
                  'weekdays': ['monday', 'friday'], 'start_date': '2026-12-01', 'interval': 2}
        responses.add(responses.POST, f"{BASE}recurring_reservation_schedules", status=201,
                      json=dict(SCHEDULE, interval=2), match=[matchers.json_params_matcher(params)])
        assert client.create_recurring_reservation_schedule(params=params).interval == 2

    @responses.activate
    def test_create_recurring_reservation_schedule_refused(self, client):
        responses.add(responses.POST, f"{BASE}recurring_reservation_schedules", status=422,
                      json={'errors': ['Start date must be today or later']})
        with pytest.raises(ValidationError) as raised:
            client.create_recurring_reservation_schedule(params={'listing_id': 1})
        assert raised.value.errors == ['Start date must be today or later']

    @responses.activate
    def test_create_recurring_reservation_schedule_forbidden(self, client):
        responses.add(responses.POST, f"{BASE}recurring_reservation_schedules", status=403, json={'message': 'No'})
        with pytest.raises(ClientError) as raised:
            client.create_recurring_reservation_schedule(params={'listing_id': 1})
        assert raised.value.response.status_code == 403

    @responses.activate
    def test_patch_recurring_reservation_schedule_clears_end_date(self, client):
        responses.add(responses.PATCH, f"{BASE}recurring_reservation_schedules/4", status=200, json=SCHEDULE,
                      match=[matchers.json_params_matcher({'weekdays': ['tuesday'], 'end_date': None})])
        schedule = client.patch_recurring_reservation_schedule(
            resource_id='4', params={'weekdays': ['tuesday'], 'end_date': None})
        assert schedule.end_date is None

    @responses.activate
    def test_patch_stopped_recurring_reservation_schedule(self, client):
        message = 'This recurring booking has been stopped'
        responses.add(responses.PATCH, f"{BASE}recurring_reservation_schedules/4", status=422,
                      json={'error': 'unprocessable', 'message': message})
        with pytest.raises(ValidationError) as raised:
            client.patch_recurring_reservation_schedule(resource_id='4', params={'interval': 3})
        assert raised.value.errors == [message]

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_recurring_reservation_schedule(resource_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_recurring_reservation_schedule(resource_id='', params={})


class TestBatch30Changes:
    @responses.activate
    def test_delete_pet_with_history(self, client):
        responses.add(responses.DELETE, f"{BASE}pets/3", status=422,
                      json={'error': 'pet_has_history', 'message': 'Biscuit has stays; deactivate it instead'})
        with pytest.raises(ValidationError) as raised:
            client.delete_pet(resource_id='3')
        assert raised.value.body['error'] == 'pet_has_history'
        assert raised.value.errors == ['Biscuit has stays; deactivate it instead']

    @responses.activate
    def test_delete_accommodation_forbidden_for_staff(self, client):
        responses.add(responses.DELETE, f"{BASE}accommodations/9", status=403, json={'message': 'Forbidden'})
        with pytest.raises(ClientError) as raised:
            client.delete_accommodation(resource_id='9')
        assert raised.value.response.status_code == 403

    @responses.activate
    def test_gift_card_invoice_payment(self, client):
        responses.add(responses.GET, f"{BASE}invoices/5/payments", status=200,
                      json=[{'id': 8, 'tender': 'gift_card', 'reported_to_stripe': True}])
        assert client.get_invoice_payments(invoice_id='5')[0].tender == 'gift_card'

    @responses.activate
    def test_no_show_appointments(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/grooming/appointments", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'status': 'no_show'})],
                      json=[{'id': 12, 'status': 'no_show'}])
        appointments = client.get_listing_grooming_appointments(listing_id='1', params={'status': 'no_show'})
        assert appointments[0].status == 'no_show'

    @responses.activate
    def test_grooming_with_membership_credits(self, client):
        params = {'customer_id': 7, 'pet_ids': [3], 'service_type_ids': [2],
                  'starts_at': '2026-12-01T09:00:00+13:00', 'pay_with_membership_credits': True}
        responses.add(responses.POST, f"{BASE}listings/1/grooming/appointments", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json=[{'id': 11, 'status': 'scheduled', 'deposit_cents': 0}])
        assert client.create_listing_grooming_appointments(listing_id='1', params=params)[0].deposit_cents == 0

    @responses.activate
    def test_grooming_without_enough_credits(self, client):
        message = "The customer's household hasn't enough membership credits for these appointments"
        responses.add(responses.GET, f"{BASE}listings/1/grooming/open_times", status=422,
                      json={'error': 'no_credit', 'message': message})
        with pytest.raises(ValidationError) as raised:
            client.get_listing_grooming_open_times(listing_id='1', params={'pay_with_membership_credits': True})
        assert raised.value.errors == [message]

    @responses.activate
    def test_membership_plan_credit_uses(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/membership_plans/2", status=200,
                      json={'id': 2, 'credit_uses': ['stays', 'grooming'], 'credit_use': 'stays',
                            'credits_cover_lessons': False})
        plan = client.get_listing_membership_plan(listing_id='1', membership_plan_id='2')
        assert plan.credit_uses == ['stays', 'grooming']
