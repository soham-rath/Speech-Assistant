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
from deep_translator import GoogleTranslator, PonsTranslator
import pyjokes

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Voice settings
informative_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\SPEECH\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
informative_volume = 1.0
informative_rate = 180

humorous_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\SPEECH\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
humorous_volume = 0.8
humorous_rate = 150

casual_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\SPEECH\\Voices\\Tokens\\TTS_MS_EN-US_HELEN_11.0"
casual_volume = 0.6
casual_rate = 160

# Predefined phrases and commands
greetings = ['hey there', 'hello', 'hi', 'hai', 'hey!', 'hey']
questions = ['how are you', 'how are you doing']
cmd_play_music = ['play music', 'play songs', 'play a song', 'open music player']
cmd_joke = ['tell a joke', 'tell me a joke', 'say something funny', 'tell something funny']
cmd_exit = ['exit', 'close', 'goodbye', 'nothing', 'stop', 'do not do anything', "don't do anything"]
cmd_thanks = ['thank you']
time_queries = ['what time is it', 'what is the time', 'time']

def set_voice_properties(voice_id, volume, rate):
    engine.setProperty('voice', voice_id)
    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)

def respond(text, voice_id=informative_voice_id, volume=informative_volume, rate=informative_rate):
    set_voice_properties(voice_id, volume, rate)
    engine.say(text)
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
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "none"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "none"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "none"

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        respond("Good Morning Sir!", informative_voice_id, informative_volume, informative_rate)
    elif 12 <= hour < 18:
        respond("Good Afternoon Sir!", informative_voice_id, informative_volume, informative_rate)
    else:
        respond("Good Evening Sir!", informative_voice_id, informative_volume, informative_rate)
    respond("I am your Assistant.", informative_voice_id, informative_volume, informative_rate)

def tell_time():
    now = datetime.datetime.now()
    respond(now.strftime("The time is %H:%M"), informative_voice_id, informative_volume, informative_rate)

def play_music():
    # Plays a default YouTube video (Rickroll placeholder)
    webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def tell_joke():
    joke = pyjokes.get_joke()
    respond(joke, humorous_voice_id, humorous_volume, humorous_rate)

def say_text(text_list):
    text_to_say = " ".join(text_list[1:])
    respond(text_to_say, casual_voice_id, casual_volume, casual_rate)

def open_website_with_search(service, query_text):
    if service == "youtube":
        pwk.playonyt(query_text)
    elif service == "wikipedia":
        try:
            summary = wikipedia.summary(query_text, sentences=2)
            respond(summary, informative_voice_id, informative_volume, informative_rate)
        except Exception:
            respond("Sorry, I couldn't find that on Wikipedia.", informative_voice_id, informative_volume, informative_rate)
    elif service == "google":
        url = f"https://www.google.com/search?q={query_text.replace(' ', '+')}"
        webbrowser.open_new_tab(url)
        respond(f"Here are the Google search results for {query_text}", informative_voice_id, informative_volume, informative_rate)
    else:
        respond(f"Sorry, I can't open {service}. Try youtube, wikipedia, or google.", informative_voice_id, informative_volume, informative_rate)

def translate_text(text_list):
    try:
        if "from" in text_list and "to" in text_list:
            from_index = text_list.index("from")
            to_index = text_list.index("to")
            source_lang = text_list[from_index + 1]
            target_lang = text_list[to_index + 1]
            text_to_translate = " ".join(text_list[to_index + 2:])
            if not text_to_translate:
                respond("Please tell me what to translate.", informative_voice_id, informative_volume, informative_rate)
                return
            translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text_to_translate)
            respond(translated, informative_voice_id, informative_volume, informative_rate)
        else:
            respond("Please specify source and target languages like: translate from english to german ...", informative_voice_id, informative_volume, informative_rate)
    except Exception:
        respond("Sorry, translation failed.", informative_voice_id, informative_volume, informative_rate)

def find_synonym(text_list):
    try:
        if "for" in text_list:
            for_index = text_list.index("for")
            word = text_list[for_index + 1]
            synonyms = PonsTranslator(source="en", target="en").translate(word, return_all=True)
            if synonyms:
                synonyms_str = ", ".join(synonyms)
                respond(f"Synonyms for {word} are: {synonyms_str}", informative_voice_id, informative_volume, informative_rate)
            else:
                respond(f"No synonyms found for {word}.", informative_voice_id, informative_volume, informative_rate)
        else:
            respond("Please specify the word to find synonym for.", informative_voice_id, informative_volume, informative_rate)
    except Exception:
        respond("Failed to find synonyms.", informative_voice_id, informative_volume, informative_rate)

def audio_to_text():
    respond("Audio to text feature is not implemented yet.", informative_voice_id, informative_volume, informative_rate)

def answer_question(query_text):
    try:
        results = list(search(query_text, num_results=3))
        if results:
            respond("I found some results for you. Opening them now.", informative_voice_id, informative_volume, informative_rate)
            for url in results:
                webbrowser.open_new_tab(url)
        else:
            respond("Sorry, I couldn't find anything related.", informative_voice_id, informative_volume, informative_rate)
    except Exception:
        respond("Sorry, I couldn't perform the search.", informative_voice_id, informative_volume, informative_rate)

def automate():
    webbrowser.open_new("https://zapier.com/apps/code/integrations")
    respond("Opening automation tools for you.", informative_voice_id, informative_volume, informative_rate)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    wishMe()
    while True:
        text = listen()
        if text == "none":
            continue
        text_list = text.split()
        print(f"Processed command: {text_list}")

        # Ignore command
        if "cancel" in text_list:
            respond("Cancelled.", casual_voice_id, casual_volume, casual_rate)
            continue

        if not text_list:
            continue

        # Say command
        if text_list[0] == "say":
            say_text(text_list)
            continue

        # Greetings
        if any(greet in text for greet in greetings):
            respond(random.choice(["Hey!", "Hello!", "Hi there!"]), casual_voice_id, casual_volume, casual_rate)
            continue

        # How are you?
        if any(q in text for q in questions):
            respond(random.choice(["I'm good, thanks for asking!", "Doing well, how about you?"]), casual_voice_id, casual_volume, casual_rate)
            continue

        # Replies for fine/good
        if "fine" in text_list or "good" in text_list:
            respond("It's good to know that you're fine.", casual_voice_id, casual_volume, casual_rate)
            continue

        # Who made you?
        if "who made you" in text or "who created you" in text:
            respond("I have been created by Soham.", casual_voice_id, casual_volume, casual_rate)
            continue

        # Play music
        if any(cmd in text for cmd in cmd_play_music):
            play_music()
            continue

        # Tell joke
        if any(cmd in text for cmd in cmd_joke):
            tell_joke()
            continue

        # Exit
        if any(cmd in text for cmd in cmd_exit):
            respond("Goodbye!", casual_voice_id, casual_volume, casual_rate)
            break

        # Thank you
        if any(cmd in text for cmd in cmd_thanks):
            respond(random.choice(["You're welcome!", "Glad I could help!"]), casual_voice_id, casual_volume, casual_rate)
            continue

        # Time query
        if any(tq in text for tq in time_queries):
            tell_time()
            continue

        # Open commands: open youtube/wikipedia/google and search/play
        if text_list[0] == "open":
            if len(text_list) >= 3:
                service = text_list[1]
                if service in ["youtube", "wikipedia", "google"]:
                    if "play" in text_list:
                        action_index = text_list.index("play")
                    elif "search" in text_list:
                        action_index = text_list.index("search")
                    else:
                        respond(f"Please say 'play' or 'search' after {service}.", informative_voice_id, informative_volume, informative_rate)
                        continue
                    query_text = " ".join(text_list[action_index + 1:])
                    if not query_text:
                        respond("Please specify what to search or play.", informative_voice_id, informative_volume, informative_rate)
                        continue
                    open_website_with_search(service, query_text)
                    continue
                else:
                    respond(f"I can't open {service}. Try youtube, wikipedia, or google.", informative_voice_id, informative_volume, informative_rate)
                    continue
            else:
                respond("Please specify what to open.", informative_voice_id, informative_volume, informative_rate)
                continue

        # Translate command
        if text_list[0] == "translate":
            translate_text(text_list)
            continue

        # Find synonym command
        if "synonym" in text_list:
            find_synonym(text_list)
            continue

        # Audio to text command
        if "audio" in text and "text" in text:
            audio_to_text()
            continue

        # Automate
        if "automate" in text_list:
            automate()
            continue

        # Fallback: treat input as a question to answer
        answer_question(text)
