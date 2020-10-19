from time_.dates import Date
from time_.timestamp import Timestamp
from translation.translate import Translator
import pandas as pd
from neobrain_skills.skills_template import SkillsTemplate

#instanciate
timestamp = Timestamp()
translator = Translator()
date = Date()

class SkillsFromJob(SkillsTemplate):
    def __init__(self, translator,matcher,emsi_df):
        self.matcher = matcher

        #translator instance
        self.translator = translator

        #EMSI dataframe
        self.emsi_df = emsi_df

    def getSkillsListWithoutSimilarity(self, jobs, language):
        #Skills dict that will be returned
        skills = {}

        #Validate dates
        for job in jobs:
            date.validate_date(jobs[job]["startDate"], job=job)
            if jobs[job]["endDate"] != "null":
                date.validate_date(jobs[job]["endDate"], job=job)

        #list with job names ordered by the newest to oldest
        jobs_ordered_by_timestamp = timestamp.get_timestamp(jobs=jobs)
        total_days = 0

        #max number of skills
        max_total_skills = 10
        if len(jobs) == 1:
            max_skills_per_job = 10
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
                if language["language"] == "fr":
                    emsi_filtered = self.emsi_df.loc[self.emsi_df["french_titles"] == value]
                elif language["language"] == "en":
                    emsi_filtered = self.emsi_df.loc[self.emsi_df["jobs"] == value]

                #Reset index and get onet code
                emsi_filtered.reset_index(drop=True,inplace=True)

                #Get the number of skills to add from the last job
                number_of_skills = round((jobs[value]["daysDifference"] / total_days) * max_total_skills)

                #If max skills per job = 10 means that we received just one job.
                if max_skills_per_job == 10:
                    pass
                
                #If received more than one job, and it's the first of the list, add 2 skills if possible
                else:
                    if (number_of_skills + 2) < max_total_skills and number_of_skills < max_skills_per_job:
                        number_of_skills += 2
                    else:
                        number_of_skills = 5

                #Get the skills
                #If french language
                if language["language"] == "fr":
                    temp_skills = list(emsi_filtered["french_skills"][0])

                #If english
                elif language["language"] == "en":
                    temp_skills = list(emsi_filtered["skills"][0])

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

                #temp_skills = temp_skills[:number_of_skills]
                #sum the total number of used skills to control the max number to 10
                skills_added += len(skills_list_to_append)

                #update the skills
                skills.update({value:skills_list_to_append})


            #not the last job
            elif skills_added < max_total_skills:
                temp_max_skills = max_total_skills - skills_added

                #Check the language to load the right title list
                if language["language"] == "fr":
                    emsi_filtered = self.emsi_df.loc[self.emsi_df["french_titles"] == value]
                elif language["language"] == "en":
                    emsi_filtered = self.emsi_df.loc[self.emsi_df["jobs"] == value]

                #Reset index and get onet code
                emsi_filtered.reset_index(drop=True,inplace=True)

                #Get the number of skills to add from the last job
                number_of_skills = round((jobs[value]["daysDifference"] / total_days) * max_total_skills)


                if number_of_skills <= temp_max_skills:
                    #Get the skills
                    #If french language
                    if language["language"] == "fr":
                        temp_skills = list(emsi_filtered["french_skills"][0])

                    #If english
                    elif language["language"] == "en":
                        temp_skills = list(emsi_filtered["skills"][0])

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
                    while sk_counter <= number_of_skills:
                        if temp_skills[sk_counter] not in skills_list_to_append and temp_skills[sk_counter] not in used_skills:
                            skills_list_to_append.append(temp_skills[sk_counter])
                            used_skills.append(temp_skills[sk_counter])
                            sk_counter +=1

                        else:
                            sk_counter +=1
                        skills_added += len(skills_list_to_append)
                        skills.update({value:skills_list_to_append})

                else:
                    #Get the skills
                    #If french language
                    if language["language"] == "fr":
                        temp_skills = list(emsi_filtered["french_skills"][0])

                    #If english
                    elif language["language"] == "en":
                        temp_skills = list(emsi_filtered["skills"][0])

                    temp_skills = temp_skills[:temp_max_skills]
                    skills_added += len(temp_skills)
                    skills.update({value:temp_skills})
                    break


        return skills
