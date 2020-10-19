
class SkillsTemplate():
    def __init__(self, translator,matcher):
        self.matcher = matcher
        self.threshold = 0.5
        self.min_level = 2.8
        self.qt = 10
        self.translator = translator


    def get_jobs(self,jobs,language):

        english_dict = {}
        titles = {}
        list_of_titles = ["CEO","CTO"]
        for i in jobs:
            if self.detect_language(i) != language and i not in list_of_titles:
                translated_title = self.translator.get_translation(i,language=language)
                english_dict.update({translated_title:jobs[i]})
                titles.update({translated_title:i})
            else:
                english_dict.update({i:jobs[i]})
                titles.update({i:i})
        return english_dict , titles

    def get_old_titles(self,titles, skills):
        old_titles = {}
        for i in skills:
            if i in titles:
                old_titles.update({titles[i]:skills[i]})
            else:
                pass
        return old_titles

    def detect_language(self,text):
        return "language"