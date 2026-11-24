import pytest
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError


@pytest.fixture
def client():
    return Client(api_key="test_key")


def test_default_url_is_www_upwoof_com():
    assert Client(api_key="test_key").url == "https://www.upwoof.com/api/v1/"


def test_clamp_per_page_leaves_a_non_numeric_per_page_alone():
    assert Client._clamp_per_page({'per_page': 'many'}) == {'per_page': 'many'}


def test_clamp_per_page_caps_a_numeric_per_page():
    assert Client._clamp_per_page({'per_page': '1000'})['per_page'] == Client.MAX_PER_PAGE


def test_client_error_without_a_response_has_no_body():
    error = ClientError()
    assert error.body is None
    assert error.errors == []


@pytest.mark.parametrize('method', ['skip_recurring_reservation_schedule_date',
                                    'restore_recurring_reservation_schedule_date'])
def test_skipped_date_methods_need_a_date(client, method):
    with pytest.raises(ValueError, match="Date cannot be blank"):
        getattr(client, method)(resource_id='4', date='')


@pytest.mark.parametrize('method', ['skip_recurring_reservation_schedule_date',
                                    'restore_recurring_reservation_schedule_date'])
def test_skipped_date_methods_need_an_id(client, method):
    with pytest.raises(ValueError, match="ID cannot be blank"):
        getattr(client, method)(resource_id='', date='2026-12-01')
