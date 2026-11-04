import pytest
import responses
from upwoof_listings.client import Client

@pytest.fixture
def client():
    return Client(api_key='test_key')

class TestVaccinationRecordsDSL:
    @responses.activate
    def test_get_pet_vaccination_records(self, client):
        responses.add(responses.GET, 'https://pethotels.upwoof.com/api/v1/pets/1/vaccination_records',
                      json=[{'ID': 1, 'VACCINE_NAME': 'rabies', 'PET_ID': 1}], status=200)
        records = client.get_pet_vaccination_records(pet_id='1')
        assert isinstance(records, list)
        assert records[0].id == 1
        assert records[0].vaccine_name == 'rabies'

    def test_get_pet_vaccination_records_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_pet_vaccination_records(pet_id='')

    @responses.activate
    def test_create_pet_vaccination_record(self, client):
        responses.add(responses.POST, 'https://pethotels.upwoof.com/api/v1/pets/1/vaccination_records',
                      json={'ID': 1, 'VACCINE_NAME': 'rabies', 'PET_ID': 1}, status=201)
        record = client.create_pet_vaccination_record(
            pet_id='1', params={'vaccine_name': 'rabies', 'administered_on': '2026-01-01'}
        )
        assert record.id == 1
        assert record.pet_id == 1

    def test_create_pet_vaccination_record_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_pet_vaccination_record(pet_id='', params={})
