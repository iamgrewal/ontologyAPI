import requests
import json

class HandleForm():
    def get_skills(self,result):
        titles = []
        start_dates = []
        end_dates = []
        try:
            titles.append(result.getlist("job_title_1"))
        except:
            pass

        try:
            titles.append(result.getlist("job_title_2"))
        except:
            pass

        try:
            titles.append(result.getlist("job_title_3"))
        except:
            pass

        try:
            start_dates.append(result.getlist("start_date_1"))
        except:
            pass

        try:
            start_dates.append(result.getlist("start_date_2"))
        except:
            pass

        try:
            start_dates.append(result.getlist("start_date_3"))
        except:
            pass

        try:
            end_dates.append(result.getlist("end_date_1"))
        except:
            pass

        try:
            end_dates.append(result.getlist("end_date_2"))
        except:
            pass

        try:
            end_dates.append(result.getlist("end_date_3"))
        except:
            pass

        try:
            language =  result.getlist("language")
        except:
            pass
        
        if language[0] == "English":
            language = "en"
        elif language[0] == "French":
            language = "fr"
        try:
            skill_nr =  result.getlist("number_of_skills")
        except:
            pass


        js = {"job_titles":[],"language":{"language":language},"max_skills":skill_nr[0]}
        query = {}
        for i in range(len(titles)):
            if titles[i][0] != "":
                query.update({titles[i][0]:{"startDate":str(start_dates[i][0]),"endDate":str(end_dates[i][0])}})
        js.update({"job_titles":query})

        response = requests.post('http://127.0.0.1:5000/skills', json = js)
        skills_dict = json.loads(response.text)
        return skills_dict
        #{"job_titles":{title: {"startDate":"2016-10-10","endDate":"2016-10-20"}},"language":{"language":"en"}})
