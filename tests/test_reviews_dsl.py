import pytest
import responses
from upwoof_listings.client import Client

@pytest.fixture
def client():
    return Client(api_key='test_key')

class TestReviewsDSL:
    @responses.activate
    def test_get_listing_reviews(self, client):
        responses.add(responses.GET, 'https://pethotels.upwoof.com/api/v1/listings/1/reviews',
                      json=[{'ID': 1, 'RATING': 5, 'BODY': 'Great stay'}], status=200)
        reviews = client.get_listing_reviews(listing_id='1')
        assert len(reviews) == 1
        assert reviews[0].id == 1
        assert reviews[0].rating == 5
        assert reviews[0].body == 'Great stay'

    @responses.activate
    def test_create_reservation_review(self, client):
        responses.add(responses.POST, 'https://pethotels.upwoof.com/api/v1/reservations/1/review',
                      json={'ID': 2, 'RATING': 4, 'RESERVATION_ID': 1}, status=201)
        review = client.create_reservation_review(reservation_id='1', params={'rating': 4})
        assert review.id == 2
        assert review.rating == 4
        assert review.reservation_id == 1

    def test_get_listing_reviews_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_reviews(listing_id='')

    def test_create_reservation_review_no_id(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_reservation_review(reservation_id='', params={'rating': 5})
