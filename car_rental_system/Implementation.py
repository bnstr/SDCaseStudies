from datetime import datetime

class Vehicle:
    def __init__(self, vehicle_id, make, model, year, rental_rate):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.rental_rate = rental_rate
        self.availability_status = True

    def update_availability(self, status):
        self.availability_status = status

    def get_vehicle_details(self):
        return {
            'vehicle_id': self.vehicle_id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'rental_rate': self.rental_rate,
            'availability_status': self.availability_status
        }

class Rental:
    def __init__(self, rental_id, customer, vehicle, rental_start_date, rental_end_date):
        self.rental_id = rental_id
        self.customer = customer
        self.vehicle = vehicle
        self.rental_start_date = rental_start_date
        self.rental_end_date = rental_end_date
        self.status = 'Active'
        self.cost = 0

    def calculate_cost(self):
        days = (self.rental_end_date - self.rental_start_date).days
        self.cost = self.vehicle.rental_rate * days
        return self.cost

    def return_vehicle(self):
        self.status = 'Returned'
        self.vehicle.update_availability(True)

    def get_rental_details(self):
        return {
            'rental_id': self.rental_id,
            'customer': self.customer.name,
            'vehicle': self.vehicle.get_vehicle_details(),
            'rental_start_date': self.rental_start_date,
            'rental_end_date': self.rental_end_date,
            'status': self.status,
            'cost': self.cost
        }

class Customer:
    def __init__(self, customer_id, name, email, phone, address):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.rentals = []

    def rent_vehicle(self, vehicle, start_date, end_date):
        if vehicle.availability_status:
            rental = Rental(f"R-{len(self.rentals)+1}", self, vehicle, start_date, end_date)
            vehicle.update_availability(False)
            rental.calculate_cost()
            self.rentals.append(rental)
            return rental
        else:
            return None

    def return_vehicle(self, rental):
        rental.return_vehicle()
        return rental

    def view_rentals(self):
        return [rental.get_rental_details() for rental in self.rentals]

class Pricing:
    def __init__(self, vehicle_type, daily_rate, weekly_rate):
        self.vehicle_type = vehicle_type
        self.daily_rate = daily_rate
        self.weekly_rate = weekly_rate

    def calculate_rental_cost(self, days):
        if days > 7:
            return (days // 7) * self.weekly_rate + (days % 7) * self.daily_rate
        return days * self.daily_rate

class Payment:
    def __init__(self, payment_id, rental, amount):
        self.payment_id = payment_id
        self.rental = rental
        self.amount = amount
        self.payment_date = datetime.now()
        self.payment_status = 'Pending'

    def process_payment(self):
        # Logic to process payment
        self.payment_status = 'Completed'

    def refund_payment(self):
        # Logic to refund payment
        self.payment_status = 'Refunded'

    def get_payment_details(self):
        return {
            'payment_id': self.payment_id,
            'rental': self.rental.rental_id,
            'amount': self.amount,
            'payment_date': self.payment_date,
            'payment_status': self.payment_status
        }
