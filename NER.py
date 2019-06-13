from __future__ import unicode_literals, print_function
from pathlib import Path
import plac
import spacy
import random
from tqdm import tqdm
import pandas as pd
import os
 
output_dir = os.getcwd()
df = pd.read_csv('data.csv')
diseasess = []
for value in df['prognosis']:
    diseasess.append(value)

SYMPTOMS = []

MODEL = spacy.load(output_dir)

def algo(message):
    "Removing diseases that can not be relevant. By symptoms behaviour generating question for user"
    n = MODEL(message)
    
    for item in n.ents:
        SYMPTOMS.append(item.text.lower().replace(" ", "_"))


    for index, row in df.iterrows():  
        for symptom in SYMPTOMS:
            if row[symptom] == 0:
                if row['prognosis'] in diseasess:
                    diseasess.remove(row['prognosis'])

    top3 = ['vomiting', 'fatigue', 'high_fever']

    potential_diseas = []
    things_to_ask = []

    for index, row in df.iterrows():  
        for symptom in top3:
            if row[symptom] == 1 and row['prognosis'] in diseasess:
                potential_diseas.append(row['prognosis'])
                if symptom not in things_to_ask:
                    things_to_ask.append(symptom.replace("_", " "))
                break

    
    return diseasess, potential_diseas, things_to_ask

def final_diseas(message, things_to_ask, diseasess):
    "Computing final diseases based on user answer"
    
    new_symptom = []
    answer = []
    
    n = MODEL(message)
    for item in n.ents:
        answer.append(str(item))


    for item in things_to_ask:
        if item in answer:
            new_symptom.append(item)
       
    for index, row in df.iterrows():
        if row['prognosis'] in diseasess:
            for item in new_symptom:
                if row[item] == 0:
                     diseasess.remove(row['prognosis'])
                     
    return diseasess
