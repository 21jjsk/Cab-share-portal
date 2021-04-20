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


# Work in progress starts here
# Student
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
@app.route("/admin", methods=["POST"])
def login_admin():
    data = request.get_json()
    print(data.get('admin_id') + " " + data.get('password'))
    result = AdminService().search(data.get('admin_id'), data.get('password'))

    return json.dumps(result)
    # return what???


# Car
# verified

@app.route("/car", methods=["POST"])
def create_car():
    # CarService().create()
    CarService().create(request.get_json())
    return "car inserted"


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route("/findCar", methods=["POST"])
def find_car():
    data = request.get_json()
    location = data.get('location')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    print(location)
    print(start_time)
    print(end_time)
    res=json.dumps(CarService().find_cars(location, start_time, end_time))
    print(res)
    return res

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
    ress=json.dumps(TripService().trip_history(s_id))
    print(ress)
    return ress


# /trip/findtrip?source=Campus&destination=Airport&leave_by_earliest=blah&leave_by_latest=blah
@app.route("/findtrip", methods=["POST"])
def find_trip():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    leave_by_earliest = data.get('leave_by_earliest')
    leave_by_latest = data.get('leave_by_latest')
    return jsonify(TripService().search(source, destination, leave_by_earliest, leave_by_latest))

@app.route("/status", methods=["POST"])
def update_status():
    data=request.get_json()
    return jsonify(TripService().status(data.get('trip_id')))

@app.route("/update", methods=["POST"])
def update_item():
    return jsonify(TripService().update(request.get_json()))
@app.route("/linkcab", methods=["POST"])
def linkcab():
    return jsonify(TripService().linkcar(request.get_json()))

@app.route("/delete", methods=["POST"])
def delete_item():
    data=request.get_json()
    return jsonify(TripService().delete(data.get('trip_id')))


# Work in progress ends here


if __name__ == "__main__":
    Schema()
    app.run(debug=True)
