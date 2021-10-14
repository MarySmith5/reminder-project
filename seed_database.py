import os
import crud
import model
import server

os.system('dropdb reminders')
os.system('createdb reminders')

model.connect_to_db(server.app)
model.db.create_all()

crud.create_salon('Test Salon', 'test@test.com', 'tester')
crud.create_stylist('Testana Testalini', 555-214-2626, 1)
crud.create_customer('Customer', 'Try', 555-123=4567, None, 'customer@test.test')
crud.create_appointment(1, 1, 'hair', 'woman cut', datetime.strptime(11-2-2021, "%-m-%-d-%Y"), datetime.strptime(4-30-PM, "%-I-%M-%p"), datetime.strptime(5-15-PM, "%-I-%M-%p"))
crud.create_reminder(1, 'Remember hair today at 4:30', datetime.strptime(11-2-2021 8-00-AM, "%-m-%-d-%Y %-I-%M-%p"), datetime.strptime(11-1-2021 8-00-AM, "%-m-%-d-%Y %-I-%M-%p"))


