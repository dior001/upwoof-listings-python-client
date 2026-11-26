from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
import requests

from . import errors, resources


class SiteClient:
    """The site API (/api/v1/site): what a listing's own UpWoof website reads and sends. Authenticated by the
    website's site token (UPWOOF_SITE_TOKEN), always sent as `Authorization: Bearer <token>`, never in the URL.
    Each token sees one listing. Errors are `{error, message}`: a refusal raises ValidationError (its
    `body['error']` the code), a bad token ClientError (401), too many requests ClientError (429)."""

    HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def __init__(self, site_token: str, url: Optional[str] = None):
        if not site_token:
            raise ValueError("Site token cannot be blank")
        from . import url as global_url
        self.site_token = site_token
        self.url = url or global_url
        self.session = requests.Session()

    def get_site_config(self) -> resources.SiteConfig:
        """Theme, palette, hosts, status and booking switch."""
        return resources.SiteConfig.parse(self._request('get', 'site'))

    def get_site_listing(self) -> resources.SiteListing:
        """The listing's public facts."""
        return resources.SiteListing.parse(self._request('get', 'site/listing'))

    def get_site_accommodations(self) -> List[resources.SiteAccommodation]:
        """The units a customer could book online."""
        return resources.SiteAccommodation.parse(self._request('get', 'site/accommodations'))

    def get_site_reviews(self, *, page: Optional[int] = None) -> resources.SiteReviewPage:
        """A page of published reviews (`reviews`, `page`, `total_pages`)."""
        return resources.SiteReviewPage.parse(self._request('get', 'site/reviews', query={'page': page}))

    def get_site_availability(self, *, params: Dict[str, Any]) -> resources.SiteAvailability:
        """`check_in`, `check_out` (YYYY-MM-DD), `dogs`, `cats`."""
        return resources.SiteAvailability.parse(self._request('get', 'site/availability', query=params))

    def create_site_booking_request(self, *, params: Dict[str, Any],
                                    visitor_ip: Optional[str] = None) -> resources.SiteBookingRequest:
        """A booking request, awaiting the listing's review. `check_in`, `check_out`, `accommodation_id`,
        `drop_off_window_id`, `pick_up_window_id`, `owner`, `pets`, `notes`, `accepted_terms`. Pass the visitor's
        address as `visitor_ip` (sent as X-Visitor-IP)."""
        return resources.SiteBookingRequest.parse(
            self._request('post', 'site/booking_requests', query=params, visitor_ip=visitor_ip))

    def create_site_inquiry(self, *, params: Dict[str, Any],
                            visitor_ip: Optional[str] = None) -> resources.SiteInquiry:
        """A question to the listing: `first_name`, `last_name`, `email`, `phone`, `message`, `pet_name`,
        `species`."""
        return resources.SiteInquiry.parse(
            self._request('post', 'site/inquiries', query=params, visitor_ip=visitor_ip))

    def _request(self, method: str, path: str, query: Optional[Dict[str, Any]] = None,
                 visitor_ip: Optional[str] = None) -> requests.Response:
        headers = {**self.HEADERS, 'Authorization': f"Bearer {self.site_token}"}
        if visitor_ip:
            headers['X-Visitor-IP'] = visitor_ip
        kwargs: Dict[str, Any] = {'headers': headers}
        if method == 'get':
            kwargs['params'] = {key: value for key, value in (query or {}).items() if value is not None}
        else:
            kwargs['json'] = query or {}
        response = self.session.request(method, urljoin(self.url, path), **kwargs)

        if 200 <= response.status_code <= 299:
            return response
        if response.status_code == 404:
            raise errors.ResourceNotFoundError(response=response)
        if response.status_code == 422:
            raise errors.ValidationError(response=response)
        raise errors.ClientError(response=response)
