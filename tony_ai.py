import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import re
import time

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def clean_command(command):
    command = re.sub(r'\btony\b', '', command, flags=re.IGNORECASE).strip()
    return command

def listen_for_wake_word():
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=1)
        voice = listener.listen(source, timeout=5, phrase_time_limit=5)
        command = listener.recognize_google(voice).lower()
        if 'tony' in command:
            print("Wake word 'Tony' detected!")
            return True
    return False

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            print('Listening for a command...')
            voice = listener.listen(source, timeout=8, phrase_time_limit=8)
            command = listener.recognize_google(voice).lower()
            print(f"Raw command: {command}")
            command = clean_command(command)  # Clean up the command
            print(f"Cleaned command: {command}")
    except sr.UnknownValueError:
        talk("Sorry, I did not understand the audio.")
    except sr.RequestError:
        talk("Could not request results; check your internet connection.")
    except Exception as e:
        talk(f"Error while taking command: {e}")
    return command

def play_on_youtube_music(song_name):
    try:
        talk(f"Playing {song_name} on YouTube Music.")
        pywhatkit.playonyt(song_name + " song on YouTube Music")
    except Exception as e:
        talk("I encountered an issue playing on YouTube Music. Please try again.")

def run_ai():
    
    date_count=0
    talk('You can ask me anything, I am listening ')
    command = take_command()
    if 'play' in command and 'youtube':
        song = re.sub(r'\bplay\b', '', command).strip()
        play_on_youtube_music(song)
        run_ai()
        
        
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {current_time}')
        run_ai()
        
        
    elif 'who is' in command or 'who are you' in command:
        person = command.replace('who is', '').replace('who are you', '').strip()
        try:
            info = wikipedia.summary(person, sentences=1)
            talk(info)
            run_ai()
            
        except wikipedia.exceptions.DisambiguationError:
            talk("Multiple results found, please be more specific.")
            run_ai()
            
        except wikipedia.exceptions.PageError:
            talk("Page not found for the requested information.")
            run_ai()
        
            
            
    elif 'date' in command:
        date_count+=1
        if date_count==0:
            talk("I think you are kidding with me, aren't you ?")
        elif date_count==1:
            talk("I think you are in a joyful mode, but I appreciate that!")
        elif date_count==2:
            talk("I think it was the third time you are asking me the same, ")
        run_ai()

    elif 'are you single' in command:
        talk('I am in a relationship with a bully.')
        run_ai()
        
        
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        talk('How was it ?')
        time.sleep(1)
        talk('I found it very funny')
        run_ai()
        
        
    else:
        talk("I can't hear you, Please speak clear")
        run_ai()
        
        
def main():
    talk("reporting TONY sir!")
    while True:
        if listen_for_wake_word():
            talk("How can I help you?")
            run_ai()
            time.sleep(2)
main()
