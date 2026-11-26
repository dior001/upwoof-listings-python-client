from .listings import ListingsDSL
from .listing_websites import ListingWebsitesDSL
from .pets import PetsDSL
from .accommodations import AccommodationsDSL
from .credit_notes import CreditNotesDSL
from .customers import CustomersDSL
from .invoices import InvoicesDSL
from .orders import OrdersDSL
from .reservations import ReservationsDSL
from .reviews import ReviewsDSL
from .users import UsersDSL
from .accommodation_types import AccommodationTypesDSL
from .animal_types import AnimalTypesDSL
from .breeds import BreedsDSL
from .vaccination_records import VaccinationRecordsDSL
from .waiver_signatures import WaiverSignaturesDSL
from .report_cards import ReportCardsDSL
from .pet_evaluations import PetEvaluationsDSL
from .store_credits import StoreCreditsDSL
from .pricing_rules import PricingRulesDSL
from .membership_plans import MembershipPlansDSL
from .custom_fields import CustomFieldsDSL
from .special_opening_hours import SpecialOpeningHoursDSL
from .notification_templates import NotificationTemplatesDSL
from .training_courses import TrainingCoursesDSL
from .card_readers import CardReadersDSL
from .grooming import GroomingDSL
from .play_yards import PlayYardsDSL
from .authorized_pickups import AuthorizedPickupsDSL
from .customer_tags import CustomerTagsDSL
from .stay_products import StayProductsDSL
from .invoice_payments import InvoicePaymentsDSL
from .attendance_confirmations import AttendanceConfirmationsDSL
from .recurring_reservation_schedules import RecurringReservationSchedulesDSL
from .pet_care_plans import PetCarePlansDSL
from .care_log_entries import CareLogEntriesDSL
from .appointment_no_shows import AppointmentNoShowsDSL
from .email_addresses import EmailAddressesDSL
from .ai_tasks import AiTasksDSL

class DSL(
    ListingsDSL,
    ListingWebsitesDSL,
    PetsDSL,
    AccommodationsDSL,
    CreditNotesDSL,
    CustomersDSL,
    InvoicesDSL,
    OrdersDSL,
    ReservationsDSL,
    ReviewsDSL,
    UsersDSL,
    AccommodationTypesDSL,
    AnimalTypesDSL,
    BreedsDSL,
    VaccinationRecordsDSL,
    WaiverSignaturesDSL,
    ReportCardsDSL,
    PetEvaluationsDSL,
    StoreCreditsDSL,
    PricingRulesDSL,
    MembershipPlansDSL,
    CustomFieldsDSL,
    SpecialOpeningHoursDSL,
    NotificationTemplatesDSL,
    TrainingCoursesDSL,
    CardReadersDSL,
    GroomingDSL,
    PlayYardsDSL,
    AuthorizedPickupsDSL,
    CustomerTagsDSL,
    StayProductsDSL,
    InvoicePaymentsDSL,
    AttendanceConfirmationsDSL,
    RecurringReservationSchedulesDSL,
    PetCarePlansDSL,
    CareLogEntriesDSL,
    AppointmentNoShowsDSL,
    EmailAddressesDSL,
    AiTasksDSL
):
    @property
    def resources(self):
        from .. import resources
        return resources
