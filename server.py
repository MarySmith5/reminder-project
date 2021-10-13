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
    
    flash("You are now logged in!")
    return redirect('/appointments')