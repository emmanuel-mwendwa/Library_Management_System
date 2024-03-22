# Library Management System

<hr>

# View it live 

www.library.emmanuel-mwendwa.xyz

- For test cases you can use the username *"john@gmail.com"* and the password *"asdf"*

<hr>

The Library Management System (LMS) is designed to be used by library staff, specifically the Librarian. Upon logging in to the system, the Librarian is presented with a dashboard containing various options to manage the library's operations efficiently.
It is built using Flask, HTML and CSS

The librarian can:
<li>create, read, update and delete books</li>
<li>create, read, update and delete members</li>
<li>Issue books and process book returns</li>

<hr>

<h3>To run this system</h3>
<h4>git clone https://github.com/emmanuel-mwendwa/Library_Management_System.git</h4>

<h4>pip install -r requirements.txt</h4>

<h4>flask --app main db upgrade</h4>

<h4>flask --app main run</h4>

<hr>

## Dashboard Options:

- **List Books**: View a list of all available books, including details such as title, author, publication date, ISBN, available copies, and total copies. This option also provides functionalities to update or delete specific books from the database.

- **Add Book**: Add a new book to the system records, providing details such as title, author, publication date, ISBN (International Standard Book Number), and total copies. Note that ISBN is unique for each book.

- **List Members**: View a list of all members, including details such as first name, last name, email, and registration date (date the person became a member). This option also allows updating or deleting specific members from the database.

- **Add Member**: Add a new member to the system records, providing details such as first name, last name, and email. The registration date is automatically generated using real-time data from the system.

- **View Transactions**: View all transactions, including details such as the member who borrowed the book (names), book title, issue date, return date, rent fee (accrued cost due to overdue borrowing time), expected return date, and status (borrowed or returned).

- **Issue Book**: Record a member who borrowed a book by capturing the member ID and the book ID, along with the date borrowed.

- **Return Book**: Confirm that a member returned a book they had borrowed, ensuring it is returned against the expected return date and confirming any rental fees accrued due to overdue borrowing time.

## Usage Instructions:

1. **Login**: Log in to the system using your credentials as the Librarian.

   - For test cases you can use the username *"john@gmail.com"* and the password *"asdf"*

3. **Navigate Dashboard**: Once logged in, you'll see the dashboard with various options listed above.

4. **Perform Actions**: Select the desired option from the dashboard to perform specific actions such as listing books, adding members, issuing books, etc.

5. **Manage Transactions**: Use the "View Transactions" option to monitor all transactions, including book borrowings and returns.

6. **Update or Delete Records**: Utilize the functionalities available in the "List Books" and "List Members" options to update or delete specific records from the database as needed.

## Conclusion:

The Library Management System streamlines library operations, providing efficient management of books, members, and transactions. With its user-friendly interface and comprehensive features, the LMS ensures smooth functioning of the library, making it an indispensable tool for librarians.


This is what the system looks like
<h2>Dashboard</h2>

![Dashoard](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/9cfd86c6-2865-4728-8511-d79c926f570d)

<h2>View Books</h2>

![View_Books](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/2812f307-9668-4ef7-b722-dc3545c4d3e4)
![View_Books(1)](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/bf99ecec-a26c-4b4d-9b0f-12f9d7b9593b)

<h2>Add Book</h2>

![Add_Book](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/8be7671b-62d7-48fa-8921-353ce016e2f6)

<h2>View Members</h2>

![View_Members](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/695d46ab-ac04-4459-a524-0acc54c719de)

<h2>Add Member</h2>

![Add_Member](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/0600d2ef-d607-4ed5-b011-b039672aaeb8)

<h2>View Transactions</h2>

![View_Transactions](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/3f6fe087-2b35-4412-82d2-f2e39f39cd6e)

<h2>Issue Book</h2>

![Issue_Book](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/aba5055f-a86b-4ab6-97ae-7ea85279066c)

<h2>Return Book</h2>

![Return_Book](https://github.com/emmanuel-mwendwa/Library_Management_System/assets/82759762/285c7aa7-63bd-4288-8edd-690cd31a7124)


