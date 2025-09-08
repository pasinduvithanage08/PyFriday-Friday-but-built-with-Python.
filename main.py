import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import subprocess
import platform
import urllib.parse
import wikipedia
import requests
import os
from openai import OpenAI
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def speak(text):
    engine = pyttsx3.init()
    for sentence in text.split('. '):
        engine.say(sentence)
    engine.runAndWait()

def get_greeting():
    return "Good evening, sir, I am Friday, how may I help you?"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)
            command = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"Recognized command: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No command heard, waiting for your next command, sir...")
            return None
        except sr.UnknownValueError:
            print("Sorry, sir, I couldn't understand your command. Please speak clearly.")
            speak("Sorry, sir, I couldn't understand your command. Please speak clearly.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; check your internet connection, sir: {e}")
            speak("Could not request results; check your internet connection, sir.")
            return None

def recognize_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word 'hello Friday'...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)
            command = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"Recognized: {command}")
            return "hello friday" in command
        except sr.WaitTimeoutError:
            print("No wake word heard. Say 'hello Friday' to activate.")
            return False
        except sr.UnknownValueError:
            print("Could not understand. Say 'hello Friday' to activate.")
            return False
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            speak("Could not request results; check your internet connection.")
            return False

def get_deepseek_response(query, api_key=None):
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY") or "your_api_key_here"
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Friday, providing concise and accurate answers."},
                {"role": "user", "content": query}
            ],
            stream=False
        )
        answer = response.choices[0].message.content
        print(f"DeepSeek response: {answer}")
        speak(answer)
        return answer
    except Exception as e:
        error_message = f"Sorry, sir, I couldn't process the request with DeepSeek: {e}"
        print(error_message)
        speak(error_message)
        return None

def get_weather(city):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY") or "your_openweathermap_api_key_here"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            result = f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius."
            print(result)
            speak(result)
        else:
            result = f"Sorry, sir, I couldn't find weather data for {city}."
            print(result)
            speak(result)
        return result
    except Exception as e:
        result = f"An error occurred while fetching weather data, sir: {e}"
        print(result)
        speak(result)
        return None

def get_current_time():
    current_time = datetime.now(ZoneInfo("Asia/Colombo")).strftime("%I:%M %p")
    result = f"The current time is {current_time}."
    print(result)
    speak(result)
    return result

def get_current_date():
    current_date = datetime.now(ZoneInfo("Asia/Colombo")).strftime("%A, %B %d, %Y")
    result = f"Today is {current_date}."
    print(result)
    speak(result)
    return result

def play_song(song):
    if song:
        print(f"Playing {song} on YouTube, sir...")
        speak(f"Playing {song} on YouTube, sir")
        search_query = urllib.parse.quote(song)
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
    else:
        default_song = "Bohemian Rhapsody"
        print(f"Playing {default_song} on YouTube, sir...")
        speak(f"Playing {default_song} on YouTube, sir")
        search_query = urllib.parse.quote(default_song)
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

def open_application(app_name):
    app_map = {
        "notepad": {
            "Windows": "notepad.exe",
            "Darwin": ["open", "-a", "TextEdit"],
            "Linux": "gedit"
        },
        "calculator": {
            "Windows": "calc.exe",
            "Darwin": ["open", "-a", "Calculator"],
            "Linux": "gnome-calculator"
        },
        "chrome": {
            "Windows": "chrome.exe",
            "Darwin": ["open", "-a", "Google Chrome"],
            "Linux": "google-chrome"
        },
        "firefox": {
            "Windows": "firefox.exe",
            "Darwin": ["open", "-a", "Firefox"],
            "Linux": "firefox"
        },
        "vscode": {
            "Windows": "code.cmd",
            "Darwin": ["open", "-a", "Visual Studio Code"],
            "Linux": "code"
        },
        "youtube": {
            "Windows": "https://www.youtube.com",
            "Darwin": "https://www.youtube.com",
            "Linux": "https://www.youtube.com"
        },
        "whatsapp": {
            "Windows": "https://web.whatsapp.com",
            "Darwin": ["open", "-a", "WhatsApp"],
            "Linux": "https://web.whatsapp.com"
        },
        "github": {
            "Windows": "https://github.com",
            "Darwin": "https://github.com",
            "Linux": "https://github.com"
        }
    }

    system = platform.system()
    app_name = app_name.lower().strip()

    if app_name in app_map:
        cmd = app_map[app_name].get(system, app_map[app_name]["Windows"])
        print(f"Opening {app_name}, sir...")
        speak(f"Opening {app_name}, sir")
        try:
            if cmd.startswith("http"):
                webbrowser.open(cmd)
            elif system == "Windows":
                subprocess.run([cmd])
            elif system == "Darwin":
                subprocess.run(cmd)
            elif system == "Linux":
                subprocess.run([cmd])
            else:
                print("Unsupported operating system for this command.")
                speak("Unsupported operating system for this command, sir.")
                return False
            return True
        except Exception as e:
            print(f"Failed to open {app_name}: {e}")
            speak(f"Failed to open {app_name}, sir.")
            return False
    else:
        print(f"Attempting to launch {app_name}, sir...")
        speak(f"Attempting to launch {app_name}, sir")
        try:
            if system == "Windows":
                subprocess.run([app_name])
            elif system == "Darwin":
                subprocess.run(["open", "-a", app_name])
            elif system == "Linux":
                subprocess.run([app_name])
            else:
                print("Unsupported operating system for this command.")
                speak("Unsupported operating system for this command, sir.")
                return False
            return True
        except Exception as e:
            print(f"Failed to launch {app_name}: {e}")
            speak(f"Failed to launch {app_name}, sir.")
            return False

def process_command(command):
    if not command:
        return False

    # Check for stop commands
    if command in ["friday exit", "friday stop"]:
        print("Goodbye, sir!")
        speak("Goodbye, sir!")
        return True

    # Split commands by "and" or "then"
    commands = [cmd.strip() for cmd in command.replace(" then ", " and ").split(" and ")]

    for cmd in commands:
        # Check if command starts with "friday"
        if not cmd.startswith("friday "):
            print(f"Invalid command: '{cmd}'. Please start your command with 'friday', sir.")
            speak("Please start your command with 'friday', sir.")
            continue

        # Normalize command: remove "friday" prefix
        cmd = cmd.replace("friday ", "", 1).strip()
        cmd = cmd.replace("you tube", "youtube").replace("play songs", "play song").replace("song", "").replace("play a ", "play ")

        print(f"Processing command: {cmd}")
        if "open" in cmd or "launch" in cmd:
            app_name = cmd.replace("open", "").replace("launch", "").strip()
            if app_name:
                if "youtube" in app_name:
                    open_application("youtube")
                elif "whatsapp" in app_name:
                    open_application("whatsapp")
                elif "github" in app_name:
                    open_application("github")
                elif "google chrome" in app_name:
                    open_application("chrome")
                elif "google" in app_name and "search" in app_name:
                    search_query = app_name.replace("google", "").replace("search", "").strip()
                    if search_query:
                        print(f"Searching Google for {search_query}, sir...")
                        speak(f"Searching Google for {search_query}, sir")
                        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(search_query)}")
                    else:
                        print("Opening Google, sir...")
                        speak("Opening Google, sir")
                        webbrowser.open("https://www.google.com")
                elif "." in app_name:
                    url = f"https://www.{app_name}.com"
                    print(f"Opening {app_name}, sir...")
                    speak(f"Opening {app_name}, sir")
                    webbrowser.open(url)
                else:
                    open_application(app_name)
            else:
                print("No application or website specified, sir.")
                speak("No application or website specified, sir.")
        elif "play" in cmd:
            song = cmd.replace("play", "").strip()
            play_song(song)
        elif "explain" in cmd or "tell me about" in cmd:
            topic = cmd.replace("explain", "").replace("tell me about", "").strip()
            if topic:
                query = f"Explain {topic} in a concise manner."
                get_deepseek_response(query)
            else:
                print("No topic specified, sir. Please say 'friday explain' or 'friday tell me about' followed by a topic.")
                speak("No topic specified, sir. Please say 'friday explain' or 'friday tell me about' followed by a topic.")
        elif "answer" in cmd:
            question = cmd.replace("answer", "").strip()
            if question:
                get_deepseek_response(question)
            else:
                print("No question specified, sir. Please say 'friday answer' followed by a question.")
                speak("No question specified, sir. Please say 'friday answer' followed by a question.")
        elif "weather" in cmd or "check weather" in cmd:
            city = cmd.replace("check weather in", "").replace("check weather", "").replace("weather in", "").replace("weather", "").strip()
            if city:
                get_weather(city)
            else:
                print("No city specified, sir. Please say 'friday check weather in' followed by a city name.")
                speak("No city specified, sir. Please say 'friday check weather in' followed by a city name.")
        elif "time" in cmd or "tell me the time" in cmd:
            get_current_time()
        elif "date" in cmd or "tell me the date" in cmd:
            get_current_date()
        else:
            print(f"I’m not sure what you mean by '{cmd}', sir. Let me search for it.")
            speak(f"I’m not sure what you mean by '{cmd}', sir. Let me search for it.")
            search_query = urllib.parse.quote(cmd)
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
    return False

def main():
    print("Say 'hello Friday' to activate the assistant.")
    while True:
        if recognize_wake_word():
            greeting = get_greeting()
            print(greeting)
            speak(greeting)
            break
        else:
            continue
    
    while True:
        command = recognize_speech()
        if process_command(command):
            break

if __name__ == "__main__":
    main()