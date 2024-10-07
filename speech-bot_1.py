"""

comands:
so that computer ignores say: cancel
so that the computer says something you wnánt it to say: say ...
You can say/ask:
greetings = ['hey there', 'hello', 'hi', 'hai', 'hey!', 'hey']
question = ['how are you', 'how are you doing']
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
to automate something say: automate
"""

import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import pywhatkit as pwk
import datetime
import os
import random
from googlesearch import search
from deep_translator import GoogleTranslator
from deep_translator import PonsTranslator
import pyjokes

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Voice settings
informative_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
informative_volume = 1.0
informative_rate = 180

humorous_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
humorous_volume = 0.8
humorous_rate = 150

casual_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\TTS_MS_EN-US_HELEN_11.0"
casual_volume = 0.6
casual_rate = 160

# Greetings and responses
question = ['how are you', 'how are you doing']
responses = ['okay', "I'm fine", "I'm doing great, thank you!"]

# Commands
cmd1 = ['play music', 'play songs', 'play a song', 'open music player']
cmd2 = ['tell a joke', 'tell me a joke', 'say something funny', 'tell something funny']
cmd3 = ['exit', 'close', 'goodbye', 'nothing', 'stop', 'do not do anything', "don't do anything"]
cmd4 = ['thank you']
replies = ['you\'re welcome', 'glad I could help you']
time = ['what time is it','what is the time']

# Jokes
jokes = [
    'Can a kangaroo jump higher than a house? Of course, a house doesn’t jump at all.',
    'My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.',
    'Doctor: I\'m sorry, but you suffer from a terminal illness and have only 10 to live. Patient: What do you mean, 10? 10 what? Months? Weeks?! Doctor: Nine.'
]

def set_voice_properties(voice_id, volume, rate):
    engine.setProperty('voice', voice_id)
    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)

def respond(t, voice_id, volume, rate):
    set_voice_properties(voice_id, volume, rate)
    engine.say(t)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
        print("Recognizing...")
        
    try:
        # Using google to recognize audio
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"An unexpected error occurred; {e}")
        return "None"
        
    return query
  

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        respond("Good Morning Sir !", informative_voice_id, informative_volume, informative_rate)
    elif hour>= 12 and hour<18:
        respond("Good Afternoon Sir !", informative_voice_id, informative_volume, informative_rate)  
    else:
        respond("Good Evening Sir !", informative_voice_id, informative_volume, informative_rate) 
    respond("I am your Assistant", informative_voice_id, informative_volume, informative_rate)
def tell_time():
    now = datetime.datetime.now()
    respond(now.strftime("The time is %H:%M"), informative_voice_id, informative_volume, informative_rate)
def tell_reply():
    respond(random.choice(replies), casual_voice_id, casual_volume, casual_rate)
def give_response():
    respond(random.choice(responses), casual_voice_id, casual_volume, casual_rate)
def say_goodbye():
    respond("Goodbye!", casual_voice_id, casual_volume, casual_rate)
    exit()
def play_music():
    webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    listen()
def tell_joke():
    respond(pyjokes.get_joke(), humorous_voice_id, humorous_volume, humorous_rate)
def say_text(text_list):
    text_list = text_list[1:-1]
    respond("".join(text_list), casual_voice_id, casual_volume, casual_rate)
def cmd_open(text_list):
    text_list.pop(0)
    if text_list[0] == "youtube":
        search_youtube(text_list)
    elif text_list[0] == "wikipedia":
        search_wikipedia(text_list)
    elif text_list[0] == "google":
        search_google(text_list)
def search_youtube(text_list):
    text_list = text_list[3:-3]
    pwk.playonyt("".join(text))
    listen()
def search_wikipedia(text_list):
    text_list = text_list[3:-3]
    respond(wikipedia.summary(text_list), informative_voice_id, informative_volume, informative_rate)
    listen()
def search_google(text_list):
    text_list = text_list[3:-3]
    text = "".join(text_list)
    url = f"https://www.google.com.tr/search?q={text}"
    webbrowser.open_new_tab(url)
    listen()
def translate_text(text_list):
    text_list = text_list[5:-5]
    source_lang = None
    target_lang = None
    query = []
    for word in text_list:
        if word.lower() == "from":
            source_lang = text_list[text_list.index(word) + 1]
        elif word.lower() == "to":
            target_lang = text_list[text_list.index(word) + 1]
        else:
            query.append(word)
    query = " ".join(query)
    translated = GoogleTranslator(source=source_lang, target=target_lang).translate(query)
    print(translated)
    respond(translated, informative_voice_id, informative_volume, informative_rate)
    listen()
def synonym_word(text_list):
    text_list = text_list[5:-5]
    source_lang = None
    target_lang = None
    query = []
    for word in text_list:
        if word.lower() == "from":
            source_lang = text_list[text_list.index(word) + 1]
        elif word.lower() == "to":
            target_lang = text_list[text_list.index(word) + 1]
        else:
            query.append(word)
    query = " ".join(query)
    translated = PonsTranslator(source=source_lang, target=target_lang).translate(query,  return_all=True)
    print(translated)
    respond(translated, informative_voice_id, informative_volume, informative_rate)
    listen()
def audio_text(text_list):
    text_list = text_list[4:-4]
    print(text_list)
def query(text):
    searchResultList = list(search(text, advanced=True))
    respond(searchResultList[0].title, informative_voice_id, informative_volume, informative_rate)
    respond(searchResultList[0].description, informative_voice_id, informative_volume, informative_rate)
def automate():
    webbrowser.open_new("zapier.com/apps/code/integrations")

if __name__ == '__main__':
    set_voice_properties(informative_voice_id, informative_volume, informative_rate)
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    while True:
        text = listen().lower()
        text_list = text.split()
        print(text_list)
        if text_list == "none":
            continue
        elif "cancel" in text_list:
            listen()
        elif text_list[0] == "say":
            say_text(text_list)
        elif text in question:
            give_response()
        elif "fine" in text_list or "good" in text_list:
            respond("It's good to know that your fine", casual_voice_id, casual_volume, casual_rate)
        elif "who made you" in text or "who created you" in text_list:
            respond("I have been created by Soham.", casual_voice_id, casual_volume, casual_rate)
        elif text in cmd1:
            play_music()
        elif text in cmd2:
            tell_joke()
        elif text in cmd3:
            say_goodbye()
        elif text in cmd4:
            tell_reply()
        elif text in time:
            tell_time()
        elif text_list[0] == "open":
            cmd_open(text_list)
        elif "translate" in text_list:
            translate_text(text_list)
        elif "synonym" in text_list:
            synonym_word(text_list)
        elif "audio into text" in text_list:
            audio_text(text_list)
        else:
            query(text)