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


class TestPlayYardsDSL:
    @responses.activate
    def test_get_listing_play_yards(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/play_yards", status=200,
                      json=[{'id': 2, 'name': 'Big yard', 'capacity': 12, 'max_weight_lbs': None}])
        yards = client.get_listing_play_yards(listing_id='1')
        assert yards[0].capacity == 12

    @responses.activate
    def test_get_listing_play_yard(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/play_yards/2", status=200, json={'id': 2})
        assert client.get_listing_play_yard(listing_id='1', play_yard_id='2').id == 2

    @responses.activate
    def test_create_listing_play_yard(self, client):
        params = {'name': 'Small yard', 'capacity': 6, 'max_weight_lbs': 25.0}
        responses.add(responses.POST, f"{BASE}listings/1/play_yards", status=201,
                      match=[matchers.json_params_matcher(params)], json={'id': 3, 'name': 'Small yard'})
        assert client.create_listing_play_yard(listing_id='1', params=params).name == 'Small yard'

    @responses.activate
    def test_create_listing_play_yard_duplicate_name(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/play_yards", status=422,
                      json={'errors': ['Name has already been taken']})
        with pytest.raises(ValidationError):
            client.create_listing_play_yard(listing_id='1', params={'name': 'Small yard', 'capacity': 6})

    @responses.activate
    def test_patch_listing_play_yard(self, client):
        responses.add(responses.PATCH, f"{BASE}listings/1/play_yards/2", status=200,
                      match=[matchers.json_params_matcher({'calm_dogs_only': True})],
                      json={'id': 2, 'calm_dogs_only': True})
        yard = client.patch_listing_play_yard(listing_id='1', play_yard_id='2', params={'calm_dogs_only': True})
        assert yard.calm_dogs_only is True

    @responses.activate
    def test_delete_listing_play_yard(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/play_yards/2", status=204)
        assert client.delete_listing_play_yard(listing_id='1', play_yard_id='2') is True

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_play_yards(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_play_yard(listing_id='1', play_yard_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_listing_play_yard(listing_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_listing_play_yard(listing_id='1', play_yard_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_listing_play_yard(listing_id='', play_yard_id='2')


class TestPlaygroupAssignmentsDSL:
    @responses.activate
    def test_get_listing_playgroup_assignments(self, client):
        query = {'access_token': 'test_key', 'date': '2026-12-01', 'from': '09:00', 'to': '11:00'}
        responses.add(responses.GET, f"{BASE}listings/1/playgroup_assignments", status=200,
                      match=[matchers.query_param_matcher(query)],
                      json=[{'id': 8, 'play_yard_id': 2, 'warnings': ['over_capacity', 'size']}])
        assignments = client.get_listing_playgroup_assignments(
            listing_id='1', params={'date': '2026-12-01', 'from': '09:00', 'to': '11:00'})
        assert assignments[0].warnings == ['over_capacity', 'size']

    @responses.activate
    def test_create_listing_playgroup_assignment(self, client):
        params = {'reservation_id': 4, 'pet_id': 3, 'play_yard_id': 2,
                  'starts_at': '2026-12-01T09:00:00+13:00', 'ends_at': '2026-12-01T10:00:00+13:00'}
        responses.add(responses.POST, f"{BASE}listings/1/playgroup_assignments", status=201,
                      match=[matchers.json_params_matcher(params)], json={'id': 8, 'warnings': []})
        assert client.create_listing_playgroup_assignment(listing_id='1', params=params).warnings == []

    @responses.activate
    def test_create_listing_playgroup_assignment_stay_not_checked_in(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/playgroup_assignments", status=404, json={})
        with pytest.raises(ResourceNotFoundError):
            client.create_listing_playgroup_assignment(listing_id='1', params={'reservation_id': 4})

    @responses.activate
    def test_patch_listing_playgroup_assignment(self, client):
        responses.add(responses.PATCH, f"{BASE}listings/1/playgroup_assignments/8", status=200,
                      match=[matchers.json_params_matcher({'play_yard_id': 5})], json={'id': 8, 'play_yard_id': 5})
        assignment = client.patch_listing_playgroup_assignment(listing_id='1', playgroup_assignment_id='8',
                                                               play_yard_id=5)
        assert assignment.play_yard_id == 5

    @responses.activate
    def test_delete_listing_playgroup_assignment(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/playgroup_assignments/8", status=204)
        assert client.delete_listing_playgroup_assignment(listing_id='1', playgroup_assignment_id='8') is True

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_playgroup_assignments(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_listing_playgroup_assignment(listing_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_listing_playgroup_assignment(listing_id='1', playgroup_assignment_id='8', play_yard_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_listing_playgroup_assignment(listing_id='1', playgroup_assignment_id='')
