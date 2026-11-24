import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ValidationError

BASE = "https://www.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestTrainingCoursesDSL:
    @responses.activate
    def test_get_training_courses(self, client):
        responses.add(responses.GET, f"{BASE}training_courses", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'active': 'True'})],
                      json=[{'id': 1, 'title': 'Puppy basics'}])
        assert client.get_training_courses({'active': True})[0].title == 'Puppy basics'

    @responses.activate
    def test_get_training_course(self, client):
        responses.add(responses.GET, f"{BASE}training_courses/1", status=200, json={'id': 1, 'places_left': 3})
        assert client.get_training_course(resource_id='1').places_left == 3

    @responses.activate
    def test_get_training_course_sessions(self, client):
        responses.add(responses.GET, f"{BASE}training_courses/1/sessions", status=200,
                      json=[{'id': 4, 'online': True}])
        assert client.get_training_course_sessions(training_course_id='1')[0].online is True

    @responses.activate
    def test_get_training_course_enrollments(self, client):
        responses.add(responses.GET, f"{BASE}training_courses/1/enrollments", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'status': 'enrolled'})],
                      json=[{'id': 6, 'status': 'enrolled'}])
        enrollments = client.get_training_course_enrollments(training_course_id='1', params={'status': 'enrolled'})
        assert enrollments[0].id == 6

    @responses.activate
    def test_create_training_course_enrollment(self, client):
        params = {'pet_id': 3, 'use_membership_credit': True}
        responses.add(responses.POST, f"{BASE}training_courses/1/enrollments", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json={'id': 7, 'paid_with_membership_credit': True})
        enrollment = client.create_training_course_enrollment(training_course_id='1', params=params)
        assert enrollment.paid_with_membership_credit is True

    @responses.activate
    def test_create_training_course_enrollment_course_full(self, client):
        responses.add(responses.POST, f"{BASE}training_courses/1/enrollments", status=422,
                      json={'errors': ['This course is full']})
        with pytest.raises(ValidationError) as raised:
            client.create_training_course_enrollment(training_course_id='1', params={'pet_id': 3})
        assert raised.value.errors == ['This course is full']

    @responses.activate
    def test_get_training_course_waitlist_entries(self, client):
        responses.add(responses.GET, f"{BASE}training_courses/1/waitlist_entries", status=200,
                      json=[{'id': 8, 'status': 'offered'}])
        assert client.get_training_course_waitlist_entries(training_course_id='1')[0].status == 'offered'

    @responses.activate
    def test_get_training_enrollment(self, client):
        responses.add(responses.GET, f"{BASE}training_enrollments/7", status=200, json={'id': 7})
        assert client.get_training_enrollment(resource_id='7').id == 7

    @responses.activate
    def test_cancel_training_enrollment(self, client):
        responses.add(responses.POST, f"{BASE}training_enrollments/7/cancel", status=200,
                      json={'id': 7, 'status': 'cancelled'})
        assert client.cancel_training_enrollment(resource_id='7').status == 'cancelled'

    @pytest.mark.parametrize('call', [
        lambda c: c.get_training_course(resource_id=''),
        lambda c: c.get_training_course_sessions(training_course_id=''),
        lambda c: c.get_training_course_enrollments(training_course_id=''),
        lambda c: c.create_training_course_enrollment(training_course_id='', params={}),
        lambda c: c.get_training_course_waitlist_entries(training_course_id=''),
        lambda c: c.get_training_enrollment(resource_id=''),
        lambda c: c.cancel_training_enrollment(resource_id=''),
    ])
    def test_blank_ids(self, client, call):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            call(client)
