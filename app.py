
from future.builtins import next
#@author: amaurya
import streamlit as st
import pandas as pd
import os
import csv
import re
import logging
import optparse
from unidecode import unidecode
import base64
import spacy
import numpy as np
import spacy_streamlit
import test
import sentiment_analysis
import data_cleaning
import spacy_streamlit
import next_word_prediction
import string_similarity
#st.title(test.test_print(18))
st.set_page_config(page_title='Text Processing System')
st.title('Text Processing System')
#added this from lap2
#added from my lap1
def main():
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",["Show instructions","NER","NER_Visualization", "Sentiment Analysis",
    "Word Prediction","Data Cleaning","String Similarity"])
    st.write("Enter your sentence/word here:")
    text=st.text_input('Enter your sentence/word here:')
    if app_mode == "Show instructions":
        st.sidebar.success('To continue select another')
    elif app_mode == "NER":
        models=st.selectbox("Select a Model to use use :",["Large","Medium","Small"])
        if st.button("Identify Entities"):
            with st.spinner('Processing File...'):
                Output=spacy_ner(text,models)
                st.write(Output)
        else:
            st.markdown("> ** Click on Identify Entities Button to start the processing ** ")
    elif app_mode=="NER_Visualization":
            models = ["en_core_web_sm", "en_core_web_md","en_core_web_lg"]
            #default_text = "Sundar Pichai is the CEO of Google."
            spacy_streamlit.visualize(models,text)
    elif app_mode == "Test":
        test.execute(text)
    elif app_mode == "Sentiment Analysis":
        sentiment_analysis.start_run(text)
    elif app_mode == "Data Cleaning":
        data_cleaning.start_cleaning(text)
    elif app_mode=="Word Prediction":
        next_word_prediction.next_word(text)
    elif app_mode=="String Similarity":
        text2=st.text_input('Enter your second sentence/word here:')
        if st.button("Get Similarity"):
            string_similarity.analyze(text,text2)


@st.cache()
def spacy_ner(text,model_name):
    if model_name=='Large':
        nlp = spacy.load('en_core_web_md')
        st.write()
    elif model_name=='Small':
        nlp = spacy.load('en_core_web_sm')
    elif model_name=='Medium':
        nlp = spacy.load('en_core_web_lg')
    else:
        st.write('Please Choose a Model')
    a=[]
    doc = nlp(str(text))
    i_names={}
    #identified=[]
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
        i_names[text[int(ent.start_char):int(ent.end_char)]]=(ent.label_)
        #identified.append(ent.label_)
    print("-----------------------------------")
    a.append(i_names)
    return a

    #doc = nlp(str(text))
    #spacy_streamlit.visualize(nlp, text)
    #for ent in doc.ents:
    #    print(ent.text, ent.start_char, ent.end_char, ent.label_)
    #from next_word_prediction import GPT2
    #>>> gpt2 = GPT2()
    #>>> text = "The course starts next"
    #>>> gpt2.predict_next(text, 5)
    #The course starts next ['week', 'to', 'month', 'year', 'Monday']


if __name__ == "__main__":
    main()
