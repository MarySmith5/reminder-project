"""Server for appointment reminder app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def homepage():
    """Renders the homepage"""

    return render_template('homepage.html')


@app.route('/', methods=['POST'])
def process_login():
    """Checks if login info is in our database"""

    email = request.form.get('email')
   
    password = request.form.get('password')
   
    salon = crud.get_salon_by_email(email)

    if not salon:
        flash("Invalid email")
        return redirect('/')
    
    if salon.password != password:
        flash("Invlaid password")
        return redirect('/')


    session['salon'] = salon.email
    
    flash(f"Hi, {salon.salon_name}! You are now logged in.")
    return redirect('/appointments')


@app.route('/signup', methods=['GET'])
def signup():
    """Renders the page to create an account"""

    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def create_account():
    """Creates a new salon/user and stores it in the database"""

    salon_email = request.form.get('email')
    salon_name = request.form .get('salon_name')
    password = request.form.get('password')

    user = crud.get_salon_by_email(email)

    if user:
        flash("Account already exists with that email. Try again.")
        return redirect('/signup')
    else:
        crud.create_salon(salon_name, salon_email, password)
        flash("Account created! Please log in.")
        return redirect('/')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

