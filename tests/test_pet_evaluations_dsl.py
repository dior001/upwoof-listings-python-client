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


class TestPetEvaluationsDSL:
    @responses.activate
    def test_get_pet_evaluations_filters(self, client):
        responses.add(responses.GET, f"{BASE}pet_evaluations", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'result': 'passed',
                                                           'pet_id': '3'})],
                      json=[{'id': 1, 'result': 'passed', 'evaluation_type': 'temperament'}])
        evaluations = client.get_pet_evaluations({'result': 'passed', 'pet_id': 3})
        assert evaluations[0].id == 1
        assert evaluations[0].evaluation_type == 'temperament'

    @responses.activate
    def test_get_pet_evaluation(self, client):
        responses.add(responses.GET, f"{BASE}pet_evaluations/5", json={'id': 5, 'expires_on': None}, status=200)
        evaluation = client.get_pet_evaluation(resource_id='5')
        assert evaluation.id == 5
        assert evaluation.expires_on is None

    @responses.activate
    def test_get_pet_evaluation_not_found(self, client):
        responses.add(responses.GET, f"{BASE}pet_evaluations/9", json={'error': 'not found'}, status=404)
        with pytest.raises(ResourceNotFoundError):
            client.get_pet_evaluation(resource_id='9')

    @responses.activate
    def test_create_reservation_pet_evaluation(self, client):
        params = {'pet_id': 3, 'result': 'passed', 'evaluation_type': 'meet_and_greet'}
        responses.add(responses.POST, f"{BASE}reservations/7/pet_evaluations", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json={'id': 2, 'pet_id': 3, 'reservation_id': 7, 'result': 'passed'})
        evaluation = client.create_reservation_pet_evaluation(reservation_id='7', params=params)
        assert evaluation.reservation_id == 7

    @responses.activate
    def test_create_reservation_pet_evaluation_refused(self, client):
        responses.add(responses.POST, f"{BASE}reservations/7/pet_evaluations", status=422,
                      json={'error': 'unprocessable entity', 'message': 'Expires on must be after evaluated on'})
        with pytest.raises(ValidationError) as raised:
            client.create_reservation_pet_evaluation(reservation_id='7', params={'pet_id': 3, 'result': 'passed'})
        assert raised.value.errors == ['Expires on must be after evaluated on']

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_pet_evaluation(resource_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_reservation_pet_evaluation(reservation_id='', params={})


class TestPetDeactivationDSL:
    @responses.activate
    def test_deactivate_pet(self, client):
        responses.add(responses.POST, f"{BASE}pets/4/deactivation", status=200,
                      match=[matchers.json_params_matcher({'deactivation_reason': 'passed_away'})],
                      json={'id': 4, 'status': 'inactive', 'deactivation_reason': 'passed_away'})
        pet = client.deactivate_pet(resource_id='4', deactivation_reason='passed_away')
        assert pet.status == 'inactive'

    @responses.activate
    def test_deactivate_pet_already_inactive(self, client):
        responses.add(responses.POST, f"{BASE}pets/4/deactivation", status=422,
                      json={'error': 'unprocessable entity', 'message': 'Pet is already inactive'})
        with pytest.raises(ValidationError):
            client.deactivate_pet(resource_id='4', deactivation_reason='other')

    @responses.activate
    def test_reactivate_pet(self, client):
        responses.add(responses.DELETE, f"{BASE}pets/4/deactivation", status=200,
                      json={'id': 4, 'status': 'active', 'deactivated_at': None})
        pet = client.reactivate_pet(resource_id='4')
        assert pet.status == 'active'

    @responses.activate
    def test_booking_an_inactive_pet_is_refused(self, client):
        responses.add(responses.POST, f"{BASE}reservations/", status=422,
                      json={'error': 'unprocessable entity', 'message': "Inactive pets can't be booked: Rex"})
        with pytest.raises(ValidationError) as raised:
            client.create_reservation(params={'pet_id': 4})
        assert raised.value.errors == ["Inactive pets can't be booked: Rex"]

    def test_blank_arguments(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.deactivate_pet(resource_id='', deactivation_reason='other')
        with pytest.raises(ValueError, match="Deactivation reason cannot be blank"):
            client.deactivate_pet(resource_id='4', deactivation_reason='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.reactivate_pet(resource_id='')
