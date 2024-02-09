"""
All variables and function naming is done using snake case.
The purpose of this program is to create a menu-driven program to be used as a very simple library system.
"""


# Start function containing inner functions and this function is the first thing called at the start of the program
def start():
    # Default books available provided by assignment [ISBN, Title, Author, Edition, Borrowers]
    all_books = [
        ['9780596007126', "The Earth Inside Out", "Mike B", 2, ['Ali']],
        ['9780134494166', "The Human Body", "Dave R", 1, []],
        ['9780321125217', "Human on Earth", "Jordan P", 1, ['David', 'b1', 'user123']]
    ]

    # Initialize empty array of ISBNs/Books that are already borrowed
    borrowed_isbns = []

    # Function to print a menu for the user
    def print_menu():
        print('\n######################')
        print('1: (A)dd a new book.')
        print('2: Bo(r)row books.')
        print('3: Re(t)urn a book.')
        print('4: (L)ist all books.')
        print('5: E(x)it.')
        print('######################\n')

        # Depending on what the user inputs it will run through conditional if statements and run the correct function
        user_input = input("Your selection: ")

        if user_input in ["1", "A", "a"]:
            add_new_book()
        elif user_input in ["2", "R", "r"]:
            borrow_book()
        elif user_input in ["3", "T", "t"]:
            return_book()
        elif user_input in ["4", "L", "l"]:
            list_all_books()
        elif user_input in ["5", "X", "x"]:
            list_all_books(True)
        else:
            print("Wrong selection! Please selection a valid option.")
            print_menu()

    # List all books function
    def list_all_books(is_exit=False):
        if is_exit:
            print("$$$$$$$$ FINAL LIST OF BOOKS $$$$$$$$")
        # Loop through each book in the 'all_books' list
        for book in all_books:
            print("---------------")
            if book[0] in borrowed_isbns:
                # If the ISBN is in the 'borrowed_isbns' list, mark the book as unavailable
                print("[Unavailable]")
            else:
                # If the ISBN is not in the 'borrowed_isbns' list, mark the book as available
                print("[Available]")
            print(f"{book[1]} - {book[2]}")
            print(f"E: {book[3]} ISBN: {book[0]}")
            print("borrowed By:", book[4])
        if not is_exit:
            print_menu()

    def add_new_book():
        # Input the book name and making sure string is not empty or contains '%' or '*'
        book_name = input("Book Name: ")
        while book_name == "" or "%" in book_name or "*" in book_name:
            print("Invalid book name!")
            book_name = input("Enter the book name: ")

        # Get the author name
        author = input("Author: ")

        # Input the edition number and make sure it's an integer
        while True:
            try:
                # Get edition number and convert to int
                edition = int(input("Edition: "))
                break
            except ValueError:
                print("Invalid edition number. Please try again.")

        # Input and check the ISBN of the book (must be 13 characters long)
        while True:
            try:
                # Doing replace here incase extra spaces are present (doing the test cases in the pdf some of the ISBNs had extra spaces in the end)
                isbn = input("ISBN: ").replace(" ", "")
                if len(isbn) != 13:
                    # Rasing ValueError if length of isbn is not 13
                    raise ValueError
                break
            except ValueError:
                print("Invalid ISBN!")

        # Weight factors used for ISBN verification
        weight_factors = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1]
        # "Initialize 'total' to 0 for ISBN checksum calculation."
        total = 0

        # Calculate the ISBN checksum using weight factors
        for i in range(13):
            total += int(isbn[i]) * weight_factors[i]

        # Check if the ISBN is valid (total is divisible by 10)
        if total % 10 == 0:
            # Create a new book with all of the information we have got from the user
            new_book = [isbn, book_name, author, edition, []]

            # Check if the ISBN is already in use before adding the new book
            for book in all_books:
                if book[0] == isbn:
                    print("Duplicate ISBN is found! Cannot add the book.")
                    return print_menu()

            # If ISBN is not in use, add the new book to the 'all_books' list
            all_books.append(new_book)
            print("A new book is added successfully.")

        else:
            print("Invalid ISBN!")
        return print_menu()

    def borrow_book():
        # Get input from user
        borrower = input("Borrowed By: ")

        # Input the search keyword for the book (case-insensitive so we use .lower())
        search = input("Which book are you searching for? ").lower()

        # Initialize a list to store matching books
        matching_books = []

        # Check if the search keyword ends with '*'
        if search[-1] == '*':
            # Iterate through all books and find books with names containing the search keyword (excluding the '*')
            for book in all_books:
                book_name = book[1].lower()
                if search[:-1] in book_name:
                    matching_books.append(book)

        # Check if the search keyword ends with '%'
        elif search[-1] == '%':
            # Iterate through all books and find books with names starting with the search keyword (excluding the '%')
            for book in all_books:
                book_name = book[1].lower()
                if book_name.startswith(search[:-1]):
                    matching_books.append(book)

        else:
            # Exact match search - Iterate through all books and find books with names matching the search keyword
            for book in all_books:
                book_name = book[1].lower()
                if book_name == search:
                    matching_books.append(book)

        # Init variable saying that no books are found
        book_found = False
        # Check if any matching books were found
        if matching_books:
            # Iterate through the matching books
            for book in matching_books:
                if book[0] not in borrowed_isbns:
                    # If the book is not already borrowed, mark it as borrowed
                    borrowed_isbns.append(book[0])
                    book[4].append(borrower)
                    print(f"-\"{book[1]}\" is borrowed!")
                    book_found = True
        if not book_found or not matching_books:
            print("No books found!")

        # Return to the main menu
        return print_menu()

    # Return book function
    def return_book():
        # Get ISBN from user as a string
        isbn = input("ISBN: ")
        # Check if the ISBN is in the list of borrowed ISBNs and if its found remove it
        if isbn in borrowed_isbns:
            borrowed_isbns.remove(isbn)
            for book in all_books:
                if book[0] == isbn:
                    print(f"\"{book[1]}\" is returned.")
        else:
            print("No book is found!")

        # Return to the main menu
        return print_menu()

    # Printing menu (for the first time)
    print_menu()


# Calling start function
start()
