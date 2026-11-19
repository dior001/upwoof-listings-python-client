import pytest
import responses
from responses import matchers
from upwoof_listings.client import Client
from upwoof_listings.errors import ClientError, ResourceNotFoundError, ValidationError

BASE = "https://pethotels.upwoof.com/api/v1/"

# pylint: disable=redefined-outer-name

PART = {'id': 8, 'invoice_id': 5, 'listing_id': 1, 'tender': 'cash', 'amount_cents': 2000, 'currency': 'NZD',
        'net_amount_cents': 2000, 'refundable_cents': 2000, 'refunded_cents': 0, 'reported_to_stripe': False,
        'recorded_by_user_id': 3, 'reversed_at': None, 'source_type': None, 'source_id': None}


@pytest.fixture
def client():
    return Client(api_key="test_key")


class TestInvoicePaymentsDSL:
    @responses.activate
    def test_get_invoice_payments(self, client):
        responses.add(responses.GET, f"{BASE}invoices/5/payments", status=200, json=[PART],
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'page': '2'})])
        parts = client.get_invoice_payments(invoice_id='5', params={'page': 2})
        assert isinstance(parts[0], client.resources.InvoicePayment)
        assert parts[0].tender == 'cash'
        assert parts[0].refundable_cents == 2000

    @responses.activate
    def test_create_invoice_payment(self, client):
        responses.add(responses.POST, f"{BASE}invoices/5/payments", status=201, json=PART,
                      match=[matchers.json_params_matcher({'tender': 'cash', 'amount_cents': 2000})])
        part = client.create_invoice_payment(invoice_id='5', params={'tender': 'cash', 'amount_cents': 2000})
        assert part.id == 8

    @responses.activate
    def test_create_invoice_payment_refused(self, client):
        responses.add(responses.POST, f"{BASE}invoices/5/payments", status=422,
                      json={'errors': ['Amount is more than the invoice still owes']})
        with pytest.raises(ValidationError) as raised:
            client.create_invoice_payment(invoice_id='5', params={'tender': 'check', 'amount_cents': 99999})
        assert raised.value.errors == ['Amount is more than the invoice still owes']

    @responses.activate
    def test_create_invoice_payment_forbidden_for_staff(self, client):
        responses.add(responses.POST, f"{BASE}invoices/5/payments", status=403, json={'message': 'Forbidden'})
        with pytest.raises(ClientError) as raised:
            client.create_invoice_payment(invoice_id='5', params={'tender': 'cash'})
        assert raised.value.response.status_code == 403

    @responses.activate
    def test_refund_invoice_payment(self, client):
        refunded = dict(PART, refunded_cents=500, net_amount_cents=1500, refundable_cents=1500)
        responses.add(responses.POST, f"{BASE}invoices/5/payments/8/refund", status=200, json=refunded,
                      match=[matchers.json_params_matcher({'amount_cents': 500})])
        part = client.refund_invoice_payment(invoice_id='5', payment_id='8', params={'amount_cents': 500})
        assert isinstance(part, client.resources.InvoicePayment)
        assert part.net_amount_cents == 1500

    @responses.activate
    def test_refund_invoice_payment_whole_part(self, client):
        responses.add(responses.POST, f"{BASE}invoices/5/payments/8/refund", status=200,
                      json=dict(PART, refunded_cents=2000, refundable_cents=0))
        assert client.refund_invoice_payment(invoice_id='5', payment_id='8').refundable_cents == 0

    @responses.activate
    def test_refund_invoice_payment_not_found(self, client):
        responses.add(responses.POST, f"{BASE}invoices/5/payments/9/refund", status=404, json={'message': 'Not found'})
        with pytest.raises(ResourceNotFoundError):
            client.refund_invoice_payment(invoice_id='5', payment_id='9')

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_invoice_payments(invoice_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.create_invoice_payment(invoice_id='', params={'tender': 'cash'})
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.refund_invoice_payment(invoice_id='5', payment_id='')


class TestCreditNoteNamingAPart:
    @responses.activate
    def test_create_credit_note_with_invoice_payment_id(self, client):
        params = {'invoice_id': 5, 'invoice_payment_id': 8, 'credit_note_line_items': []}
        responses.add(responses.POST, f"{BASE}credit_notes/", status=201, json={'id': 12, 'invoice_id': 5},
                      match=[matchers.json_params_matcher(params)])
        assert client.create_credit_note(params=params).id == 12

    @responses.activate
    def test_create_credit_note_without_a_part_on_a_split_paid_invoice(self, client):
        message = 'Payment to refund must be chosen: this invoice was paid in parts'
        responses.add(responses.POST, f"{BASE}credit_notes/", status=422, json={'errors': [message]})
        with pytest.raises(ValidationError) as raised:
            client.create_credit_note(params={'invoice_id': 5})
        assert raised.value.errors == [message]


class TestPatchReservationRetailItem:
    @responses.activate
    def test_patch_reservation_retail_item(self, client):
        responses.add(responses.PATCH, f"{BASE}reservations/3/retail_items/6", status=200,
                      match=[matchers.json_params_matcher({'quantity': 3})],
                      json={'id': 6, 'quantity': 3, 'unit_price_cents': 1200})
        item = client.patch_reservation_retail_item(reservation_id='3', retail_item_id='6', params={'quantity': 3})
        assert isinstance(item, client.resources.ReservationRetailItem)
        assert item.quantity == 3

    @responses.activate
    def test_patch_reservation_retail_item_refused(self, client):
        responses.add(responses.PATCH, f"{BASE}reservations/3/retail_items/6", status=422,
                      json={'errors': ['Not enough in stock']})
        with pytest.raises(ValidationError) as raised:
            client.patch_reservation_retail_item(reservation_id='3', retail_item_id='6', params={'quantity': 50})
        assert raised.value.errors == ['Not enough in stock']

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.patch_reservation_retail_item(reservation_id='3', retail_item_id='', params={'quantity': 1})


class TestAttendanceConfirmationsDSL:
    REQUEST = {'id': 2, 'reservation_id': 3, 'status': 'pending', 'visit_on': '2026-11-20',
               'visit_date': '2026-11-20', 'requested_at': '2026-11-19T08:00:00Z', 'responded_at': None}

    @responses.activate
    def test_get_reservation_attendance_confirmations(self, client):
        responses.add(responses.GET, f"{BASE}reservations/3/attendance_confirmations", status=200,
                      json=[self.REQUEST])
        requests = client.get_reservation_attendance_confirmations(reservation_id='3')
        assert isinstance(requests[0], client.resources.AttendanceConfirmation)
        assert requests[0].visit_date == '2026-11-20'

    @responses.activate
    def test_get_listing_attendance_confirmations_filtered(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/attendance_confirmations", status=200,
                      json=[dict(self.REQUEST, status='declined')],
                      match=[matchers.query_param_matcher({'access_token': 'test_key', 'date': '2026-11-20',
                                                           'status': 'declined'})])
        requests = client.get_listing_attendance_confirmations(
            listing_id='1', params={'date': '2026-11-20', 'status': 'declined'})
        assert requests[0].status == 'declined'

    @responses.activate
    def test_get_listing_attendance_confirmations_bad_status(self, client):
        responses.add(responses.GET, f"{BASE}listings/1/attendance_confirmations", status=400,
                      json={'error': 'status does not have a valid value'})
        with pytest.raises(ClientError) as raised:
            client.get_listing_attendance_confirmations(listing_id='1', params={'status': 'maybe'})
        assert raised.value.response.status_code == 400

    def test_blank_ids(self, client):
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_reservation_attendance_confirmations(reservation_id='')
        with pytest.raises(ValueError, match="ID cannot be blank"):
            client.get_listing_attendance_confirmations(listing_id='')
