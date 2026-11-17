import json


def _body_from(response):
    """The parsed JSON error body, or None when there is none."""
    if response is None:
        return None
    try:
        return response.json()
    except (ValueError, AttributeError):
        try:
            return json.loads(response.text)
        except (ValueError, TypeError, AttributeError):
            return None


def _errors_from(body):
    """The API's messages from an error body: its `errors` list (a dict of messages keyed by field gives its
    values), else its single `message` (`{"error": ..., "message": ...}`), else an empty list."""
    if not isinstance(body, dict):
        return []
    found = body.get('errors')
    if found is None:
        message = body.get('message')
        return [message] if message else []
    if isinstance(found, dict):
        return list(found.values())
    return list(found) if isinstance(found, (list, tuple)) else [found]


class ClientError(Exception):
    def __init__(self, response=None):
        self.response = response
        self.body = _body_from(response)
        self.errors = _errors_from(self.body)
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
