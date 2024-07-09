from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Users(db.Model):
    __tablename__ ="Userinformation"


    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(55),nullable=False,unique=True)
    password=db.Column(db.String(120),nullable=False)
    name = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(1200),nullable=False)


    def __repr__(self):
           return '<Users %r>' %self.username

class AppointmentBooking(db.Model):
    __tablename__ = "AppointmentsData"

    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    service=db.Column(db.String(100),nullable=False)
    date=db.Column(db.String(100),nullable=False)
    time=db.Column(db.String(100),nullable=False)
    status=db.Column(db.String(100),nullable=False,default='Booked')
    def __repr__(self):
        return '<Appointment %r>' %self.name