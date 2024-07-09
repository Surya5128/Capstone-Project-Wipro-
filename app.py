from flask import Flask,request,jsonify
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from models import Users,AppointmentBooking,db
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Password%401@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='SECRET KEY'



db.init_app(app)

with app.app_context():
    db.create_all()
@app.route('/register',methods=['POST'])
def register():
    data = request.json
    print("received register request with data",data)
    username = data['username']
    password = data['password']
    name = data['name']
    email = data['email']

    if not username and not password and not name and not email:
        print("Missing details",data)
        return jsonify({"message":"Missing details"})


    if Users.query.filter((Users.username == username) | (Users.email == email)).first():
        return jsonify({'message':'Username or Email already exists'}),400
    new_user = Users(username=username,password=password,name=name,email=email)
    db.session.add(new_user)
    db.session.commit()
    print("register successful",new_user)
    return jsonify({'message':'Username registered successfully'}),201
@app.route('/login',methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = Users.query.filter_by(username=username,password=password).first()
    if user:
        return jsonify({'message':'Login successful'}),200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

def slot_available(date,time,id=None):
    query=AppointmentBooking.query.filter_by(date=date,time=time)
    if id:
        query=query.filter(AppointmentBooking.id != id)
    return query.count() == 0

@app.route('/appointment',methods=['GET'])
def getappointments():
    appointments=AppointmentBooking.query.all()
    return [{'id':app.id,'name':app.name,'service':app.service,
             'date':app.date,'time':app.time,'status':app.status} for app in appointments]

@app.route('/appointment',methods=['POST'])
def createappointment():
    data = request.json

    name=request.json["name"]
    service=request.json["service"]
    date=request.json["date"]
    time=request.json["time"]
    status=request.json["status"]

    if not (name and service and date and time and status):
        return jsonify({"message":"Missing Details"}),400

    if not slot_available(date,time):
        return jsonify({"message":"Slot not Available"}),400
    appointment=AppointmentBooking(name=name,service=service,date=date,time=time,status=status)
    db.session.add(appointment)
    db.session.commit()
    return jsonify({"message":"Appointment Booked Successfully"})

@app.route('/appointment/<int:id>',methods=['PUT'])
def updateappointment(id):
    appointment=AppointmentBooking.query.get_or_404(id)
    data = request.json

    newdate=data["date"]
    newtime=data["time"]

    if not slot_available(newdate,newtime,id):
        return jsonify({"message":"Slot Not Available"})
    appointment.name=data["name"]
    appointment.service = data["service"]
    appointment.status = data["status"]
    appointment.date = newdate
    appointment.time=newtime

    db.session.commit()
    return jsonify({"message":"Appointment Details Updated Successfully"})

@app.route('/appointment/<int:id>',methods=['DELETE'])
def cancelappointment(id):
    appointment=AppointmentBooking.query.get_or_404(id)

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message":"Appointment Cancelled Successfully"})





if __name__ == '__main__':
    app.run()
