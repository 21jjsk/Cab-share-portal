from flask import Flask, request, jsonify
import service
import models
import json

app = Flask(__name__)


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def hello():
    return "Hello World!"

# Work in progress starts here
# Student
@app.route("/student", methods=["POST"])
def create_student():
    StudentService().create(request.get_json())
    # return what???

@app.route("/student", methods=["GET"])
def list_student():
    return jsonify(StudentService().get_details())


# Admin
@app.route("/admin", methods=["POST"])
def create_student():
    AdminService().create(request.get_json())
    # return what???


# Car
@app.route("/car", methods=["POST"])
def create_student():
    CarService().create(request.get_json())
    # return what???


# Pickup details
@app.route("/pickup", methods=["POST"])
def create_student():
    Pickup_details_Service().create(request.get_json())
    # return what???


# Trip
@app.route("/trip", methods=["POST"])
def create_trip():
    TripService().create(request.get_json())
    # return what???

# /trip/findtrip?source=Campus&destination=Airport&leave_by_earliest=blah&leave_by_latest=blah
@app.route("/trip/findtrip", methods=["GET"])
def find_trip():
    source = request.args.get('source', type = str)
    destination = request.args.get('destination', type = str)
    leave_by_earliest = request.args.get('leave_by_earliest', type = str)
    leave_by_latest = request.args.get('leave_by_latest', type = str)
    return jsonify(TripService().search(source, destination, leave_by_earliest, leave_by_latest))

# @app.route("/trip/<trip_id>", methods=["PUT"])
# def update_item(trip_id):
#     return jsonify(TripService().update(trip_id, request.get_json()))

@app.route("/todo/<trip_id>", methods=["DELETE"])
def delete_item(trip_id):
    return jsonify(TripService().delete(trip_id))
# Work in progress ends here


if __name__ == "__main__":
    Schema()
    app.run(debug=True)