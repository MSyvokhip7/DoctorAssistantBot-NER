from NER import *
import time
import telebot
import spacy
import os
import json
 
output_dir = os.getcwd()
MODEL = spacy.load(output_dir)

TOKEN = "881147208:AAGDY-ZvgqonfxS12Dn3GDPubCl4jiJtPJA"
bot = telebot.TeleBot(token=TOKEN)

FLAG = False
FLAG2 = True

diseasess = []
potential_diseas = []
things_to_ask = []

greeting_words = ["hi", "hello", "hey", "helloo", "hellooo",
                  "g morining", "gmorning", "good morning", "morning",
                  "good day", "good afternoon", "good evening", "greetings",
                  "greeting", "good to see you", "its good seeing you",
                  "how are you", "how're you", "how are you doing",
                  "how ya doin'", "how ya doin", "how is everything",
                  "how is everything going", "how's everything going",
                  "how is you", "how's you", "how are things",
                  "how're things",
                  "how is it going", "how's it going", "how's it goin'",
                  "how's it goin", "how is life been treating you",
                  "how's life been treating you", "how have you been",
                  "how've you been", "what is up", "what's up",
                  "what is cracking", "what's cracking", "what is good",
                  "what's good", "what is happening", "what's happening",
                  "what is new", "what's new", "what is neww", "g’day",
                  "howdy"]

@bot.message_handler(commands=['start']) 
def send_welcome(message):
    bot.reply_to(message, '''Hello, welcome to Doctor Asistant Bot. Please write all the symptomps that are bothering you, so that I can detect your disease.''')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'ALPHA = FEATURES MAY NOT WORK')
FLAG = False
@bot.message_handler(content_types=['text'])
def send_text(message):
    global FLAG
    global diseasess
    global potential_diseas
    global things_to_ask
    global MODEL
    global FLAG2

    counter = 1
    
    while FLAG:
        FLAG2 = False
        result = final_diseas(message.text,things_to_ask,diseasess)
        bot.send_message(message.chat.id, "Here is the list of potential diseases: ")
        for dis in result:
            bot.send_message(message.chat.id, str(counter) + ". " + dis)
            counter += 1
        FLAG = False
        
    if message.text.lower() in greeting_words:
        bot.send_message(message.chat.id, 'Hello, welcome to Doctor Asistant Bot. Please writ all the symptomps that are bothering you, so that I can detect your disease.')
        FLAG2 = True

    elif FLAG2:
        diseasess, potential_diseas, things_to_ask = algo(message.text)
        FLAG = True
        FLAG2 = False
        line_end = ''
        for symptom in things_to_ask:
            if symptom == things_to_ask[-1]:
                line_end += symptom
            else:
                line_end += symptom + " or "
        bot.send_message(message.chat.id, 'Can you please tell me which of the following symptoms do you have : ' + line_end)
    

@bot.message_handler(func=lambda msg: msg.text is not None)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):    texts = message.text.split()
    #print(texts)
while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
