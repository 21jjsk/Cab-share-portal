import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('cab_share.db')
        self.create_student_table()
        self.create_admin_table()
        self.create_car_table()
        self.create_trip_table()
        self.create_pick_up_details_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    # Creating all the tables if they do not exist
    def create_student_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Student" (
        s_id varchar(15) PRIMARY KEY, 
        name varchar(30), 
        email varchar(50), 
        password varchar(15), 
        gender varchar(6), 
        phone_no varchar(15), 
        room_no varchar(8));
        );
        """
        self.conn.execute(query)

    def create_admin_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Admin" (
        admin_id varchar(15) PRIMARY KEY, 
        name varchar(30), 
        email varchar(50), 
        password varchar(15), 
        phone_no varchar(15)
        );
        """
        self.conn.execute(query)
    
    def create_car_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Car" (
        car_no varchar(12) PRIMARY KEY, 
        admin_id varchar(15) FOREIGNKEY REFERENCES Admin(admin_id), 
        model varchar(10), 
        car_capacity int, 
        driver_name varchar(30), 
        driver_phone varchar(15)
        );
        """
        self.conn.execute(query)

    def create_trip_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Trip" (
        trip_id int PRIMARY KEY AUTOINCREMENT, 
        s_id varchar(15) FOREIGNKEY REFERENCES Student(s_id), 
        source varchar(20), 
        destination varchar(20), 
        leave_by_earliest date, 
        leave_by_latest date, 
        car_no varchar(12) FOREIGNKEY REFERENCES Car(car_no)
        );
        """
        self.conn.execute(query)

    def create_pick_up_details_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Pickup_details" (
        car_no varchar(12) FOREIGNKEY REFERENCES Car(car_no), 
        location varchar(20), 
        start_time date, 
        end_time date, 
        PRIMARY KEY (car_no, location, start_time)
        );
        """
        self.conn.execute(query)

# generic helper function to return a formatted string :=
# insert into {tablename} (attributes...) values (params.get(attrib)...)
def get_query(params, tablename, ls):
    attribs = ', '.join(ls)
    attribs2 = ', '.join(f'"{params.get(attr)}"' for attr in ls)
    return f'insert into {tablename} ({attribs}) values ({attribs2})'

  
class Student:
    TABLENAME = "Student"

    def create(self, params):
        result = self.conn.execute(get_query(params, self.TABLENAME, 
                ['s_id', 'name', 'email', 'password', 'gender', 'phone_no', 'room_no']))
        # return self.get_by_id(result.lastrowid)

    # get details of student by passing s_id
    def get_details(self, s_id):
        query = f""" 
        SELECT s_id, name, email, gender, phone_no, room_no
        FROM Student 
        WHERE s_id = {s_id};
        """
        result = self.conn.execute(query)
        return result.fetchone()



class Admin:
    TABLENAME = "Admin"
    
    def create(self, params):
        result = self.conn.execute(getquery(params, self.TABLENAME, 
                ['name', 'email', 'password', 'phone_no']))
    # remember not to pass admin_id here in params (it is auto generated)


class Car:
    TABLENAME = "Car"
    
    def create(self, params):
        result = self.conn.execute(getquery(params, self.TABLENAME, 
                ['car_no', 'admin_id', 'model', 'car_capacity', 'driver_name', 'driver_phone']))

        
    # def find_cars(self, location, ):
        # to be completed
        



class Trip:
    TABLENAME = "Trip"

    def create(self, params):
        query =f"""
        INSERT INTO Trip (s_id, source, destination, leave_by_earliest, leave_by_latest, car_no) VALUES ({params.get('s_id')}, {params.get('source')}, {parms.get('destination')}, to_date({params.get('leave_by_earliest')}, 'YYYY-MM-DD HH24:MI'), to_date({params.get('leave_by_latest')}, 'YYYY-MM-DD HH24:MI'), NULL);
        """
        # Initially assigning NULL to car_no

        # result = self.conn.execute(getquery(params, self.TABLENAME, 
        #         ['s_id', 'source', 'destination', 'leave_by_earliest', 'leave_by_latest', 'car_no']))

    def search(self, source, destination, leave_by_earliest, leave_by_latest):
        # also needed s_name, email, phone_no, room_no
       query = f"""
        SELECT trip_id, s_id, name, source, destination, 
        to_char(leave_by_earliest, 'DD-MM-YYYY HH24:MI   ') as leave_by_earliest, to_char(leave_by_latest, 'DD-MM-YYYY HH24:MI   ') as leave_by_latest, car_no 
        FROM Trip
        WHERE NOT (leave_by_earliest < to_date('{leave_by_earliest}   ', 'YYYY-MM-DD HH24:MI   ') 
        AND leave_by_latest > to_date('{leave_by_latest}   ', 'YYYY-MM-DD HH24:MI   ')) 
        AND source = {source} 
        AND destination = {destination};
       """
       result = self.conn.execute(query)
       return result.fetchall()

    # attributes to be changed are passed in attribs
    def update(self, trip_id, attribs):
        temp = ""
        flg = false
        for key in attribs:
            if(flg):
                temp += ', '
            flg = true
            temp += key
            temp += ' = '
            if(key == 'leave_by_earliest' or key == 'leave_by_latest'):
                temp += f"to_date('{attribs[key]}', 'YYYY-MM-DD HH24:MI')"
            else:
                temp += attribs[key]
            
        query = f"""
        UPDATE trip 
        SET {temp}
        WHERE trip_id = {trip_id};
        """
        self.conn.execute(query)

    def delete(self, trip_id):
        query = f"""
        DELETE from Trip
        WHERE trip_id = {trip_id};
        """
        self.conn.execute(query)


class Pickup_details:
    TABLENAME = "Pickup_details"

    def create(self, params):
        result = self.conn.execute(getquery(params, self.TABLENAME, 
                ['car_no', 'location' , 'start_time' , 'end_time']))

