<<<<<<< HEAD
# from flask import Flask, render_template, request, redirect, session
# from flask_mysqldb import MySQL
# from flask_bcrypt import Bcrypt
# from datetime import date
# app = Flask(__name__)
# import os
# import math
# from openai import OpenAI

# # Initialize the OpenAI Client (Make sure to set OPENAI_API_KEY in your system environment variables)
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# app.secret_key = "library_secret_key"

# # MySQL Config
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '1234'
# app.config['MYSQL_DB'] = 'digital_library'

# mysql = MySQL(app)
# bcrypt = Bcrypt(app)


# # Home Page
# @app.route('/')
# def home():
#     return render_template('index.html')

# def get_embedding(text):
#     """Generates a text embedding using OpenAI's standard model."""
#     try:
#         response = client.embeddings.create(
#             input=[text],
#             model="text-embedding-3-small"
#         )
#         return response.data[0].embedding
#     except Exception as e:
#         print(f"Embedding error: {e}")
#         return None

# def cosine_similarity(v1, v2):
#     """Calculates the similarity score between two vector arrays."""
#     dot_product = sum(a * b for a, b in zip(v1, v2))
#     magnitude1 = math.sqrt(sum(a * a for a in v1))
#     magnitude2 = math.sqrt(sum(b * b for b in v2))
#     if not magnitude1 or not magnitude2:
#         return 0
#     return dot_product / (magnitude1 * magnitude2)

# # Register
# @app.route('/register', methods=['GET', 'POST'])
# def register():

#     if request.method == 'POST':

#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']

#         hashed_password = bcrypt.generate_password_hash(
#             password
#         ).decode('utf-8')

#         cur = mysql.connection.cursor()

#         cur.execute(
#             """
#             INSERT INTO users(name, email, password)
#             VALUES(%s, %s, %s)
#             """,
#             (name, email, hashed_password)
#         )

#         mysql.connection.commit()
#         cur.close()

#         return redirect('/login')

#     return render_template('register.html')


# # Login
# @app.route('/login', methods=['GET', 'POST'])
# def login():

#     if request.method == 'POST':

#         email = request.form['email']
#         password = request.form['password']

#         cur = mysql.connection.cursor()

#         cur.execute(
#             "SELECT * FROM users WHERE email=%s",
#             (email,)
#         )

#         user = cur.fetchone()

#         cur.close()

#         if user:

#             stored_password = user[3]

#             if bcrypt.check_password_hash(
#                 stored_password,
#                 password
#             ):

#                 session['user_id'] = user[0]
#                 session['name'] = user[1]

#                 return redirect('/dashboard')

#         return "Invalid Email or Password"

#     return render_template('login.html')


# # Dashboard
# @app.route('/dashboard')
# def dashboard():

#     if 'user_id' not in session:
#         return redirect('/login')

#     return render_template(
#         'dashboard.html',
#         name=session['name']
#     )

# @app.route('/books')
# def books():

#     cur = mysql.connection.cursor()

#     cur.execute("SELECT * FROM books")

#     books = cur.fetchall()

#     cur.close()

#     return render_template(
#         'books.html',
#         books=books
#     )
# @app.route('/add-book', methods=['GET', 'POST'])
# def add_book():

#     if request.method == 'POST':

#         title = request.form['title']
#         author = request.form['author']
#         genre = request.form['genre']
#         year = request.form['year']
#         copies = request.form['copies']

#         cur = mysql.connection.cursor()

#         cur.execute(
#             """
#             INSERT INTO books
#             (title, author, genre, publication_year, available_copies)
#             VALUES(%s,%s,%s,%s,%s)
#             """,
#             (title, author, genre, year, copies)
#         )

#         mysql.connection.commit()
#         cur.close()

#         return redirect('/books')

#     return render_template('add_book.html')

# @app.route('/search')
# def search():

#     keyword = request.args.get('keyword', '')

#     cur = mysql.connection.cursor()

#     cur.execute(
#         """
#         SELECT * FROM books
#         WHERE title LIKE %s
#         OR author LIKE %s
#         OR genre LIKE %s
#         """,
#         (
#             f"%{keyword}%",
#             f"%{keyword}%",
#             f"%{keyword}%"
#         )
#     )

#     books = cur.fetchall()

#     cur.close()

#     return render_template(
#         'books.html',
#         books=books
#     )
# @app.route('/borrow/<int:book_id>')
# def borrow_book(book_id):
#     try:
#         history.insert_one({
#             "user_id": user_id,
#             "book_id": book_id,
#             "action": "borrow"
#         })
#     except:
#         pass
#     if 'user_id' not in session:
#         return redirect('/login')

#     user_id = session['user_id']

#     cur = mysql.connection.cursor()

#     cur.execute(
#         "SELECT available_copies FROM books WHERE id=%s",
#         (book_id,)
#     )

#     book = cur.fetchone()

#     if not book or book[0] <= 0:
#         cur.close()
#         return "Book Not Available"

#     cur.execute(
#         """
#         INSERT INTO borrow_records
#         (user_id, book_id, borrow_date, status)
#         VALUES(%s,%s,%s,%s)
#         """,
#         (
#             user_id,
#             book_id,
#             date.today(),
#             'Borrowed'
#         )
#     )

#     cur.execute(
#         """
#         UPDATE books
#         SET available_copies = available_copies - 1
#         WHERE id=%s
#         """,
#         (book_id,)
#     )

#     history.insert_one({
#         "user_id": user_id,
#         "book_id": book_id,
#         "action": "borrow"
#     })

#     mysql.connection.commit()

#     cur.close()

#     return redirect('/books')

# @app.route('/my-books')
# def my_books():

#     if 'user_id' not in session:
#         return redirect('/login')

#     user_id = session['user_id']

#     cur = mysql.connection.cursor()

#     cur.execute(
#         """
#         SELECT
#         borrow_records.id,
#         books.title,
#         books.author,
#         borrow_records.borrow_date,
#         borrow_records.status

#         FROM borrow_records

#         JOIN books
#         ON books.id = borrow_records.book_id

#         WHERE borrow_records.user_id=%s
#         """,
#         (user_id,)
#     )

#     records = cur.fetchall()

#     cur.close()

#     return render_template(
#         'booksBorrowed.html',
#         records=records
#     )

# @app.route('/return-book/<int:borrow_id>')
# def return_book(borrow_id):
#     if 'user_id' not in session:
#         return redirect('/login')

#     cur = mysql.connection.cursor()

#     cur.execute(
#         """
#         SELECT book_id
#         FROM borrow_records
#         WHERE id=%s
#         """,
#         (borrow_id,)
#     )

#     book = cur.fetchone()

#     if not book:
#         return redirect('/my-books')

#     book_id = book[0]

#     cur.execute(
#         """
#         UPDATE borrow_records
#         SET status='Returned',
#             return_date=CURDATE()
#         WHERE id=%s
#         """,
#         (borrow_id,)
#     )

#     cur.execute(
#         """
#         UPDATE books
#         SET available_copies =
#             available_copies + 1
#         WHERE id=%s
#         """,
#         (book_id,)
#     )

#     mysql.connection.commit()

#     cur.close()

#     return redirect('/my-books')
# from mongo import wishlist, reviews, history
# @app.route('/edit-book/<int:id>', methods=['GET', 'POST'])
# def edit_book(id):

#     cur = mysql.connection.cursor()

#     if request.method == 'POST':

#         title = request.form['title']
#         author = request.form['author']
#         genre = request.form['genre']
#         year = request.form['year']
#         copies = request.form['copies']

#         cur.execute(
#             """
#             UPDATE books
#             SET title=%s,
#                 author=%s,
#                 genre=%s,
#                 publication_year=%s,
#                 available_copies=%s
#             WHERE id=%s
#             """,
#             (
#                 title,
#                 author,
#                 genre,
#                 year,
#                 copies,
#                 id
#             )
#         )

#         mysql.connection.commit()

#         cur.close()

#         return redirect('/books')

#     cur.execute(
#         "SELECT * FROM books WHERE id=%s",
#         (id,)
#     )

#     book = cur.fetchone()

#     cur.close()

#     return render_template(
#         'edit_book.html',
#         book=book
#     )


# @app.route('/delete-book/<int:id>')
# def delete_book(id):

#     cur = mysql.connection.cursor()

#     cur.execute(
#         "DELETE FROM books WHERE id=%s",
#         (id,)
#     )

#     mysql.connection.commit()

#     cur.close()

#     return redirect('/books')
# from mongo import wishlist
# @app.route('/wishlist/add/<int:book_id>')
# def add_to_wishlist(book_id):

#     if 'user_id' not in session:
#         return redirect('/login')

#     wishlist.insert_one({
#         "user_id": session['user_id'],
#         "book_id": book_id
#     })

#     return redirect('/books')

# @app.route('/wishlist')
# def view_wishlist():

#     if 'user_id' not in session:
#         return redirect('/login')

#     data = list(
#         wishlist.find(
#             {"user_id": session['user_id']}
#         )
#     )

#     return render_template(
#         'wishlist.html',
#         items=data
#     )

# from mongo import reviews
# @app.route('/review/<int:book_id>', methods=['GET','POST'])
# def review_book(book_id):

#     if request.method == 'POST':

#         rating = request.form['rating']
#         comment = request.form['comment']

#         reviews.insert_one({

#             "book_id": book_id,

#             "user_id":
#             session['user_id'],

#             "rating":
#             int(rating),

#             "comment":
#             comment

#         })

#         return redirect('/books')

#     return render_template(
#         'review.html',
#         book_id=book_id
#     )

# @app.route('/review/<int:book_id>', methods=['GET','POST'])
# def review_book(book_id):

#     if 'user_id' not in session:
#         return redirect('/login')
#     data = list(
#         reviews.find(
#             {"book_id": book_id}
#         )
#     )

#     return render_template(
#         'reviews.html',
#         reviews=data
#     )



# @app.route('/recommendations')
# def recommendations():
#     if 'user_id' not in session:
#         return redirect('/login')

#     user_id = session['user_id']
#     cur = mysql.connection.cursor()

#     cur.execute("""
#     SELECT genre,
#            COUNT(*) AS total

#     FROM borrow_records

#     JOIN books
#     ON books.id = borrow_records.book_id

#     WHERE user_id=%s

#     GROUP BY genre

#     ORDER BY total DESC

#     LIMIT 1
#     """,(user_id,))

#     genre = cur.fetchone()

#     if genre:

#         cur.execute(
#             """
#             SELECT *
#             FROM books
#             WHERE genre=%s
#             LIMIT 5
#             """,
#             (genre[0],)
#         )

#         books = cur.fetchall()

#     else:
#         books = []

#     return render_template(
#         'recommendations.html',
#         books=books
#     )
# # Logout
# @app.route('/logout')
# def logout():

#     session.clear()

#     return redirect('/login')
# try:
#     cur = mysql.connection.cursor()
#     print("MySQL Connected Successfully")
# except Exception as e:
#     print("Connection Error:", e)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, session, flash
from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from openai import OpenAI
from datetime import date
import os

# ==================================================
# APP CONFIG
# ==================================================

app = Flask(__name__)

app.secret_key = "library_secret_key"

# ==================================================
# MYSQL CONFIG
# ==================================================

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'digital_library'

mysql = MySQL(app)

# ==================================================
# BCRYPT
# ==================================================

bcrypt = Bcrypt(app)

# ==================================================
# MAIL CONFIG
# ==================================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Replace with your gmail
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'

# Gmail App Password
app.config['MAIL_PASSWORD'] = 'your_app_password'

mail = Mail(app)

# ==================================================
# GROQ AI CONFIG
# ==================================================

import os
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def admin_required():

    if session.get("role") != "admin":
        return False

    return True

# ==================================================
# EMAIL REMINDER FUNCTION
# ==================================================

def send_reminders():

    with app.app_context():

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT
                users.email,
                books.title,
                borrow_records.borrow_date

            FROM borrow_records

            JOIN users
            ON users.id = borrow_records.user_id

            JOIN books
            ON books.id = borrow_records.book_id

            WHERE borrow_records.status='Borrowed'
            AND DATEDIFF(CURDATE(), borrow_records.borrow_date) >= 30
        """)

        records = cur.fetchall()

        for row in records:

            email = row[0]
            title = row[1]
            borrow_date = row[2]

            try:

                msg = Message(
                    "Library Book Reminder",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[email]
                )

                msg.body = f"""
Dear Student,

You borrowed:

{title}

Borrow Date:
{borrow_date}

Please return the book as soon as possible.

Thank You,
Library Management System
"""

                mail.send(msg)

            except Exception as e:
                print("Mail Error:", e)

        cur.close()

# ==================================================
# SCHEDULER
# ==================================================

scheduler = BackgroundScheduler()

scheduler.add_job(
    func=send_reminders,
    trigger="interval",
    hours=24
)

scheduler.start()

# ==================================================
# HOME
# ==================================================

@app.route('/')
def home():

    return render_template('index.html')

# ==================================================
# REGISTER
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO users(name,email,password,role)
            VALUES(%s,%s,%s,%s)
            """,
            (name, email, hashed, role)
        )

        mysql.connection.commit()
        cur.close()

        flash("Registration Successful!", "success")

        return redirect("/login")

    return render_template("register.html")
# ==================================================
# LOGIN
# ==================================================

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE email=%s AND role=%s
            """,
            (email, role)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            if bcrypt.check_password_hash(user[3], password):

                session['user_id'] = user[0]
                session['name'] = user[1]
                session['role'] = user[4]

                if role == "admin":
                    return redirect('/admin/dashboard')
                else:
                    return redirect('/dashboard')

        return "Invalid Credentials"

    return render_template("login.html")
# ==================================================
# LOGOUT
# ==================================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# ==================================================
# DASHBOARD
# ==================================================
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    # ==========================
    # Statistics
    # ==========================

    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("SELECT SUM(available_copies) FROM books")
    available_books = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT COUNT(*)
        FROM borrow_records
        WHERE status='Borrowed'
    """)
    borrowed_books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    stats = {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "total_users": total_users
    }

    # ==========================
    # Top 5 Trending Books
    # ==========================

    cur.execute("""
SELECT
    books.id,
    books.title,
    books.author,
    COUNT(borrow_records.book_id) AS borrow_count

FROM books

LEFT JOIN borrow_records
ON books.id = borrow_records.book_id

GROUP BY books.id, books.title, books.author

ORDER BY borrow_count DESC

LIMIT 5
""")

    trending_books = []

    for row in cur.fetchall():
        trending_books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "borrow_count": row[3]
        })

    # ==========================
    # Recently Added Books
    # ==========================

    cur.execute("""
        SELECT
            id,
            title,
            author
        FROM books
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_books = []

    for row in cur.fetchall():
        recent_books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2]
        })
    # ==========================
    # AI Recommendations
    # ==========================

    cur.execute("""
        SELECT
            id,
            title,
            author,
            genre,
            ai_description
        FROM books
        ORDER BY RAND()
        LIMIT 3
    """)

    recommendations = []

    for row in cur.fetchall():
        recommendations.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "genre": row[3],
            "ai_description": row[4]
        })

    cur.close()

    return render_template(
    "dashboard.html",
    name=session["name"],
    role=session["role"],
    stats=stats,
    trending_books=trending_books,
    recent_books=recent_books,
    recommendations=recommendations
)

@app.route('/book-ranking')
def book_ranking():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            books.id,
            books.title,
            COUNT(borrow_records.id) AS borrow_count
        FROM books
        LEFT JOIN borrow_records
        ON books.id = borrow_records.book_id
        GROUP BY books.id, books.title
        ORDER BY borrow_count DESC
        LIMIT 10
    """)

    trending_books = []

    for row in cur.fetchall():
        trending_books.append({
            "id": row[0],
            "title": row[1],
            "borrow_count": row[2]
        })

    print(trending_books)   # <-- Debug

    cur.close()

    return render_template(
        "book_ranking.html",
        trending_books=trending_books
    )
# ==================================================
# VIEW BOOKS
# ==================================================

@app.route('/books')
def books():

    if 'user_id' not in session:
        return redirect('/login')

    search = request.args.get("search")

    cur = mysql.connection.cursor()

    if search:

        cur.execute("""
        SELECT *
        FROM books
        WHERE title LIKE %s
        OR author LIKE %s
        OR genre LIKE %s
        """,(
        "%" + search + "%",
        "%" + search + "%",
        "%" + search + "%"
        ))

    else:

        cur.execute("SELECT * FROM books ORDER BY id DESC")

    rows = cur.fetchall()

    books=[]

    for row in rows:

        books.append({

            "id":row[0],

            "title":row[1],

            "author":row[2],

            "genre":row[3],

            "publication_year":row[4],

            "available_copies":row[5]

        })

    cur.close()

    return render_template("books.html",books=books)
# ==================================================
# SEARCH BOOKS
# ==================================================

@app.route('/search')
def search():

    if 'user_id' not in session:
        return redirect('/login')

    keyword = request.args.get('keyword', '')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, title, author, genre, publication_year, available_copies
        FROM books
        WHERE title LIKE %s
        OR author LIKE %s
        OR genre LIKE %s
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    books = cur.fetchall()
    cur.close()

    return render_template('books.html', books=books)

# ==================================================
# ADD BOOK (ADMIN ONLY)
# ==================================================

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied: Admin Only"

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        copies = request.form['copies']

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO books
            (title, author, genre, publication_year, available_copies)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, author, genre, year, copies))

        mysql.connection.commit()
        cur.close()

        return redirect('/books')

    return render_template('add_book.html')

# ==================================================
# EDIT BOOK (ADMIN ONLY)
# ==================================================

@app.route('/edit-book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied: Admin Only"

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        copies = request.form['copies']

        cur.execute("""
            UPDATE books
            SET title=%s,
                author=%s,
                genre=%s,
                publication_year=%s,
                available_copies=%s
            WHERE id=%s
        """, (title, author, genre, year, copies, id))

        mysql.connection.commit()
        cur.close()

        return redirect('/books')

    cur.execute("""
        SELECT id, title, author, genre, publication_year, available_copies
        FROM books
        WHERE id=%s
    """, (id,))

    book = cur.fetchone()
    cur.close()

    return render_template('edit_book.html', book=book)

# ==================================================
# DELETE BOOK (ADMIN ONLY)
# ==================================================

@app.route('/delete-book/<int:id>')
def delete_book(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied: Admin Only"

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM books WHERE id=%s", (id,))

    mysql.connection.commit()
    cur.close()

    return redirect('/books')

# ==================================================
# BOOK DETAIL + AI SUMMARY + RECOMMENDATION
# ==================================================

@app.route('/book/<int:book_id>')
def book_detail(book_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, title, author, genre, publication_year, available_copies, ai_description, image 
        FROM books 
        WHERE id = %s
    """, (book_id,))

    book = cur.fetchone()

    if not book:
        cur.close()
        return "Book Not Found"

    ai_description = book[6]

    # ===============================
    # AI SUMMARY GENERATION (GROQ)
    # ===============================

    if not ai_description:

        prompt = f"""
        Give a short 3-line summary for:
        Title: {book[1]}
        Author: {book[2]}
        Genre: {book[3]}
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            ai_description = response.choices[0].message.content

            cur.execute("""
                UPDATE books
                SET ai_description=%s
                WHERE id=%s
            """, (ai_description, book_id))

            mysql.connection.commit()

        except Exception as e:
            ai_description = "AI summary not available"

    # ===============================
    # SIMPLE RECOMMENDATIONS (BY GENRE)
    # ===============================

    cur.execute("""
        SELECT id, title, author
        FROM books
        WHERE genre=%s
        AND id != %s
        LIMIT 5
    """, (book[3], book_id))

    recommendations = cur.fetchall()

    cur.close()

    return render_template(
        'book_detail.html',
        book=book,
        ai_description=ai_description,
        recommendations=recommendations
    )
# ==================================================
# BORROW BOOK
# ==================================================

@app.route('/borrow/<int:book_id>')
def borrow_book(book_id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    cur = mysql.connection.cursor()

    # Check availability
    cur.execute("""
        SELECT available_copies
        FROM books
        WHERE id=%s
    """, (book_id,))

    book = cur.fetchone()

    if not book:
        cur.close()
        return "Book Not Found"

    if book[0] <= 0:
        cur.close()
        return "No Copies Available"

    # Insert borrow record
    cur.execute("""
        INSERT INTO borrow_records
        (user_id, book_id, borrow_date, status)
        VALUES (%s, %s, CURDATE(), 'Borrowed')
    """, (user_id, book_id))

    # Decrease stock
    cur.execute("""
        UPDATE books
        SET available_copies = available_copies - 1
        WHERE id=%s
    """, (book_id,))

    mysql.connection.commit()
    cur.close()

    return redirect('/my-books')

# ==================================================
# MY BORROWED BOOKS
# ==================================================

@app.route('/my-books')
def my_books():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'student':
        return redirect('/admin/borrowed-books')

    user_id = session['user_id']

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            borrow_records.id,
            books.title,
            books.author,
            borrow_records.borrow_date,
            borrow_records.return_date,
            borrow_records.status

        FROM borrow_records

        JOIN books
        ON books.id = borrow_records.book_id

        WHERE borrow_records.user_id=%s

        ORDER BY borrow_records.borrow_date DESC
    """, (user_id,))

    records = cur.fetchall()

    cur.close()

    return render_template(
        "my_books.html",
        records=records
    )

# ==================================================
# RETURN BOOK
# ==================================================

@app.route('/return-book/<int:borrow_id>')
def return_book(borrow_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    # Get book_id from borrow record
    cur.execute("""
        SELECT book_id
        FROM borrow_records
        WHERE id=%s
    """, (borrow_id,))

    record = cur.fetchone()

    if not record:
        cur.close()
        return "Invalid Record"

    book_id = record[0]

    # Update borrow record
    cur.execute("""
        UPDATE borrow_records
        SET status='Returned',
            return_date=CURDATE()
        WHERE id=%s
    """, (borrow_id,))

    # Increase stock
    cur.execute("""
        UPDATE books
        SET available_copies = available_copies + 1
        WHERE id=%s
    """, (book_id,))

    mysql.connection.commit()
    cur.close()

    return redirect('/my-books')
@app.route('/admin/dashboard')
def admin_dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    cur = mysql.connection.cursor()

    # ==========================
    # Statistics
    # ==========================

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("SELECT SUM(available_copies) FROM books")
    available_books = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT COUNT(*)
        FROM borrow_records
        WHERE status='Borrowed'
    """)
    borrowed_books = cur.fetchone()[0]

    # ==========================
    # Top 5 Trending Books
    # ==========================

    cur.execute("""
        SELECT
            b.id,
            b.title,
            b.author,
            COUNT(br.book_id) AS borrow_count
        FROM books b
        LEFT JOIN borrow_records br
            ON b.id = br.book_id
        GROUP BY
            b.id,
            b.title,
            b.author
        ORDER BY borrow_count DESC
        LIMIT 5
    """)

    trending_books = []

    for row in cur.fetchall():
        trending_books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "borrow_count": row[3]
        })

    # ==========================
    # Recently Added Books
    # ==========================

    cur.execute("""
        SELECT
            id,
            title,
            author
        FROM books
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_books = []

    for row in cur.fetchall():
        recent_books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2]
        })

    # ==========================
    # AI Recommendations
    # ==========================

    cur.execute("""
        SELECT
            id,
            title,
            author,
            genre,
            ai_description
        FROM books
        ORDER BY RAND()
        LIMIT 3
    """)

    recommendations = []

    for row in cur.fetchall():
        recommendations.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "genre": row[3],
            "ai_description": row[4] if row[4] else "AI summary not available."
        })

    cur.close()

    stats = {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "total_users": total_users
    }

    return render_template(
    "dashboard.html",
    name=session["name"],
    role=session["role"],
    stats=stats,
    trending_books=trending_books,
    recent_books=recent_books,
    recommendations=recommendations
)
# ==================================================
# ADMIN - VIEW ALL BORROWED BOOKS
# ==================================================

@app.route('/admin/borrowed-books')
def admin_borrowed_books():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            borrow_records.id,
            users.name,
            users.email,
            books.title,
            books.author,
            borrow_records.borrow_date,
            borrow_records.return_date,
            borrow_records.status

        FROM borrow_records

        JOIN users
        ON users.id = borrow_records.user_id

        JOIN books
        ON books.id = borrow_records.book_id

        ORDER BY borrow_records.borrow_date DESC
    """)

    records = cur.fetchall()

    cur.close()

    return render_template(
        "admin_borrowed_books.html",
        records=records
    )

# ==================================================
# OPTIONAL: SIMPLE HOME REDIRECT LOGIC
# ==================================================

@app.route('/home')
def home_redirect():

    if 'user_id' in session:
        return redirect('/dashboard')

    return redirect('/login')

# ==================================================
# RUN APP
# ==================================================

if __name__ == '__main__':
=======
# from flask import Flask, render_template, request, redirect, session
# from flask_mysqldb import MySQL
# from flask_bcrypt import Bcrypt
# from datetime import date
# app = Flask(__name__)
# import os
# import math
# from openai import OpenAI

# # Initialize the OpenAI Client (Make sure to set OPENAI_API_KEY in your system environment variables)
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# app.secret_key = "library_secret_key"

# # MySQL Config
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '1234'
# app.config['MYSQL_DB'] = 'digital_library'

# mysql = MySQL(app)
# bcrypt = Bcrypt(app)


# # Home Page
# @app.route('/')
# def home():
#     return render_template('index.html')

# def get_embedding(text):
#     """Generates a text embedding using OpenAI's standard model."""
#     try:
#         response = client.embeddings.create(
#             input=[text],
#             model="text-embedding-3-small"
#         )
#         return response.data[0].embedding
#     except Exception as e:
#         print(f"Embedding error: {e}")
#         return None

# def cosine_similarity(v1, v2):
#     """Calculates the similarity score between two vector arrays."""
#     dot_product = sum(a * b for a, b in zip(v1, v2))
#     magnitude1 = math.sqrt(sum(a * a for a in v1))
#     magnitude2 = math.sqrt(sum(b * b for b in v2))
#     if not magnitude1 or not magnitude2:
#         return 0
#     return dot_product / (magnitude1 * magnitude2)

# # Register
# @app.route('/register', methods=['GET', 'POST'])
# def register():

#     if request.method == 'POST':

#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']

#         hashed_password = bcrypt.generate_password_hash(
#             password
#         ).decode('utf-8')

#         cur = mysql.connection.cursor()

#         cur.execute(
#             """
#             INSERT INTO users(name, email, password)
#             VALUES(%s, %s, %s)
#             """,
#             (name, email, hashed_password)
#         )

#         mysql.connection.commit()
#         cur.close()

#         return redirect('/login')

#     return render_template('register.html')


# # Login
# @app.route('/login', methods=['GET', 'POST'])
# def login():

#     if request.method == 'POST':

#         email = request.form['email']
#         password = request.form['password']

#         cur = mysql.connection.cursor()

#         cur.execute(
#             "SELECT * FROM users WHERE email=%s",
#             (email,)
#         )

#         user = cur.fetchone()

#         cur.close()

#         if user:

#             stored_password = user[3]

#             if bcrypt.check_password_hash(
#                 stored_password,
#                 password
#             ):

#                 session['user_id'] = user[0]
#                 session['name'] = user[1]

#                 return redirect('/dashboard')

#         return "Invalid Email or Password"

#     return render_template('login.html')


# # Dashboard
# @app.route('/dashboard')
# def dashboard():

#     if 'user_id' not in session:
#         return redirect('/login')

#     return render_template(
#         'dashboard.html',
#         name=session['name']
#     )

# @app.route('/books')
# def books():

#     cur = mysql.connection.cursor()

#     cur.execute("SELECT * FROM books")

#     books = cur.fetchall()

#     cur.close()

#     return render_template(
#         'books.html',
#         books=books
#     )
# @app.route('/add-book', methods=['GET', 'POST'])
# def add_book():

#     if request.method == 'POST':

#         title = request.form['title']
#         author = request.form['author']
#         genre = request.form['genre']
#         year = request.form['year']
#         copies = request.form['copies']

#         cur = mysql.connection.cursor()

#         cur.execute(
#             """
#             INSERT INTO books
#             (title, author, genre, publication_year, available_copies)
#             VALUES(%s,%s,%s,%s,%s)
#             """,
#             (title, author, genre, year, copies)
#         )

#         mysql.connection.commit()
#         cur.close()

#         return redirect('/books')

#     return render_template('add_book.html')

# @app.route('/search')
# def search():

#     keyword = request.args.get('keyword', '')

#     cur = mysql.connection.cursor()

#     cur.execute(
#         """
#         SELECT * FROM books
#         WHERE title LIKE %s
#         OR author LIKE %s
#         OR genre LIKE %s
#         """,
#         (
#             f"%{keyword}%",
#             f"%{keyword}%",
#             f"%{keyword}%"
#         )
#     )

#     books = cur.fetchall()

#     cur.close()

#     return render_template(
#         'books.html',
#         books=books
#     )
# @app.route('/borrow/<int:book_id>')
# def borrow_book(book_id):
#     try:
#         history.insert_one({
#             "user_id": user_id,
#             "book_id": book_id,
#             "action": "borrow"
#         })
#     except:
#         pass
#     if 'user_id' not in session:
#         return redirect('/login')

#     user_id = session['user_id']

#     cur = mysql.connection.cursor()

#     cur.execute(
#         "SELECT available_copies FROM books WHERE id=%s",
#         (book_id,)
#     )

#     book = cur.fetchone()

#     if not book or book[0] <= 0:
#         cur.close()
#         return "Book Not Available"

#     cur.execute(
#         """
#         INSERT INTO borrow_records
#         (user_id, book_id, borrow_date, status)
#         VALUES(%s,%s,%s,%s)
#         """,
#         (
#             user_id,
#             book_id,
#             date.today(),
#             'Borrowed'
#         )
#     )

#     cur.execute(
#         """
#         UPDATE books
#         SET available_copies = available_copies - 1
#         WHERE id=%s
#         """,
#         (book_id,)
#     )

#     history.insert_one({
#         "user_id": user_id,
#         "book_id": book_id,
#         "action": "borrow"
#     })

#     mysql.connection.commit()

#     cur.close()

#     return redirect('/books')

# @app.route('/my-books')
# def my_books():

#     if 'user_id' not in session:
#         return redirect('/login')

#     user_id = session['user_id']

#     cur = mysql.connection.cursor()

#     cur.execute(
#         """
#         SELECT
#         borrow_records.id,
#         books.title,
#         books.author,
#         borrow_records.borrow_date,
#         borrow_records.status

#         FROM borrow_records

#         JOIN books
#         ON books.id = borrow_records.book_id

#         WHERE borrow_records.user_id=%s
#         """,
#         (user_id,)
#     )

#     records = cur.fetchall()

#     cur.close()

#     return render_template(
#         'booksBorrowed.html',
#         records=records
#     )

# @app.route('/return-book/<int:borrow_id>')
# def return_book(borrow_id):
#     if 'user_id' not in session:
#         return redirect('/login')

#     cur = mysql.connection.cursor()

#     cur.execute(
#         """
#         SELECT book_id
#         FROM borrow_records
#         WHERE id=%s
#         """,
#         (borrow_id,)
#     )

#     book = cur.fetchone()

#     if not book:
#         return redirect('/my-books')

#     book_id = book[0]

#     cur.execute(
#         """
#         UPDATE borrow_records
#         SET status='Returned',
#             return_date=CURDATE()
#         WHERE id=%s
#         """,
#         (borrow_id,)
#     )

#     cur.execute(
#         """
#         UPDATE books
#         SET available_copies =
#             available_copies + 1
#         WHERE id=%s
#         """,
#         (book_id,)
#     )

#     mysql.connection.commit()

#     cur.close()

#     return redirect('/my-books')
# from mongo import wishlist, reviews, history
# @app.route('/edit-book/<int:id>', methods=['GET', 'POST'])
# def edit_book(id):

#     cur = mysql.connection.cursor()

#     if request.method == 'POST':

#         title = request.form['title']
#         author = request.form['author']
#         genre = request.form['genre']
#         year = request.form['year']
#         copies = request.form['copies']

#         cur.execute(
#             """
#             UPDATE books
#             SET title=%s,
#                 author=%s,
#                 genre=%s,
#                 publication_year=%s,
#                 available_copies=%s
#             WHERE id=%s
#             """,
#             (
#                 title,
#                 author,
#                 genre,
#                 year,
#                 copies,
#                 id
#             )
#         )

#         mysql.connection.commit()

#         cur.close()

#         return redirect('/books')

#     cur.execute(
#         "SELECT * FROM books WHERE id=%s",
#         (id,)
#     )

#     book = cur.fetchone()

#     cur.close()

#     return render_template(
#         'edit_book.html',
#         book=book
#     )


# @app.route('/delete-book/<int:id>')
# def delete_book(id):

#     cur = mysql.connection.cursor()

#     cur.execute(
#         "DELETE FROM books WHERE id=%s",
#         (id,)
#     )

#     mysql.connection.commit()

#     cur.close()

#     return redirect('/books')
# from mongo import wishlist
# @app.route('/wishlist/add/<int:book_id>')
# def add_to_wishlist(book_id):

#     if 'user_id' not in session:
#         return redirect('/login')

#     wishlist.insert_one({
#         "user_id": session['user_id'],
#         "book_id": book_id
#     })

#     return redirect('/books')

# @app.route('/wishlist')
# def view_wishlist():

#     if 'user_id' not in session:
#         return redirect('/login')

#     data = list(
#         wishlist.find(
#             {"user_id": session['user_id']}
#         )
#     )

#     return render_template(
#         'wishlist.html',
#         items=data
#     )

# from mongo import reviews
# @app.route('/review/<int:book_id>', methods=['GET','POST'])
# def review_book(book_id):

#     if request.method == 'POST':

#         rating = request.form['rating']
#         comment = request.form['comment']

#         reviews.insert_one({

#             "book_id": book_id,

#             "user_id":
#             session['user_id'],

#             "rating":
#             int(rating),

#             "comment":
#             comment

#         })

#         return redirect('/books')

#     return render_template(
#         'review.html',
#         book_id=book_id
#     )

# @app.route('/review/<int:book_id>', methods=['GET','POST'])
# def review_book(book_id):

#     if 'user_id' not in session:
#         return redirect('/login')
#     data = list(
#         reviews.find(
#             {"book_id": book_id}
#         )
#     )

#     return render_template(
#         'reviews.html',
#         reviews=data
#     )



# @app.route('/recommendations')
# def recommendations():
#     if 'user_id' not in session:
#         return redirect('/login')

#     user_id = session['user_id']
#     cur = mysql.connection.cursor()

#     cur.execute("""
#     SELECT genre,
#            COUNT(*) AS total

#     FROM borrow_records

#     JOIN books
#     ON books.id = borrow_records.book_id

#     WHERE user_id=%s

#     GROUP BY genre

#     ORDER BY total DESC

#     LIMIT 1
#     """,(user_id,))

#     genre = cur.fetchone()

#     if genre:

#         cur.execute(
#             """
#             SELECT *
#             FROM books
#             WHERE genre=%s
#             LIMIT 5
#             """,
#             (genre[0],)
#         )

#         books = cur.fetchall()

#     else:
#         books = []

#     return render_template(
#         'recommendations.html',
#         books=books
#     )
# # Logout
# @app.route('/logout')
# def logout():

#     session.clear()

#     return redirect('/login')
# try:
#     cur = mysql.connection.cursor()
#     print("MySQL Connected Successfully")
# except Exception as e:
#     print("Connection Error:", e)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, session, flash
from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from openai import OpenAI
from datetime import date
import os

# ==================================================
# APP CONFIG
# ==================================================

app = Flask(__name__)

app.secret_key = "library_secret_key"

# ==================================================
# MYSQL CONFIG
# ==================================================

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'digital_library'

mysql = MySQL(app)

# ==================================================
# BCRYPT
# ==================================================

bcrypt = Bcrypt(app)

# ==================================================
# MAIL CONFIG
# ==================================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Replace with your gmail
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'

# Gmail App Password
app.config['MAIL_PASSWORD'] = 'your_app_password'

mail = Mail(app)

# ==================================================
# GROQ AI CONFIG
# ==================================================

import os
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def admin_required():

    if session.get("role") != "admin":
        return False

    return True

# ==================================================
# EMAIL REMINDER FUNCTION
# ==================================================

def send_reminders():

    with app.app_context():

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT
                users.email,
                books.title,
                borrow_records.borrow_date

            FROM borrow_records

            JOIN users
            ON users.id = borrow_records.user_id

            JOIN books
            ON books.id = borrow_records.book_id

            WHERE borrow_records.status='Borrowed'
            AND DATEDIFF(CURDATE(), borrow_records.borrow_date) >= 30
        """)

        records = cur.fetchall()

        for row in records:

            email = row[0]
            title = row[1]
            borrow_date = row[2]

            try:

                msg = Message(
                    "Library Book Reminder",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[email]
                )

                msg.body = f"""
Dear Student,

You borrowed:

{title}

Borrow Date:
{borrow_date}

Please return the book as soon as possible.

Thank You,
Library Management System
"""

                mail.send(msg)

            except Exception as e:
                print("Mail Error:", e)

        cur.close()

# ==================================================
# SCHEDULER
# ==================================================

scheduler = BackgroundScheduler()

scheduler.add_job(
    func=send_reminders,
    trigger="interval",
    hours=24
)

scheduler.start()

# ==================================================
# HOME
# ==================================================

@app.route('/')
def home():

    return render_template('index.html')

# ==================================================
# REGISTER
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO users(name,email,password,role)
            VALUES(%s,%s,%s,%s)
            """,
            (name, email, hashed, role)
        )

        mysql.connection.commit()
        cur.close()

        flash("Registration Successful!", "success")

        return redirect("/login")

    return render_template("register.html")
# ==================================================
# LOGIN
# ==================================================

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE email=%s AND role=%s
            """,
            (email, role)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            if bcrypt.check_password_hash(user[3], password):

                session['user_id'] = user[0]
                session['name'] = user[1]
                session['role'] = user[4]

                if role == "admin":
                    return redirect('/admin/dashboard')
                else:
                    return redirect('/dashboard')

        return "Invalid Credentials"

    return render_template("login.html")
# ==================================================
# LOGOUT
# ==================================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# ==================================================
# DASHBOARD
# ==================================================
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    user_name = session['name']
    role = session['role']

    cur = mysql.connection.cursor()

    # ==========================
    # 📊 Statistics
    # ==========================

    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("SELECT SUM(available_copies) FROM books")
    available_books = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT COUNT(*)
        FROM borrow_records
        WHERE status='Borrowed'
    """)
    borrowed_books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    stats = {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "total_users": total_users
    }

    # ==========================
    # 🔥 Trending Books
    # ==========================

    cur.execute("""
        SELECT
            books.id,
            books.title,
            books.author,
            COUNT(borrow_records.book_id) AS borrow_count
        FROM books
        LEFT JOIN borrow_records
            ON books.id = borrow_records.book_id
        GROUP BY books.id, books.title, books.author
        ORDER BY borrow_count DESC
        LIMIT 5
    """)

    trending_books = [
        {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "borrow_count": row[3]
        }
        for row in cur.fetchall()
    ]

    # ==========================
    # 🆕 Recent Books
    # ==========================

    cur.execute("""
        SELECT id, title, author
        FROM books
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_books = [
        {"id": r[0], "title": r[1], "author": r[2]}
        for r in cur.fetchall()
    ]

    # ==========================
    # 🤖 AI Recommendations
    # ==========================

    cur.execute("""
        SELECT id, title, author, genre, ai_description
        FROM books
        ORDER BY RAND()
        LIMIT 3
    """)

    recommendations = [
        {
            "id": r[0],
            "title": r[1],
            "author": r[2],
            "genre": r[3],
            "ai_description": r[4]
        }
        for r in cur.fetchall()
    ]

    cur.close()

    # ==========================
    # 🤖 CHATBOT CONTEXT DATA (NEW)
    # ==========================

    chat_context = {
        "user_id": user_id,
        "name": user_name,
        "role": role,
        "stats": stats
    }

    return render_template(
        "dashboard.html",
        name=user_name,
        role=role,
        stats=stats,
        trending_books=trending_books,
        recent_books=recent_books,
        recommendations=recommendations,

        # IMPORTANT: for chatbot
        chat_context=chat_context
    )
@app.route('/book-ranking')
def book_ranking():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            books.id,
            books.title,
            COUNT(borrow_records.id) AS borrow_count
        FROM books
        LEFT JOIN borrow_records
        ON books.id = borrow_records.book_id
        GROUP BY books.id, books.title
        ORDER BY borrow_count DESC
        LIMIT 10
    """)

    trending_books = []

    for row in cur.fetchall():
        trending_books.append({
            "id": row[0],
            "title": row[1],
            "borrow_count": row[2]
        })

    # print(trending_books)   # <-- Debug

    cur.close()

    return render_template(
        "book_ranking.html",
        trending_books=trending_books
    )
# ==================================================
# VIEW BOOKS
# ==================================================

@app.route('/books')
def books():

    if 'user_id' not in session:
        return redirect('/login')

    search = request.args.get("search")

    cur = mysql.connection.cursor()

    if search:

        cur.execute("""
        SELECT *
        FROM books
        WHERE title LIKE %s
        OR author LIKE %s
        OR genre LIKE %s
        """,(
        "%" + search + "%",
        "%" + search + "%",
        "%" + search + "%"
        ))

    else:

        cur.execute("SELECT * FROM books ORDER BY id DESC")

    rows = cur.fetchall()

    books=[]

    for row in rows:

        books.append({

            "id":row[0],

            "title":row[1],

            "author":row[2],

            "genre":row[3],

            "publication_year":row[4],

            "available_copies":row[5]

        })

    cur.close()

    return render_template("books.html",books=books)
# ==================================================
# SEARCH BOOKS
# ==================================================

@app.route('/search')
def search():

    if 'user_id' not in session:
        return redirect('/login')

    keyword = request.args.get('keyword', '')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, title, author, genre, publication_year, available_copies
        FROM books
        WHERE title LIKE %s
        OR author LIKE %s
        OR genre LIKE %s
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    books = cur.fetchall()
    cur.close()

    return render_template('books.html', books=books)

# ==================================================
# ADD BOOK (ADMIN ONLY)
# ==================================================

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied: Admin Only"

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        copies = request.form['copies']

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO books
            (title, author, genre, publication_year, available_copies)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, author, genre, year, copies))

        mysql.connection.commit()
        cur.close()

        return redirect('/books')

    return render_template('add_book.html')

# ==================================================
# EDIT BOOK (ADMIN ONLY)
# ==================================================

@app.route('/edit-book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied: Admin Only"

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        copies = request.form['copies']

        cur.execute("""
            UPDATE books
            SET title=%s,
                author=%s,
                genre=%s,
                publication_year=%s,
                available_copies=%s
            WHERE id=%s
        """, (title, author, genre, year, copies, id))

        mysql.connection.commit()
        cur.close()

        return redirect('/books')

    cur.execute("""
        SELECT id, title, author, genre, publication_year, available_copies
        FROM books
        WHERE id=%s
    """, (id,))

    book = cur.fetchone()
    cur.close()

    return render_template('edit_book.html', book=book)

# ==================================================
# DELETE BOOK (ADMIN ONLY)
# ==================================================

@app.route('/delete-book/<int:id>')
def delete_book(id):

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied: Admin Only"

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM books WHERE id=%s", (id,))

    mysql.connection.commit()
    cur.close()

    return redirect('/books')

from flask import request, jsonify
import requests
import os

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    user_id = session.get("user_id")
    user_name = session.get("name")

    if not user_id:
        return jsonify({"reply": "⚠️ Please login again to use chatbot."})
    # =============================
    # 📚 USER PERSONAL QUERIES
    # =============================

    if "my books" in user_message or "borrowed" in user_message:

        books = Borrow.query.filter_by(user_id=user_id).all()

        if not books:
            return jsonify({"reply": f"{user_name}, you have not borrowed any books."})

        book_list = "\n".join([f"- {b.book.title}" for b in books])

        return jsonify({
            "reply": f"{user_name}, your borrowed books are:\n{book_list}"
        })

    # =============================
    # 📖 AVAILABLE BOOK SEARCH
    # =============================

    if "python" in user_message:
        books = Book.query.filter(Book.title.contains("Python")).all()

        result = "\n".join([f"- {b.title}" for b in books])

        return jsonify({"reply": f"Python books:\n{result}"})

    # =============================
    # ⏰ QUICK ANSWERS
    # =============================

    if "timing" in user_message:
        return jsonify({"reply": "Library is open from 9 AM to 9 PM."})

    # =============================
    # 🤖 AI FALLBACK (SMART CONTEXT)
    # =============================

    import requests
    from dotenv import load_dotenv
    load_dotenv()
    import os
    url="https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    print("KEY LOADED:", os.getenv("GROQ_API_KEY"))
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": f"""
You are a Smart Library AI Assistant.

User details:
- Name: {user_name}
- User ID: {user_id}

You can answer:
- books
- library info
- user queries

If user asks personal questions, use their context.

Be friendly and concise.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

# Debug (VERY IMPORTANT while testing)
    print("STATUS:", response.status_code)
    print("RESPONSE:", data)

    # Safety check
    if "choices" not in data:
        return jsonify({
            "reply": "AI service error. Please check API key / model."
        })

    reply = data["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})
# ==================================================
# BOOK DETAIL + AI SUMMARY + RECOMMENDATION
# ==================================================

@app.route('/book/<int:book_id>')
def book_detail(book_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id, title, author, genre, publication_year, available_copies, ai_description, image 
        FROM books 
        WHERE id = %s
    """, (book_id,))

    book = cur.fetchone()

    if not book:
        cur.close()
        return "Book Not Found"

    ai_description = book[6]

    # ===============================
    # AI SUMMARY GENERATION (GROQ)
    # ===============================

    if not ai_description:

        prompt = f"""
        Give a short 3-line summary for:
        Title: {book[1]}
        Author: {book[2]}
        Genre: {book[3]}
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            ai_description = response.choices[0].message.content

            cur.execute("""
                UPDATE books
                SET ai_description=%s
                WHERE id=%s
            """, (ai_description, book_id))

            mysql.connection.commit()

        except Exception as e:
            ai_description = "AI summary not available"

    # ===============================
    # SIMPLE RECOMMENDATIONS (BY GENRE)
    # ===============================

    cur.execute("""
        SELECT id, title, author
        FROM books
        WHERE genre=%s
        AND id != %s
        LIMIT 5
    """, (book[3], book_id))

    recommendations = cur.fetchall()

    cur.close()

    return render_template(
        'book_detail.html',
        book=book,
        ai_description=ai_description,
        recommendations=recommendations
    )
# ==================================================
# BORROW BOOK
# ==================================================

@app.route('/borrow/<int:book_id>')
def borrow_book(book_id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    cur = mysql.connection.cursor()

    # Check availability
    cur.execute("""
        SELECT available_copies
        FROM books
        WHERE id=%s
    """, (book_id,))

    book = cur.fetchone()

    if not book:
        cur.close()
        return "Book Not Found"

    if book[0] <= 0:
        cur.close()
        return "No Copies Available"

    # Insert borrow record
    cur.execute("""
        INSERT INTO borrow_records
        (user_id, book_id, borrow_date, status)
        VALUES (%s, %s, CURDATE(), 'Borrowed')
    """, (user_id, book_id))

    # Decrease stock
    cur.execute("""
        UPDATE books
        SET available_copies = available_copies - 1
        WHERE id=%s
    """, (book_id,))

    mysql.connection.commit()
    cur.close()

    return redirect('/my-books')

# ==================================================
# MY BORROWED BOOKS
# ==================================================

@app.route('/my-books')
def my_books():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'student':
        return redirect('/admin/borrowed-books')

    user_id = session['user_id']

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            borrow_records.id,
            books.title,
            books.author,
            borrow_records.borrow_date,
            borrow_records.return_date,
            borrow_records.status

        FROM borrow_records

        JOIN books
        ON books.id = borrow_records.book_id

        WHERE borrow_records.user_id=%s

        ORDER BY borrow_records.borrow_date DESC
    """, (user_id,))

    records = cur.fetchall()

    cur.close()

    return render_template(
        "my_books.html",
        records=records
    )

# ==================================================
# RETURN BOOK
# ==================================================

@app.route('/return-book/<int:borrow_id>')
def return_book(borrow_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    # Get book_id from borrow record
    cur.execute("""
        SELECT book_id
        FROM borrow_records
        WHERE id=%s
    """, (borrow_id,))

    record = cur.fetchone()

    if not record:
        cur.close()
        return "Invalid Record"

    book_id = record[0]

    # Update borrow record
    cur.execute("""
        UPDATE borrow_records
        SET status='Returned',
            return_date=CURDATE()
        WHERE id=%s
    """, (borrow_id,))

    # Increase stock
    cur.execute("""
        UPDATE books
        SET available_copies = available_copies + 1
        WHERE id=%s
    """, (book_id,))

    mysql.connection.commit()
    cur.close()

    return redirect('/my-books')
@app.route('/admin/dashboard')
def admin_dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    cur = mysql.connection.cursor()

    # ==========================
    # Statistics
    # ==========================

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("SELECT SUM(available_copies) FROM books")
    available_books = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT COUNT(*)
        FROM borrow_records
        WHERE status='Borrowed'
    """)
    borrowed_books = cur.fetchone()[0]

    # ==========================
    # Top 5 Trending Books
    # ==========================

    cur.execute("""
        SELECT
            b.id,
            b.title,
            b.author,
            COUNT(br.book_id) AS borrow_count
        FROM books b
        LEFT JOIN borrow_records br
            ON b.id = br.book_id
        GROUP BY
            b.id,
            b.title,
            b.author
        ORDER BY borrow_count DESC
        LIMIT 5
    """)

    trending_books = []

    for row in cur.fetchall():
        trending_books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "borrow_count": row[3]
        })

    # ==========================
    # Recently Added Books
    # ==========================

    cur.execute("""
        SELECT
            id,
            title,
            author
        FROM books
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_books = []

    for row in cur.fetchall():
        recent_books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2]
        })

    # ==========================
    # AI Recommendations
    # ==========================

    cur.execute("""
        SELECT
            id,
            title,
            author,
            genre,
            ai_description
        FROM books
        ORDER BY RAND()
        LIMIT 3
    """)

    recommendations = []

    for row in cur.fetchall():
        recommendations.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "genre": row[3],
            "ai_description": row[4] if row[4] else "AI summary not available."
        })

    cur.close()

    stats = {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "total_users": total_users
    }

    return render_template(
    "dashboard.html",
    name=session["name"],
    role=session["role"],
    stats=stats,
    trending_books=trending_books,
    recent_books=recent_books,
    recommendations=recommendations
)
# ==================================================
# ADMIN - VIEW ALL BORROWED BOOKS
# ==================================================

@app.route('/admin/borrowed-books')
def admin_borrowed_books():

    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return "Access Denied"

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            borrow_records.id,
            users.name,
            users.email,
            books.title,
            books.author,
            borrow_records.borrow_date,
            borrow_records.return_date,
            borrow_records.status

        FROM borrow_records

        JOIN users
        ON users.id = borrow_records.user_id

        JOIN books
        ON books.id = borrow_records.book_id

        ORDER BY borrow_records.borrow_date DESC
    """)

    records = cur.fetchall()

    cur.close()

    return render_template(
        "admin_borrowed_books.html",
        records=records
    )

# ==================================================
# OPTIONAL: SIMPLE HOME REDIRECT LOGIC
# ==================================================

@app.route('/home')
def home_redirect():

    if 'user_id' in session:
        return redirect('/dashboard')

    return redirect('/login')

# ==================================================
# RUN APP
# ==================================================

if __name__ == '__main__':
>>>>>>> f040d97 (Add project modifications)
    app.run(debug=True)