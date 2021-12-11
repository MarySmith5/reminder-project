"""Models for reminder app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
import arrow

db = SQLAlchemy()


class Customer(db.Model):
    """A person receiving a service"""

    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    text_num = db.Column(db.String(25))
    landline = db.Column(db.String(25))
    email = db.Column(db.String(50))

    appts = db.relationship('Appointment', back_populates='my_customer')

    def __repr__(self):
        """Show info about a customer"""
        return f"{self.first_name} {self.last_name} ({self.text_num[2:5]}){self.text_num[5:8]}-{self.text_num[8:]}"


    

class Appointment(db.Model):
    """A scheduled event"""

    __tablename__ = "appointments"

    appoint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    gen_service = db.Column(db.String(25), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    timezone = db.Column(db.String(25), nullable=False)
    duration = db.Column(db.Interval)
    specific_service = db.Column(db.String(100))
    body = db.Column(db.Text)
    body_1 = db.Column(db.Text)
    body_2 = db.Column(db.Text)
    is_canceled = db.Column(db.Boolean)
    sent_1 = db.Column(db.Boolean)
    sent_2 = db.Column(db.Boolean)
    

    my_customer = db.relationship("Customer", back_populates="appts")
    
    def __repr__(self):
        """Show info about an appointment"""
        return f"Service= {self.gen_service}, date= {self.date} time= {self.time}, CANCELED= {self.is_canceled}"

    def get_readable_time(self):
        t = (self.time)
        read_time = t.strftime("%I:%M %p")
        return read_time


    def get_remind_time1(self):
        appointment_time = arrow.get(self.date_time)
        reminder_time1 = appointment_time.shift(days=-1)
        return reminder_time1

    def get_remind_time2(self):
        appointment_time = arrow.get(self.date_time)
        reminder_time2 = appointment_time.shift(hours=-3)
        return reminder_time2



def connect_to_db(flask_app, db_uri="postgresql:///reminders", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    
    connect_to_db(app, echo=False)












