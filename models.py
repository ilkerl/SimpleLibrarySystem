from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Define the base class that our models will inherit from.
Base = declarative_base()

class Book(Base):
    """
    This class represents the 'books' table in our database.
    SQLAlchemy's ORM will map this class to the table.
    """
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    isbn = Column(String, unique=True, index=True)

    def __str__(self):
        """
        Returns a user-friendly string representation of the book.
        """
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'

