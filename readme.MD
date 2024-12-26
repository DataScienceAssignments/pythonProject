**_Design Document for Library Management System**_

_**_A. The Data Structure Model Chosen with Justifications**__

**Data Structure:** Binary Search Tree (BST)
Books Representation:
Each book is stored as a node in a Binary Search Tree (BST), where the key is the bookId and the attributes include:

    bookId: A unique identifier for each book (used as the key).
    title: The title of the book.
    author: The author of the book.
    isbn: The ISBN number of the book.
    available: A boolean indicating whether the book is available for borrowing.
    borrowed_count: Tracks how many times the book has been borrowed.
    left: Pointer to the left child in the BST.
    right: Pointer to the right child in the BST.

**_Justification:_**

**Efficient Search, Insertion, and Deletion:** 

    The BST allows for efficient search, insertion, and deletion operations. In an average case, these operations have a time complexity of O(log n), where n is the number of books in the system.
    Ordered Data: Since the BST maintains the order based on the bookId, it allows for efficient traversal (like listing all books in ascending order of their bookId).
    Patrons Representation:

Each patron is stored as a node in a separate BST, where the key is the patronId and the attributes include:
    
    patronId: A unique identifier for each patron (used as the key).
    name: The name of the patron.
    borrowedBooks: A list of book IDs that the patron has borrowed.
    left: Pointer to the left child in the BST.
    right: Pointer to the right child in the BST.
    
**Justification:**

Similar to the book representation, using a BST for patrons offers efficient operations for adding, searching, and deleting patrons. Searching and adding patrons are done in O(log n) time on average.

**Key Advantages:**

**Scalability:** The BST adapts well to dynamic operations like adding, removing, and searching for books and patrons.

    Memory Efficiency: Each node in the tree is dynamically allocated, minimizing memory usage by avoiding unused space.
    Structured Access: The ordered structure of the BST supports efficient operations like listing books or patrons in sorted order.

_**_B. Details of Each Operation with Time Complexity and Justifications**__

**Book Operations:**

    Add a Book: 
        Inserts a new book node into the BST or updates an existing node if a book with the same bookId already exists.
        Time Complexity: O(h), where h is the height of the BST.
        Justification: Insertion involves a recursive traversal of the BST, and the height of the tree determines the time complexity. On average, for a balanced BST, h = log n.

    Remove a Book:
        Deletes a book node, adjusting pointers to maintain the BST structure.
        Time Complexity: O(h).
        Justification: Deleting a node requires finding the node and adjusting the tree structure. Special cases arise when the node has one or two children, but the overall complexity remains dependent on the height of the tree.

    Search for a Book:
        Locates a book node using the bookId.
        Time Complexity: O(h).
        Justification: A book is found by traversing the tree based on the BST properties (i.e., left for smaller values, right for larger ones). On average, h = log n.

    List Available Books:
        Performs an in-order traversal to collect books that are available (available = True).
        Time Complexity: O(n), where n is the total number of books.
        Justification: In-order traversal visits each node once, making this operation proportional to the number of nodes in the tree.

    List Books by Author:
        Traverses all nodes to find books written by the given author.
        Time Complexity: O(n).
        Justification: Each node must be checked to see if its author matches the given author name.

**Patron Operations:**

    Add a Patron:
        Inserts a new patron node or updates an existing node.
        Time Complexity: O(h).
        Justification: Similar to book addition, patron addition involves a recursive traversal of the BST to find the correct position for insertion. On average, h = log n.

    Borrow a Book:
        Searches for the book and patron nodes, then updates the book's availability and the patron's borrowed list.
        Time Complexity: O(h) for both the book and the patron search.
        Justification: The operation combines search and update operations, making the time complexity dependent on the height of the tree for both book and patron nodes. On average, h = log n.

    Return a Book:
        Searches for the book and patron nodes, then updates the book's availability and removes the book from the patron's borrowed list.
        Time Complexity: O(h) for both the book and the patron search.
        Justification: Similar to the borrow operation, this also involves searching and updating nodes. On average, h = log n.

    List Patron’s Borrowed Books:
        Retrieves the patron node and iterates over the list of borrowed book IDs.
        Time Complexity: O(k), where k is the number of books borrowed by the patron.
        Justification: This operation involves searching for the patron node and then iterating over the patron's list of borrowed books.

_**_C. One Alternate Way of Modeling the Problem with Cost Implications**__

Alternate Model: 
    
    Hash Tables for Books and Patrons

    Description:
        Instead of using BSTs, hash tables could be used to store both books and patrons. Each hash table entry would be indexed by bookId for books and patronId for patrons. Each entry would store the respective book or patron data.

    Advantages:
        Constant Time Complexity: In the average case, hash tables allow O(1) time complexity for search, insertion, and deletion operations.
        Simplified Access: Direct access to a book or patron can be achieved without recursive tree traversal.

    Disadvantages:
        No Ordered Data: Hash tables do not maintain any inherent order, making operations like listing books or patrons in sorted order more complex and time-consuming (requiring sorting).
        Memory Overhead: Hash tables require extra memory for maintaining the hash table itself, and there may be collisions which can degrade performance if not handled properly.

    Cost Implications:
        Time: Hash tables perform well for direct access operations but are inefficient for ordered operations (e.g., listing books or patrons).
        Space: Hash tables generally have higher memory usage due to the overhead of maintaining the table structure and potential collisions, which may require additional storage.