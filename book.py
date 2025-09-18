class Book:
    """
    Represents a single book in the library.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The International Standard Book Number, used as a unique identifier.
    """

    def __init__(self, title, author, isbn):
        """
        Initializes a new Book object.
        This method takes the title, author, and isbn attributes as specified in the project document.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN of the book.
        """
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        """
        Returns a user-friendly string representation of the book.
        This method is overridden to produce an output matching the format specified in the document,
        like "Ulysses by James Joyce (ISBN: 978-0199535675)".

        Returns:
            str: The formatted string representation of the book.
        """
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'

    def to_dict(self):
        """
        Converts the Book object to a dictionary.
        This is useful for serialization, especially for writing to a JSON file.

        Returns:
            dict: A dictionary representation of the book.
        """
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn
        }
