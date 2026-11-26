import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.site_client import SiteClient
from upwoof_listings.errors import ClientError, ResourceNotFoundError, ValidationError

BASE = "https://www.upwoof.com/api/v1/"
AUTH = {'Authorization': 'Bearer uwsite_abc'}

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


@pytest.fixture
def site():
    return SiteClient('uwsite_abc')


class TestListingWebsitesDSL:
    @responses.activate
    def test_get_listing_website(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/website", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key'})],
                      json={'id': 4, 'subdomain': 'happy-paws', 'theme': 'classic'})
        website = client.get_listing_website(listing_id='1')
        assert website.subdomain == 'happy-paws'

    @responses.activate
    def test_get_listing_website_not_found(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/website", status=404,
                      json={'error': 'not_found', 'message': 'No website'})
        with pytest.raises(ResourceNotFoundError):
            client.get_listing_website(listing_id='1')

    @responses.activate
    def test_update_listing_website(self, client):
        body = {'theme': 'playful', 'palette': {'primary': '#112233'}, 'bookings_enabled': False}
        responses.add(responses.PATCH, f"{BASE}listings/1/website", status=200,
                      match=[matchers.json_params_matcher(body)], json={'id': 4, 'theme': 'playful'})
        assert client.update_listing_website(listing_id='1', params=body).theme == 'playful'

    @responses.activate
    def test_update_listing_website_refused_domain(self, client):
        responses.add(responses.PATCH, f"{BASE}listings/1/website", status=422,
                      json={'error': 'custom_domain_refused', 'message': 'Taken'})
        with pytest.raises(ValidationError) as error:
            client.update_listing_website(listing_id='1', params={'custom_domain': 'www.happy.com'})
        assert error.value.errors == ['Taken']

    def test_blank_listing_id(self, client):
        with pytest.raises(ValueError):
            client.get_listing_website(listing_id='')
        with pytest.raises(ValueError):
            client.update_listing_website(listing_id='', params={})


class TestSiteClient:
    def test_blank_site_token(self):
        with pytest.raises(ValueError):
            SiteClient('')

    @responses.activate
    def test_get_site_config_sends_the_token_as_a_bearer_header(self, site):
        responses.add(responses.GET, f"{BASE}site", status=200, json={'theme': 'modern'},
                      match=[matchers.header_matcher(AUTH), matchers.query_param_matcher({})])
        assert site.get_site_config().theme == 'modern'

    @responses.activate
    def test_get_site_listing_and_accommodations(self, site):
        responses.add(responses.GET, f"{BASE}site/listing", status=200, json={'name': 'Paws'},
                      match=[matchers.header_matcher(AUTH)])
        responses.add(responses.GET, f"{BASE}site/accommodations", status=200, json=[{'id': 2, 'name': 'Suite'}],
                      match=[matchers.header_matcher(AUTH)])
        assert site.get_site_listing().name == 'Paws'
        assert site.get_site_accommodations()[0].name == 'Suite'

    @responses.activate
    def test_get_site_reviews(self, site):
        responses.add(responses.GET, f"{BASE}site/reviews", status=200,
                      match=[matchers.query_param_matcher({'page': '2'})],
                      json={'page': 2, 'reviews': [], 'total_pages': 2})
        assert site.get_site_reviews(page=2).total_pages == 2

    @responses.activate
    def test_get_site_availability(self, site):
        query = {'check_in': '2026-12-07', 'check_out': '2026-12-09', 'dogs': '1'}
        responses.add(responses.GET, f"{BASE}site/availability", status=200,
                      match=[matchers.query_param_matcher(query)], json={'nights': 2, 'options': []})
        result = site.get_site_availability(params={'check_in': '2026-12-07', 'check_out': '2026-12-09', 'dogs': 1})
        assert result.nights == 2

    @responses.activate
    def test_create_site_booking_request_with_the_visitor_address(self, site):
        body = {'check_in': '2026-12-07', 'check_out': '2026-12-09', 'accommodation_id': 2, 'accepted_terms': True}
        responses.add(responses.POST, f"{BASE}site/booking_requests", status=201,
                      match=[matchers.json_params_matcher(body),
                             matchers.header_matcher({**AUTH, 'X-Visitor-IP': '198.51.100.7'})],
                      json={'reference': 'R-1', 'status': 'awaiting_review'})
        request = site.create_site_booking_request(params=body, visitor_ip='198.51.100.7')
        assert request.status == 'awaiting_review'

    @responses.activate
    def test_create_site_booking_request_refused(self, site):
        responses.add(responses.POST, f"{BASE}site/booking_requests", status=422,
                      json={'error': 'unavailable', 'message': 'Fully booked'})
        with pytest.raises(ValidationError) as error:
            site.create_site_booking_request(params={})
        assert error.value.body['error'] == 'unavailable'

    @responses.activate
    def test_create_site_inquiry(self, site):
        responses.add(responses.POST, f"{BASE}site/inquiries", status=201, json={'status': 'received'},
                      match=[matchers.header_matcher(AUTH)])
        assert site.create_site_inquiry(params={'first_name': 'Ana'}).status == 'received'

    @responses.activate
    def test_errors(self, site):
        responses.add(responses.GET, f"{BASE}site", status=401, json={'error': 'unauthorized'})
        responses.add(responses.GET, f"{BASE}site/listing", status=404, json={})
        with pytest.raises(ClientError):
            site.get_site_config()
        with pytest.raises(ResourceNotFoundError):
            site.get_site_listing()
