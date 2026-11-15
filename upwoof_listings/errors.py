import json


def _errors_from(response):
    """The `errors` list from an API error body (`{"errors": [...]}`), else an empty list."""
    if response is None:
        return []
    try:
        body = response.json()
    except (ValueError, AttributeError):
        try:
            body = json.loads(response.text)
        except (ValueError, TypeError, AttributeError):
            return []
    if not isinstance(body, dict) or 'errors' not in body:
        return []
    found = body['errors']
    if found is None:
        return []
    return list(found) if isinstance(found, (list, tuple)) else [found]


class ClientError(Exception):
    def __init__(self, response=None):
        self.response = response
        self.errors = _errors_from(response)
        super().__init__(f"Client error: {response.status_code if response is not None else 'Unknown'}")


class ResourceNotFoundError(ClientError):
    def __init__(self, response=None):
        super().__init__(response)
        self.message = "Resource not found"


class ValidationError(ClientError):
    """HTTP 422: the API refused the request. `errors` holds its messages, e.g. a reservation date change
    that fails the availability check, or a gift card that can't be redeemed against this order."""

    def __init__(self, response=None):
        super().__init__(response)
        self.message = "Validation failed"
