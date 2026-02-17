import mysql.connector
from datetime import date
from colorama import init, Fore, Style

init(autoreset=True)  # For color reset on each line

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root",
    database="My_Library"
)
cursor = conn.cursor()

def banner(title):
    print(Fore.CYAN + "╔" + "═" * 56 + "╗")
    print(Fore.CYAN + f"║{title.center(56)}║")
    print(Fore.CYAN + "╚" + "═" * 56 + "╝")

def add_student():
    banner("➕ ADD STUDENT")
    sid = int(input("Enter Student ID   : "))
    name = input("Enter Student Name : ")
    cursor.execute("INSERT INTO students (student_id, student_name) VALUES (%s, %s)", (sid, name))
    conn.commit()
    print(Fore.GREEN + f"✅ Student '{name}' added successfully.")

def remove_student():
    banner("❌ REMOVE STUDENT")
    sid = int(input("Enter Student ID to remove: "))
    cursor.execute("DELETE FROM students WHERE student_id = %s", (sid,))
    conn.commit()
    print(Fore.RED + "🚫 Student removed.")

def view_students():
    banner("👨‍🎓 STUDENT RECORDS")
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    print("┌────────────┬────────────────────────┐")
    print("│ Student ID │ Student Name           │")
    print("├────────────┼────────────────────────┤")
    for sid, name in rows:
        print(f"│ {str(sid).ljust(11)} │ {name.ljust(23)} │")
    print("└───────────┴────────────────────────┘")

def add_book():
    banner("📘 ADD BOOK")
    bid = int(input("Enter Book ID     : "))
    title = input("Enter Book Title  : ")
    price = float(input("Enter Book Price  : "))
    quantity = int(input("Enter Quantity    : "))
    cursor.execute("INSERT INTO books (book_id, book_title, book_price, book_quantity) VALUES (%s, %s, %s, %s)", (bid, title, price, quantity))
    conn.commit()
    print(Fore.GREEN + f"✅ Book '{title}' added.")

def discard_book():
    banner("🗑️ DISCARD BOOK")
    bid = int(input("Enter Book ID to discard: "))
    cursor.execute("DELETE FROM books WHERE book_id = %s", (bid,))
    conn.commit()
    print(Fore.RED + "📕 Book discarded.")

def view_books():
    banner("📚 AVAILABLE BOOKS")
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    print("┌────────┬────────────────────────────┬────────┬────────┐")
    print("│ BookID │ Title                      │ Price  │ Stock  │")
    print("├────────┼────────────────────────────┼────────┼────────┤")
    for bid, title, price, qty in rows:
        print(f"│ {str(bid).ljust(6)} │ {title.ljust(26)} │ ₹{str(price).ljust(6)} │ {str(qty).ljust(6)} │")
    print("└────────┴────────────────────────────┴────────┴────────┘")

def issue_book():
    banner("📦 ISSUE BOOK")
    sid = int(input("Enter Student ID: "))
    bid = int(input("Enter Book ID   : "))
    cursor.execute("SELECT book_quantity FROM books WHERE book_id = %s", (bid,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        cursor.execute("INSERT INTO issued_books (student_id, book_id, issue_date) VALUES (%s, %s, %s)", (sid, bid, date.today()))
        cursor.execute("UPDATE books SET book_quantity = book_quantity - 1 WHERE book_id = %s", (bid,))
        conn.commit()
        print(Fore.GREEN + "✅ Book issued successfully.")
    else:
        print(Fore.RED + "❌ Book not available!")

def return_book():
    banner("📤 RETURN BOOK")
    sid = int(input("Enter Student ID: "))
    bid = int(input("Enter Book ID   : "))
    cursor.execute("UPDATE issued_books SET return_date = %s WHERE student_id = %s AND book_id = %s AND return_date IS NULL", (date.today(), sid, bid))
    cursor.execute("UPDATE books SET book_quantity = book_quantity + 1 WHERE book_id = %s", (bid,))
    conn.commit()
    print(Fore.GREEN + "📘 Book returned successfully.")

def view_issued_books():
    banner("📝 ISSUED BOOKS")
    cursor.execute("""
        SELECT ib.issue_id, s.student_name, b.book_title, ib.issue_date, ib.return_date
        FROM issued_books ib
        JOIN students s ON ib.student_id = s.student_id
        JOIN books b ON ib.book_id = b.book_id
    """)
    rows = cursor.fetchall()
    print("┌────┬────────────────────┬────────────────────┬────────────┬────────────┐")
    print("│ ID │ Student Name       │ Book Title         │ Issued On  │ Returned   │")
    print("├────┼────────────────────┼────────────────────┼────────────┼────────────┤")
    for rid, sname, btitle, idate, rdate in rows:
        rdate_str = str(rdate) if rdate else "Pending"
        print(f"│ {str(rid).ljust(2)} │ {sname.ljust(18)} │ {btitle.ljust(18)} │ {str(idate)} │ {rdate_str.ljust(10)} │")
    print("└────┴────────────────────┴────────────────────┴────────────┴────────────┘")

def menu():
    while True:
        banner("📚 SHREE'S LIBRARY SYSTEM")
        print(Fore.YELLOW + "  [1] ➤ Add Student        [6] ➤ View Books")
        print("  [2] ➤ Remove Student     [7] ➤ Issue Book")
        print("  [3] ➤ View Students      [8] ➤ Return Book")
        print("  [4] ➤ Add Book           [9] ➤ View Issued Books")
        print("  [5] ➤ Discard Book       [0] ➤ Exit System")
        print("────────────────────────────────────────────────────────")
        choice = input(Fore.CYAN + "Enter your choice (0-9): ")

        if choice == '1': add_student()
        elif choice == '2': remove_student()
        elif choice == '3': view_students()
        elif choice == '4': add_book()
        elif choice == '5': discard_book()
        elif choice == '6': view_books()
        elif choice == '7': issue_book()
        elif choice == '8': return_book()
        elif choice == '9': view_issued_books()
        elif choice == '0':
            print(Fore.MAGENTA + "\n👋 Thank you for using SHREE'S LIBRARY SYSTEM!")
            break
        else:
            print(Fore.RED + "❌ Invalid choice! Try again.")

menu()
cursor.close()
conn.close()
