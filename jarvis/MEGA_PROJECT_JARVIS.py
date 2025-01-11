import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import movie
import pygame
import threading
import os,time
import google.generativeai as genai

r = sr.Recognizer()  # Recognizes the sound
engine = pyttsx3.init()
newsapi = "news api"
link = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=newsapi"

def speak(text):
    if not listening_flag.is_set(): 
        engine.say(text)
        engine.runAndWait()

def googleai(c):
    assistant_thread = threading.Thread()
    assistant_thread.start()

    genai.configure(api_key="your_api_key")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(c)
    response.max_output_tokens = 250
   
    while not listening_flag.is_set():  # Stop if the flag is set
        print(response.text)
        speak(response.text)
        time.sleep(1)  # Pause between speeches


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open chat gpt" in c.lower():
        webbrowser.open("https://chatgpt.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link1 = musicLibrary.music[song]
        webbrowser.open(link1)
    elif c.lower().startswith("watch"):
        mov = c.lower().split(" ")[1]
        link1 = movie.mov[mov]
        os.startfile(link1)
    elif "news" in c.lower():
        r = requests.get("{link}")
        if r.status_code == 200:
            # parse the json response
            data = r.json()

            #extract the articles
            articles = data.get('articles',[])

            # speak the articles
            for article in articles:
                print(article['title'])
                speak(article['title'])
    else:
        googleai(c)
         

def listen():
    with sr.Microphone() as source:  
            print("listening....")
            # r.adjust_for_ambient_noise(source)
            audio = r.listen(source,timeout=5,phrase_time_limit=2)  
            print("recognizing....")
            word = r.recognize_google(audio)
            print(word)
            return word
listening_flag = threading.Event()

def listen_for_stop():
    recognizer = sr.Recognizer()
    print("Listening for 'stop' command...")
    while not listening_flag.is_set():  # Keep listening until the flag is set
        try:
            with sr.Microphone() as source:
                # recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {command}")
            if "stop" in command:
                print("Stop command detected!")
                listening_flag.set()  # Signal to stop
                break
        except sr.UnknownValueError:
            continue  # Ignore unrecognized commands
        except sr.WaitTimeoutError:
            continue  # Keep waiting if no input

if __name__ == "__main__":
    speak("initializing JARVIS.......")
    while True:
        try:
            word = listen()
            if (word.lower() == "jarvis"):
                speak("yes sir?")
                while(True):
                # listen for command
                    command = listen()
                    listen_thread = threading.Thread(target=listen_for_stop)
                    listen_thread.start()
                    processCommand(command)
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error with recognition service: {e}")
        except sr.WaitTimeoutError as e:
            print(f"wait time out: {e}")
