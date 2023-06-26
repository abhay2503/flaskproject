from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/library'

db = SQLAlchemy(app)


class bookdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    pages = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    genre = db.Column(db.String(40), nullable=False)


class issuedetails(db.Model):
    inid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    bookid = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(100), nullable=False)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/bookissue")
def issue():
    return render_template('issue.html')


@app.route("/viewby")
def view():
    return render_template('viewby.html')




@app.route("/insertdetails", methods=["GET", "POST"])
def insert():

    data = request.json
    name = data["name"]
    pages = data["pages"]
    price = data["price"]
    author = data["author"]
    genre = data["genre"]

    # current_date = datetime.now().date()

    new = bookdetails(
        name=name, pages=pages, price=price, author=author, genre=genre)

    db.session.add(new)
    db.session.commit()
    response = jsonify({'success': True})
    return response


@app.route("/showbooks", methods=["POST"])
def showbooks():
    data = request.json
    genre = data["genre"]
    dat = db.session.query(bookdetails.name, bookdetails.id).distinct().filter(
        bookdetails.genre == genre).all()
    dat_list = []
    for result in dat:
        book = {
            "name": result[0],
            "id": result[1]
        }
        dat_list.append(book)

    return jsonify(dat_list)


@app.route("/insertissued", methods=["POST"])
def insertissued():
    data = request.json
    name = data["name"]
    phone = data["phone"]
    bookid = data["books"]
    date = data["date"]
    address = data["address"]
    new = issuedetails(name=name, phone=phone, bookid=bookid,
                       date=date, address=address)
    db.session.add(new)
    db.session.commit()
    response = jsonify({'success': True})
    return response


@app.route("/issuename", methods=["POST"])
def issuename():
    dat = db.session.query(issuedetails.name).distinct().all()
    dat_list = []
    for result in dat:
        dat_list.append(result[0])

    print(dat_list)
    return jsonify(dat_list)


@app.route("/genrebooks", methods=["POST"])
def genrebooks():
    data = request.json
    genre = data["genre"]
    dat = db.session.query(bookdetails).filter(
        bookdetails.genre == genre).all()
    dat_list = []
    for i in dat:
        li = {
            "id": i.id,
            "name": i.name,
            "pages": i.pages,
            "price": i.price,
            "author": i.author
        }
        dat_list.append(li)

    return jsonify(dat_list)


@app.route("/viewbyname", methods=["POST"])
def viewbyname():
    data = request.json
    name = data["name"]
    dat = db.session.query(issuedetails).filter(
        issuedetails.name == name).all()
    dat_list = []

    for i in dat:

        l = {
            "id": i.inid,
            "name": i.name,
            "phone": i.phone,
            "bookid": i.bookid,
            "date": i.date,
            "address": i.address
        }
        dat_list.append(l)

    print(dat_list)
    return jsonify(dat_list)


@app.route("/viewbytime", methods=["POST"])
def viewbytime():
    data = request.json
    start = datetime.strptime(data['start'], "%Y-%m-%d").date()
    end = datetime.strptime(data['end'], "%Y-%m-%d").date() + timedelta(days=1)
    dat = issuedetails.query.filter(
        issuedetails.date.between(start, end)).all()
    li = []

    for i in dat:
        l = {
            "id": i.inid,
            "name": i.name,
            "phone": i.phone,
            "bookid": i.bookid,
            "date": i.date,
            "address": i.address
        }
        li.append(l)
    # print(li)
    return jsonify(li)





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
