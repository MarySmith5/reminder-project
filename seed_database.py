import os
import crud
import model
import server
from datetime import datetime, time

os.system('dropdb reminders')
os.system('createdb reminders')

model.connect_to_db(server.app)
model.db.create_all()


crud.create_customer('Customer', 'Try', '5551234567', '5551234568', 'customer@test.test')
crud.create_customer('Another', 'Customer', '2385554444', None, None)
crud.create_customer('Jane', 'Doe', '5678994444', None, None)
crud.create_customer('Mary', 'Smith', '3333333333', None, None)
crud.create_customer('Mary', 'Smith', '2222222222', None, None)

crud.create_appointment(1, 'hair', datetime(2021, 12, 2, 16, 30), datetime(2021, 12, 2), time(hour=16, minute=30), "US/Mountain", "0:45", 'woman cut', "Boo", "HI", "hello", True, False, False)
crud.create_appointment(2, 'hair', datetime(2021, 12, 3, 16, 30), datetime(2021, 12, 3), time(hour=16, minute=30), "US/Mountain", "0:30", 'man cut', "Boo", "HI", "hello", True, False, False)
crud.create_appointment(3, 'hair', datetime(2021, 12, 4, 16, 30), datetime(2021, 12, 4), time(hour=16, minute=30), "US/Mountain", "0:45", 'highlights', "Boo", "HI", "hello", True, False, False)
crud.create_appointment(4, 'hair', datetime(2021, 12, 15, 16, 30), datetime(2021, 12, 15), time(hour=16, minute=30), "US/Mountain", "0:45", 'highlights', "Boo", "HI", "hello", True, False, False)
crud.create_appointment(5, 'nail', datetime(2021, 12, 7, 12, 30),  datetime(2021, 12, 7), time(hour=12, minute=30), "US/Mountain", "0:30", 'full set', "Boo", "HI", "hello", True, False, False)




