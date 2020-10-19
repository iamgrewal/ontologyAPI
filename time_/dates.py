import datetime
class Date():
    def validate_date(self,date_text, job):
        if date_text == "null":
            pass
        else:
            """ Function to validate data format"""
            try:
                datetime.datetime.strptime(date_text, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD. Job:", str(job))
   
    def get_date_diference(self,date1, date2):
        """ Calculate the difference between two dates"""
        date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        difference = date2 - date1
        return difference.days