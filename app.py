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
def create_admin():
    AdminService().create(request.get_json())
    # return what???
    return "posssst"


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


# /trip/findtrip?source=Campus&destination=Airport&leave_by_earliest=blah&leave_by_latest=blah
@app.route("/trip/findtrip", methods=["GET"])
def find_trip():
    source = request.args.get('source', type=str)
    destination = request.args.get('destination', type=str)
    leave_by_earliest = request.args.get('leave_by_earliest', type=str)
    leave_by_latest = request.args.get('leave_by_latest', type=str)
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
