import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError, ResourceNotFoundError, ValidationError

BASE = "https://pethotels.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name

SCHEDULE = {'id': 4, 'listing_id': 1, 'active': True, 'skipped_dates': [], 'weekdays': ['monday']}
FEEDING_PLAN = {'id': 6, 'listing_id': 1, 'pet_id': 3, 'meal_label': 'Breakfast', 'time_of_day': '07:30',
                'quantity': '1 cup', 'food_description': 'Kibble', 'special_feeding': False,
                'created_by_user_id': 2, 'created_at': '2026-11-24T08:00:00Z', 'updated_at': '2026-11-24T08:00:00Z'}
MEDICATION_PLAN = {'id': 8, 'listing_id': 1, 'pet_id': 3, 'medication_name': 'Apoquel', 'dosage': '16 mg',
                   'frequency': 'twice_daily', 'dose_times': [], 'effective_dose_times': ['08:00', '18:00'],
                   'instructions': 'With food'}
ENTRY = {'id': 21, 'reservation_id': 5, 'pet_id': 3, 'entry_type': 'medication', 'outcome': None,
         'scheduled_at': '2026-11-24T19:00:00Z', 'completed_at': None}


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestUnitAssignments:
    @responses.activate
    def test_moves_an_assignment_to_a_unit(self, client):
        responses.add(responses.PATCH, f"{BASE}reservations/5/unit_assignments/9", status=200,
                      match=[matchers.json_params_matcher({'accommodation_unit_id': 31})],
                      json={'id': 9, 'accommodation_id': 2,
                            'accommodation_unit': {'id': 31, 'name': 'A3', 'active': True, 'sort': 3,
                                                   'needs_cleaning': False}})
        assignment = client.update_reservation_unit_assignment(reservation_id='5', unit_assignment_id='9',
                                                               accommodation_unit_id=31)
        assert isinstance(assignment, client.resources.ReservationAccommodationAssignment)
        assert assignment.accommodation_unit['name'] == 'A3'

    @responses.activate
    def test_takes_an_assignment_out_of_its_unit(self, client):
        responses.add(responses.PATCH, f"{BASE}reservations/5/unit_assignments/9", status=200,
                      match=[matchers.json_params_matcher({'accommodation_unit_id': None})],
                      json={'id': 9, 'accommodation_id': 2, 'accommodation_unit': None})
        assert client.update_reservation_unit_assignment(
            reservation_id='5', unit_assignment_id='9').accommodation_unit is None

    @responses.activate
    def test_unit_taken(self, client):
        message = 'The unit is taken by another stay on some of these nights'
        responses.add(responses.PATCH, f"{BASE}reservations/5/unit_assignments/9", status=422,
                      json={'errors': [message]})
        with pytest.raises(ValidationError) as raised:
            client.update_reservation_unit_assignment(reservation_id='5', unit_assignment_id='9',
                                                      accommodation_unit_id=31)
        assert raised.value.errors == [message]

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.update_reservation_unit_assignment(reservation_id='5', unit_assignment_id='')


class TestRecurringScheduleActions:
    @responses.activate
    def test_deactivate(self, client):
        responses.add(responses.POST, f"{BASE}recurring_reservation_schedules/4/deactivate", status=201,
                      json=dict(SCHEDULE, active=False))
        assert client.deactivate_recurring_reservation_schedule(resource_id='4').active is False

    @responses.activate
    def test_deactivate_stopped(self, client):
        message = 'This recurring booking has been stopped'
        responses.add(responses.POST, f"{BASE}recurring_reservation_schedules/4/deactivate", status=422,
                      json={'error': 'unprocessable entity', 'message': message})
        with pytest.raises(ValidationError) as raised:
            client.deactivate_recurring_reservation_schedule(resource_id='4')
        assert raised.value.errors == [message]

    @responses.activate
    def test_skip_date(self, client):
        responses.add(responses.POST, f"{BASE}recurring_reservation_schedules/4/skipped_dates", status=201,
                      match=[matchers.json_params_matcher({'date': '2026-12-07'})],
                      json=dict(SCHEDULE, skipped_dates=['2026-12-07']))
        schedule = client.skip_recurring_reservation_schedule_date(resource_id='4', date='2026-12-07')
        assert schedule.skipped_dates == ['2026-12-07']

    @responses.activate
    def test_restore_date(self, client):
        responses.add(responses.DELETE, f"{BASE}recurring_reservation_schedules/4/skipped_dates/2026-12-07",
                      status=200, json=SCHEDULE)
        assert client.restore_recurring_reservation_schedule_date(
            resource_id='4', date='2026-12-07').skipped_dates == []

    @responses.activate
    def test_restore_date_not_skipped(self, client):
        responses.add(responses.DELETE, f"{BASE}recurring_reservation_schedules/4/skipped_dates/2026-12-08",
                      status=422, json={'error': 'unprocessable entity', 'message': 'That date is not skipped'})
        with pytest.raises(ValidationError):
            client.restore_recurring_reservation_schedule_date(resource_id='4', date='2026-12-08')

    @responses.activate
    def test_forbidden(self, client):
        responses.add(responses.POST, f"{BASE}recurring_reservation_schedules/4/deactivate", status=403,
                      json={'message': 'No'})
        with pytest.raises(ClientError):
            client.deactivate_recurring_reservation_schedule(resource_id='4')

    def test_blank_arguments(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.deactivate_recurring_reservation_schedule(resource_id='')
        with pytest.raises(ValueError, match="Date cannot be blank"):
            client.skip_recurring_reservation_schedule_date(resource_id='4', date='')
        with pytest.raises(ValueError, match="Date cannot be blank"):
            client.restore_recurring_reservation_schedule_date(resource_id='4', date='')


class TestAppointmentNoShows:
    @pytest.mark.parametrize('method,kind_path', [('mark_grooming_appointment_no_show', 'grooming'),
                                                  ('mark_lesson_no_show', 'lessons'),
                                                  ('mark_tour_no_show', 'tours'),
                                                  ('mark_transport_no_show', 'transports')])
    @responses.activate
    def test_marks_a_no_show(self, client, method, kind_path):
        responses.add(responses.POST, f"{BASE}listings/1/{kind_path}/appointments/12/no_show", status=201,
                      json={'id': 12, 'status': 'no_show', 'deposit_status': 'forfeited',
                            'reminder_sent_at': '2026-11-23T20:00:00Z'})
        appointment = getattr(client, method)(listing_id='1', appointment_id='12')
        assert isinstance(appointment, client.resources.GroomingAppointment)
        assert appointment.status == 'no_show'
        assert appointment.reminder_sent_at == '2026-11-23T20:00:00Z'

    @responses.activate
    def test_not_markable(self, client):
        message = 'Only a scheduled or confirmed appointment whose start has passed can be marked a no-show'
        responses.add(responses.POST, f"{BASE}listings/1/grooming/appointments/12/no_show", status=422,
                      json={'errors': [message]})
        with pytest.raises(ValidationError) as raised:
            client.mark_grooming_appointment_no_show(listing_id='1', appointment_id='12')
        assert raised.value.errors == [message]

    @responses.activate
    def test_deposit_held_needs_owner(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/tours/appointments/12/no_show", status=403,
                      json={'message': 'No'})
        with pytest.raises(ClientError) as raised:
            client.mark_tour_no_show(listing_id='1', appointment_id='12')
        assert raised.value.response.status_code == 403

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.mark_lesson_no_show(listing_id='1', appointment_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.mark_lesson_no_show(listing_id='', appointment_id='12')


class TestPetCarePlans:
    @responses.activate
    def test_get_feeding_plans(self, client):
        responses.add(responses.GET, f"{BASE}pets/3/feeding_plans", status=200, json=[FEEDING_PLAN],
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'listing_id': '1',
                                                           'page': '2'})])
        plans = client.get_pet_feeding_plans(pet_id='3', listing_id='1', params={'page': 2})
        assert isinstance(plans[0], client.resources.PetFeedingPlan)
        assert plans[0].time_of_day == '07:30'

    @responses.activate
    def test_get_feeding_plan(self, client):
        responses.add(responses.GET, f"{BASE}pets/3/feeding_plans/6", status=200, json=FEEDING_PLAN,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'listing_id': '1'})])
        assert client.get_pet_feeding_plan(pet_id='3', plan_id='6', listing_id='1').meal_label == 'Breakfast'

    @responses.activate
    def test_create_feeding_plan(self, client):
        params = {'listing_id': 1, 'meal_label': 'Dinner', 'time_of_day': '18:00', 'special_feeding': True}
        responses.add(responses.POST, f"{BASE}pets/3/feeding_plans", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json=dict(FEEDING_PLAN, meal_label='Dinner', special_feeding=True))
        assert client.create_pet_feeding_plan(pet_id='3', params=params).special_feeding is True

    @responses.activate
    def test_patch_feeding_plan_untimed(self, client):
        params = {'listing_id': 1, 'time_of_day': ''}
        responses.add(responses.PATCH, f"{BASE}pets/3/feeding_plans/6", status=200,
                      match=[matchers.json_params_matcher(params)], json=dict(FEEDING_PLAN, time_of_day=None))
        assert client.patch_pet_feeding_plan(pet_id='3', plan_id='6', params=params).time_of_day is None

    @responses.activate
    def test_delete_feeding_plan(self, client):
        responses.add(responses.DELETE, f"{BASE}pets/3/feeding_plans/6", status=204,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'listing_id': '1'})])
        assert client.delete_pet_feeding_plan(pet_id='3', plan_id='6', listing_id='1') is True

    @responses.activate
    def test_medication_plans(self, client):
        responses.add(responses.GET, f"{BASE}pets/3/medication_plans", status=200, json=[MEDICATION_PLAN])
        responses.add(responses.GET, f"{BASE}pets/3/medication_plans/8", status=200, json=MEDICATION_PLAN)
        plans = client.get_pet_medication_plans(pet_id='3', listing_id='1')
        assert isinstance(plans[0], client.resources.PetMedicationPlan)
        plan = client.get_pet_medication_plan(pet_id='3', plan_id='8', listing_id='1')
        assert plan.effective_dose_times == ['08:00', '18:00']

    @responses.activate
    def test_create_and_patch_medication_plan(self, client):
        params = {'listing_id': 1, 'medication_name': 'Apoquel', 'frequency': 'twice_daily',
                  'dose_times': ['07:00', '19:00']}
        responses.add(responses.POST, f"{BASE}pets/3/medication_plans", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json=dict(MEDICATION_PLAN, dose_times=['07:00', '19:00']))
        responses.add(responses.PATCH, f"{BASE}pets/3/medication_plans/8", status=200,
                      match=[matchers.json_params_matcher({'listing_id': 1, 'frequency': 'as_needed'})],
                      json=dict(MEDICATION_PLAN, frequency='as_needed', effective_dose_times=[]))
        assert client.create_pet_medication_plan(pet_id='3', params=params).dose_times == ['07:00', '19:00']
        plan = client.patch_pet_medication_plan(pet_id='3', plan_id='8',
                                                params={'listing_id': 1, 'frequency': 'as_needed'})
        assert plan.effective_dose_times == []

    @responses.activate
    def test_medication_plan_refused(self, client):
        responses.add(responses.POST, f"{BASE}pets/3/medication_plans", status=422,
                      json={'error': 'unprocessable entity', 'message': "Dose times couldn't be read"})
        with pytest.raises(ValidationError):
            client.create_pet_medication_plan(pet_id='3', params={'listing_id': 1, 'medication_name': 'X'})

    @responses.activate
    def test_delete_medication_plan_elsewhere(self, client):
        responses.add(responses.DELETE, f"{BASE}pets/3/medication_plans/8", status=404, json={'error': 'x'})
        with pytest.raises(ResourceNotFoundError):
            client.delete_pet_medication_plan(pet_id='3', plan_id='8', listing_id='1')

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_pet_feeding_plans(pet_id='3', listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_pet_medication_plan(pet_id='3', plan_id='', listing_id='1')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_pet_feeding_plan(pet_id='', params={})


class TestCareLogEntries:
    @responses.activate
    def test_get_care_log_entries(self, client):
        responses.add(responses.GET, f"{BASE}reservations/5/care_log_entries", status=200, json=[ENTRY],
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'date': '2026-11-24',
                                                           'status': 'pending'})])
        entries = client.get_reservation_care_log_entries(reservation_id='5',
                                                          params={'date': '2026-11-24', 'status': 'pending'})
        assert isinstance(entries[0], client.resources.CareLogEntry)
        assert entries[0].entry_type == 'medication'

    @responses.activate
    def test_complete_care_log_entry(self, client):
        params = {'outcome': 'refused', 'administration_notes': 'Spat it out'}
        responses.add(responses.POST, f"{BASE}care_log_entries/21/complete", status=200,
                      match=[matchers.json_params_matcher(params)],
                      json=dict(ENTRY, outcome='refused', completed_at='2026-11-24T19:05:00Z'))
        assert client.complete_care_log_entry(resource_id='21', params=params).outcome == 'refused'

    @responses.activate
    def test_complete_care_log_entry_refused(self, client):
        responses.add(responses.POST, f"{BASE}care_log_entries/21/complete", status=422,
                      json={'error': 'unprocessable entity', 'message': 'This task is already done'})
        with pytest.raises(ValidationError):
            client.complete_care_log_entry(resource_id='21')

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_reservation_care_log_entries(reservation_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.complete_care_log_entry(resource_id='')


class TestGiftCardHolds:
    @responses.activate
    def test_redeem_gift_card_holds_the_card(self, client):
        responses.add(responses.POST, f"{BASE}orders/7/redeem_gift_card", status=200,
                      match=[matchers.json_params_matcher({'code': 'GC-1'})],
                      json={'id': 7, 'price_cents': 10000, 'order_line_items': [],
                            'gift_card_holds': [{'id': 1, 'gift_card_id': 4, 'amount_cents': 2500,
                                                 'currency': 'NZD', 'invoice_payment_id': None,
                                                 'settled_at': None, 'reversed_at': None}]})
        order = client.redeem_gift_card(resource_id='7', code='GC-1')
        assert order.price_cents == 10000
        assert order.gift_card_holds[0]['amount_cents'] == 2500
