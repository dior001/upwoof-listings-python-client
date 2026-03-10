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

## Documentation

https://www.upwoof.com/api-docs/v1

## Contributing

1. Fork it ( https://github.com/dior001/upwoof-listings-python-client/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## License

The library is available as open source under the terms of the [MIT License](LICENSE).
