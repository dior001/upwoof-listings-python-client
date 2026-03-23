from datetime import datetime
import pytest
import responses
from upwoof_listings.client import Client
from upwoof_listings.resources import UwListingCmsApp

@pytest.fixture
def client():
    return Client(api_key='test_key')

class TestUwListingCmsAppsDSL:
    @responses.activate
    def test_get_uw_listing_cms_apps(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/uw_listing_cms_apps/',
                      json=[{'ID': 1, 'APP_ID': 'app_1', 'CREATED_AT': '2023-01-01T12:00:00Z'}], status=200)
        apps = client.get_uw_listing_cms_apps()
        assert len(apps) == 1
        assert apps[0].id == 1
        assert apps[0].app_id == 'app_1'
        assert isinstance(apps[0].created_at, datetime)

    @responses.activate
    def test_get_uw_listing_cms_app(self, client):
        responses.add(responses.GET, 'https://www.upwoof.com/api/v1/uw_listing_cms_apps/1',
                      json={'ID': 1, 'APP_ID': 'app_1'}, status=200)
        app = client.get_uw_listing_cms_app(resource_id='1')
        assert app.id == 1
        assert app.app_id == 'app_1'

    @responses.activate
    def test_create_uw_listing_cms_app(self, client):
        responses.add(responses.POST, 'https://www.upwoof.com/api/v1/uw_listing_cms_apps/',
                      json={'ID': 2, 'APP_ID': 'new_app'}, status=201)
        app = client.create_uw_listing_cms_app(params={'app_id': 'new_app'})
        assert app.id == 2
        assert app.app_id == 'new_app'

    @responses.activate
    def test_update_uw_listing_cms_app(self, client):
        responses.add(responses.PUT, 'https://www.upwoof.com/api/v1/uw_listing_cms_apps/1',
                      json={'ID': 1, 'APP_ID': 'updated_app'}, status=200)
        app = client.update_uw_listing_cms_app(resource_id='1', params={'app_id': 'updated_app'})
        assert app.app_id == 'updated_app'

    @responses.activate
    def test_patch_uw_listing_cms_app(self, client):
        responses.add(responses.PATCH, 'https://www.upwoof.com/api/v1/uw_listing_cms_apps/1',
                      json={'ID': 1, 'APP_ID': 'patched_app'}, status=200)
        app = client.patch_uw_listing_cms_app(resource_id='1', params={'app_id': 'patched_app'})
        assert app.app_id == 'patched_app'

    @responses.activate
    def test_delete_uw_listing_cms_app(self, client):
        responses.add(responses.DELETE, 'https://www.upwoof.com/api/v1/uw_listing_cms_apps/1',
                      status=204)
        success = client.delete_uw_listing_cms_app(resource_id='1')
        assert success is True

    def test_get_uw_listing_cms_app_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_uw_listing_cms_app(resource_id='')

    def test_update_uw_listing_cms_app_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.update_uw_listing_cms_app(resource_id='', params={})

    def test_delete_uw_listing_cms_app_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_uw_listing_cms_app(resource_id='')
