import sqlite3

DBNAME = 'cab_share.db'


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS "Student" (
                s_id varchar(15) PRIMARY KEY, 
                name varchar(30), 
                email varchar(50), 
                password varchar(15), 
                gender varchar(6), 
                phone_no varchar(15), 
                room_no varchar(8)
            );
            CREATE TABLE IF NOT EXISTS "Admin" (
                admin_id varchar(15) PRIMARY KEY, 
                name varchar(30), 
                email varchar(50), 
                password varchar(15), 
                phone_no varchar(15)
            );
            CREATE TABLE IF NOT EXISTS "Car" (
                car_no varchar(12) PRIMARY KEY, 
                admin_id varchar(15) , 
                model varchar(10), 
                car_capacity int, 
                driver_name varchar(30), 
                driver_phone varchar(15) ,
                FOREIGN KEY(admin_id) REFERENCES Admin(admin_id)
            );
              
            CREATE TABLE IF NOT EXISTS "Trip" (
                trip_id integer PRIMARY KEY AUTOINCREMENT, 
                s_id varchar(15) , 
                source varchar(20), 
                destination varchar(20), 
                leave_by_earliest varchar(20), 
                leave_by_latest varchar(20), 
                FOREIGN KEY (s_id)
                 REFERENCES  Student(s_id)
            );
            CREATE TABLE IF NOT EXISTS "Pickup_details" (
                car_no varchar(12), 
                location varchar(20), 
                start_time date, 
                end_time date, 
                PRIMARY KEY (car_no, location, start_time),
                FOREIGN KEY (car_no)
                    REFERENCES Car(car_no)
            );
        """
        )
        # # create student table
        # self.conn.execute()
        #
        # # create admin table
        # self.conn.execute("""
        #     CREATE TABLE IF NOT EXISTS "Admin" (
        #         admin_id varchar(15) PRIMARY KEY,
        #         name varchar(30),
        #         email varchar(50),
        #         password varchar(15),
        #         phone_no varchar(15)
        #     );
        # """)
        #
        # # create car table
        # self.conn.execute("""
        #     CREATE TABLE IF NOT EXISTS "Car" (
        #         car_no varchar(12) PRIMARY KEY,
        #         admin_id varchar(15) FOREIGNKEY REFERENCES Admin(admin_id),
        #         model varchar(10),
        #         car_capacity int,
        #         driver_name varchar(30),
        #         driver_phone varchar(15)
        #     );
        # """)

        # # create trip table
        # self.conn.execute("""
        #     CREATE TABLE IF NOT EXISTS "Trip" (
        #         trip_id int PRIMARY KEY AUTOINCREMENT,
        #         s_id varchar(15) FOREIGNKEY REFERENCES Student(s_id),
        #         source varchar(20),
        #         destination varchar(20),
        #         leave_by_earliest date,
        #         leave_by_latest date,
        #         car_no varchar(12) FOREIGNKEY REFERENCES Car(car_no)
        #     );
        # """)
        #
        # # create pickup_details table
        # self.conn.execute("""
        #     CREATE TABLE IF NOT EXISTS "Pickup_details" (
        #     car_no varchar(12) FOREIGNKEY REFERENCES Car(car_no),
        #     location varchar(20),
        #     start_time date,
        #     end_time date,
        #     PRIMARY KEY (car_no, location, start_time)
        # );
        # """)

    def __del__(self):
        self.conn.commit()
        self.conn.close()


class Student:
    TABLENAME = "Student"

    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create(self, params):
        attributes = ['s_id', 'name', 'email', 'password', 'gender', 'phone_no', 'room_no']
        self.conn.execute(f"""
            INSERT INTO {self.TABLENAME} ({', '.join(attributes)})
            VALUES ({', '.join(f'"{params.get(attr)}"' for attr in attributes)});
        """)

    # get details of student by passing s_id
    def get_details(self, id, pas):
        print("inside model" + id)
        cur = self.conn.cursor()
        temp = cur.execute(f"""
            SELECT s_id,name, email, gender, phone_no, room_no
            FROM Student
            WHERE s_id ="{id}" and password="{pas}";
        """).fetchone()
        # print(temp)
        dict = {"s_id": temp[0], "name": temp[1], "email": temp[2], "gender": temp[3], "phone_no": temp[4],
                "room_no": temp[5]}
        print(dict)
        return dict


class Admin:
    TABLENAME = "Admin"

    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    # remember not to pass admin_id here in params (it is auto generated)
    def create(self, params):
        attributes = ['name', 'email', 'password', 'phone_no']
        self.conn.execute(f"""
            INSERT INTO {self.TABLENAME} ({', '.join(attributes)})
            VALUES ({', '.join(f'"{params.get(attr)}"' for attr in attributes)});
        """)


class Car:
    TABLENAME = "Car"

    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create(self, params):
        attributes = ['car_no', 'admin_id', 'model', 'car_capacity', 'driver_name', 'driver_phone']
        self.conn.execute(f"""
            INSERT INTO {self.TABLENAME} ({', '.join(attributes)})
            VALUES ({', '.join(f'"{params.get(attr)}"' for attr in attributes)});
        """)

    def find_cars(self, location, start_time, end_time):
        self.conn.execute(f"""
            SELECT p.car_no, c.model, c.car_capacity, p.location, 
            to_char(p.start_time, 'HH24:MI') AS start_time, 
            to_char(p.end_time, 'HH24:MI') AS end_time, 
            c.driver_name, c.driver_phone 
            FROM car c, pick_up_details p 
            WHERE c.car_no = p.car_no 
            AND NOT (to_char(p.end_time, 'HH24:MI') < to_char({start_time}, 'HH24:MI')
            OR to_char(p.start_time, 'HH24:MI') > to_char({end_time}, 'HH24:MI')) 
            AND location = {location};
        """)

    def find_cars(self, start_time, end_time):
        self.conn.execute(f"""
            SELECT p.car_no, c.model, c.car_capacity, p.location, 
            to_char(p.start_time, 'HH24:MI') AS start_time, 
            to_char(p.end_time, 'HH24:MI') AS end_time, 
            c.driver_name, c.driver_phone 
            FROM car c, pick_up_details p 
            WHERE c.car_no = p.car_no 
            AND NOT (to_char(p.end_time, 'HH24:MI') < to_char({start_time}, 'HH24:MI')
            OR to_char(p.start_time, 'HH24:MI') > to_char({end_time}, 'HH24:MI'));
        """)

    def find_cars(self, location):
        self.conn.execute(f"""
            SELECT p.car_no, c.model, c.car_capacity, p.location, 
            to_char(p.start_time, 'HH24:MI') AS start_time, 
            to_char(p.end_time, 'HH24:MI') AS end_time, 
            c.driver_name, c.driver_phone 
            FROM car c, pick_up_details p 
            WHERE c.car_no = p.car_no 
            AND location = {location};
        """)


class Pickup_details:
    TABLENAME = "Pickup_details"

    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create(self, params):
        self.conn.execute(f"""
            INSERT INTO {self.TABLENAME} (car_no, location, start_time, end_time)
            VALUES ("{params.get("car_no")}"", "{params.get("location")}"",
                to_date("{params.get('start_time')}", "YYYY-MM-DD HH24:MI"),
                to_date("{params.get('end_time')}", "YYYY-MM-DD HH24:MI"));
        """)

    # def create(self, params):
    #     attributes = ['car_no', 'location' , 'start_time' , 'end_time']
    #     self.conn.execute(f"""
    #         INSERT INTO {self.TABLENAME} ({', '.join(attributes)})
    #         VALUES ({', '.join(f'"{params.get(attr)}"' for attr in attributes)});
    #     """)


class Trip:
    TABLENAME = "Trip"

    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create(self, params):
        self.conn.execute(f"""
            INSERT INTO {self.TABLENAME} (s_id, source, destination, leave_by_earliest, leave_by_latest, car_no)
            VALUES ("{params.get('s_id')}", "{params.get('source')}", "{params.get('destination')}", 
                "{params.get('leave_by_earliest')}", 
                "{params.get('leave_by_latest')}", 
                "{params.get('car_no', 'NULL')}");
        """)  # car_no = NULL if it does not exist

    def trip_history(self, s_id):
        print("inside models")
        results = self.conn.execute(
            f""" SELECT * FROM {self.TABLENAME} WHERE s_id="{s_id}" """
        ).fetchall()
        results_dic = []
        for result in results:
            results_dic.append(
                {"trip_id": result[0], "s_id": result[1], "location": result[2], "destination": result[3],
                 "leave_by_earliest": result[4], "leave_by_latest": result[5]})
        return results_dic

    def search(self, source, destination, leave_by_earliest, leave_by_latest):
        # also needed s_name, email, phone_no, room_no
        return self.conn.execute(f"""
            SELECT *
            FROM {self.TABLENAME}
             WHERE source = '{source}' AND destination ='{destination}' AND  (NOT((leave_by_earliest > '{leave_by_latest}')
            OR leave_by_latest < '{leave_by_earliest}'));
        """).fetchall()

    # attributes to be changed are passed in attribs
    def update(self, trip_id, attribs):
        get = lambda key, val: f'to_date("{val}","YYYY-MM-DD  HH24:MI")' if key == "leave_by_earliest" or key == "leave_by_latest" else f'"{val}"'

        self.conn.execute(f"""
                UPDATE {self.TABLENAME} 
                SET {', '.join(f'{key} = {get(key, val)}' for key, val in attribs.items())}
                WHERE trip_id = {trip_id};
            """)

    def delete(self, trip_id):
        self.conn.execute(f"""
                DELETE from {self.TABLENAME}
                WHERE trip_id = {trip_id};
            """)
