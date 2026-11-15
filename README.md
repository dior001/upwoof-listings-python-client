# UpWoof Listings Python Client

A Python wrapper for the UpWoof Listings API.

## Installation

Install the package via pip:

```bash
pip install upwoof-listings-python-client
```

## Usage

```python
import upwoof_listings

# Set your API key
upwoof_listings.api_key = 'your_api_key'

# Get the client
client = upwoof_listings.get_client()

# List all listings
listings = client.get_listings()
```

### Errors

Every non-2xx response raises a `upwoof_listings.errors.ClientError` carrying the `response` and the
API's messages in `errors` (a list, empty when the body has none). Two subclasses narrow it:

* `ResourceNotFoundError` (HTTP 404). `redeem_gift_card` answers 404 for any code that isn't a usable gift
  card for the order's listing (unknown, expired, used up or another listing's), the same for each.
* `ValidationError` (HTTP 422): the API refused the request. Changing a reservation's dates through
  `update_reservation`/`patch_reservation` runs the availability check, rebuilds the order and fires
  `reservation.duration_changed`; a date change it refuses raises this, with the reasons in `errors`.

```python
from upwoof_listings.errors import ValidationError

try:
    client.patch_reservation(resource_id='42', params={'when_reservation_finish': '2026-12-20'})
except ValidationError as error:
    print(error.errors)
```

### Pagination

List methods take `page` and `per_page` params. The API returns at most 100 records a page (default 20),
so the client never asks for more: a larger `per_page` is sent as 100 (`Client.MAX_PER_PAGE`).

### Verifying webhooks

Each webhook delivery carries `X-Upwoof-Timestamp` (Unix seconds) and `X-Upwoof-Timestamped-Signature`
(`Base64(HMAC-SHA256(secret, "<timestamp>.<body>"))`) alongside the body-only `X-Upwoof-Signature`.
Verify the timestamped one against the raw request body; it also rejects a delivery more than five minutes
old (or ahead), so a captured request can't be replayed:

```python
from upwoof_listings import webhooks

if not webhooks.verify_timestamped_signature(
        raw_body, headers[webhooks.TIMESTAMP_HEADER],
        headers[webhooks.TIMESTAMPED_SIGNATURE_HEADER], secret):  # tolerance=300 by default
    return 400
```

`webhooks.verify_signature(raw_body, headers[webhooks.SIGNATURE_HEADER], secret)` still checks the
body-only signature.

## Documentation

https://pethotels.upwoof.com/api-docs/v1

## Contributing

1. Fork it ( https://github.com/dior001/upwoof-listings-python-client/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## License

The library is available as open source under the terms of the [MIT License](LICENSE).
