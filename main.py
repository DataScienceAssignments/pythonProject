import logging
import time  # Added to calculate execution time

# Configure logging for debugging output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Node class representing each book in the library
class BookNode:
    def __init__(self, bookId, title, author, isbn):
        self.bookId = bookId  # Unique identifier for the book
        self.title = title  # Title of the book
        self.author = author  # Author of the book
        self.isbn = isbn  # ISBN of the book
        self.available = True  # Boolean to check if the book is available
        self.borrowed_count = 0  # Tracks how many times the book has been borrowed
        self.left = None  # Left child in the BST
        self.right = None  # Right child in the BST


# Node class representing each patron in the library
class PatronNode:
    def __init__(self, patronId, name):
        self.patronId = patronId  # Unique identifier for the patron
        self.name = name  # Name of the patron
        self.borrowedBooks = []  # List of book IDs borrowed by the patron
        self.left = None  # Left child in the BST
        self.right = None  # Right child in the BST


# Main class to implement the Library Management System
class LibraryManagementSystem:
    def __init__(self):
        self.books_root = None  # Root node for the books BST
        self.patrons_root = None  # Root node for the patrons BST

    # Helper function to insert a book into the BST
    def _addBookRec(self, node, bookId, title, author, isbn):
        logging.debug(f"Inserting book with ID {bookId}")
        if node is None:  # If position is found, create a new BookNode
            return BookNode(bookId, title, author, isbn)
        if bookId < node.bookId:  # Traverse to the left subtree if bookId is smaller
            node.left = self._addBookRec(node.left, bookId, title, author, isbn)
        elif bookId > node.bookId:  # Traverse to the right subtree if bookId is larger
            node.right = self._addBookRec(node.right, bookId, title, author, isbn)
        else:  # If book already exists, update its details
            logging.info(f"Updating book with ID {bookId}")
            node.title = title
            node.author = author
            node.isbn = isbn
        return node

    # Public method to add a book to the system
    def addBook(self, bookId, title, author, isbn):
        logging.info(f"Adding book: {bookId}, {title}, {author}, {isbn}")
        self.books_root = self._addBookRec(self.books_root, bookId, title, author, isbn)
        return f'Added Book: {bookId} - "{title}" by {author}, ISBN: {isbn}'

    # Helper function to remove a book from the BST
    def _removeBookRec(self, node, bookId):
        logging.debug(f"Attempting to remove book with ID {bookId}")
        if node is None:  # If the node is not found
            return None, None

        if bookId < node.bookId:  # Traverse the left subtree
            node.left, deleted = self._removeBookRec(node.left, bookId)
        elif bookId > node.bookId:  # Traverse the right subtree
            node.right, deleted = self._removeBookRec(node.right, bookId)
        else:  # Node to be deleted is found
            if not node.available:  # Check if the book is borrowed
                logging.warning(f"Cannot remove borrowed book with ID {bookId}")
                return node, None  # Cannot delete a borrowed book
            deleted = node  # Mark the node for deletion
            if node.left is None:  # If no left child, replace with the right child
                return node.right, deleted
            elif node.right is None:  # If no right child, replace with the left child
                return node.left, deleted
            # Node with two children: Get the inorder successor
            successor = self._minValueNode(node.right)
            node.bookId, node.title, node.author, node.isbn, node.available = (
                successor.bookId, successor.title, successor.author, successor.isbn, successor.available
            )
            node.right, _ = self._removeBookRec(node.right, successor.bookId)
        return node, deleted

    # Helper function to find the node with the minimum value in a subtree
    def _minValueNode(self, node):
        logging.debug("Finding minimum value node")
        current = node
        while current.left is not None:  # Keep traversing to the leftmost node
            current = current.left
        return current

    # Public method to remove a book from the system
    def removeBook(self, bookId):
        logging.info(f"Removing book with ID {bookId}")
        self.books_root, deleted = self._removeBookRec(self.books_root, bookId)
        if deleted:
            logging.info(f"Book with ID {bookId} removed")
            return f'Removed Book: {bookId} - "{deleted.title}" by {deleted.author}'
        return f'Book ID {bookId} not found or is currently borrowed.'

    # Helper function to search for a book by ID
    def _searchBook(self, node, bookId):
        logging.debug(f"Searching for book with ID {bookId}")
        if node is None or node.bookId == bookId:  # Base case: Node is found or does not exist
            return node
        if bookId < node.bookId:  # Traverse to the left subtree
            return self._searchBook(node.left, bookId)
        return self._searchBook(node.right, bookId)  # Traverse to the right subtree

    # Public method to search for a book by ID
    def searchBook(self, bookId):
        logging.info(f"Searching book with ID {bookId}")
        book = self._searchBook(self.books_root, bookId)
        if book:
            availability = "Yes" if book.available else "No"
            return f'''Book Details for ID {bookId}:
            - "{book.title}" by {book.author}, ISBN: {book.isbn}, Available: {availability}'''
        return f'Book ID {bookId} not found.'

    # Helper function to add a patron into the BST
    def _addPatronRec(self, node, patronId, name):
        logging.debug(f"Inserting patron with ID {patronId}")
        if node is None:  # If position is found, create a new PatronNode
            return PatronNode(patronId, name)
        if patronId < node.patronId:  # Traverse to the left subtree
            node.left = self._addPatronRec(node.left, patronId, name)
        elif patronId > node.patronId:  # Traverse to the right subtree
            node.right = self._addPatronRec(node.right, patronId, name)
        return node

    # Public method to add a patron to the system
    def addPatron(self, patronId, name):
        logging.info(f"Adding patron: {patronId}, {name}")
        self.patrons_root = self._addPatronRec(self.patrons_root, patronId, name)
        return f'Added Patron: {patronId} - {name}'

    # Method for a patron to borrow a book
    def borrowBook(self, bookId, patronId):
        logging.info(f"Borrowing book with ID {bookId} for patron {patronId}")
        book = self._searchBook(self.books_root, bookId)  # Find the book
        patron = self._searchPatron(self.patrons_root, patronId)  # Find the patron
        if not book:
            return f'Book ID {bookId} not found.'
        if not patron:
            return f'Patron ID {patronId} not found.'
        if not book.available:  # Check if the book is already borrowed
            logging.warning(f"Book ID {bookId} is already borrowed")
            return f'Book ID {bookId} is already borrowed.'
        # Update book and patron details
        book.available = False
        book.borrowed_count += 1
        patron.borrowedBooks.append(bookId)
        return f'Patron {patronId} borrowed "{book.title}" (Book ID: {bookId})'

    # Method for a patron to return a book
    def returnBook(self, bookId, patronId):
        logging.info(f"Returning book with ID {bookId} for patron {patronId}")
        book = self._searchBook(self.books_root, bookId)  # Find the book
        patron = self._searchPatron(self.patrons_root, patronId)  # Find the patron
        if not book:
            return f'Book ID {bookId} not found.'
        if not patron:
            return f'Patron ID {patronId} not found.'
        if bookId not in patron.borrowedBooks:  # Check if the patron has borrowed the book
            logging.warning(f"Book ID {bookId} not borrowed by patron {patronId}")
            return f'Patron {patronId} did not borrow Book ID {bookId}.'
        # Update book and patron details
        book.available = True
        patron.borrowedBooks.remove(bookId)
        return f'Patron {patronId} returned "{book.title}" (Book ID: {bookId})'

    # Recursive helper to list available books in order
    def _listAvailableBooksRec(self, node, result):
        if node:
            self._listAvailableBooksRec(node.left, result)
            if node.available:  # Check if the book is available
                result.append(f'- Book ID {node.bookId}: "{node.title}" by {node.author}')
            self._listAvailableBooksRec(node.right, result)

    # Public method to list all available books
    def listAvailableBooks(self):
        logging.info("Listing available books")
        result = []
        self._listAvailableBooksRec(self.books_root, result)
        return "Available Books:\n" + "\n".join(result)

    # Recursive helper to list books by a specific author
    def _listBooksByAuthorRec(self, node, authorName, result):
        if node:
            self._listBooksByAuthorRec(node.left, authorName, result)
            if node.author == authorName:  # Check if the author matches
                result.append(f'- Book ID {node.bookId}: "{node.title}" by {node.author}')
            self._listBooksByAuthorRec(node.right, authorName, result)

    # Public method to list books by a specific author
    def listBooksByAuthor(self, authorName):
        logging.info(f"Listing books by author {authorName}")
        result = []
        self._listBooksByAuthorRec(self.books_root, authorName, result)
        return f'Books by Author "{authorName}":\n' + "\n".join(
            result) if result else f'No books found by Author "{authorName}".'

    # Helper function to search for a patron by ID
    def _searchPatron(self, node, patronId):
        logging.debug(f"Searching for patron with ID {patronId}")
        if node is None or node.patronId == patronId:  # Base case: Node is found or does not exist
            return node
        if patronId < node.patronId:  # Traverse to the left subtree
            return self._searchPatron(node.left, patronId)
        return self._searchPatron(node.right, patronId)  # Traverse to the right subtree

    # Public method to list all books borrowed by a patron
    def listPatronsBooks(self, patronId):
        logging.info(f"Listing books borrowed by patron {patronId}")
        patron = self._searchPatron(self.patrons_root, patronId)
        if not patron:
            return f'Patron ID {patronId} not found.'
        if not patron.borrowedBooks:  # Check if the patron has borrowed books
            return f'Patron {patronId} has not borrowed any books.'
        # Retrieve book titles for borrowed books
        result = [f'- "{self._searchBook(self.books_root, bookId).title}" (Book ID: {bookId})'
                  for bookId in patron.borrowedBooks]
        return f'Patron {patronId} borrowed the following books:\n' + "\n".join(result)

    # Method to process commands from an input file and write results to an output file
    def processInputFile(self, input_file, output_file):
        start_time = time.time()  # Record the start time
        logging.info(f"Processing input file {input_file}")
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                parts = line.strip().split(': ')
                command = parts[0]  # Extract command name
                args = parts[1] if len(parts) > 1 else ''  # Extract arguments if present

                if command == 'addBook':
                    bookId, title, author, isbn = args.split(', ')
                    bookId = int(bookId)
                    title = title.strip('"')
                    author = author.strip('"')
                    isbn = isbn.strip('"')
                    result = self.addBook(bookId, title, author, isbn)

                elif command == 'addPatron':  # Add patron to the system
                    patronId, name = args.split(', ')
                    patronId = int(patronId)
                    name = name.strip('"')
                    result = self.addPatron(patronId, name)

                elif command == 'borrowBook':
                    bookId, patronId = map(int, args.split(', '))
                    result = self.borrowBook(bookId, patronId)

                elif command == 'returnBook':
                    bookId, patronId = map(int, args.split(', '))
                    result = self.returnBook(bookId, patronId)

                elif command == 'checkBook':
                    bookId = int(args)
                    result = self.searchBook(bookId)

                elif command == 'listAvailableBooks':
                    result = self.listAvailableBooks()

                elif command == 'listBooksByAuthor':
                    authorName = args.strip('"')
                    result = self.listBooksByAuthor(authorName)

                elif command == 'listPatronsBooks':
                    patronId = int(args)
                    result = self.listPatronsBooks(patronId)

                elif command == 'removeBook':
                    bookId = int(args)
                    result = self.removeBook(bookId)

                else:  # Handle unknown commands
                    logging.error(f"Unknown command: {command}")
                    result = f'Unknown command: {command}'

                logging.debug(f"Command result: {result}")
                outfile.write(result + '\n')
        end_time = time.time()  # Record the end time
        elapsed_time_ms = (end_time - start_time)  # Calculate time in milliseconds
        logging.info(f"Processing completed. Total time taken: {elapsed_time_ms:.2f} ms")


lms = LibraryManagementSystem()
lms.processInputFile('./inputs_outputs/inputPS04.txt', './inputs_outputs/outputPS04.txt')