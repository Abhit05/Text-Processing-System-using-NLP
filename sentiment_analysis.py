#Necessary imports
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
import nltk
nltk.download('punkt')

#Headings for Web Application
st.title("Natural Language Processing Web Application Example")
st.subheader("What type of NLP service would you like to use?")

#Picking what NLP task you want to do
option = st.selectbox('NLP Service',('Sentiment Analysis', 'Entity Extraction', 'Text Summarization')) #option is stored in this variable

#Textbox for text user is entering
st.subheader("Enter the text you'd like to analyze.")
text = st.text_input('Enter text') #text is stored in this variable

#Display results of the NLP task
st.header("Results")

#Function to take in dictionary of entities, type of entity, and returns specific entities of specific type
def entRecognizer(entDict, typeEnt):
    entList = [ent for ent in entDict if entDict[ent] == typeEnt]
    return entList


#Sentiment Analysis
if option == 'Sentiment Analysis':

    #Creating graph for sentiment across each sentence in the text inputted
    sents = sent_tokenize(text)
    entireText = TextBlob(text)
    sentScores = []
    for sent in sents:
        text = TextBlob(sent)
        score = text.sentiment[0]
        sentScores.append(score)

    #Plotting sentiment scores per sentencein line graph
    st.line_chart(sentScores)

    #Polarity and Subjectivity of the entire text inputted
    sentimentTotal = entireText.sentiment
    st.write("The sentiment of the overall text below.")
    st.write(sentimentTotal)

#Named Entity Recognition
elif option == 'Entity Extraction':

    #Getting Entity and type of Entity
    entities = []
    entityLabels = []
    doc = nlp(text)
    for ent in doc.ents:
        entities.append(ent.text)
        entityLabels.append(ent.label_)
    entDict = dict(zip(entities, entityLabels)) #Creating dictionary with entity and entity types

    #Using function to create lists of entities of each type
    entOrg = entRecognizer(entDict, "ORG")
    entCardinal = entRecognizer(entDict, "CARDINAL")
    entPerson = entRecognizer(entDict, "PERSON")
    entDate = entRecognizer(entDict, "DATE")
    entGPE = entRecognizer(entDict, "GPE")

    #Displaying entities of each type
    st.write("Organization Entities: " + str(entOrg))
    st.write("Cardinal Entities: " + str(entCardinal))
    st.write("Personal Entities: " + str(entPerson))
    st.write("Date Entities: " + str(entDate))
    st.write("GPE Entities: " + str(entGPE))

#Text Summarization
else:
    summWords = summarize(text)
    st.subheader("Summary")
    st.write(summWords)
'''import streamlit as st
import pandas as pd

st.title('Sentiment Analysis App')

def main():
    #st.sidebar.title("What to do")
    #app_mode = st.sidebar.selectbox("Choose the algorithm for Sentiment Analysis",["Logistic Regression", "Naïve Bayes"])
    st.write("Enter your sentence/word here:")
    text=st.text_input('Enter your sentence/word here:')
    model_to_be_used=st.selectbox('Select the Model', ["Logistic Regression", "Naïve Bayes"])
    if st.button("Identify Sentiment"):
        with st.spinner('Processing File...'):
            if model_to_be_used=='Logistic Regression':
                start_regression(text)
            elif model_to_be_used=='Naïve Bayes':
                start_naive(text)
    else:
        st.markdown("> ** Click on Identify Sentiment Button to start the processing ** ")
    #if app_mode == "Logistic Regression":
    #    st.sidebar.success('Logistic Regression Model')
    #    logistic_model()
    #elif app_mode == "Naïve Bayes":
    #    st.sidebar.success('Naïve Bayes Model')
    #    naive_bayes_algo()

if __name__ == "__main__":
    main()'''
