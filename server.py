"""Server for appointment reminder app."""

import arrow
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, Appointment
import crud
from jinja2 import StrictUndefined
from datetime import datetime, date, timedelta, time
import os
from celery import Celery



app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

USER_SESSION = session

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        #timezone=app.config['TIMEZONE']
    )
    
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# Falsey: False, None, "", [], {}, ()
@app.route('/')
def show_homepage():
    """Renders the signup page"""
    
    if session.get('stylist'): 
        return redirect('/login')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET'])
def show_login():
    """Renders the login page"""
    if not session.get("stylist"):
        return redirect('/')

    else:
        return render_template('homepage.html')


@app.route('/login', methods=['POST'])
def process_login():
    """Checks if login info is in our session"""
    password = request.form.get('entry_password')
   
    if password != session.get('password'):
        flash("Invalid password")
        return redirect('/login')

    else:
        flash(f"Hi, {session['stylist']}! You are now logged in.")
        return redirect('/customer_options')


@app.route('/', methods=['POST'])
def create_account():
    """Creates a new stylist/user and stores it in the session"""

    session['stylist'] = request.form.get('stylist')
    session['business_name'] = request.form .get('business')
    session['contact_number'] = request.form.get('contact')
    session['password'] = request.form.get('password')
    #session['timezone'] = request.form.get('timezone')

    return redirect("/login")
    

@app.route('/customer_options')
def opt_customers():
    """Render template to choose to create or find customer"""
    return render_template('cust_opt.html')


@app.route('/new_customer')
def get_new_customer():
    """Renders template to create a new customer"""
    return render_template('new_customer.html')


@app.route('/new_customer', methods=['POST'])
def process_new_customer():
    """Creates a new customer"""
    first_name = request.form.get('first_name').title()
    last_name = request.form.get('last_name').title()
    text_num_data = request.form.get('text_num')

    if not text_num_data.isdigit() or len(text_num_data) != 10:
        flash("Invalid phone number. Please enter 10 digits without spaces or other characters.")
        return render_template('new_customer.html')
    else:
        text_num = f"+1{text_num_data}"

    landline = request.form.get('landline')
    email = request.form.get('email')

    if crud.check_existing_cust(first_name, last_name, text_num):
        flash("This customer already exists.")
        return redirect('/customer_options')
    else:
        customer = crud.create_customer(first_name, last_name, text_num, landline, email)
        number = f"({customer.text_num[2:5]}){customer.text_num[5:8]}-{customer.text_num[8:]}"
        flash(f'{customer.first_name} {customer.last_name} {number} has been added to the database.')
        return redirect(f'/add_appointment/{customer.customer_id}')


@app.route('/customer_options', methods=['POST'])
def find_customer():
    first_name = request.form.get('first_name').title()
    last_name = request.form.get('last_name').title()
    customers = crud.get_cust(first_name, last_name)
    if customers:
        return render_template('customers.html', customers=customers)
    else:
        flash(f"There are no customers named {first_name} {last_name}.")
        return redirect('/customer_options')


@app.route("/customers/<customer_id>")
def view_customer_appointments(customer_id):
    """Shows all existing appointments of a customer"""
    name = crud.get_cust_fname(customer_id)
    appts = crud.get_appointment(customer_id)
    return render_template('choose_appointment.html', appts=appts, customer_id=customer_id, name=name)


@app.route("/add_appointment/<customer_id>")
def create_appt(customer_id):
    """Renders the add_appointment template"""
    name = crud.get_cust_fname(customer_id)
    return render_template('add_appointment.html', customer_id=customer_id, name=name)


@app.route("/process_new_appt", methods=['POST'])
def process_appt():
    """Takes info from form and creates an appointment"""
    customer_id = request.form.get('customer_id')
    gen_service = request.form.get('gen_service')
    specific_service = request.form.get('specific_service')
    date_data = request.form.get('date')
    time_data = request.form.get('time')
    timezone = request.form.get('timezone')
    duration = request.form.get('duration')
    greeting = request.form.get('greeting')
    closing = request.form.get('closing')

   
    date = datetime.strptime(date_data, "%Y-%m-%d")
    d = datetime.date(date)
    time = datetime.strptime(time_data, "%H:%M")
    t = datetime.time(time)
    read_time = t.strftime("%I:%M %p")
    read_date = d. strftime("%A, %B %e")
 #date_time = arrow.Arrow(year=d.year, month=d.month, day=d.day, hour=t.hour, minute=t.minute, tzinfo=session['timezone']).to('utc').naive
    date_time = datetime.combine(d, t)
    # import pdb # python debugger
    # pdb.set_trace()
    first_name = crud.get_cust_fname(customer_id)
    body = f"{first_name}, you have a {gen_service} appointment  at {session['business_name']} on {read_date} at {read_time}. Click the above date to add it to your calendar. Thank you!!!"
    body_1 = f"{greeting} {first_name}, remember your {gen_service} appointment TOMORROW, {read_date} at {read_time}. \nIf this doesn't work, contact {session['stylist']} at {session['contact_number']} {closing}."
    body_2 = f"{greeting} {first_name}, remember your {gen_service} appointment TODAY, {read_date} at {read_time}. \nIf this doesn't work, contact {session['stylist']} at {session['contact_number']} {closing}."
    
    appt = crud.create_appointment(customer_id, 
                                   gen_service,  
                                   date_time,
                                   date,
                                   time,
                                   timezone, 
                                   duration,
                                   specific_service,
                                   body, 
                                   body_1, 
                                   body_2)
    
    flash(f"{first_name} has a {gen_service} appointment on {date_data} at {read_time}.")
    return render_template('another_appt.html', customer_id=appt.customer_id)


@app.route('/appts/<appoint_id>')
def offer_cancel(appoint_id):
    """Gives the option to cancel a specific appointment"""
    appointment = crud.get_appt_by_id(appoint_id)
    cust = crud.get_cust_by_appt_id(appoint_id)
    return render_template('cancel.html', appointment=appointment, customer_id=cust)


@app.route("/canceled/<appoint_id>", methods=['POST'])
def cancel_appt(appoint_id):
    """Marks an appointment as canceled"""
    appointment = crud.cancel_appt(appoint_id)
    flash(f"{appointment.my_customer.first_name} {appointment.my_customer.last_name}'s {appointment.date} appointment is CANCELED.")
    return redirect('/customer_options')


# @app.route("/get-user-timezone", methods=['GET'])
# def get_user_timezone():S
#     return jsonify({'timezone': session.get('timezone', datetime.today())}) 


#tasks.every_morning()


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

