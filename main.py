import speech_recognition as sr
import pyttsx3
import os

def speak(text):
    engine = pyttsx3.init()

    # List available voices and set to Zira
    voices = engine.getProperty('voices')
    zira_voice = None
    for voice in voices:
        if "Zira" in voice.name:
            zira_voice = voice
            break
    
    if zira_voice:
        engine.setProperty('voice', zira_voice.id)
    else:
        print("Zira voice not found. Using default voice.")
    
    # Set speech rate and volume if needed
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    engine.say(text)
    engine.runAndWait()

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()  # Return lowercased command for uniformity
    except sr.UnknownValueError:
        print("Error, received audio unrecognizable.")
        return None
    except sr.RequestError:
        print("Error, discrepancy detected with Voice Recognition Systems.")
        return None

def handle_command(command):
    if "take a note" in command:
        take_note()
    elif "timer" in command:
        start_timer()
    elif "rename note" in command:
        rename_note()
    elif "delete note" in command:
        delete_note()
    else:
        response = "Error, command not recognized."
        print(response)
        speak(response)

def take_note():
    response = "Affirmative, awaiting entry."
    print(response)
    speak(response)
    note = recognize_speech_from_mic()
    if note:
        response = f"Entry logged: {note}"
        print(response)
        speak(response)
        # Save the note to a text file
        with open("notes.txt", "a") as file:
            file.write(note + "\n")
        speak("Note saved.")

def rename_note():
    response = "Please say the current name of the note you want to rename."
    print(response)
    speak(response)
    current_name = recognize_speech_from_mic()
    
    if current_name:
        response = f"Please say the new name for the note '{current_name}'."
        print(response)
        speak(response)
        new_name = recognize_speech_from_mic()
        
        if new_name:
            try:
                os.rename(current_name, new_name)
                response = f"Note '{current_name}' has been renamed to '{new_name}'."
                print(response)
                speak(response)
            except FileNotFoundError:
                response = f"Note '{current_name}' not found."
                print(response)
                speak(response)
            except Exception as e:
                response = f"An error occurred: {e}"
                print(response)
                speak(response)

def delete_note():
    response = "Please say the name of the note you want to delete."
    print(response)
    speak(response)
    note_name = recognize_speech_from_mic()
    
    if note_name:
        try:
            os.remove(note_name)
            response = f"Note '{note_name}' has been deleted."
            print(response)
            speak(response)
        except FileNotFoundError:
            response = f"Note '{note_name}' not found."
            print(response)
            speak(response)
        except Exception as e:
            response = f"An error occurred: {e}"
            print(response)
            speak(response)

def start_timer():
    response = "Starting a timer..."
    print(response)
    speak(response)
    # Add timer logic here

if __name__ == "__main__":
    speak("Hello, I am ERIN, your personal AI assistant.")
    command = recognize_speech_from_mic()
    if command:
        handle_command(command)


