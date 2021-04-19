from models import *


class StudentService:
    def __init__(self):
        self.model = Student()

    def create(self, params):
        self.model.create(params)

    def get_details(self, s_id, password):
        print("inside service" + s_id)
        return self.model.get_details(s_id, password)


class AdminService:
    def __init__(self):
        self.model = Admin()

    # remember not to pass admin_id here in params (it is auto generated)
    def create(self, params):
        self.model.create(params)

    def search(self, id, password):
        print(id + " " + password + "service")
        return self.model.search(id, password)


class CarService:
    def __init__(self):
        self.model = Car()

    def create(self, params):
        return self.model.create(params)

    def find_cars(self, location, start_time, end_time):
        return self.model.find_cars(location, start_time, end_time)


class Pickup_details_Service:
    def __init__(self):
        self.model = Pickup_details()

    def create(self, params):
        return self.model.create(params)


class TripService:
    def __init__(self):
        self.model = Trip()

    def create(self, params):
        self.model.create(params)

    def search(self, source, destination, leave_by_earliest, leave_by_latest):
        return self.model.search(source, destination, leave_by_earliest, leave_by_latest)

    def trip_history(self, s_id):
        print("inside service")
        return self.model.trip_history(s_id)

    # attributes to be changed are passed in attribs
    def status(self, trip_id):
        self.model.status(trip_id)

    def update(self, attribs):
        self.model.update(attribs.get('trip_id'), attribs.get('s_id'), attribs.get('source'),
                          attribs.get('destination'), attribs.get('leave_by_earliest'), attribs.get('leave_by_latest'))

    def linkcar(self, attribs):
        self.model.linkcar(attribs.get('trip_id'),attribs.get('car_no'))

    def delete(self, trip_id):
        return self.model.delete(trip_id)
