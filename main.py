from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Set the database URI for SQLite
db = SQLAlchemy(app)


# Define the Book model using SQLAlchemy
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)


# Route to display a list of books
@app.route('/books')
def books():
    books_list = Book.query.all()  # Retrieve all books from the database
    return render_template('books.html', books=books_list)


# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get book information from the form
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']

        # Create a new Book object and add it to the database
        new_book = Book(title=title, author=author, publication_year=publication_year)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('books'))  # Redirect to the book list page after adding a new book

    return render_template('add_book.html')  # Render the form to add a new book


# Run the application if this script is executed
if __name__ == '__main__':
    db.create_all()  # Create the database tables
    app.run(debug=True)
