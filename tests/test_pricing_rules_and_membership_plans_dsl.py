import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ValidationError

BASE = "https://pethotels.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestPricingRulesDSL:
    @responses.activate
    def test_get_listing_pricing_rules(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/pricing_rules", status=200,
                      json=[{'id': 3, 'name': 'VIP', 'stacking_mode': 'stack', 'breed_ids': [1, 2]}])
        rules = client.get_listing_pricing_rules(listing_id='1')
        assert rules[0].breed_ids == [1, 2]

    @responses.activate
    def test_get_listing_pricing_rule(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/pricing_rules/3", status=200, json={'id': 3})
        assert client.get_listing_pricing_rule(listing_id='1', pricing_rule_id='3').id == 3

    @responses.activate
    def test_create_listing_pricing_rule(self, client):
        params = {'name': 'Big dogs', 'animal_type_id': 1, 'direction': 'surcharge', 'adjustment_percent': 10}
        responses.add(responses.POST, f"{BASE}listings/1/pricing_rules", status=201,
                      match=[matchers.json_params_matcher(params)], json={'id': 4, 'name': 'Big dogs'})
        assert client.create_listing_pricing_rule(listing_id='1', params=params).name == 'Big dogs'

    @responses.activate
    def test_create_listing_pricing_rule_with_stay_and_tag_conditions(self, client):
        params = {'name': 'Long VIP stays', 'customer_tag_ids': [5], 'minimum_nights': 7, 'minimum_pets': 2,
                  'minimum_weight_lbs': 40.5, 'stacking_mode': 'exclusive_stay_adjustment'}
        responses.add(responses.POST, f"{BASE}listings/1/pricing_rules", status=201,
                      match=[matchers.json_params_matcher(params)],
                      json={'id': 5, 'customer_tag_ids': [5], 'minimum_nights': 7, 'minimum_pets': 2,
                            'minimum_weight_lbs': 40.5, 'stacking_mode': 'exclusive_stay_adjustment'})
        rule = client.create_listing_pricing_rule(listing_id='1', params=params)
        assert rule.customer_tag_ids == [5]
        assert rule.minimum_weight_lbs == 40.5

    @responses.activate
    def test_create_listing_pricing_rule_needs_a_condition(self, client):
        responses.add(responses.POST, f"{BASE}listings/1/pricing_rules", status=422,
                      json={'errors': ['A rule needs at least one condition']})
        with pytest.raises(ValidationError) as raised:
            client.create_listing_pricing_rule(listing_id='1', params={'name': 'Nothing'})
        assert raised.value.errors == ['A rule needs at least one condition']

    @responses.activate
    def test_patch_listing_pricing_rule_clears_a_field(self, client):
        responses.add(responses.PATCH, f"{BASE}listings/1/pricing_rules/3", status=200,
                      match=[matchers.json_params_matcher({'customer_id': None})], json={'id': 3, 'customer_id': None})
        rule = client.patch_listing_pricing_rule(listing_id='1', pricing_rule_id='3', params={'customer_id': None})
        assert rule.customer_id is None

    @responses.activate
    def test_delete_listing_pricing_rule(self, client):
        responses.add(responses.DELETE, f"{BASE}listings/1/pricing_rules/3", status=204)
        assert client.delete_listing_pricing_rule(listing_id='1', pricing_rule_id='3') is True

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_pricing_rules(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_pricing_rule(listing_id='1', pricing_rule_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_listing_pricing_rule(listing_id='', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_listing_pricing_rule(listing_id='', pricing_rule_id='3', params={})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.delete_listing_pricing_rule(listing_id='1', pricing_rule_id='')


class TestMembershipPlansDSL:
    @responses.activate
    def test_get_listing_membership_plans(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/membership_plans", status=200,
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'per_page': '100'})],
                      json=[{'id': 2, 'stay_discount_percent': 10.0, 'plan_type': 'punch_card'}])
        plans = client.get_listing_membership_plans(listing_id='1', params={'per_page': 500})
        assert plans[0].stay_discount_percent == 10.0

    @responses.activate
    def test_get_listing_membership_plan(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/membership_plans/2", status=200, json={'id': 2})
        assert client.get_listing_membership_plan(listing_id='1', membership_plan_id='2').id == 2

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_membership_plans(listing_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_membership_plan(listing_id='1', membership_plan_id='')
