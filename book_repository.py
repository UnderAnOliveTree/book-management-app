'''Pseydocode

Create a book repository database <ebookstore> to list books in the repository in a table <book>.
The table <book> has four columns; book id, book tilte, book author, available book quantity.
Populate the table with the available values from th provided data.

Create a book repository management application that gives the user the ability to 
1. add new books to the database <ebookstore>
2. update book information for a book available in the database <ebookstore>; the information that can be updated is the
    -book tile
    -book author
    -quantity,
3. delete books from the database <ebookstore>,
4. search the database <ebookstore> to find a specific book.

When the user enters the program, asks user to choose one option from a menu with five options; 1-4 as above and 5 to exit the program.
1. Enter book; to enter a new book in the database <ebookstore>.
    When the user wants to enter a book, 
    - it checks if the book is alreaady in the table
        - if the book is already in the database, the user receives information about the book, 
        and is asked if there is another book to enter, 
        - if the book is not in the database, 
            - the id of the book is automatically updated to the next larger integer, 
            - the user is asked to input  
             the book title, the author, and the book quantity available. 
             - The book quantity is a positive integer.
    The entry is added in the database.

2. Update book; to update information about a book. 
The user is asked about the book they want to update.
The book entry is brought up. 
The user is asked about what information they want to update.
The user updates the book information.
The entry is updated in the database.

3. Delete book; to delete a book from the database. 
The user is asked about the book they want to delete.
They are presented with information about the book.
They are asked to confirm whether they want to delete the book.
Upon confirmation the book entry is deleted. 

4. Search books; to search for books in the database.
The user can search for a book using the title or author
The user can search for books with low availability (ten) and
for books in zero quantity.

5. Exit the program; to exit the program.

Additional reading:
https://pynative.com/python-sqlite/ 
https://stackoverflow.com/questions/52815376/how-to-fetch-data-from-sqlite-using-python 
https://stackoverflow.com/questions/13225461/how-to-add-a-positive-integer-constraint-to-a-integer-column-in-mysql 
https://stackoverflow.com/questions/27758564/python-how-to-check-if-an-entry-already-exists-in-a-sql-database 
https://stackoverflow.com/questions/49499577/sqlite3-python-input-to-table-trouble-with-auto-increment
 '''


# Imports the SQLite3 module to create and manipulate databases
import sqlite3

# Creates, opens and closes database <ebookstore>
with sqlite3.connect('ebookstore.db') as db:
    # Gets a cursor object to allow changes to the database <ebookstore>
    cursor = db.cursor()

    # Creates table <book> in the database <ebookstore> if the table does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            qty INTEGER
            )
        ''')
    # Allows handling of cursor
    cursor.execute('SELECT * FROM book')
# Checkpoint for code up to this point
print("Database table created.")
# Saves changes to the database <ebookstore>
db.commit()

# Lists the books to be entered in the database
book_details = [
    (3001, 'A tale of Two Cities', 'Charles Dickens', 30),
    (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 0),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
]

for book in book_details:
    book_id, book_title, book_author, book_quantity = book

    # Check if a book with the same title already exists
    cursor.execute('SELECT id FROM book WHERE title = ?', (book_title,))
    existing_book_id = cursor.fetchone()

    if existing_book_id:
        # A book with the same title already exists, you can choose to skip or update.
        print(f"Book '{book_title}' already exists with ID {existing_book_id[0]}. Skipping insertion.")
    else:
        # Insert the book into the table
        cursor.execute(
            'INSERT INTO book(id, title, author, qty) VALUES (?, ?, ?, ?)',
            (book_id, book_title, book_author, book_quantity)
        )

# Save changes to the database
db.commit()


# Populates the table <book> with entries from 3001 to 3005
try:
    cursor.executemany('''INSERT INTO book(id, title, author, qty) 
                       VALUES(?, ?, ?, ?)''', book_details)
    db.commit()  # Save changes to the database
    # Checkpoint for code up to this point
    print("Books id 3001 to id 3005 inserted in the table.")

# Handles exception errors
except sqlite3.IntegrityError:
    print("Error: An entry with the same ID already exists in the table.")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
# Saves changes to the database <ebookstore>
db.commit()

# Defines function <enter_book> for user option 1 to add a new book in the database
# when the user wants to add a new book in the database, the function
# checks that the book is not already in the database
def enter_book():
    print("\nTo enter a new book entry you need the:"
        "\n- Book title"
        "\n- Name of the book author, and"
        "\n- The quantity of books in stock.\n")
    
    # While loop to get the details of the new book
    # takes parameters id, title, author, qty (quantity)
    # repeats until the user enters valid book details
    while True:
        # Asks the user to enter the new book title
        new_book_title = input("Enter the title of the new book: ").title()
        
        # Tests the length of title entered, which needs to be greater than zero    
        if len(new_book_title) == 0: 
            print("\nYou have not entered a valid book title.\n")
            continue

        # Checks if the new book title is already in the database
        if new_book_title.casefold():
            cursor.execute('SELECT * FROM book WHERE title=?', (new_book_title,))
            existing_book = cursor.fetchone()

            if existing_book:
                print("This book already exists in the database. Book ID: " + str(existing_book[0]) +
                     "\nTitle: " + existing_book[1] +
                     "\nAuthor: " + existing_book[2] +
                     "\nQuantity in stock: " + str(existing_book[3])
                      )
                continue    
                
        else:
            # Checkpoint of code until now
            print("The database has been searched."
               "\nThe book does not exist in the repository. Answer the questions to add it.")
            continue
            
        # Asks the user to enter the name of the author of the new book
        new_book_author = input("Enter the name of the author of the new book: ").title()
        # Checks that the length of the entry is valid (not zero in lenght)
        if len(new_book_author) == 0: 
            # If the user has not entered anything (lenght of entry equals zero)
            print("\nYou have not entered a valid author name.\n")
            # Continues until the user enters a valid input
            continue
        # if the author entry is correct, asks the user for the quantity of the books in stock
        #else:
        try:
            new_book_quantity = int(input("Enter the quantity of these new books that are in stock: "))
            # Checks that the quanity entered is a positive integer and hence valid
            # If the quantity entered is a negative integer or zero, the user receives an error message
            if new_book_quantity <= 0:
                print("You have not entered a valid quantity number. Quantity must be a number larger than zero.")
                # Loops until the user enters a valid quantity number (positive integer)
                continue
        except ValueError:
            print("You have not entered a valid number.")
            continue
        # If the user enters a valid integer, the data about the new book are entered in the database
        #else:
        # Retrieves the ID of the last book that was entered in the database <ebookstore>
        #cursor.execute('SELECT MAX(id) FROM book')                
        #last_id = cursor.fetchone()[0]
        # Sets the starting and incremental values (plus one) for the assignment of ID to each book entered
        #if last_id is None:
        #    last_id = 0
         #   next_new_id = last_id + 1        
        # Enters the new book information in the databsase
        cursor.execute('''INSERT INTO book(title, author, qty) VALUES(?, ?, ?)''',
                      (new_book_title, new_book_author, new_book_quantity)
                       )
        # Saves changes to the database <ebookstore>
        db.commit()

        # Prints information for the user - also checkpoint for the code
        print("You have successfully added the book to the repository.")
        break

# Defines function <update_book> for user option 2 to update the information of an existing book in the database
# Prints a list of all books in the database, with id, title, author, qty
# Asks user which book they want to update
# Checks that the book is in the database, and prints parameters id, title, author, qty  
# Asks user which book information they want to update, title, author, qty
def update_book():
    # Retrieves data from the database <ebookstore>
    cursor.execute('''SELECT id, title, author, qty FROM book''')
    rows = cursor.fetchall()

    if not rows:
        print("The repository does not contain any books.")
        return
    
    # Prints the list of the books in database and the information about each book
    print("BOOKS IN REPOSITORY:")
    for row in rows:
        print("ID: {}, Book Title: {}, Book Author: {}, Quantity in Stock: {}". format(row[0], row[1], row[2], row[3]))

    # Asks the user which book they want to update
    book_to_update = input("Enter the id of the book you want to update: ")

    # Looks in the database <ebookstore> for the book that needs to be updated
    cursor.execute('SELECT * FROM book WHERE id=?', (book_to_update,))
    # Retrieves the book from the database <ebookstore>
    book = cursor.fetchone()
    
    # If the book id does not exist, returns an error message
    if not book:
        print("There are no books with this ID in the repository.")
        return
    # If the book id the user entered is correct (in the database)
    elif book:
        # Prints the available information about the book, ID, title, author, available quantity
        print("\nCurrent Book Details:")
        print("Book title:", book[1])
        print("Book author:", book[2])
        print("Quantity in stock:", book[3])
                
    # Asks the user to enter the updated new title of the book
    updated_title = input("Enter the new title or key ENTER if the title is the same: ").title()
    # Asks the user to enter the updated new author name of the book
    updated_author = input("Enter the new author name or key ENTER if the author's details are correct: ").title()
    # Asks the user to enter the updated new quantity available for the book
    updated_quantity = input("Enter new quantity or press ENTER if the quantity in stock is unchanged: ")

    # If none of the information was updated, the user receives a message
    if not updated_title and not updated_author and not updated_quantity:
        print("You have not made any changes.")
        return
    
    # Updates the book title of an existing book
    if updated_title:
        cursor.execute('UPDATE book SET title=? WHERE id=?', (updated_title, book_to_update))
    # Updates the book author name of an existing book
    if updated_author:
        cursor.execute('UPDATE book SET author=? WHERE id=?', (updated_author, book_to_update))
    # Updates the available book quanity of an existing book
    if updated_quantity:
        if updated_quantity.isdigit():
            updated_quantity = int(updated_quantity)
            if updated_quantity >= 0:
                cursor.execute('UPDATE book SET qty=? WHERE id=?', (updated_quantity, book_to_update))
            else:
                print("You have not entered a valid quantity. Book quantity should be zero or larger.")
                return
            
        # Saves changes to the database <ebookstore>
        db.commit()
        print("You have finished updating this book information.")

    # If the book id the user entered is not in the database
    # Prints an error message for the user
    else:
        print("The book was not found in the repository.")
    

# Defines function <delete_book> for user option 3 to delete an existing book from the database
# Prints a list of all books in the database, with id, title, author, qty
# Asks user which book they want to delete
# Checks that the book is in the database, and prints parameters id, title, author, qty  
def delete_book():
     # Retrieves data from the database <ebookstore>
    cursor.execute('''SELECT id, title, author, qty FROM book''')
    rows = cursor.fetchall()

    if not rows:
        print("The repository does not contain any books.")
        return
    
    # Prints the list of the books in database and the information about each book
    print("BOOKS IN REPOSITORY:")
    for row in rows:
        print("ID: {}, Book Title: {}, Book Author: {}, Quantity in Stock: {}". format(row[0], row[1], row[2], row[3]))
    
    # Asks the user which book they want to delete
    book_to_delete = input("\nEnter the id of the book you want to delete."
                           "\nATTENTION: This action is irreversible."
                           "\nIf you want to undo the action, you need to re-enter the book as a new entry: ")
    # Looks in the database <ebookstore> for the book that needs to be deleted
    cursor.execute('SELECT * FROM book WHERE id=?', (book_to_delete,))
    # Retrieves the book from the database <ebookstore>
    book = cursor.fetchone()
   
    # If the book id does not exist, returns an error message
    if not book:
        print("There are no books with this ID in the repository.")
        return
    # If the book id the user entered is correct (in the database)
    elif book:
        # Prints the available information about the book, ID, title, author, available quantity
        print("\nCurrent Book Details:")
        print("\nCurrent Book Details:")
        print("Book title:", book[1])
        print("Book author:", book[2])
        print("Quantity in stock:", book[3])
            
    # Asks the user to verify they want to delete the book
    confirm_delete = input("Are you sure you want to delete this book?"
                        "\n Enter Y for yes or N for no (your entry is case-sensitive)? "
                            )
    if confirm_delete.casefold() == "y":
        # Deletes information about the book with the id the user entered
        cursor.execute('''DELETE FROM book WHERE id = ? ''', (book_to_delete,))
        # Saves changes to the database <ebookstore>
        db.commit()
        print("You have deleted the book from the repository.")
    
    # If user enters <n> if they do not want to proceed with the deletion
    elif confirm_delete.casefold() == "n": 
        print("The book was not deleted from the repository.")

    # Saves changes to the database <ebookstore>
        db.commit()
        
    else:
        print("You have not entered a valid choice.")

    
# Defines function <search_book> for user option 4 to search for an existing book in the database
# Asks user if they want to look by title, author, quantity in stock or out-of-stock books
# Checks that the book is in the database, and prints parameters id, title, author, qty  
def search_books():
    search_book_by = input("Do you want to look by book title, author name or book quantity in stock?" 
                        "\nEnter 'BT' to look with the book title, or"
                        "\nEnter 'BA' to look with author name, or "
                        "\nEnter 'LS' to look for books that are low in stock (less than 5), or"
                        "\nEnter 'OFS'to look for books that are out of stock."
                        "\nYour choice: "
                        ).casefold()
    
    # If the user wants to look for a book/books using the title
    if search_book_by == "bt":
        book_title = input("What is the title of the book you are looking for? ").casefold()
        # Checks that the book title entered is valid (has at least one character)
        if len(book_title) > 0:
            cursor.execute('SELECT * FROM book WHERE title LIKE ?', ('%' + book_title + '%',))
            searched_books = cursor.fetchall()
        if not searched_books:
            print("There are no books with this title in the repository.")

    # Else, if the user wants to look for a book/books using the author's name
    elif search_book_by == "ba":
        book_author_name = input("Enter the book author's name to search: ").casefold()
        if len(book_author_name) >0:
            cursor.execute('SELECT * FROM book WHERE author LIKE ?', ('%' + book_author_name + '%',))
            searched_books = cursor.fetchall()
        if not searched_books:
            print("There are no books by this author in the repository.")
            return
    # Else, if the user wants to look for a book/books using low quantity in stock
    elif search_book_by == "ls":
        cursor.execute('SELECT * FROM book WHERE qty < 5')
        searched_books = cursor.fetchall()
        if not searched_books:
            print("All books in the repository are in stock (at least five units).")
            return
    # Else, if the user wants to look for a book/books that are out of stock
    elif search_book_by == "ofs":
        cursor.execute('SELECT * FROM book WHERE qty = 0')
        searched_books = cursor.fetchall()
        if not searched_books:
            print("There are no out of stock books.")
            return
    # Else in case the user does not enter a valid option
    else:
        print("This option does not exist.")
        return

    if searched_books:
        print("Your repository search generated the following results: ")
        for book in searched_books:
            print("Book ID:", book[0])
            print("Book title:", book[1])
            print("Book author name:", book[2])
            print("Book quantity in stock:", book[3])
    else:
        print("There are no books with your search criteria.")



# Defines function <user_action> 
# Calling <user_action> displays the menu with the available options when the user opens the program
# The function <user_action> takes one parameters <user_choice>
def user_action():  
    # Option 5. Exit was chosen oven 0. exit in case users confuse 0 with O
    while True:    
        user_choice = input("\nChoose one of the following options:"
                            "\n\t 1. Enter a new book in the repository"
                            "\n\t 2. Update the information of a book in the repository"
                            "\n\t 3. Delete a book from the repository"
                            "\n\t 4. Search for a book in repository"
                            "\n\t 5. Exit the program."
                            "\nWhat do you want to do? "
                            )
        # if-elif statement to provide the actions for each of the user's choices
        # If the user choses <1. Enter a new book in the repository>        
        if user_choice == "1":
            # Calls the <enter_book> function
            enter_book()
            
        # If the user choses <2. Update the information of a book in the repository>
        elif user_choice == "2":
            # Calls the <update_book> function
            update_book()
            
        # If the user chooses <3. Delete a book from the repository>
        elif user_choice == "3":
            # Calls the <add_task_to_user> function
            # The user will be able to add a new task to an existing user
            delete_book()

        # If the user chooses <4. Search for a book in repository>
        elif user_choice == "4":
            # Calls the <search_book> function
            search_books()
        
        # If the user chooses <5. Exit the program.>
        elif user_choice == "5":
            print("You are exiting the application")
            exit()
        # If the user does not enter a valid choice
        else:
            print("\nYou have not entered a valid choice. Please, try again.\n")
            continue


# Calls function <user_action> as the main function
if __name__ == "__main__":
    user_action() 