
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

st.title(test.test_print(4))

st.title('Named Entity Recognition')
#added this from lap2
#added from my lap1
def main():
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",["NER", "Sentiment Analysis",
    "Word Prediction","Topic Classification","Question Answering","Translation (Maybe)",
    "Autocorrect","POS Tagging","Summarize Text(Maybe)","Text Generation","Data Cleaning"])
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


def test_code():
    """def file_chooser_settings():
        file_bytes = st.file_uploader("Upload a settings file", type=(""))
        if file_bytes is not None:
            with st.spinner('Wait for it...'):
                data = pd.read_excel(file_bytes)
                st.success('File uploaded succesful!!')
            #st.write("File selected from Folder: ", os.path.abspath("../file_bytes"))
            #st.write('You selected `%s`' % filename)
        else:
            data=pd.DataFrame()
            #st.error('Unable to Load the selected file.Please choose another!!')
        return data

    def file_chooser_training():
        file_bytes = st.file_uploader("Upload a Training file", type=(""))
        if file_bytes is not None:
            with st.spinner('Wait for it...'):
                data = pd.read_excel(file_bytes)
                st.success('File uploaded succesful!!')
            #st.write("File selected from Folder: ", os.path.abspath("../file_bytes"))
            #st.write('You selected `%s`' % filename)
        else:
            data=pd.DataFrame()
            #st.error('Unable to Load the selected file.Please choose another!!')
        return data"""



def spacy_ner(text,model_name):
    if model_name=='Large':
        nlp = spacy.load('en_core_web_md')
    elif model_name=='Small':
        nlp = spacy.load('en_core_web_sm')
    elif model_name=='Medium':
        nlp = spacy.load('en_core_web_lg')
    else:
        st.write('Please Choose a Model')


    #doc = nlp(str(text))
    spacy_streamlit.visualize(nlp, text)
    #for ent in doc.ents:
    #    print(ent.text, ent.start_char, ent.end_char, ent.label_)



if __name__ == "__main__":
    main()
