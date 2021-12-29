from datetime import datetime
#import pytz
#from flask import session
import os
from twilio.rest import Client
from model import Appointment, connect_to_db, db
import crud
from server import app, make_celery
from celery import Celery, chain

from celery.schedules import crontab
from celery.utils.log import get_task_logger
#import requests

logger = get_task_logger(__name__)

twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_NUMBER']
client = Client(twilio_account_sid, twilio_auth_token)

connect_to_db(app)


# def get_user_timezone():
#     response = requests.get('http://localhost:5000/get-user-timezone')
#     result = response.json()
#     return result['timezone'][-3:]

# app.conf.timezone = 'US/Mountain'
# app.conf.timezone = session['timezone']
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
    
celery = make_celery(app)

# print('TIMEZONE!!!!', app.config['TIMEZONE'])

def send_sms_reminder_now(appoint_id):
    logger.info("HI" * 20)
    appointment = Appointment.query.filter_by(appoint_id=appoint_id).one()
    if appointment.is_canceled == False:
        
        body = appointment.body
        to = appointment.my_customer.text_num
        client.messages.create(body=body, from_=twilio_number, to=to)

        
# @celery.task
# def process_remind1(appoint_id):
#     remind1 = chain(send_sms_reminder1.s(appoint_id=appoint_id), mark_as_sent1.s())
#     remind1()        


@celery.task
def send_sms_reminder1(appoint_id):
    logger.info("HI" * 20)
    now = datetime.utcnow()
    appointment = Appointment.query.filter_by(appoint_id=appoint_id).one()
    if now > appointment.date_time:
        appointment.is_canceled = True
        db.session.commit()
    if appointment.is_canceled == False and appointment.sent_1 == False:

        body = appointment.body_1
        to = appointment.my_customer.text_num
        msg = client.messages.create(body=body, from_=twilio_number, to=to)
        if msg.error_code == None:
            appointment.sent_1 = True
            db.session.commit()


# @celery.task
# def mark_as_sent1( appoint_id, msg):
#     appointment = Appointment.query.filter_by(appoint_id=appoint_id).one()
#     if msg.sid:
#         appointment.sent_1 = True
#         db.session.commit()


# @celery.task
# def process_remind2(appoint_id):
#     remind2 = chain(send_sms_reminder2.s(appoint_id=appoint_id), mark_as_sent2.s())
#     remind2()   



@celery.task
def send_sms_reminder2(appoint_id):
    # logger.info("Hey" * 20)
    now = datetime.utcnow()
    appointment = Appointment.query.filter_by(appoint_id=appoint_id).one()
    if now > appointment.date_time:
        appointment.is_canceled = True
        db.session.commit()
    if appointment.is_canceled == False and appointment.sent_2 == False:

        body = appointment.body_2
        to = appointment.my_customer.text_num
        msg = client.messages.create(body=body, from_=twilio_number, to=to)
        if msg.error_code == None:
            appointment.sent_2 = True
            db.session.commit()


# @celery.task
# def mark_as_sent2( appoint_id, msg):
#     appointment = Appointment.query.filter_by(appoint_id=appoint_id).one()
#     if msg.sid:
#         appointment.sent_2 = True
#         db.session.commit()
        


# {
#   "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#   "api_version": "2010-04-01",
#   "body": "Hi there",
#   "date_created": "Thu, 30 Jul 2015 20:12:31 +0000",
#   "date_sent": "Thu, 30 Jul 2015 20:12:33 +0000",
#   "date_updated": "Thu, 30 Jul 2015 20:12:33 +0000",
#   "direction": "outbound-api",
#   "error_code": null,
#   "error_message": null,
#   "from": "+14155552345",
#   "messaging_service_sid": null,
#   "num_media": "0",
#   "num_segments": "1",
#   "price": null,
#   "price_unit": null,
#   "sid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#   "status": "sent",
#   "subresource_uris": {
#     "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Media.json"
#   },
#   "to": "+14155552345",
#   "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
# }



# @celery.task
# def first_reminder():
#     """Processes sending the first reminder for each appoinment in a list"""
#     appts1 = crud.get_remind1()
#     print(appts1)
#     for appt in appts1:
#         send_sms_reminder(appt.appoint_id, appt.body_1, appt.send_1)

        
# @celery.task
# def second_reminder():
#     """Processes sending the second reminder for each appoinment in a list"""
#     appts2= crud.get_remind2()
#     print(appts2)
#     for appt in appts2:
#         send_sms_reminder(appt.appoint_id, appt.body_2, appt.send_2)


# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
    
#     # Executes every morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=22, minute=5),
#         first_reminder.s(),
#     )
#     sender.add_periodic_task(
#         crontab(hour=22, minute=5),
#         second_reminder.s(),
#     )

        

        
       







