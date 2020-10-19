from matcher.matcher import Matcher
import pandas as pd
import spacy
from translation.translate import Translator
from time_.timestamp import Timestamp
from time_.dates import Date
from neobrain_skills.skills_with_similarity import SkillsWithSimilarity
from neobrain_skills.skills_from_job_list import SkillsFromJob
from db_persist.persist import Persistence


#Load the EMSI dataframe
job_list_df = pd.read_pickle("data/job_titles.pkl")

#Load Spacy Model
#nlp = spacy.load("fr_core_news_md")
nlp = spacy.load("en_core_web_md", parser=False)

#Create Spacy token documents for each job in job_list_df jobs
token_list = list(nlp.pipe(job_list_df["jobs"]))

#Instances
timestamp = Timestamp()
translator = Translator()
date = Date()
matcher = Matcher()
skills_with_similarity = SkillsWithSimilarity(translator,matcher,job_list_df,nlp,token_list)
skills_from_job = SkillsFromJob(translator,matcher,job_list_df)
persistence = Persistence()

class SkillsList():
    """ This class receive the current requests and call the methods. The main objective is to load everything just once
    and distribute the calls."""

    #Match using spacy similarity
    def getSkillsList(self, jobs, language, max_skills):
        return skills_with_similarity.getSkillsList(jobs=jobs,language=language,max_skills=max_skills)

    #Match using a job list
    def getSkillsListWithoutSimilarity(self, jobs, language):
        return skills_from_job.getSkillsListWithoutSimilarity(jobs=jobs,language=language)

    def saveFeedBack(self, job_titles):
        return persistence.save_feedback(job_titles=job_titles)

    def saveScores(self, job_titles):
        return persistence.save_scores(job_titles=job_titles)