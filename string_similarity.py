import pandas as pd
from difflib import SequenceMatcher
from cleanco import cleanco
import os
import time
from fuzzywuzzy import fuzz
import streamlit as st

def get_bigrams(string):
    s = str(string).lower()
    return [s[i:i+2] for i in list(range(len(s) - 1))]
def string_similarity(str1, str2):
    #print(str(str1)+"===>"+str(str2))
    pairs1 = get_bigrams(str(str1))
    pairs2 = get_bigrams(str(str2))
    union  = len(pairs1) + len(pairs2)
    if union==0:
        union=1
    #print(union)
    hit_count = 0
    for x in pairs1:
        for y in pairs2:
            if x == y:
                hit_count += 1
                break
    return (2.0 * hit_count) / union


#x=string_similarity('AFA','AFA')

def cal(a,b):
    score=[]
    for r in zip(a,b):
        #print(r[0],"---->", r[1])
        score.append(SequenceMatcher(None, str(r[0]).lower().strip(),str(r[1]).lower().strip()).ratio())
    return score

def analyze(txt1,txt2):
    st.write("The Similarity between the two text are:",round(string_similarity(txt1,txt2),2)*100,"%")
