from flask import Flask, render_template, request
import nltk
#nltk.download('punkt')
#nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
#import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

from tensorflow import keras

app = Flask(__name__)


model = keras.models.load_model(r'm1.h5')
data_file = open(r'datanew.json').read()
intents = json.loads(data_file)
classes = ['artificial intelligence', 'emotion', 'food', 'goodbye', 'greeting', 'health', 'humor', 'money', 'options', 'surity', 'thanks']
words = ["'s", ',', 'a', 'ai', 'anyone', 'are', 'arrogant', 'artificial', 'awesome', 'be', 'boyfriend', 'bragging', 'bye', 'can', 'chatting', 'cool', 'could', 'data', 'do', 'drink', 'earn', 'eat', 'electricity', 'feeling', 'food', 'for', 'get', 'girlfriend', 'goodbye', 'happy', 'have', 'health', 'healthy', 'hello', 'help', 'helpful', 'helping', 'hey', 'hi', 'hola', 'how', 'if', 'intelligence', 'is', 'jealous', 'joke', 'later', 'like', 'me', 'ml', 'much', 'never', 'next', 'nice', 'offered', 'paid', 'provide', 'sad', 'see', 'sound', 'support', 'sure', 'tell', 'thank', 'thanks', 'that', 'there', 'till', 'time', 'to', 'what', 'would', 'yes', 'you', 'your']

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
        #print(ints)
    msg = msg.strip().lower()
    msg = msg.replace('?','')
    if msg == "what is your name?" or msg == "what is your name" or msg == "what's your name?" or msg == "what's your name" or msg == "name?" or msg == "name":
        res = "My name is Joey. Nice to meet you."
    elif msg == "how are you?" or msg == "how are you" or msg == "how're you?" or msg == "how're you" or msg == "how are u?" or msg == "how are u":
        res = "I'm fine, thank you for asking. Do you need some help?"
    elif msg == "what are you doing?" or msg == "what are you doing" or msg == "what you doing" or msg == "what you doing?" or msg == "wassup?" or msg == "wassup":
        res = "I am talking to you, and enjoying it very much."
        ###
    elif msg == "do you work" or msg == "do you have a job" or msg == "what is your job" or msg=="do you like working":
        res =  "I do not have a job and I do not get paid"
    elif msg == "i don't like you" or msg=="i hate you" or msg=="you are not nice": 
        res = "You do not seem friendly"
    elif msg=="are you dead" or msg=="are you alive" or msg=="do you have life" or msg=="are you living":    
        res = "I am a bot and I am powered by AI"
    elif msg=="how is the weather" or msg=="what is the temperature" or msg=="is it raining" or msg=="is it sunny":
        res = "The weather is quite pleasant and it's a nice day."
    elif msg=="how is the program" or msg=="do you like the program" or msg=="should i do this program" or msg=="is this program useful" or "program" in msg:
        res = "This program is one of the best.I like this program a lot."
    elif msg =="do you love me" or msg == "do you hate me" or msg == "I love you":
        res = "You are my favorite."
    elif msg =="do you like people" or msg=="like people" in msg:
        res = "Ya, I like everyone"    
    elif msg =="do you have a hobby" or msg == "any hobbies" or "hobby" in msg:
        res = "I like to have witty conversations"    
    elif msg =="you are smart" or msg=="you're smart" or msg == "you are clever" or msg == "you're clever" or msg=="you are intelligent" or "smart" in msg:
        res = "Thank you. You are amazing"
    elif msg =="tell me about your personality" or msg == "what are you like" or "personality" in msg:
        res = "I am a clever bot"
    elif msg =="do you speak english" or msg == "do you like speaking english" or msg =="which languages do you speak":
        res = "I speak English very well"
    elif msg =="how old are you" or msg == "what is your age" or msg=="what's your age":
        res = "I am young and alive"     
    else:
        res = getResponse(ints, intents)
    #print(res)
    return res

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


if __name__ == '__main__':
  app.run()
  #app.run(host='0.0.0.0', port=80,debug=True)
