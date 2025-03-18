import json


class BookCollection:
    """A class to manage a collection of books, allowing users to store and organize their reading materials."""

    def __init__(self):
        """Initialize a new book collection with an empty list and set up file storage."""
        self.book_list = []
        self.favorite_books = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        """Load saved books from a JSON file into memory.
        If the file doesn't exist or is corrupted, start with an empty collection."""
        try:
            with open(self.storage_file, "r") as file:
                data = json.load(file)
                self.book_list = data.get("books", [])
                self.favorite_books = data.get("favorites", [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []
            self.favorite_books = []

    def save_to_file(self):
        """Store the current book collection to a JSON file for permanent storage."""
        with open(self.storage_file, "w") as file:
            json.dump({"books": self.book_list, "favorites": self.favorite_books}, file, indent=4)

    def create_new_book(self):
        """Add a new book to the collection by gathering information from the user."""
        book_title = input("Enter book title: ")
        book_author = input("Enter author: ")
        publication_year = input("Enter publication year: ")
        book_genre = input("Enter genre: ")
        is_book_read = (
            input("Have you read this book? (yes/no): ").strip().lower() == "yes"
        )
        is_favorite = input("Is this book a favorite? (yes/no): ").strip().lower() == "yes"

        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publication_year,
            "genre": book_genre,
            "read": is_book_read,
            "favorite": is_favorite
        }

        self.book_list.append(new_book)
        if is_favorite:
            self.favorite_books.append(new_book)
        self.save_to_file()
        print("Book added successfully!\n")

    def delete_book(self):
        """Remove a book from the collection using its title."""
        book_title = input("Enter the title of the book to remove: ")

        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                self.book_list.remove(book)
                if book in self.favorite_books:
                    self.favorite_books.remove(book)
                self.save_to_file()
                print("Book removed successfully!\n")
                return
        print("Book not found!\n")

    def find_book(self):
        """Search for books in the collection by title or author name."""
        search_type = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
        search_text = input("Enter search term: ").lower()
        found_books = [
            book
            for book in self.book_list
            if search_text in book["title"].lower()
            or search_text in book["author"].lower()
        ]

        if found_books:
            print("Matching Books:")
            for index, book in enumerate(found_books, 1):
                reading_status = "Read" if book["read"] else "Unread"
                print(
                    f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}"
                )
        else:
            print("No matching books found.\n")

    def update_book(self):
        """Modify the details of an existing book in the collection."""
        book_title = input("Enter the title of the book you want to edit: ")
        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                print("Leave blank to keep existing value.")
                book["title"] = input(f"New title ({book['title']}): ") or book["title"]
                book["author"] = (
                    input(f"New author ({book['author']}): ") or book["author"]
                )
                book["year"] = input(f"New year ({book['year']}): ") or book["year"]
                book["genre"] = input(f"New genre ({book['genre']}): ") or book["genre"]
                book["read"] = (
                    input("Have you read this book? (yes/no): ").strip().lower()
                    == "yes"
                )
                book["favorite"] = (
                    input("Is this book a favorite? (yes/no): ").strip().lower()
                    == "yes"
                )
                self.save_to_file()
                print("Book updated successfully!\n")
                return
        print("Book not found!\n")

    def show_all_books(self):
        """Display all books in the collection with their details."""
        if not self.book_list:
            print("Your collection is empty.\n")
            return

        print("Your Book Collection:")
        for index, book in enumerate(self.book_list, 1):
            reading_status = "Read" if book["read"] else "Unread"
            print(
                f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}"
            )
        print()

    def show_favorite_books(self):
        """Display all favorite books in the collection."""
        if not self.favorite_books:
            print("You have no favorite books.\n")
            return

        print("Your Favorite Books:")
        for index, book in enumerate(self.favorite_books, 1):
            print(f"{index}. {book['title']} by {book['author']} ({book['year']})")

    def show_books_by_genre(self):
        """Display books sorted by genre."""
        genres = set(book["genre"] for book in self.book_list)
        for genre in genres:
            print(f"\nBooks in genre: {genre}")
            for book in self.book_list:
                if book["genre"] == genre:
                    reading_status = "Read" if book["read"] else "Unread"
                    print(
                        f"- {book['title']} by {book['author']} ({book['year']}) - {reading_status}"
                    )
        print()

    def show_unread_books(self):
        """Display all unread books in the collection."""
        unread_books = [book for book in self.book_list if not book["read"]]
        if not unread_books:
            print("You have read all your books!\n")
            return

        print("Unread Books:")
        for index, book in enumerate(unread_books, 1):
            print(f"{index}. {book['title']} by {book['author']} ({book['year']})")
        print()

    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress."""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        completion_rate = (
            (completed_books / total_books * 100) if total_books > 0 else 0
        )
        print(f"Total books in collection: {total_books}")
        print(f"Reading progress: {completion_rate:.2f}%\n")

    def start_application(self):
        """Run the main application loop with a user-friendly menu interface."""
        while True:
            print("📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")
            print("2. Remove a book")
            print("3. Search for books")
            print("4. Update book details")
            print("5. View all books")
            print("6. View favorite books")
            print("7. View books by genre")
            print("8. View unread books")
            print("9. View reading progress")
            print("10. Exit")
            user_choice = input("Please choose an option (1-10): ")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_favorite_books()
            elif user_choice == "7":
                self.show_books_by_genre()
            elif user_choice == "8":
                self.show_unread_books()
            elif user_choice == "9":
                self.show_reading_progress()
            elif user_choice == "10":
                self.save_to_file()
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    book_manager = BookCollection()
    book_manager.start_application()

