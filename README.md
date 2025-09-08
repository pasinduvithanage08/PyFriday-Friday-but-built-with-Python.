# PyFriday-Friday-but-built-with-Python.
An AI-powered personal assistant built with Python and Grok AI, inspired by Iron Man’s Friday. Designed to handle tasks, provide intelligent responses, and make human–AI interaction seamless."

FRIDAY Voice Assistant
FRIDAY is a voice-activated assistant inspired by JARVIS from Iron Man, built with Python. It responds to voice commands to open applications/websites, play songs on YouTube, check the weather, provide time/date, and answer questions using the DeepSeek API. The assistant uses "hello Friday" as the wake word and requires all commands to start with "friday" (e.g., "friday open google chrome"). It operates in real-time, listening continuously for commands without prompting, and stops with "friday exit" or "friday stop."
Features

Wake Word: Say "hello Friday" to activate the assistant.
Commands (must start with "friday"):
Open applications/websites: e.g., "friday open google chrome," "friday open github," "friday open whatsapp."
Play songs: e.g., "friday play Yaka Crew song," "friday play Daddy Yankee" (opens YouTube search).
Check weather: e.g., "friday check weather in Colombo" (uses OpenWeatherMap API).
Get time/date: e.g., "friday what is the time?" (uses Sri Jayawardanapura timezone, UTC+05:30).
Answer questions: e.g., "friday explain quantum physics" (uses DeepSeek API).
Google search fallback for unrecognized commands.


Multiple Commands: Supports chained commands (e.g., "friday open youtube and friday play Yaka Crew song and friday open github").
Stop Commands: Say "friday exit" or "friday stop" to terminate the program with "Goodbye, sir!"
Timezone: Set to Sri Jayawardanapura (UTC+05:30).

Prerequisites

Python: Version 3.8 or higher.
Operating System: Windows (developed on Windows; macOS/Linux partially supported).
Microphone: Required for voice input.
Internet Connection: Needed for speech recognition (Google API), DeepSeek API, and OpenWeatherMap API.
GitHub Repository: Clone this repository to your local machine.

2. Create and Activate a Virtual Environment
Create a virtual environment to manage dependencies:
cd C:\Users\YourUsername\Documents\AI Project
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # On Windows
# or
source .venv/bin/activate  # On macOS/Linux

3. Install Required Libraries
Install the necessary Python libraries using pip:
pip install wikipedia SpeechRecognition PyAudio pyttsx3 requests openai

If PyAudio installation fails (common on Windows):
pip install pipwin
pipwin install PyAudio

Verify installed libraries:
pip show wikipedia SpeechRecognition PyAudio pyttsx3 requests openai

Required Libraries:

wikipedia: For fetching Wikipedia summaries (optional, not currently used but included for future expansion).
SpeechRecognition: For voice input processing via Google Speech Recognition API.
PyAudio: For microphone input (dependency of SpeechRecognition).
pyttsx3: For text-to-speech output.
requests: For making API calls to OpenWeatherMap.
openai: For DeepSeek API integration (used for "friday explain" or "friday answer" commands).

4. Set Up API Keys
FRIDAY uses two APIs that require keys:

DeepSeek API (for answering questions):
Obtain a DeepSeek API key from DeepSeek.
Set the environment variable:$env:DEEPSEEK_API_KEY = "your_deepseek_api_key_here"

Alternatively, edit voice_recognition.py (line ~85) and replace "your_api_key_here" with your key.


OpenWeatherMap API (for weather queries):
Obtain an API key from OpenWeatherMap.
Set the environment variable:$env:OPENWEATHERMAP_API_KEY = "your_openweathermap_api_key_here"

Alternatively, edit voice_recognition.py (line ~110) and replace "your_openweathermap_api_key_here" with your key.



5. Run the Program
Save the main script as voice_recognition.py (or main.py) in your project directory and run it:
python voice_recognition.py

The console will display:
Say 'hello Friday' to activate the assistant.

Usage

Activate the Assistant:

Say "hello Friday" clearly to activate. The assistant responds with:Good evening, sir, I am Friday, how may I help you?

(Time-sensitive greeting based on UTC+05:30, Sri Jayawardanapura).


Issue Commands:

All commands must start with "friday". Examples:
Open Applications/Websites:
"friday open google chrome" (opens Google Chrome).
"friday open youtube" (opens https://www.youtube.com).
"friday open whatsapp" (opens https://web.whatsapp.com or WhatsApp app on macOS).
"friday open github" (opens https://github.com).


Play Songs:
"friday play Yaka Crew song" (opens https://www.youtube.com/results?search_query=Yaka+Crew).
"friday play Daddy Yankee" (opens https://www.youtube.com/results?search_query=Daddy+Yankee).


Weather:
"friday check weather in Colombo" (fetches weather using OpenWeatherMap API).


Time/Date:
"friday what is the time?" (e.g., "The current time is 10:12 PM.").
"friday what is the date?" (e.g., "Today is Monday, September 08, 2025.").


Questions/Explanations:
"friday explain quantum physics" (uses DeepSeek API for a concise explanation).
"friday answer what is the capital of France?" (uses DeepSeek API).


Multiple Commands:
"friday open youtube and friday play Yaka Crew song and friday open github" (executes all in sequence).


Stop the Program:
"friday exit" or "friday stop" (exits with "Goodbye, sir!").






Behavior:

After activation, FRIDAY listens continuously for commands in real-time (no prompting for continuation).
Commands without "friday" prefix (e.g., "open youtube") trigger: "Please start your command with 'friday', sir."
Unrecognized commands trigger a Google search (e.g., "friday what is XYZ" opens a Google search for "XYZ").



Troubleshooting Common Errors
1. Speech Recognition Issues

Error: "Sorry, sir, I couldn't understand your command. Please speak clearly." or "No command heard."

Cause: Microphone issues, background noise, or unclear speech.
Fix:
Ensure a quiet environment.
Verify microphone is set as default:
Right-click sound icon (Windows taskbar) > Sounds > Recording > Select microphone > Set Default.


Test microphone in Windows Voice Recorder.
Speak clearly and slowly (e.g., "friday exit").
Check console for recognized text (e.g., "Recognized command: friday exitt") and adjust pronunciation if misrecognized.




Error: "Could not request results; check your internet connection, sir."

Cause: No internet or Google Speech Recognition API failure.
Fix:
Verify internet connection (open a website in browser).
Restart the program after restoring connectivity.





2. API Key Errors

Error: DeepSeek or OpenWeatherMap API fails (e.g., "Sorry, sir, I couldn't process the request with DeepSeek").
Cause: Invalid or missing API keys.
Fix:
Ensure API keys are set (see "Set Up API Keys" above).
Check console for specific error messages (e.g., "Invalid API key").
Replace placeholder keys in voice_recognition.py if not using environment variables.





3. Application Opening Issues

Error: "Failed to open google chrome" or similar.
Cause: Application not installed or not found in system PATH.
Fix:
Ensure the application is installed (e.g., Google Chrome, WhatsApp).
For macOS/Linux, verify app names match (e.g., "Google Chrome" for macOS).
Check console for error details (e.g., "Failed to open chrome: [Errno 2] No such file").





4. Program Won’t Stop

Error: "friday exit" or "friday stop" not recognized.
Cause: Speech recognition misinterpreting the command.
Fix:
Check console for recognized command (e.g., "Recognized command: friday stopp").
Speak clearly or try the alternative command ("friday exit" or "friday stop").
Manually stop the program:
Press Ctrl+C in the terminal (may show KeyboardInterrupt).
Close the terminal (VS Code: click trash can icon; command prompt: click X).
Use Task Manager (Windows):
Ctrl+Shift+Esc > Find python.exe or pythonw.exe > End Task.









5. PyAudio Installation Failure

Error: pip install PyAudio fails on Windows.
Fix:pip install pipwin
pipwin install PyAudio





Example Commands
Run the program and say "hello Friday" to activate. Then try:
friday open google chrome
friday open github
friday open whatsapp
friday play Daddy Yankee
friday check weather in Colombo
friday what is the time?
friday explain artificial intelligence
friday open youtube and friday play Yaka Crew song and friday open github
friday exit  # or friday stop
