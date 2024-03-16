from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer, String, Float
class Base(DeclarativeBase):
  pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pog.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
all_books = [

]




class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250),nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=False)



with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Books).order_by(Books.title))
        all_books = result.scalars().all()
        print(all_books)
    return render_template("index.html", all_books=all_books)


@app.route("/add",methods=["GET","POST"])
def add():
    if request.method =="POST":
        book = Books(
            title= request.form["name"],
            author = request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(book)
        db.session.commit()
        # with app.app_context():
        #     result = db.session.execute(db.select(Books).order_by(Books.title))
        #     all_books = result.scalars().all()
        #     print(all_books)
        return redirect(url_for('home'))
    else:
      return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    if request.method =="GET":
        with app.app_context():
            book = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
            print (book)
        return render_template("edit.html", book=book)
    if request.method == "POST":
        with app.app_context():
            book_to_update = db.session.execute(db.select(Books).where(Books.id == request.form["id"])).scalar()
            print(book_to_update)
            book_to_update.rating = request.form["rating"]
            db.session.commit()
        return redirect(url_for('home'))

@app.route("/delete", methods=["GET","POST"])
def delete():
    book_id = request.args.get("id")
    print (book_id)
    with app.app_context():
        book_to_delete = db.get_or_404(Books, book_id)
        print(book_to_delete)
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for("home"))
if __name__ == "__main__":
    app.run(debug=True)

