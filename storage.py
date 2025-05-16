
import csv
import os
import uuid

class LibraryStorage:
    def __init__(self, data_dir="./data"):
        self.books_file = os.path.join(data_dir, "books.csv")
        self.members_file = os.path.join(data_dir, "members.csv")
        self.loans_file = os.path.join(data_dir, "loans.csv")

        # Ensure all data files exist
        for file in [self.books_file, self.members_file, self.loans_file]:
            if not os.path.exists(file):
                with open(file, "w", newline="") as f:
                    writer = csv.writer(f)
                    if "books" in file:
                        writer.writerow(["id", "title", "author"])
                    elif "members" in file:
                        writer.writerow(["id", "name"])
                    elif "loans" in file:
                        writer.writerow(["member_id", "book_id"])

    def get_all_books(self):
        with open(self.books_file, "r") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def add_book(self, book):
        book_id = str(uuid.uuid4())[:8]
        with open(self.books_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([book_id, book["title"], book["author"]])

    def get_all_members(self):
        with open(self.members_file, "r") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def is_book_borrowed(self, book_id):
        with open(self.loans_file, "r") as f:
            reader = csv.DictReader(f)
            return any(row["book_id"] == book_id for row in reader)

    def borrow_book(self, member_id, book_id):
        if self.is_book_borrowed(book_id):
            return False
        with open(self.loans_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([member_id, book_id])
        return True

    def return_book(self, member_id, book_id):
        rows = []
        returned = False
        with open(self.loans_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["member_id"] == member_id and row["book_id"] == book_id:
                    returned = True
                    continue
                rows.append(row)
        if returned:
            with open(self.loans_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["member_id", "book_id"])
                writer.writeheader()
                writer.writerows(rows)
        return returned
