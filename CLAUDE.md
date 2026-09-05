# UpWoof Listings Python Client

A Python wrapper for the UpWoof Listings API. Sibling to `upwoof-listings-ruby-client`, which
wraps the same API for Ruby callers — the two should stay behaviourally equivalent.

## Stack

Python package (`upwoof_listings/`), tests in `tests/`.

```bash
pip install -e .
pytest
```

## Conventions

A thin wrapper: endpoints to methods, responses parsed. Business logic belongs in the consuming
app. When the API changes, change both this and the Ruby client — a caller should not be able to
tell which language it is talking from.

Never hit the live API from a test.
