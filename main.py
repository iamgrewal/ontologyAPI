from flask import Flask, render_template, request, url_for
from flask_restful import Api,Resource
from neobrain_skills.skills import SkillsList
from test_template.test import TestForm
from test_template.feedback import FeedbackForm
from flask import render_template, redirect
from test_template.handle_submit import HandleForm
import json
from copy import deepcopy
import requests
from db_persist.persist import Persistence



app = Flask(__name__)
app.config['SECRET_KEY'] = 'neobrain2020'
api = Api(app)
""" This is the main file that makes the API run."""

#Instanciate
skills_list = SkillsList()
h_form = HandleForm()
persistence = Persistence()




#______________________________________________________________________________________________________________
#test template
@app.route('/test', methods=['GET', 'post'])
def test():
    form = TestForm()
    if form.is_submitted():
        result = request.form
        skill_list = h_form.get_skills(result)
        #Return the get feedback function with the list of skills

        ##This part encodes the apostoprhe as $#$
        final = {}
        skill_updated = {}
        for job in skill_list["job_titles"]:
            job_updated = {}
            for skill in skill_list["job_titles"][job]:
                job_updated.update({str(skill).replace("'","$#$"):0})
            skill_updated.update({str(job).replace("'","$#$"):job_updated})
        final.update({"job_titles":skill_updated})
        return redirect(url_for('.get_feedback', skill_list=final))

    return render_template('test-form.html', title='Sign In', form=form)

#______________________________________________________________________________________________________________

@app.route('/feedback/<skill_list>',methods=['GET', 'post'])
def get_feedback(skill_list):
    """This function receives a list of skills, render it in a template, collect the feedback and save into the database."""
    if skill_list != "null":
        #Prepare the data and pass it to the form
        skill_list = skill_list.replace("'",'"')
        skill_list = dict(json.loads(skill_list))

        ##This part decodes the apostoprhe as $#$
        final = {}
        skill_updated = {}
        for job in skill_list["job_titles"]:
            job_updated = {}
            for skill in skill_list["job_titles"][job]:
                job_updated.update({str(skill).replace("$#$","'"):0})
            skill_updated.update({str(job).replace("$#$","'"):job_updated})
        final.update({"job_titles":skill_updated})
        skill_list = final

        skills_set = []
        for job in skill_list["job_titles"]:
            for skill in skill_list["job_titles"][job]:
                if skill != "ID":
                    #append and decode apostrophe
                    skills_set.append({"name":str(skill)})
        form = FeedbackForm(skills=skills_set)

        #When the form is submitted
        if form.is_submitted():
            return_dict = deepcopy(skill_list)
            result = request.form
            #Iterate over jobs
            for job in skill_list["job_titles"]:
                #get the list of skills for this job
                list_of_job_skills = []
                for skill in skill_list["job_titles"][job]:
                    if skill == "ID":
                        pass
                    else:
                        list_of_job_skills.append(skill)
                #Iterate over form results
                for r in result:
                    #check if any skill returned from the form is from this job
                    if r in list_of_job_skills:
                        #If it is set it as 1
                        return_dict["job_titles"][job].update({r:1})

            json_request = json.dumps(return_dict)
            response = requests.post("http://127.0.0.1:5000/feedback", json=json_request)
            response=response.text
            return response

        #If it is received for the first time (non submited)
        return render_template("skills.html", result=skill_list["job_titles"])
    else:
        return "The inputted job titles didnt found matches."

#______________________________________________________________________________________________________________

#Job report
@app.route("/job_report")
def job_report():
    data = persistence.select_query("SELECT * from JobRequest")
    return render_template("job_report.html", data=data)

#______________________________________________________________________________________________________________

#Skill report
@app.route("/skill_report")
def skill_report():
    data = persistence.select_query("SELECT * from SkillResponse")
    return render_template("skill_report.html", data=data)

#______________________________________________________________________________________________________________

#Index page
@app.route("/")
def index():
    return render_template("index.html")
#______________________________________________________________________________________________________________

#JSON response example
@app.route("/json_response")
def json_response():
    return render_template("json.html")
#______________________________________________________________________________________________________________

#JSON request example
@app.route("/json_request")
def json_request():
    return render_template("request_json_example.html")
#______________________________________________________________________________________________________________

#Thank you
@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

#______________________________________________________________________________________________________________

class GetSkillsList(Resource):
    """ The request come from ip/skills and use spacy similarity to get the most similar jobs.
    This class receive the request and parse the parameters and call the responsible method. """
    def post(self):
        json_data = request.get_json(force=True)
        jobs = json_data['job_titles']
        jobs = dict(jobs)
        language = json_data['language']
        language = dict(language)

        #Set defaul maximum number of returned skills
        max_skills = 10
        try:
            max_skills = int(json_data['max_skills'])
        except:
            pass

        ret = skills_list.getSkillsList(jobs=jobs, language=language, max_skills=max_skills)
        if ret != "null":
            return ret
        else:
            return "null"

class GetSkillsListWithoutSimilarity(Resource):
    """ The request come from ip/skills_list and use a list of jobs to match the skills.
    This class receive the request and parse the parameters and call the responsible method. """
    def post(self):
        json_data = request.get_json(force=True)
        jobs = json_data['job_titles']
        jobs = dict(jobs)
        language = json_data['language']
        language = dict(language)
        return skills_list.getSkillsListWithoutSimilarity(jobs=jobs, language=language)

class ReceiveSkillsFeedback(Resource):
    """ The request come from ip/feedback. Will receive the skills dict with the feedback from user. """
    def post(self):
        json_data = request.get_json(force=True)
        json_data = dict(json.loads(json_data))
        job_titles = json_data['job_titles']
        job_titles = dict(job_titles)

        try:
            result = skills_list.saveFeedBack(job_titles=job_titles)
            return redirect(url_for(".thank_you"))
        except:
            #TODO implement if fails
            return redirect(url_for(".thank_you"))


#Set the url's
api.add_resource(GetSkillsList, "/skills")
api.add_resource(GetSkillsListWithoutSimilarity, "/skills_list")
api.add_resource(ReceiveSkillsFeedback, "/feedback")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


