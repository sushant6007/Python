# __code starts here__

# __code starts here__
import json
import pandas as pd
import mongomock
from pymongo import MongoClient
import matplotlib.pyplot as plt
# __code ends here__


class Book:
    def __init__(self, book_id, title, author, copies_sold):
        self.__book_id = book_id
        self.title = title
        self.author = author
        self.__copies_sold = copies_sold

    def __str__(self):
        return f"Book(BookId={self.__book_id}, Title={self.title}, Author={self.author}, CopiesSold={self.__copies_sold})"

    @staticmethod
    def validate_copies(copies_sold):
        if copies_sold < 0:
            raise ValueError("Copies sold cannot be negative")

    @classmethod
    def from_dict(cls, data):
        try:
            book_id = data.get('id') or data.get('book_id')
            title = data['title']
            author = data['author']
            copies_sold = data.get('copies') or data.get('copies_sold', 0)
            cls.validate_copies(copies_sold)
            return cls(book_id, title, author, copies_sold)
        except KeyError as e:
            return f"Missing key: {str(e)}"
        except ValueError as e:
            return str(e)

    def get_copies_sold(self):
        return self.__copies_sold
# __code ends here__


# __code starts here__
class EBook(Book):
    def __init__(self, book_id, title, author, copies_sold, download_link, publish_date):
        super().__init__(book_id, title, author, copies_sold)
        self.download_link = download_link
        self.publish_date = publish_date

    def __str__(self):
        return (f"EBook(BookId={self._Book__book_id}, Title={self.title}, "
                f"Author={self.author}, CopiesSold={self.get_copies_sold()}, "
                f"DownloadLink={self.download_link}, PublishDate={self.publish_date})")
# __code ends here__


# __code starts here__
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return "Error: File not found"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format"
# __code ends here__

# __code starts here__
def fetch_books_and_ebooks(data):
    try:
        books_data = data.get('books')
        ebooks_data = data.get('ebooks')

        if books_data is None or ebooks_data is None:
            return "Error: Missing expected keys"

        all_books = []
        for item in books_data:
            book_instance = Book.from_dict(item)
            if isinstance(book_instance, Book):
                all_books.append(book_instance)

        for item in ebooks_data:
            try:
                book_id = item.get('id') or item.get('book_id')
                title = item['title']
                author = item['author']
                copies_sold = item.get('copies') or item.get('copies_sold', 0)
                Book.validate_copies(copies_sold)
                download_link = item['download_link']
                publish_date = item['publish_date']
                all_books.append(EBook(book_id, title, author, copies_sold, download_link, publish_date))
            except KeyError as e:
                return f"Missing key: {str(e)}"
            except ValueError as e:
                return str(e)

        return all_books
    except Exception as e:
        return str(e)
# __code ends here__


# __code starts here__
def create_dataframe(all_books):
    try:
        df = pd.DataFrame([{
            'Title': book.title,
            'Authors': book.author,
            'Copies Sold': book.get_copies_sold()
        } for book in all_books])
        
        return df
    except Exception as e:
        return str(e)
# __code ends here__


# __code starts here__
def calculate_mean_and_visualize(dataframe):
    try:
        if 'Copies Sold' not in dataframe.columns:
            return "Error: 'Copies Sold' column not found in dataframe"
        
        mean_copies = dataframe['Copies Sold'].mean()
        dataframe.plot(kind='bar', x='Title', y='Copies Sold', title='Copies Sold per Book')
        plt.xlabel('Book Title')
        plt.ylabel('Copies Sold')
        plt.show()

        return mean_copies
    except Exception as e:
        return str(e)
# __code ends here__

# __code starts here__
def create_mongo_client_and_db():
    try:
        client = mongomock.MongoClient()
        database = client['Library_database']
        return database
    except Exception as e:
        return str(e)
# __code ends here__

# __code starts here__
def insert_books_into_db(all_books, database):
    try:
        books_collection = database['books']
        books_data = []
        
        for book in all_books:
            book_data = {
                'book_id': book._Book__book_id,
                'title': book.title,
                'author': book.author,
                'copies_sold': book.get_copies_sold()
            }
            if isinstance(book, EBook):
                book_data.update({
                    'download_link': book.download_link,
                    'publish_date': book.publish_date
                })
            books_data.append(book_data)

        books_collection.insert_many(books_data)
        return "All books inserted successfully"
    except Exception as e:
        return str(e)
# __code ends here__

# __code starts here__
def fetch_book_from_db(database, book_id):
    try:
        books_collection = database['books']
        book_data = books_collection.find_one({'book_id': book_id})

        if not book_data:
            return "No book found with the given ID"

        if 'download_link' in book_data:
            return EBook(book_data['book_id'], book_data['title'], book_data['author'],
                         book_data['copies_sold'], book_data['download_link'], book_data['publish_date'])
        else:
            return Book(book_data['book_id'], book_data['title'], book_data['author'], book_data['copies_sold'])
    except Exception as e:
        return str(e)
# __code ends here__


