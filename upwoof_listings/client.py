from typing import Any, Dict, Optional
from urllib.parse import urljoin
import requests

from . import errors
from .dsl import DSL

class Client(DSL):
    REQUESTS = ['get', 'post', 'put', 'patch', 'delete']
    HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def __init__(self, api_key: Optional[str] = None, url: str = 'https://www.upwoof.com/api/v1/'):
        from . import api_key as global_api_key
        self.api_key = api_key or global_api_key
        self.url = url
        self.session = requests.Session()

    def request(self, method: str, path: str, query: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None) -> requests.Response:
        method = method.lower()
        if method not in self.REQUESTS:
            raise ValueError(f"Unsupported method {method}. Only get, post, put, patch, delete are allowed")

        full_url = urljoin(self.url, path)
        params = {'access_token': self.api_key}

        request_headers = self.HEADERS.copy()
        if headers:
            request_headers.update(headers)

        # requests handles json= for application/json automatically
        kwargs = {'params': params, 'headers': request_headers}
        if method in ['post', 'put', 'patch']:
            if request_headers.get('Content-Type') == 'application/json':
                kwargs['json'] = query
            else:
                kwargs['data'] = query
        elif method == 'get' and query:
            kwargs['params'].update(query)

        response = self.session.request(method, full_url, **kwargs)

        if 200 <= response.status_code <= 299:
            return response
        if response.status_code == 404:
            raise errors.ResourceNotFoundError(response=response)
        raise errors.ClientError(response=response)
