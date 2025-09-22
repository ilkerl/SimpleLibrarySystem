# We no longer need to import the Book class here,
# as the Library class now handles that detail internally.
from crud import Library

def main():
    """
    Main function to run the command-line interface for the library application.
    """
    lib = Library()

    while True:
        print("\n--- Library Menu ---")
        # Update the menu text to reflect the new functionality.
        print("1. Add Book (by ISBN)")
        print("2. Remove Book")
        print("3. List Books")
        print("4. Find Book")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        # --- CHANGE IS HERE ---
        if choice == '1':
            # We only ask for the ISBN now.
            isbn = input("Enter the ISBN of the book to add: ").strip()

            if isbn:
                # The library.add_book method now only takes an isbn.
                lib.add_book(isbn)
            else:
                print("Error: ISBN cannot be empty.")

        elif choice == '2':
            isbn = input("Enter the ISBN of the book to remove: ").strip()
            if isbn:
                lib.remove_book(isbn)
            else:
                print("Error: ISBN cannot be empty.")

        elif choice == '3':
            lib.list_books()

        elif choice == '4':
            isbn = input("Enter the ISBN of the book to find: ").strip()
            if isbn:
                book = lib.find_book(isbn)
                if book:
                    print(f"\nBook found: {book}")
                else:
                    print(f"No book found with this ISBN: {isbn}")
            else:
                print("Error: ISBN cannot be empty.")

        elif choice == '5':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

