# '''
# Features to be added:
# 1) whatsapp calling
# 2) any search related activities------------------ done
# 3) weather monitoring ------------------- done
# 4) birthday wishes
# 5) flight booking
# 6) train bookings
# 7) automating emails
# 8) automatic messaging
# 9) automatic job application in linkedin
# 10) story telling / jokes-----done
# 11) play music / movie
# 12)
# '''
#
import pyttsx3
import datetime
import random
import speech_recognition as sr
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

API_KEY = "sk-YOUR_API_KEY"

def Call_Chat_Gpt(query):
    url = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': query,
        'temperature': 0.7,
        'max_tokens': 200
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    print("Printing from Function ===> ", result["choices"][0]["text"])
    final = result["choices"][0]["text"]
    if 'joke' in query:
        final += ' haha ha ha '
    return final

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def timenow():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak('Time now')
    speak(Time)

def date():
    speak("Today's date")
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = months[month - 1]
    day = int(datetime.datetime.now().day)
    speak(month + " " + str(day) + " " + str(year))

def wishme():
    speak('Welcome back sir.')
    timenow()
    date()
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak('Good morning sir. I hope you have a good sleep')
    elif 12 <= hour < 16:
        speak('Good afternoon sir. How is your day?')
    elif 16 <= hour < 24:
        speak('Good evening sir you can ask me any question')
    else:
        speak("Good morning sir. I think it's too late. You need some sleep. Otherwise mom will scold me. Please take some rest sir.")

wishme()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language="en-in")
        print(query)
    except Exception as e:
        print(e)
        speak('I am unable to hear you, sir. Can you please re-check the microphone and try again?')
        return 'None'
    return query

def send_email(subject, body, to):
    from_email = "your_email@example.com"
    from_password = "your_password"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to, text)
    server.quit()

taking_commands = True
while taking_commands:
    query = takeCommand().lower()
    if query and query != 'none':
        if "send email" in query:
            speak("What should be the subject?")
            subject = takeCommand()
            speak("What should be the message?")
            body = takeCommand()
            speak("Whom should I send the email to?")
            to = takeCommand()
            send_email(subject, body, to)
            speak("Email has been sent.")
        else:
            from_cht = Call_Chat_Gpt(query)
            speak(from_cht)
    elif "what is your name" in query or 'who are you' in query or 'who is speaking' in query:
        speak('My name is Feeling. I am a personal assistant equipped with the latest version of Chat GPT.')
    else:
        speak('I am under development. Currently, those services are not available.')

