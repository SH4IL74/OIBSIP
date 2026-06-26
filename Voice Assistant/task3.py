"""
A Friendly Command-Line Voice Assistant
-----------------------------------------

Requires:
    pip install speechrecognition pyttsx3 pyaudio

If pyaudio/microphone setup gives trouble, the assistant will
automatically fall back to typed input, so it still works either way.
"""

import webbrowser
import datetime
import random

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_MODE_AVAILABLE = True
except ImportError:
    VOICE_MODE_AVAILABLE = False


def setup_voice_engine():
    """Prepare the text-to-speech engine, or return None if unavailable."""
    if not VOICE_MODE_AVAILABLE:
        return None
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    return engine


def speak(engine, text):
    """Speak the text out loud if possible, and always print it too."""
    print(f"Assistant: {text}")
    if engine is not None:
        engine.say(text)
        engine.runAndWait()


def listen(recognizer):
    """Try to capture and recognize speech. Fall back to typed input."""
    if not VOICE_MODE_AVAILABLE:
        return input("You (type here): ").strip()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except Exception:
        print("Could not hear you clearly, switching to typed input.")
        return input("You (type here): ").strip()


def handle_command(command, engine):
    """Look at the command text and decide what to do. Returns False to quit."""
    command = command.lower()

    if "search for" in command:
        topic = command.split("search for", 1)[1].strip()
        if topic:
            speak(engine, f"Searching the web for {topic}")
            webbrowser.open(f"https://www.google.com/search?q={topic}")
        else:
            speak(engine, "What would you like me to search for?")

    elif "open youtube" in command:
        speak(engine, "Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open wikipedia" in command:
        speak(engine, "Opening Wikipedia")
        webbrowser.open("https://www.wikipedia.org")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(engine, f"The current time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(engine, f"Today's date is {today}")

    elif "joke" in command:
        speak(engine, "Why don't scientists trust atoms? Because they make up everything!")

    elif "your name" in command:
        speak(engine, "I'm your command-line assistant, built with simple Python.")

    elif "stop" in command or "exit" in command or "quit" in command:
        speak(engine, "Goodbye, have a great day.")
        return False

    elif command == "":
        speak(engine, "I didn't catch that, could you try again?")

    else:
        speak(engine, "I'm not sure how to help with that yet. Try asking me to search, tell a joke, or give the time.")

    return True


def print_intro():
    print("=" * 55)
    print(" COMMAND-LINE VOICE ASSISTANT ")
    print("=" * 55)
    print("Try things like:")
    print(" - 'search for python tutorials'")
    print(" - 'open youtube' / 'open wikipedia'")
    print(" - 'what is the time' / 'what is the date'")
    print(" - 'tell me a joke'")
    print(" - 'stop' to exit")
    if not VOICE_MODE_AVAILABLE:
        print("\n(Voice libraries not found, running in typed mode.)")
    print("=" * 55)


def main():
    print_intro()
    engine = setup_voice_engine()
    recognizer = sr.Recognizer() if VOICE_MODE_AVAILABLE else None

    speak(engine, "Hello, how can I help you today?")

    running = True
    while running:
        command = listen(recognizer)
        running = handle_command(command, engine)


if __name__ == "__main__":
    main()