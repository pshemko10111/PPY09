import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

books = [
    {'book': 'Harry Potter', 'price': 10.00},
    {'book': 'The Hobbit', 'price': 12.00},
    {'book': '1984', 'price': 8.00},
    {'book': 'To Kill a Mockingbird', 'price': 9.00}
]

persons = [
    {'id': 1, 'first_name': 'John', 'last_name': 'Doe', 'reservations': []},
    {'id': 2, 'first_name': 'Jane', 'last_name': 'Smith', 'reservations': []},
    {'id': 3, 'first_name': 'Alice', 'last_name': 'Johnson', 'reservations': []}
]

reservations = []


class Reservation:
    def __init__(self, book_title, days, start_date):
        self.book_title = book_title
        self.days = days
        self.start_date = start_date

    def __str__(self):
        return '(Book: {0}, Days: {1}, Start date: {2})'.format(self.book_title, self.days, self.start_date)


def home():
    st.title("Book Rental System")
    st.write(
        "Welcome to the Book Rental System. You can browse available books, make reservations, and check your reservations.")


def view_books():
    st.title("Available Books")
    df_books = pd.DataFrame(books)
    st.table(df_books)


def make_reservation():
    st.title("Make a Reservation")
    person_id = st.number_input("Enter your ID", min_value=0, step=1)
    book_title = st.selectbox("Select Book", [book['book'] for book in books])
    days = st.number_input("Number of Days", min_value=1, step=1)
    start_date = st.date_input("Start Date")

    if st.button("Reserve"):
        for person in persons:
            if person['id'] == person_id:
                reservation = {
                    'book_title': book_title,
                    'days': days,
                    'start_date': start_date.strftime("%Y-%m-%d")
                }
                person['reservations'].append(reservation)
                reservations.append({'person_id': person_id, **reservation})
                st.success(f"Reserved {book_title} for {days} days starting from {start_date}")
                return
        st.error("Person not found")


def check_reservations():
    st.title("Check Reservations")
    person_id = st.number_input("Enter your ID", min_value=0, step=1)
    if st.button("Check"):
        for person in persons:
            if person['id'] == person_id:
                if person['reservations']:
                    df_reservations = pd.DataFrame(person['reservations'])
                    st.table(df_reservations)
                else:
                    st.warning("No reservations found")
                return
        st.error("Person not found")


def reservations_statistics():
    st.title("Reservations Statistics")
    current_month = datetime.now().month
    days_in_month = pd.date_range(start=f"{datetime.now().year}-{current_month}-01", periods=30).strftime(
        "%Y-%m-%d").tolist()
    reservations_per_day = {day: 0 for day in days_in_month}

    for reservation in reservations:
        if reservation['start_date'][:7] == f"{datetime.now().year}-{current_month:02d}":
            reservations_per_day[reservation['start_date']] += 1

    df_stats = pd.DataFrame(list(reservations_per_day.items()), columns=['Date', 'Reservations'])
    plt.figure(figsize=(10, 5))
    plt.plot(df_stats['Date'], df_stats['Reservations'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Reservations')
    plt.title('Reservations in the Current Month')
    plt.xticks(rotation=45)
    st.pyplot(plt)


def main():
    st.sidebar.title("Navigation")
    options = ["Home", "View Books", "Make Reservation", "Check Reservations", "Reservations Statistics"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Home":
        home()
    elif choice == "View Books":
        view_books()
    elif choice == "Make Reservation":
        make_reservation()
    elif choice == "Check Reservations":
        check_reservations()
    elif choice == "Reservations Statistics":
        reservations_statistics()


if __name__ == '__main__':
    main()
