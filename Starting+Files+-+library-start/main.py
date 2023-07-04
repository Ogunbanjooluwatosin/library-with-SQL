# ======================imports============
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///book.db"

db = SQLAlchemy()
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False, unique=True)
    title = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


# ======================Create The Tables============
with app.app_context():
    db.create_all()


# ======================routes============

@app.route('/')
def home():
    # to read tables
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(
            author=request.form['author'],
            title=request.form['title'],
            rating=request.form['rating']
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    # to update a field
    if request.method == 'POST':
        book_id = request.form['id']
        updated_book = db.get_or_404(Book, book_id)
        updated_book.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get("id")
    selected_book = db.get_or_404(Book, book_id)
    return render_template('edit.html', book=selected_book)


@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
