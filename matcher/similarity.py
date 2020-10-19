#imports
import spacy
import pandas as pd
class Similarity():
    def __init__(self):
        print("")

    def get_title_similarity(self, title_search_token, title_found_token):
        """
        title_search: The text used on job query. eg.: Java Developer
        title_found: The Title returned by the response from the host. eg.: Senior Java Web Developer


        Logic Summary:

        Title == Title_Found: Similarity == 1

        Title in Title_Found: Similarity == Similarity * 1.3 if Similarity < 0.6

        Title in Title_Found: Similarity == Similarity * 1.2 if the equation is lower than 1
            else:
                Similarity == Similarity * 1.1 if the equation is lower than 1
                    else:
                        Similarity == Similarity * 1.05 if the equation is lower than 1
                            else:
                                Similarity == Similarity


        If none of the above rules fits than:
            Check if all the words from Title are inside Title Found and give a 20% bonus.

        Afterall if Title in Title_found and yet the Similarity is lower than 0.6, set Similarity=0.6

        """
        #Check if the job title searched is inside the job title found
        title_search = str(title_search_token.text).lower()
        title_found = str(title_found_token.text).lower()
        similarity_value = 0
        if title_search in title_found:
            #check if its equal and set 1.0 to equal
            if title_search.lower() == title_found.lower():
                #max value for similarity
                similarity_value = 1.3
            else:



                #If it has Title in Title Found, we don't want the similarity being too low
                #so We give a 20% bonus for these cases
                if float(title_search_token.similarity(title_found_token)) < 0.6:
                    similarity_value = float(title_search_token.similarity(title_found_token)) * 1.3

                #if it's not equal but it has the title inside give a 20% bonus of similarity
                #if the similarity time 1.1 is less than 1
                elif (float(title_search_token.similarity(title_found_token)) * 1.2) < 1.2:
                    similarity_value = float(title_search_token.similarity(title_found_token)) * 1.2

                #else if the similarity times 1.1 is smaller than 1
                elif (float(title_search_token.similarity(title_found_token)) * 1.1) < 1.2:
                    similarity_value = float(title_search_token.similarity(title_found_token)) * 1.1

                #else if the similarity times 1.05 is smaller than 1
                elif (float(title_search_token.similarity(title_found_token)) * 1.05) < 1.2:
                    similarity_value = (title_search_token.similarity(title_found_token)) * 1.05

                #if not just set the similarity
                else:
                    similarity_value = float(title_search_token.similarity(title_found_token))
        #if the job title searched is not inside the job title found just set the similarity
        else:
            #Check if all the words in the title are inside Title_found
            words_in_title_found = True
            
            for word in title_search.split():
                if str(word).lower() not in title_found.lower():
                    words_in_title_found = False




            #if all the words are inside the title found but in diferent order give 10% bonus to similarity
            if words_in_title_found:
                similarity_value = float(title_search_token.similarity(title_found_token)) * 1.1

            #if not, just set the similarity
            else:
                similarity_value = float(title_search_token.similarity(title_found_token))

        #Afterall if the Title is inside the Title_Found and yet the similarity is lower the 0.6
        #fix it at 0.6 - we don't want it to be less than 0.6
        if title_search.lower() in title_found.lower():

            if float(title_search_token.similarity(title_found_token)) < 0.6:
                similarity_value = 0.6
        return round(similarity_value,4)