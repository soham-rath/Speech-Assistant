"""
so that computer listens start with: computer ...
comands:
so that computer ignores say: cancel
so that the computer says something you wnánt it to say: say ...
You can say/ask:
greetings = ['hey there', 'hello', 'hi', 'hai', 'hey!', 'hey']
question = ['how are you?', 'how are you doing?']
comand1 = ['play music', 'play songs', 'play a song', 'open music player']
comand2 = ['tell a joke', 'tell me a joke', 'say something funny', 'tell something funny']
comand3 = ['exit', 'close', 'goodbye', 'nothing', 'stop', 'do not do anything', "don't do anything"]
comand4 = ['thank you']
time = ['what time is it', 'what is the time', 'time']
to open youtube say: open youtube and play ...
to open wikipedia say: open wikipedia and search ...
to open google say: open google and search ...
to translate say: translate from (language) to (language) ...
to find synonym and translate say: find the synonym for ...
to turn audio into text say: turn audio into text ...
to answer questions just ask question
"""

import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import pywhatkit as pwk
import datetime
import random
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from deep_translator import PonsTranslator
#from googleapi import google


recognizer = sr.Recognizer()
engine = pyttsx3.init()

greetings = ['hey there', 'hello', 'hi ', 'hai', 'hey!', 'hey']
greetings = ('hey there', 'hello', 'hi ', 'hai', 'hey!', 'hey')
question = ('how are you?', 'how are you doing?')
responses = ('okay', "I'm fine", "I'm doing great, thank you!")
time = ('what time is it', 'what is the time', 'time')
cmd1 = ('play music', 'play songs', 'play a song', 'open music player')
cmd2 = ('tell a joke', 'tell me a joke', 'say something funny', 'tell something funny')
jokes = (
    'Can a kangaroo jump higher than a house? Of course, a house doesn’t jump at all.',
    'My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.',
    'Doctor: I\'m sorry, but you suffer from a terminal illness and have only 10 to live. Patient: What do you mean, 10? 10 what? Months? Weeks?! Doctor: Nine.'
)
cmd3 = ('exit', 'close', 'goodbye', 'nothing', 'stop', 'do not do anything', "don't do anything")
cmd4 = ('thank you')
replies = ('you\'re welcome', 'glad I could help you')

def popf(t,n):
    for i in range(1,n+1):
        t.pop(0)
    return t

def respond(t):
    engine.say(t)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    t = input("Input: ")
    print(t)
    text = t.lower().split()
    commands(text,t)
    try:
        print("Recognizing")
        t = recognizer.recognize_google(audio)
        text = t.lower().split()
        commands(text)
    except sr.UnknownValueError:
        listen()
    except sr.RequestError:
        respond("Sorry, my speech recognition service is down.")

def commands(text,t):
    #text = popf(text,2)
    if "cancel" in text:
        main()
    elif text[0] == "say":
        say_text(text)
    elif t in greetings:
        greet()
    elif t in question:
        give_response()
    elif t in cmd1:
        play_music()
    elif t in cmd2:
        tell_joke()
    elif t in cmd3:
        say_goodbye()
    elif t in cmd4:
        tell_reply()
    elif t in time:
        tell_time()
    elif text[0] == "open":
        cmd_open(text)
    elif "translate" in text:
        translate_text(text)
    elif "synonym" in text:
        synonym_word(text)
    elif "audio into text" in text:
        audio_text(text)
    elif "wikipedia" in text:
        wikipedia(text)
    else:
        query(t)
def tell_time():
    now = datetime.datetime.now()
    respond(now.strftime("The time is %H:%M"))
def tell_reply():
    respond(random.choice(replies))
def greet():
    respond(random.choice(greetings))
def give_response():
    respond(random.choice(responses))
def say_goodbye():
    respond("Goodbye!")
    exit()
def play_music():
    webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    listen()
def tell_joke():
    respond(random.choice(jokes))
def say_text(text):
    text = popf(text,1)
    respond(text)
def cmd_open(text):
    text = popf(text,1)
    if text[0] == "youtube":
        search_youtube(text)
    elif text[0] == "wikipedia":
        search_wikipedia(text)
    elif text[0] == "google":
        search_google(text)
def search_youtube(text):
    text = popf(text,3)
    search_query = " ".join(text)
    pwk.playonyt(search_query)
    listen()
def search_wikipedia(text):
    text = popf(text,3)
    respond(wikipedia.summary(text,2))
    listen()
def search_google(text):
    text = popf(text,3)
    url = f"https://www.google.com.tr/search?q={text}"
    webbrowser.open_new_tab(url)
    listen()
def translate_text(text):
    text = popf(text,5)
    source_lang = None
    target_lang = None
    query = []
    for word in text:
        if word.lower() == "from":
            source_lang = text[text.index(word) + 1]
        elif word.lower() == "to":
            target_lang = text[text.index(word) + 1]
        else:
            query.append(word)
    query = " ".join(query)
    translated = GoogleTranslator(source=source_lang, target=target_lang).translate(query)
    print(translated)
    respond(translated)
    listen()
def synonym_word(text):
    text = popf(text,4)
    source_lang = None
    target_lang = None
    query = []
    for word in text:
        if word.lower() == "from":
            source_lang = text[text.index(word) + 1]
        elif word.lower() == "to":
            target_lang = text[text.index(word) + 1]
        else:
            query.append(word)
    query = " ".join(query)
    translated = PonsTranslator(source=source_lang, target=target_lang).translate(query,  return_all=True)
    print(translated)
    respond(translated)
    listen() 
def wikipedia(text):
    text = popf(text,1)
    url = f"https://de.wikipedia.org/wiki/{text}"
    webbrowser.open_new_tab(url)
def audio_text(text):
    text = popf(text,4)
    respond(text)
    print(text)
def query(text):
    respond(wikipedia.summary(text,2))
    listen()
    #URL = "https://www.google.com.tr/search?q=" + t
    #headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    #page = requests.get(URL, headers=headers)
    #soup = BeautifulSoup(page.content, "html.parser")
    #result = soup.find(class_="ZOLcW XcVN5d").get_text()
    #respond("The answer is", result)
    #respond("I dont know!")
def automate():
    webbrowser.open_new("zapier.com/apps/code/integrations")

def main():
    respond("What can I do for you?")
    listen()

#if __name__ == '__main__':
while True:
    main()