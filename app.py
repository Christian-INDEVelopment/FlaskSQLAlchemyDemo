from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

#Configuring Flask and DB
flask_app = Flask(__name__)
flask_app.debug = True
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flask_app)

#DB Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=False, nullable=False)
    email = db.Column(db.String(32), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    #Provides a meaningful string representation of a model instance.
    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"

#Flask routes
@flask_app.route('/')
def index():
    #Gets all users and sends it to index.html.
    users = User.query.all()
    return render_template('index.html', users=users)

@flask_app.route('/add_data')
def add_data():
    return render_template('add_user.html')

@flask_app.route('/add', methods=["POST"])
def users():

    #Gets info from /add_data
    username = request.form.get("username")
    email = request.form.get("email")
    age = request.form.get("age")

    #Checking the fields to make sure they aren't empty.
    if username is not None and email is not None and age is not None:
        #Defines the user, adds it to db, then commits it.
        u = User(username=username, email=email, age=age)
        db.session.add(u)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@flask_app.route('/delete/<int:id>')
def erase(id): 
    #Gets the id from the url and deletes it.
    data = User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

#Ensures the app only runs here, and not as a module into another script.
if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()

    flask_app.run(debug=True)
