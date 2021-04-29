import pandas as pd
import streamlit as st
import string
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import re
def tokenize(text):
    split=re.split("\W+",text)
    return split
stopword = nltk.corpus.stopwords.words('english')

def remove_stopwords(text):
    text=[word for word in text.split(' ') if word not in stopword]
    return text

def simplify(text):
	import unicodedata
	try:
		text = unicode(text, 'utf-8')
	except NameError:
		pass
	text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
	return str(text)

def start_cleaning(text):
    app_mode = st.selectbox("Choose cleaning Needed",["Punctuation Removal","Tokenization",
    "Lower Casing","Stop words removal","Stemming","Lemmatization","Remove Numbers","Remove HTML Tags",
    "ASCII Conversion"])
    if app_mode == "Punctuation Removal":
        #s = "string. With. Punctuation?" # Sample string
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        no_punct = ""
        for char in text:
            if char not in punctuations:
                no_punct = no_punct + char
        st.write(no_punct)
        #st.sidebar.success('To continue select another')
    elif app_mode == "Tokenization":
        st.write(tokenize(text))
    elif app_mode=="Lower Casing":
        st.write(text.lower())
    elif app_mode == "Stop words removal":
        st.write(remove_stopwords(text))
    elif app_mode == "Stemming":
        porter = PorterStemmer()
        st.write(porter.stem(text))
    elif app_mode == "Lemmatization":
        lancaster=LancasterStemmer()
        st.write(lancaster.stem(text))
    elif app_mode=="Remove Numbers":
        st.write(''.join([i for i in text if not i.isdigit()]))
    elif app_mode=="ASCII Conversion":
        st.write(simplify(text))
