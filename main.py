from library import Library
from book import Book

def main():
    """
    Main function to run the command-line interface for the library application.
    """
    # Create an instance of our Library class.
    # This will automatically load books from "library.json" if it exists.
    lib = Library()

    while True:
        # Display the main menu to the user.
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. List Books")
        print("4. Find Book")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            # Get book details from the user.
            title = input("Enter title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()

            # Basic validation to ensure inputs are not empty.
            if title and author and isbn:
                new_book = Book(title, author, isbn)
                lib.add_book(new_book)
            else:
                print("Error: Title, author, and ISBN cannot be empty.")

        elif choice == '2':
            isbn = input("Enter ISBN of the book to remove: ").strip()
            if isbn:
                lib.remove_book(isbn)
            else:
                print("Error: ISBN cannot be empty.")

        elif choice == '3':
            lib.list_books()

        elif choice == '4':
            isbn = input("Enter ISBN of the book to find: ").strip()
            if isbn:
                book = lib.find_book(isbn)
                if book:
                    print(f"\nFound book: {book}")
                else:
                    print(f"No book found with ISBN {isbn}.")
            else:
                print("Error: ISBN cannot be empty.")

        elif choice == '5':
            print("Exiting the application. Goodbye!")
            break # Exit the while loop to terminate the program.

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# This standard Python construct ensures that the main() function is called
# only when the script is executed directly.
if __name__ == "__main__":
    main()
