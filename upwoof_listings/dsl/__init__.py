from .listings import ListingsDSL

class PetsDSL:
    def get_pets(self):
        return self.resources.Pet.parse(self.request('get', 'pets/'))
    def get_pet(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Pet.parse(self.request('get', f"pets/{id}"))
    def create_pet(self, params):
        return self.resources.Pet.parse(self.request('post', 'pets/', query=params))
    def update_pet(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Pet.parse(self.request('put', f"pets/{id}", query=params))
    def patch_pet(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Pet.parse(self.request('patch', f"pets/{id}", query=params))
    def delete_pet(self, id):
        if not id: raise ValueError("ID cannot be blank")
        return self.request('delete', f"pets/{id}").status_code == 204

class AccommodationsDSL:
    def get_accommodations(self):
        return self.resources.Accommodation.parse(self.request('get', 'accommodations/'))
    def get_accommodation(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Accommodation.parse(self.request('get', f"accommodations/{id}"))
    def create_accommodation(self, params):
        return self.resources.Accommodation.parse(self.request('post', 'accommodations/', query=params))
    def update_accommodation(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Accommodation.parse(self.request('put', f"accommodations/{id}", query=params))
    def patch_accommodation(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Accommodation.parse(self.request('patch', f"accommodations/{id}", query=params))
    def delete_accommodation(self, id):
        if not id: raise ValueError("ID cannot be blank")
        return self.request('delete', f"accommodations/{id}").status_code == 204

class CreditNotesDSL:
    def get_credit_notes(self):
        return self.resources.CreditNote.parse(self.request('get', 'credit_notes/'))
    def get_credit_note(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.CreditNote.parse(self.request('get', f"credit_notes/{id}"))
    def create_credit_note(self, params):
        return self.resources.CreditNote.parse(self.request('post', 'credit_notes/', query=params))
    def update_credit_note(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.CreditNote.parse(self.request('put', f"credit_notes/{id}", query=params))
    def patch_credit_note(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.CreditNote.parse(self.request('patch', f"credit_notes/{id}", query=params))
    def delete_credit_note(self, id):
        if not id: raise ValueError("ID cannot be blank")
        return self.request('delete', f"credit_notes/{id}").status_code == 204

class CustomersDSL:
    def get_customers(self):
        return self.resources.Customer.parse(self.request('get', 'customers/'))
    def get_customer(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Customer.parse(self.request('get', f"customers/{id}"))
    def create_customer(self, params):
        return self.resources.Customer.parse(self.request('post', 'customers/', query=params))
    def update_customer(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Customer.parse(self.request('put', f"customers/{id}", query=params))
    def patch_customer(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Customer.parse(self.request('patch', f"customers/{id}", query=params))
    def delete_customer(self, id):
        if not id: raise ValueError("ID cannot be blank")
        return self.request('delete', f"customers/{id}").status_code == 204

class InvoicesDSL:
    def get_invoices(self):
        return self.resources.Invoice.parse(self.request('get', 'invoices/'))
    def get_invoice(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Invoice.parse(self.request('get', f"invoices/{id}"))
    def create_invoice(self, params):
        return self.resources.Invoice.parse(self.request('post', 'invoices/', query=params))
    def update_invoice(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Invoice.parse(self.request('put', f"invoices/{id}", query=params))
    def patch_invoice(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Invoice.parse(self.request('patch', f"invoices/{id}", query=params))
    def delete_invoice(self, id):
        if not id: raise ValueError("ID cannot be blank")
        return self.request('delete', f"invoices/{id}").status_code == 204

class OrdersDSL:
    def get_orders(self):
        return self.resources.Order.parse(self.request('get', 'orders/'))
    def get_order(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Order.parse(self.request('get', f"orders/{id}"))
    def create_order(self, params):
        return self.resources.Order.parse(self.request('post', 'orders/', query=params))
    def update_order(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Order.parse(self.request('put', f"orders/{id}", query=params))
    def patch_order(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Order.parse(self.request('patch', f"orders/{id}", query=params))
    def delete_order(self, id):
        if not id: raise ValueError("ID cannot be blank")
        return self.request('delete', f"orders/{id}").status_code == 204

class ReservationsDSL:
    def get_reservations(self):
        return self.resources.Reservation.parse(self.request('get', 'reservations/'))
    def get_reservation(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Reservation.parse(self.request('get', f"reservations/{id}"))
    def create_reservation(self, params):
        return self.resources.Reservation.parse(self.request('post', 'reservations/', query=params))
    def update_reservation(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Reservation.parse(self.request('put', f"reservations/{id}", query=params))
    def patch_reservation(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Reservation.parse(self.request('patch', f"reservations/{id}", query=params))
    def delete_reservation(self, id):
        if not id: raise ValueError("ID cannot be blank")
        return self.request('delete', f"reservations/{id}").status_code == 204

class UsersDSL:
    def get_users(self):
        return self.resources.User.parse(self.request('get', 'users/'))
    def get_user(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.User.parse(self.request('get', f"users/{id}"))
    def create_user(self, params):
        return self.resources.User.parse(self.request('post', 'users/', query=params))
    def update_user(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.User.parse(self.request('put', f"users/{id}", query=params))
    def patch_user(self, id, params):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.User.parse(self.request('patch', f"users/{id}", query=params))
    def delete_user(self, id):
        if not id: raise ValueError("ID cannot be blank")
        return self.request('delete', f"users/{id}").status_code == 204

class AccommodationTypesDSL:
    def get_accommodation_types(self):
        return self.resources.AccommodationType.parse(self.request('get', 'accommodation_types/'))
    def get_accommodation_type(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.AccommodationType.parse(self.request('get', f"accommodation_types/{id}"))

class AnimalTypesDSL:
    def get_animal_types(self):
        return self.resources.AnimalType.parse(self.request('get', 'animal_types/'))
    def get_animal_type(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.AnimalType.parse(self.request('get', f"animal_types/{id}"))

class BreedsDSL:
    def get_breeds(self):
        return self.resources.Breed.parse(self.request('get', 'breeds/'))
    def get_breed(self, id: str):
        if not id: raise ValueError("ID cannot be blank")
        return self.resources.Breed.parse(self.request('get', f"breeds/{id}"))

class DSL(ListingsDSL, PetsDSL, AccommodationsDSL, CreditNotesDSL, CustomersDSL, InvoicesDSL, OrdersDSL, ReservationsDSL, UsersDSL, AccommodationTypesDSL, AnimalTypesDSL, BreedsDSL):
    @property
    def resources(self):
        from .. import resources
        return resources
