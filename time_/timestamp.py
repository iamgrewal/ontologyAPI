import datetime
from collections import OrderedDict
import time

class Timestamp():
    def get_timestamp(self,jobs):
        """Get the timestamp from each job and return a list with the last two"""
        timestamp = {}

        for key,i in enumerate(jobs):
            if jobs[i]["endDate"] != "null":
                endDate = jobs[i]["endDate"]
            else:
                now = datetime.datetime.now()
                day= now.strftime("%d")
                month= now.strftime("%m")
                year= now.strftime("%Y")
                endDate =year+"-"+month+"-"+day
            stamp = int(time.mktime(datetime.datetime.strptime(endDate, "%Y-%m-%d").timetuple()))
            timestamp.update({i:stamp})
            #order by value
        ordered =  OrderedDict(sorted(timestamp.items(), key=lambda t: t[1], reverse=True))

        #Get the most recent jobs
        last_jobs = []
        for key in ordered.keys():
            last_jobs.append(key)

        return last_jobs