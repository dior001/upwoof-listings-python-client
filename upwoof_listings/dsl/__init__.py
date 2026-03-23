from .listings import ListingsDSL
from .pets import PetsDSL
from .accommodations import AccommodationsDSL
from .credit_notes import CreditNotesDSL
from .customers import CustomersDSL
from .invoices import InvoicesDSL
from .orders import OrdersDSL
from .reservations import ReservationsDSL
from .users import UsersDSL
from .accommodation_types import AccommodationTypesDSL
from .animal_types import AnimalTypesDSL
from .breeds import BreedsDSL
from .uw_listing_cms_apps import UwListingCmsAppsDSL

class DSL(
    ListingsDSL,
    PetsDSL,
    AccommodationsDSL,
    CreditNotesDSL,
    CustomersDSL,
    InvoicesDSL,
    OrdersDSL,
    ReservationsDSL,
    UsersDSL,
    AccommodationTypesDSL,
    AnimalTypesDSL,
    BreedsDSL,
    UwListingCmsAppsDSL
):
    @property
    def resources(self):
        from .. import resources
        return resources
