import mysql.connector

class ConnectionFactory():
    """ This method is responsible for the connections on the feedback database"""
    def __init__(self,database):
        if database == "feedback":
            self.host = '165.227.231.233'
            #self.host = 'localhost'
            self.user = 'root'
            self.password = 'dsneobrain'
            #self.password = 'arvore22'
            self.port = 3306
            self.db = 'feedback'


    def get_connection(self):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            port=self.port,
            db=self.db
        )
        cursor = conn.cursor()

        return conn,cursor