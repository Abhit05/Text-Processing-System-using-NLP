
from future.builtins import next
#@author: amaurya
import streamlit as st
import pandas as pd
import os
import csv
import re
import logging
import optparse
import dedupe
from unidecode import unidecode
import base64
import spacy
import numpy as np


st.title('End Users Script')

def main():
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",["Endusers Identification", "Show instructions"])
    if app_mode == "Show instructions":
        st.sidebar.success('To continue select "Deduplication".')
    elif app_mode == "Endusers Identification":
        #readme_text.empty()
        #st.sidebar.success('To get instruction select a radio box from below.')
        #st.title("Deduplications")
        nlp_ner()


def file_chooser():
    file_bytes = st.file_uploader("Upload a file", type=("csv","xlsx",".xls"))
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

def preProcess(column):
    """
    Do a little bit of data cleaning with the help of Unidecode and Regex.
    Things like casing, extra spaces, quotes and new lines can be ignored.
    """
    try : # python 2/3 string differences
        column = column.decode('utf8')
    except AttributeError:
        pass
    column = unidecode(column)
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
    # If data is missing, indicate that by setting the value to `None`
    if not column:
        column = None
    return column

def readData(filename,id_col):
    """
    Read in our data from a CSV file and create a dictionary of records,
    where the key is a unique record ID and each value is dict
    """
    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
            print(clean_row)
            row_id = int(row[id_col])
            data_d[row_id] = dict(clean_row)
    return data_d

def trans(x):
    return unidecode(str(x))


def nlp_ner():
    data=pd.DataFrame()
    st.write("Choose a File")
    data=file_chooser()
    st.subheader("Source Data")
    if st.checkbox("Show Source Data"):
        st.write("The Sample Data is as follows:")
        st.write(data.head())
    msg1=("Total number of records : " + str(len(data)))
    st.info(msg1)
    cols_for_identification = st.selectbox('Select column to use for EUI', data.columns)
    country_columns = st.selectbox('Select Country column to use', data.columns)
    tags=st.multiselect("Select a Model to use use :",["Large","Medium","Small"])
    if st.button("Start EUI"):
        with st.spinner('Processing File...'):
            data=spacy_models(data,cols_for_identification,country_columns)
            st.success('Completed! **You can download the file using the below Link :)**')
        st.balloons()
        #if output_name is not None:
        #    csv = out.to_csv(index=False)
            #csv = out.to_excel("Output_"+str(date.today())+"_"+output_name,index=False)
        #else:
        #    output_name="Default"
        #    csv = out.to_csv(index=False)
            #csv = out.to_excel("Output_"+str(date.today())+"_"+output_name,index=False)
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">Download Output File</a> (right-click and save as &lt;some_name&gt;.csv)'
        st.markdown(href, unsafe_allow_html=True)
            #output_name=("Output_",datetime.datetime.today())
    else:
        st.markdown("> ** Click on Start webscraping Button to Start the processing ** ")

def spacy_models(data,column_as,country_col):
    nlp = spacy.load('en_core_web_md')
    for indexes,row in data.iterrows():
        val=row[column_as]
        #print(val)
        if val=='nan' or len(str(val))<=1:
            a.append("No Tag")
        else:
            doc = nlp(str(val))
            i_names={}
            cell_tag=[]
            for ent in doc.ents:
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)
                i_names[val[int(ent.start_char):int(ent.end_char)]]=(ent.label_)
                cell_tag.append(ent.label_)
            #print("-----------------------------------")
            a.append(i_names)
            tags.append(cell_tag)

if __name__ == "__main__":
    main()
