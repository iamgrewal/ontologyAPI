from matcher.matcher import Matcher
from time_.dates import Date
from time_.timestamp import Timestamp
from translation.translate import Translator
from neobrain_skills.skills_template import SkillsTemplate
from db_persist.persist import Persistence
from copy import deepcopy
from random import randint
import requests
import json
#instances
timestamp = Timestamp()
translator = Translator()
date = Date()
persistance = Persistence()


class SkillsWithSimilarity(SkillsTemplate):

    def __init__(self, translator,matcher,job_list_df,nlp,token_list):
        self.matcher = matcher

        self.translator = translator
        self.job_list_df = job_list_df
        self.nlp = nlp
        self.token_list = token_list


    def getSkillsList(self, jobs, language, max_skills=10):
        skills = {}

        #Works to validate if the dates are null or not
        is_null = False


        #Translate the job titles to the language
        jobs, old_job_titles = self.get_jobs(jobs,language["language"])

        #This list will be filled with the matched titles
        matched_titles = []

        #Validate dates
        #If the date is "null" assign a default value to it
        for job in jobs:
            if jobs[job]["startDate"] == "null":
                jobs[job].update({"startDate":"2019-01-01"})
                is_null = True
            else:
                date.validate_date(jobs[job]["startDate"], job=job)

            if jobs[job]["endDate"] == "null":
                jobs[job].update({"endDate":"2020-01-01"})
                is_null = True
            else:
                date.validate_date(jobs[job]["endDate"], job=job)

        #this will be used to persist the data into database if everything goes right

        #jobs
        jobs_query = deepcopy(self.get_old_titles(old_job_titles, jobs))

        #list with job names ordered by the newest to oldest
        jobs_ordered_by_timestamp = timestamp.get_timestamp(jobs=jobs)
        total_days = 0

        #max number of skills
        max_total_skills = max_skills

        if len(jobs) == 1:
            max_skills_per_job = max_total_skills
        else:
            max_skills_per_job = 5

        #Counter for number of skills added to the list
        skills_added = 0
        used_skills = []
        #Add daysDifference to the jobs dict and get the total number of days worked
        for key,value in enumerate(jobs):
            jobs[value].update({"daysDifference": date.get_date_diference(jobs[value]["startDate"],jobs[value]["endDate"])})
            total_days += jobs[value]["daysDifference"]

        #get the percentage for each job
        for key,value in enumerate(jobs_ordered_by_timestamp):

            #If its the actual or last job
            if key == 0:

                #Get the number of skills to add from the last job
                number_of_skills = round((jobs[value]["daysDifference"] / total_days) * max_total_skills)
                if is_null:
                    pass
                else:
                    #If received more than one job, and it's the first of the list, add 2 skills if possible
                    if (number_of_skills + 2) < max_total_skills and number_of_skills < max_skills_per_job:
                        number_of_skills += 2

                    #If the number of skills is the same as max just pass
                    elif number_of_skills == max_total_skills:
                        pass

                    else:
                        number_of_skills = max_total_skills / 2

                #Get the skills
                #If french language
                if language["language"] == "fr":
                    #split the string
                    list_of_strings = str(value).split()

                    #Join with %20
                    prepared_string = "%20".join(list_of_strings)

                    #Prepare the URL
                    prepared_url = "https://skillssuggestion.ew.r.appspot.com/?job_title=" + prepared_string + "&language=fr"+"&nb_skills_selected="+str(max_skills)

                    #Make the request to Nathan's API
                    response = requests.get(prepared_url)

                    #If job was not found
                    if "wrong input" in response.text:
                        skills_ = {"0":"null"}
                    else:
                        skills_ = dict(json.loads(response.text))

                    #Append to temp_skills
                    temp_skills = []
                    for i in skills_:
                        temp_skills.append(skills_[i])

                    #Append the matched title (last skill is the title)
                    matched_titles.append(temp_skills[-1])


                #If english
                elif language["language"] == "en":

                    #split the string
                    list_of_strings = str(value).split()

                    #Joins with %20
                    prepared_string = "%20".join(list_of_strings)

                    #Prepare the URL
                    prepared_url = "https://skillssuggestion.ew.r.appspot.com/?job_title=" + prepared_string + "&language=en"+"&nb_skills_selected="+str(max_skills)

                    #Make the request to Nathan's API
                    response = requests.get(prepared_url)

                    #If job was not found
                    if "wrong input" in response.text:
                        skills_ = {"0":"null"}
                    else:
                        skills_ = dict(json.loads(response.text))

                    #Append to temp_skills
                    temp_skills = []
                    for i in skills_:
                        temp_skills.append(skills_[i])

                    #Append the matched title (last skill is the title)
                    matched_titles.append(temp_skills[-1])


                #wrong language
                else:
                    raise Exception("Wrong language sent:",language)

                #list of skills to append
                skills_list_to_append = []

                #skill counter
                sk_counter = 0

                #if the number of skills at ontology < required skills
                if len(temp_skills) <= number_of_skills:
                    number_of_skills = len(temp_skills) - 1

                #append skills to list
                while sk_counter <= number_of_skills:
                    if temp_skills[sk_counter] not in skills_list_to_append and temp_skills[sk_counter] not in used_skills:
                        skills_list_to_append.append(temp_skills[sk_counter])
                        used_skills.append(temp_skills[sk_counter])
                        sk_counter +=1
                    else:
                        sk_counter +=1

                #temp_skills = temp_skills[:number_of_skills]
                #sum the total number of used skills to control the max number to 10
                skills_added += len(skills_list_to_append)

                d_used_skills = {}
                for i in skills_list_to_append:
                    d_used_skills.update({i.lower():0})
                #update the skills
                skills.update({value:d_used_skills})


            #not the last job
            elif skills_added < max_total_skills:
                temp_max_skills = max_total_skills - skills_added


                #Get the number of skills to add from the last job
                number_of_skills = round((jobs[value]["daysDifference"] / total_days) * max_total_skills)


                if number_of_skills <= temp_max_skills:
                    #Get the skills
                    #If french language
                    if language["language"] == "fr":
                        #Split the string
                        list_of_strings = str(value).split()

                        #Joins with %20
                        prepared_string = "%20".join(list_of_strings)

                        #Prepare the URL
                        prepared_url = "https://skillssuggestion.ew.r.appspot.com/?job_title=" + prepared_string + "&language=fr"+"&nb_skills_selected="+str(max_skills)

                        #Make the request to Nathan's API
                        response = requests.get(prepared_url)

                        #If job was not found
                        if "wrong input" in response.text:
                            skills_ = {"0":"null"}
                        else:
                            skills_ = dict(json.loads(response.text))

                        #Append to temp_skills
                        temp_skills = []
                        for i in skills_:
                            temp_skills.append(skills_[i])

                        #Append the matched title (last skill is the title)
                        matched_titles.append(temp_skills[-1])

                    #If english
                    elif language["language"] == "en":

                        #Split the string
                        list_of_strings = str(value).split()

                        #Join with %20
                        prepared_string = "%20".join(list_of_strings)

                        #Prepare the URL
                        prepared_url = "https://skillssuggestion.ew.r.appspot.com/?job_title=" + prepared_string + "&language=en"+"&nb_skills_selected="+str(max_skills)

                        #Make the request to Nathan's API
                        response = requests.get(prepared_url)

                        #If job was not found
                        if "wrong input" in response.text:
                            skills_ = {"0":"null"}
                        else:
                            skills_ = dict(json.loads(response.text))

                        #Append to temp_skills
                        temp_skills = []
                        for i in skills_:
                            temp_skills.append(skills_[i])

                        #Append the matched title (last skill is the title)
                        matched_titles.append(temp_skills[-1])

                    #wrong language
                    else:
                        raise Exception("Wrong language sent:",language)

                    if len(temp_skills) < number_of_skills:
                        number_of_skills = len(temp_skills)

                    #list of skills to append
                    skills_list_to_append = []

                    #skill counter
                    sk_counter = 0

                    #if the number of skills at ontology < required skills
                    if len(temp_skills) < number_of_skills:
                        number_of_skills = len(temp_skills)

                    #append skills to list
                    while sk_counter < number_of_skills:
                        if temp_skills[sk_counter] not in skills_list_to_append and temp_skills[sk_counter] not in used_skills:
                            skills_list_to_append.append(temp_skills[sk_counter])
                            used_skills.append(temp_skills[sk_counter])
                            sk_counter +=1

                        else:
                            sk_counter +=1

                    #sum the total number of used skills to control the max number to 10
                    skills_added += len(skills_list_to_append)

                    d_used_skills = {}
                    for i in skills_list_to_append:
                        d_used_skills.update({i.lower():0})
                    #update the skills
                    skills.update({value:d_used_skills})

                else:
                    #If french language
                    if language["language"] == "fr":

                        #Split the string
                        list_of_strings = str(value).split()

                        #Join with %20
                        prepared_string = "%20".join(list_of_strings)

                        #Prepare the URL
                        prepared_url = "https://skillssuggestion.ew.r.appspot.com/?job_title=" + prepared_string + "&language=fr"+"&nb_skills_selected="+str(max_skills)

                        #Make the request to Nathan's APi
                        response = requests.get(prepared_url)

                        #If job was not found
                        if "wrong input" in response.text:
                            skills_ = {"0":"null"}
                        else:
                            skills_ = dict(json.loads(response.text))

                        #Append to temp_skills
                        temp_skills = []
                        for i in skills_:
                            temp_skills.append(skills_[i])

                        #Append the matched title (last skill is the title)
                        matched_titles.append(temp_skills[-1])

                    #If english
                    elif language["language"] == "en":

                        #Split the string
                        list_of_strings = str(value).split()

                        #Joins with %20
                        prepared_string = "%20".join(list_of_strings)

                        #Prepare the URL
                        prepared_url = "https://skillssuggestion.ew.r.appspot.com/?job_title=" + prepared_string + "&language=en"+"&nb_skills_selected="+str(max_skills)

                        #Request the skills to the Nathan's API
                        response = requests.get(prepared_url)

                        #If job was not found
                        if "wrong input" in response.text:
                            skills_ = {"0":"null"}
                        else:
                            skills_ = dict(json.loads(response.text))

                        #Append to temp_skill
                        temp_skills = []
                        for i in skills_:
                            temp_skills.append(skills_[i])

                        #Append the matched title (last skill is the title)
                        matched_titles.append(temp_skills[-1])

                    #wrong language
                    else:
                        raise Exception("Wrong language sent:",language)

                    temp_skills = temp_skills[:temp_max_skills]
                    skills_added += len(temp_skills)

                    #set 0 as value for each selected skills (this will be used to evaluate the skills later)
                    d_used_skills = {}
                    for i in temp_skills:
                        d_used_skills.update({i.lower():0})

                    skills.update({value:d_used_skills})
                    break

        #Dictionary with the skills
        skills = self.get_old_titles(old_job_titles, skills)

        skills_ = {}
        for i in jobs_query:
            skills_.update({i:skills[i]})
        skills = skills_

        #persist in the database #jobs_query
        persist_result = persistance.save_job_request(jobs_query, language=language["language"],matched_titles=list(set(matched_titles)))

        if persist_result == "OK!":
            #Get the lastest ID
            last_job_id = persistance.get_last_jobid()

            #The size will help find the Right ids on the database.
            #For example, we added 5 jobs to JobRequest database, and we want to make the list of IDs
            #If the last id is 25:
            #Size = -4  and 25-4=21, 25-3=22, 25-2=23, 25-1=24, 25-0=25
            #job_id_list = [21,22,23,24,25] respectivelly to the jobs ids on the database
            size = (len(skills) * -1) + 1

            #append the ID's
            for i in skills:
                if skills[i] != "null":
                    skills[i].update({"ID":last_job_id+size})
                    size += 1
                else:
                    continue

            insert_job_titles ={}
            insert_job_titles.update({"job_titles":skills})
            return insert_job_titles

        else:
            return "null"