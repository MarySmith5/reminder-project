import os
import crud
import model
import server
from datetime import datetime

os.system('dropdb reminder# s')
os.system('createdb reminders')

model.connect_to_db(server.app)
model.db.create_all()



crud.create_customer('Customer', 'Try', 5551234567, None, 'customer@test.test')
crud

crud.create_appointment(1, 1, 'hair', 'woman cut', datetime.datetime(2021, 11, 2, 16, 30), datetime.strptime(4-30-PM, "%-I-%M-%p"), datetime.strptime(5-15-PM, "%-I-%M-%p"))


