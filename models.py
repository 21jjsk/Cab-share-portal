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
                car_no varchar (20),
                status varchar(20),
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
        try:

            dict = {"s_id": temp[0], "name": temp[1], "email": temp[2], "gender": temp[3], "phone_no": temp[4],
                        "room_no": temp[5]}

            print(dict)
            return dict


        except:
            return []




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

    def search(self, id, password):
        print(id + " " + password + "service")
        result = self.conn.execute(
            f"""
            SELECT admin_id from Admin WHERE admin_id="{id}" and password="{password}" ;
"""
        ).fetchone()
        print(result)
        return result


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
        result = self.conn.execute(f"""
            SELECT p.car_no, c.model, c.car_capacity, p.location, 
            p.start_time,
            p.end_time ,
            c.driver_name, c.driver_phone 
            FROM car c, Pickup_details p 
            WHERE c.car_no = p.car_no 
            AND location = '{location}'  AND ( NOT( (p.end_time <'{start_time}'
            OR p.start_time > '{end_time}')));
        """).fetchall()
        dict = []
        for r in result:
            dict.append({'car_no': r[0], 'model': r[1], 'car_capacity': r[2], 'location': r[3], 'driver_name': r[6],
                         'driver_no': r[7]})
        print(dict)
        return dict


class Pickup_details:
    TABLENAME = "Pickup_details"

    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create(self, params):
        print(params.get('car_no') + " " + params.get('location') + " " + params.get('start_time') + " " + params.get(
            'end_time'))
        return self.conn.execute(f"""
            INSERT INTO {self.TABLENAME} (car_no, location, start_time, end_time)
            VALUES ("{params.get("car_no")}", "{params.get("location")}",
                "{params.get('start_time')}",
                "{params.get('end_time')}");
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

    def status(self, trip_id):
        self.conn.execute(f"""update Trip set status='finished' where trip_id={trip_id}""")

    def create(self, params):
        self.conn.execute(f"""
            INSERT INTO {self.TABLENAME} (s_id, source, destination, leave_by_earliest, leave_by_latest, car_no,status)
            VALUES ("{params.get('s_id')}", "{params.get('source')}", "{params.get('destination')}", 
                "{params.get('leave_by_earliest')}", 
                "{params.get('leave_by_latest')}", 
                "{params.get('car_no', 'NULL')}","pending");
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
                 "leave_by_earliest": result[4], "leave_by_latest": result[5],"car_no":result[6],"status":result[7]})
        return results_dic

    def search(self, source, destination, leave_by_earliest, leave_by_latest):
        # also needed s_name, email, phone_no, room_no
        results = self.conn.execute(f"""
         SELECT *
            FROM Trip T, Student S
             WHERE T.source = '{source}' AND T.destination ='{destination}' AND  (NOT((T.leave_by_earliest > '{leave_by_latest}')
            OR T.leave_by_latest < '{leave_by_earliest}')) AND T.s_id=S.s_id and T.status='pending';
        """).fetchall()
        print(results)
        results_dic = []
        for result in results:
            results_dic.append(
                {"trip_id": result[0], "s_id": result[1], "location": result[2], "destination": result[3],
                 "leave_by_earliest": result[4], "leave_by_latest": result[5], "cab_no": result[6],"status":result[7], "name": result[9],
                 "email": result[10], "gender": result[12], "phone_no": result[13],
                 "room_no": result[14]})
        return results_dic

    # attributes to be changed are passed in attribs
    def linkcar(self, trip_id, car_no):

        self.conn.execute(f"""
               Update Trip set  car_no='{car_no}' where trip_id={trip_id};
            """)
        return "donee"

    def update(self, trip_id, s_id, source, destination, leave_by_earliest, leave_by_latest):

        self.conn.execute(f"""
               Update Trip set s_id='{s_id}', source='{source}', destination='{destination}', leave_by_earliest='{leave_by_earliest}', leave_by_latest='{leave_by_latest}' where trip_id={trip_id};
            """)
        return "donee"

    def delete(self, trip_id):
        self.conn.execute(f"""
                DELETE from {self.TABLENAME}
                WHERE trip_id = {trip_id};
            """)
        return "wooosh"
