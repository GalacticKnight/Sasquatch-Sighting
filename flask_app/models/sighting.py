from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Sighting:
    database="sasquatch_db"
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_of_sighting = data['date_of_sighting']
        self.number_of_sasquatches = data['number_of_sasquatches']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']#!!!!!!!!!!!!very important
        self.creator = None

    @staticmethod
    def validate_sighting(data):#done
        is_valid = True 
        if len(data['location']) < 3:
            flash("At least 3 characters.")
            is_valid = False
        if len(data['what_happened']) < 3:
            flash("At least 3 characters.")
            is_data = False
        if len(data['number_of_sasquatches']) < 1:
            flash("instructions")
            is_data = False
        return is_valid

    
    @classmethod
    def save(cls,data):#you need user_id!!!!!!
        query = '''INSERT INTO sightings 
        (location, what_happened, date_of_sighting, number_of_sasquatches, users_id) 
        VALUES 
        (%(location)s, %(what_happened)s, %(date_of_sighting)s,%(number_of_sasquatches)s, %(users_id)s);'''
        #you cannot assume, you HAVE TO HAVE AN ID TO LOCATIE WHERE YOU WANT TO PUT IN THE TABLE
        return connectToMySQL(cls.database).query_db(query,data)

    @classmethod
    def update(cls,data):#you need user_id!!!!!!
        query = '''UPDATE sightings SET 
        id =(%(id)s),
        location = (%(location)s),
        what_happened = (%(what_happened)s),
        date_of_sighting = (%(date_of_sighting)s),
        number_of_sasquatches = (%(number_of_sasquatches)s) 
        where id= %(id)s;'''
        return connectToMySQL(cls.database).query_db(query,data)


    @classmethod
    def delete(cls,data):
        query = '''DELETE FROM sightings WHERE ID = %(id)s;'''#??????????????????????
        results = connectToMySQL(cls.database).query_db(query,data)


    @classmethod
    def find_by_id(cls, data):
        query='''SELECT * FROM sightings LEFT JOIN users on users.id = sightings.users_id WHERE sightings.id= %(id)s'''#!!!!!!!!!!!
        results = connectToMySQL(cls.database).query_db(query,data)
        print(results)
        r = cls(results[0])
        u = {
            "id": results[0]["users.id"],
            "first_name":results[0]["first_name"],
            "last_name":results[0]["last_name"],
            "email":results[0]["email"],
            "password":results[0]["password"],
            "created_at":results[0]["users.created_at"],
            "updated_at":results[0]["users.updated_at"]
        }
        print(results)
        r.creator=User(u)#
        return r

    @classmethod
    def get_all(cls):#the goal of this
        query = '''SELECT * FROM sightings
        LEFT JOIN users on users.id = sightings.users_id;'''
        results = connectToMySQL(cls.database).query_db(query)
        print(results)
        lst =[]
        for i in results:
            r = cls(i)
            u = {
                "id": i["users.id"],
                "first_name":i["first_name"],
                "last_name":i["last_name"],
                "email":i["email"],
                "password":i["password"],
                "created_at":i["users.created_at"],
                "updated_at":i["users.updated_at"]
            }
            r.creator=User(u)#
            lst.append(r)
        print("lst",lst)
        return lst
