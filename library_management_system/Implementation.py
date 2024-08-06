from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, genre):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.availability_status = True

    def update_availability(self, status):
        self.availability_status = status

    def get_book_details(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'availability_status': self.availability_status
        }

class User:
    def __init__(self, user_id, name, email, phone, address):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.borrowed_books = []
        self.reserved_books = []

    def borrow_book(self, book):
        if book.availability_status:
            loan = Loan(f"L-{len(self.borrowed_books)+1}", self, book, datetime.now(), datetime.now() + timedelta(days=14))
            book.update_availability(False)
            self.borrowed_books.append(loan)
            return loan
        else:
            return None

    def return_book(self, book):
        for loan in self.borrowed_books:
            if loan.book == book and loan.status == 'Active':
                loan.return_book()
                book.update_availability(True)
                self.borrowed_books.remove(loan)
                return loan
        return None

    def reserve_book(self, book):
        reservation = Reservation(f"R-{len(self.reserved_books)+1}", self, book, datetime.now())
        self.reserved_books.append(reservation)
        return reservation

    def view_borrowed_books(self):
        return [loan.get_loan_details() for loan in self.borrowed_books]

    def view_reserved_books(self):
        return [reservation.get_reservation_details() for reservation in self.reserved_books]

class Loan:
    def __init__(self, loan_id, user, book, loan_date, due_date):
        self.loan_id = loan_id
        self.user = user
        self.book = book
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = None
        self.status = 'Active'

    def calculate_fine(self):
        if self.return_date and self.return_date > self.due_date:
            overdue_days = (self.return_date - self.due_date).days
            return overdue_days * 1.0  # Assuming $1 per overdue day
        return 0

    def return_book(self):
        self.return_date = datetime.now()
        self.status = 'Returned'

    def get_loan_details(self):
        return {
            'loan_id': self.loan_id,
            'user': self.user.name,
            'book': self.book.get_book_details(),
            'loan_date': self.loan_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'status': self.status,
            'fine': self.calculate_fine()
        }

class Reservation:
    def __init__(self, reservation_id, user, book, reservation_date):
        self.reservation_id = reservation_id
        self.user = user
        self.book = book
        self.reservation_date = reservation_date
        self.status = 'Active'

    def cancel_reservation(self):
        self.status = 'Cancelled'

    def get_reservation_details(self):
        return {
            'reservation_id': self.reservation_id,
            'user': self.user.name,
            'book': self.book.get_book_details(),
            'reservation_date': self.reservation_date,
            'status': self.status
        }

class Fine:
    def __init__(self, fine_id, loan, amount):
        self.fine_id = fine_id
        self.loan = loan
        self.amount = amount
        self.fine_date = datetime.now()
        self.status = 'Pending'

    def calculate_fine(self):
        return self.loan.calculate_fine()

    def pay_fine(self):
        self.status = 'Paid'

    def get_fine_details(self):
        return {
            'fine_id': self.fine_id,
            'loan': self.loan.loan_id,
            'amount': self.amount,
            'fine_date': self.fine_date,
            'status': self.status
        }
