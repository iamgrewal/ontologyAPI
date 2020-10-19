from db_persist.connections import ConnectionFactory
from datetime import datetime
from flask import url_for

class Persistence():
    def __init__(self):
        self.connection_factory = ConnectionFactory("feedback")

    def get_datetime(self):
        """This function returns the actual datetime of the system."""
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        return dt_string

    def insert_query(self,query):
        """This function execute the query received."""
        conn,cursor = self.connection_factory.get_connection()

        try:
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
            print("OK !")
        except Exception as e:
            cursor.close()
            conn.close()
            print(e)

    def all_same(self,items):
        """Check if all items from a list are the same"""
        return all(x.lower() == items[0].lower() for x in items)

    def save_job_request(self,job_request,language,matched_titles):
        """This function save each job request made on the database."""
        controller = False

        for i in matched_titles:
            #Check if we have null in all of th
            if i == "null" and self.all_same(matched_titles):
                controller = True

        if controller == True:
            return "null"
        else:
            #Get the last userID in the database
            user_id = self.get_last_userid()

            #Set the next ID
            new_user_id = str(user_id + 1)

            #Populate the query
            query = "INSERT INTO feedback.JobRequest " \
            "(UserID,JobTitle,MatchedTitle,StartDate,EndDate,ReqDateHour,Language) " \
            "VALUES "
            for k,job in enumerate(job_request):
                temp = "("+ "'" + new_user_id + "'"
                temp = temp + "," + "'" + job + "'"
                temp = temp + "," + "'" + matched_titles[k] + "'"
                temp = temp + "," + "'" + job_request[job]["startDate"] + "'"
                temp = temp + "," + "'" + job_request[job]["endDate"] + "'"
                temp = temp + "," + "'" + str(self.get_datetime()) + "'"
                temp = temp + "," + "'" + str(language) + "'),"
                query += temp

            #remove the last comma
            query = query[:-1]

            #Add a semicolon
            query +=";"

            #Persist
            self.insert_query(query)
            print("Persisted into the database.")

        return "OK!"


    def get_last_userid(self):
        #connect to database
        conn, cursor = self.connection_factory.get_connection()

        query = "SELECT UserID FROM JobRequest ORDER BY UserID DESC LIMIT 1;"

        #execute
        cursor.execute(query)
        myresult = cursor.fetchall()

        #set user_id, if the result of the query is empty set userID as 1 (this will only happen if don't have data in the DB)
        if myresult == []:
            user_id = 0
        else:
            user_id = myresult[0][0]
        cursor.close()
        conn.close()

        return int(user_id)

    def get_last_jobid(self):
        #connect to database
        conn, cursor = self.connection_factory.get_connection()

        query = "SELECT JobID FROM JobRequest ORDER BY JobID DESC LIMIT 1;"

        #execute
        cursor.execute(query)
        myresult = cursor.fetchall()

        #set user_id
        job_id = myresult[0][0]
        cursor.close()
        conn.close()

        return int(job_id)

    def save_feedback(self,job_titles):

        """ This function saves the feedback of the skill recomendation into the database"""

        #Create the query
        query = "INSERT INTO feedback.SkillResponse " \
        "(JobID,Skill,IsRight) " \
        "VALUES "
        for job in job_titles:
            for skill in job_titles[job]:
                if skill == "ID":
                    pass
                else:
                    temp = "("+ "'" + str(job_titles[job]["ID"]) + "'"
                    temp = temp + "," + "'" + skill + "'"
                    temp = temp + "," + "'" + str(job_titles[job][skill]) + "'),"
                    query += temp

        #remove the last comma
        query = query[:-1]

        #Add a semicolon
        query +=";"

        #Persist
        self.insert_query(query)
        print("Persisted into the database.")

        return "OK"


    def select_query(self,query):
        """This function execute the query received."""
        conn,cursor = self.connection_factory.get_connection()

        try:
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            print("OK !")
            return data
        except Exception as e:
            cursor.close()
            conn.close()
            print(e)

    def save_scores(self,job_titles):

        """ This function saves the Scores of the skills recomendation into the score database"""

        #Create the query
        query = "INSERT INTO feedback.Scores " \
        "(JobID,Skill,IsRight) " \
        "VALUES "
        for job in job_titles:
            for skill in job_titles[job]:
                if skill == "ID":
                    pass
                else:
                    temp = "("+ "'" + str(job_titles[job]["ID"]) + "'"
                    temp = temp + "," + "'" + skill + "'"
                    temp = temp + "," + "'" + str(job_titles[job][skill]) + "'),"
                    query += temp

        #remove the last comma
        query = query[:-1]

        #Add a semicolon
        query +=";"

        #Persist
        self.insert_query(query)
        print("Persisted into the database.")

        return "OK"