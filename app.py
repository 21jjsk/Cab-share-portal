from flask import Flask, request, jsonify
from service import *
from models import *
import json

app = Flask(__name__)


#
@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def hello():
    return "Hello World!"


# Work in progress starts here
# Student
# verified it works
# {
#     "s_id": 321,
#     "name": "jeevan",
#     "email":"jj@abc.com",
#     "password":"hahlfhlfl",
#     "gender":"male",
#     "phone_no":4313313,
#     "room_no":"v234"
#
# }
@app.route("/CreateStudent", methods=["POST"])
def create_student():
    StudentService().create(request.get_json())
    return "works"
    # return what???


# verified. this route works
@app.route("/LoginStudent", methods=["POST"])
def list_student():
    data = request.get_json()
    print(data)
    s_id = data.get('s_id')
    password = data.get('password')
    temp = StudentService().get_details(s_id, password)
    print(temp)

    return json.dumps(temp)  # returns in the form of ["123", "tan", "tan@xyz.com", "56778", "t45747", "netye"]


# Admin verified
# to fix admin ID  set to NULL for first person
# {
#     "name": "hriday",
#     "email":"HG@abc.com",
#     "password":"hhlfl",
#     "phone_no":77813313
#
# }
@app.route("/admin", methods=["POST"])
def login_admin():
    data = request.get_json()
    print(data.get('admin_id')+" "+ data.get('password'))
    result=AdminService().search(data.get('admin_id'), data.get('password'))
    print(result)
    return json.dumps(result)
    # return what???


# Car
# verified
# {
#     "car_no": 34783,
#     "admin_id": 1,
#     "model":"hhlfl",
#     "car_capacity":7,
#     "driver_name":"ram",
#     "driver_phone":3737373737
#
# }
@app.route("/car", methods=["POST"])
def create_car():
    CarService().create(request.get_json())
    return "car inserted"

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route("/findCar", methods=["POST"])
def find_car():
    CarService().create(request.get_json())


# Pickup details
@app.route("/pickup", methods=["POST"])
def create_pickup():
    Pickup_details_Service().create(request.get_json())
    return "successs"


# Trip
@app.route("/trip", methods=["POST"])
def create_trip():
    TripService().create(request.get_json())
    return "works"


@app.route("/trip_history", methods=["POST"])
def trip_history():
    data = request.get_json()
    s_id = data.get('s_id')
    return json.dumps(TripService().trip_history(s_id))


# /trip/findtrip?source=Campus&destination=Airport&leave_by_earliest=blah&leave_by_latest=blah
@app.route("/findtrip", methods=["POST"])
def find_trip():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    leave_by_earliest = data.get('leave_by_earliest')
    leave_by_latest = data.get('leave_by_latest')
    return jsonify(TripService().search(source, destination, leave_by_earliest, leave_by_latest))


@app.route("/trip/<trip_id>", methods=["PUT"])
def update_item(trip_id):
    return jsonify(TripService().update(trip_id, request.get_json()))


@app.route("/todo/<trip_id>", methods=["DELETE"])
def delete_item(trip_id):
    return jsonify(TripService().delete(trip_id))


# Work in progress ends here


if __name__ == "__main__":
    Schema()
    app.run(debug=True)
