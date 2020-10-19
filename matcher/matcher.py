import time
import spacy
import warnings
import operator
import numpy as np
import pandas as pd
import logging as log
from tqdm import tqdm
from collections import Counter
warnings.filterwarnings("ignore")
import collections
import io
from matcher.similarity import Similarity
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

simi = Similarity()

class Matcher():
    def __init__(self):
        spacy.prefer_gpu() # or spacy.require_gpu()
        self.nlp_en = spacy.load("en_core_web_md",parser=False)
        #self.nlp_fr = spacy.load("fr_core_news_md")
    def get_top_similarities(self, word, word_list, token_list, n, nlp):
        similarities = {}
        #doc1 = nlp(str(word))
        for i in tqdm(range(len(word_list))):
            #doc2 = token_list[i]
            #similarities[word_list[i]] = simi.get_title_similarity(doc1,doc2) #doc1.similarity(doc2)
            similarities[word_list[i]] = fuzz.token_set_ratio(str(word),word_list[i])
        sorted_similarity = sorted(similarities.items(),key=operator.itemgetter(1),reverse=True)
        return sorted_similarity[:n]




    def word_count(self,string):
        counts = dict()
        for i in string:
            words = i.split()
            for word in words:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
        counts = dict(sorted(counts.items(), key=operator.itemgetter(1),reverse=True))
        return counts



if __name__ == '__main__':
    matcher = Matcher()