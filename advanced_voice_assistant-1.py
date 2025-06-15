import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import smtplib
import wikipedia
import requests
import time

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Replace with your actual OpenWeatherMap API key
WEATHER_API_KEY = "1f01b1cdb2ac6cd31e08f7904580340c"

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()
    except sr.WaitTimeoutError:
        speak("Listening timed out.")
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that.")
    except sr.RequestError:
        speak("API error. Please check your internet.")
    except Exception as e:
        speak("Microphone error occurred.")
        print("Mic error:", e)
    return ""

def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {current_time}")

def tell_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {current_date}")

def search_google(query):
    speak(f"Searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(summary)
    except Exception as e:
        speak("Sorry, I couldn't find information on that topic.")
        print("Wikipedia error:", e)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url).json()
        if response["cod"] == 200:
            weather = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            speak(f"The weather in {city} is {weather} with a temperature of {temp}°C.")
        else:
            speak("City not found.")
    except Exception as e:
        speak("Couldn't retrieve weather information.")
        print("Weather error:", e)

def send_email(to_address, subject, message):
    sender_email = "youremail@gmail.com"  # Replace with your Gmail
    app_password = "yourapppassword"      # Replace with your app password

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_address, email_message)
        server.quit()
        speak("Email has been sent.")
    except Exception as e:
        speak("Failed to send the email.")
        print("Email error:", e)

def set_reminder(text, wait_seconds):
    speak(f"Setting a reminder in {wait_seconds} seconds.")
    time.sleep(wait_seconds)
    speak(f"Reminder: {text}")

def run_assistant():
    speak("Hello! I am your advanced voice assistant. How can I help you?")
    while True:
        command = listen()
        if not command:
            continue

        if "hello" in command:
            speak("Hello! What can I do for you?")
        elif "time" in command:
            tell_time()
        elif "date" in command:
            tell_date()
        elif "open google" in command:
            webbrowser.open("https://www.google.com")
        elif "search" in command:
            speak("What should I search for?")
            query = listen()
            if query:
                search_google(query)
        elif "wikipedia" in command:
            speak("What topic should I search on Wikipedia?")
            topic = listen()
            if topic:
                get_wikipedia_summary(topic)
        elif "weather" in command or "temperature" in command or "climate" in command:
            speak("Which city do you want the weather for?")
            city = listen()
            if city:
                get_weather(city)
            else:
                speak("Sorry, I couldn't understand the city name.")
        elif "email" in command:
            speak("Whom should I send the email to?")
            to = input("Enter recipient email: ")
            speak("What is the subject?")
            subject = listen()
            speak("What is the message?")
            message = listen()
            if to and subject and message:
                send_email(to, subject, message)
        elif "reminder" in command:
            speak("What should I remind you about?")
            reminder = listen()
            speak("In how many seconds?")
            try:
                seconds = int(listen())
                set_reminder(reminder, seconds)
            except ValueError:
                speak("Please say a valid number.")
        elif "exit" in command or "stop" in command or "quit" in command:
            speak("Goodbye! Have a nice day.")
            break
        else:
            speak("I'm not sure how to do that yet.")

# Run the assistant
run_assistant()