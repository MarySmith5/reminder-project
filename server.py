"""Server for appointment reminder app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
from datetime import datetime, date, timedelta, time

app = Flask(__name__)
app.secret_key = 'maryskey'
app.jinja_env.undefined = StrictUndefined

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
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    text_num = request.form.get('text_num')
    landline = request.form.get('landline')
    email = request.form.get('email')
    if crud.check_existing_cust(first_name, last_name, text_num):
        flash("This customer already exists.")
        return redirect('/customer_options')
    else:
        customer = crud.create_customer(first_name, last_name, text_num, landline, email)
        flash(f'{customer} has been added to the database.')
        return redirect(f'/add_appointment/<{customer.customer_id}>')


@app.route('/customer_options', methods=['POST'])
def find_customer():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    customers = crud.get_cust(first_name, last_name)
    if customers:
        return render_template('customers.html', customers=customers)
    else:
        flash(f"There are no customers named {first_name} {last_name}.")
        return redirect('/customer_options')


@app.route("/customers/<customer_id>")
def view_customer_appointments(customer_id):
    """Shows all existing appointments of a customer"""
    
    appts = crud.get_appointment(customer_id)
    return render_template('choose_appointment.html', appts=appts, customer_id=customer_id)


@app.route("/add_appointment/<customer_id>")
def create_appt(customer_id):
    """Renders the add_appointment template"""
    return render_template('add_appointment.html', customer_id=customer_id)


@app.route("/process_new_appt", methods=['POST'])
def process_appt():
    """Takes info from form and creates an appointment"""
    customer_id = request.form.get('customer_id')
    gen_service = request.form.get('gen_service')
    specific_service = request.form.get('specific_service')
    date_data = request.form.get('date')
    time_data = request.form.get('time')
    duration = request.form.get('duration')

   
    date = datetime.strptime(date_data, "%Y-%m-%d")
    d = datetime.date(date)
    time = datetime.strptime(time_data, "%H:%M")
    t = datetime.time(time)
    date_time = datetime.combine(d, t)
    
    when_send1 = date_time + timedelta(days=-1)
    first_name = crud.get_cust_fname(customer_id)
    body_1 = f"Hi, {first_name}! Remember your {gen_service} appointment tomorrow at {time_data}. \nIf this doesn't work, contact {session['stylist']} at {session['contact_number']}."
    when_send2 = date_time + timedelta(hours=-2)
    body_2 = f"Hi, {first_name}! Remember your {gen_service} appointment TODAY at {time_data}. \nIf this doesn't work, contact {session['stylist']} at {session['contact_number']}."
    when_send2 = date_time + timedelta(hours=-2)

    appt = crud.create_appointment(customer_id, 
                                   gen_service, 
                                   specific_service, 
                                   date_time, 
                                   duration, 
                                   body_1, 
                                   when_send1,
                                   body_2,
                                   when_send2)

    flash(f"{first_name} has a {gen_service} appointment on {date_data} at {time_data}.")
    return render_template('another_appt.html', customer_id=customer_id)


@app.route('/appts/<appoint_id>')
def offer_cancel(appoint_id):
    """Gives the option to cancel a specific appointment"""
    appointment = crud.get_appt_by_id(appoint_id)
    cust = crud.get_cust_by_appt_id(appoint_id)
    return render_template('cancel.html', appointment=appointment, customer_id=cust)


@app.route("/canceled/<appoint_id>")
def cancel_appt(appoint_id):
    """Marks an appointment as canceled"""
    appointment = crud.get_appt_by_id(appoint_id)
    appointment.is_canceled = True
    flash(f"{appointment} is CANCELED.")
    return redirect('/customer_options')





# @app.route('/appointments')
# def appointment_options():
#     """Find an existing appointment or choose to create a new appointment."""
#     return render_template('appt_opt.html')


# @app.route('/show_appointments', methods=['POST'])
# def show_appointments():
#     """Shows list of appointments for given first and last customer name"""

#     first_name = request.form.get('first_name')
#     last_name = request.form.get('last_name')

#     customers = crud.get_customers(first_name, last_name)
#     if customers == None:
#         flash("No customers exist by that name.")
#         return redirect('new_appointment.html')

#     else:
#         return crud.get_appointment(cust_id)



# @app.route('/make_appointment')
# def add_appointment():
    
#     return render_template('new_appointment.html')



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

