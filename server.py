"""Server for appointment reminder app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'maryskey'
app.jinja_env.undefined = StrictUndefined




@app.route('/')
def show_homepage():
    """Renders the signup page"""
    if session.get('stylist') != None:
        return redirect('/login')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET'])
def show_login():
    """Renders the login page"""
    if session.get("stylist") == None:
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
    """Creates a new salon/user and stores it in the database"""

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

    customer = crud.create_customer(first_name, last_name, text_num, landline, email)
    return redirect('/add_appointment', customer_id=customer.customer_id)


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
    
    appts = crud.get_appointment(customer_id)
    
    return render_template('choose_appointment.html', appts=appts)
   




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

