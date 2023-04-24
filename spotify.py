import spotipy
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr
import subprocess
import time

# Set up Spotify authentication
scope = "user-library-read user-read-playback-state user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id='4e5e7c7e1fe2455eb69820cb7a0faf52', client_secret='28b041414c1d4e939a86ac6a67550bb1', redirect_uri='http://localhost:8888/callback'))


# Set up speech recognition
r = sr.Recognizer()

# Define voice commands
commands = {
    "play": sp.start_playback,
    "pause": sp.pause_playback,
    "next": sp.next_track,
    "previous": sp.previous_track,
    "volume up": lambda: sp.volume(50),
    "volume down": lambda: sp.volume(10),
    "search": lambda query: sp.search(q=query, type="track", limit=1),
    "add": lambda uri: sp.add_to_queue(uri),
    "queue": lambda: sp.current_user_queue(),
    "shuffle on": lambda: sp.shuffle(True),
    "shuffle off": lambda: sp.shuffle(False),
    "repeat on": lambda: sp.repeat("context"),
    "repeat off": lambda: sp.repeat("off"),
}

# Start listening for voice commands
while True:
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    # Recognize the voice command
    try:
        text = r.recognize_google(audio)
        print("Heard:", text)
        words = text.split()
        command = commands.get(words[0])
        if command:
            if len(words) > 1:
                param = " ".join(words[1:])
                result = command(param)
            else:
                result = command()
            if result:
                print(result)
        else:
            print("Command not recognized")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results: ", e)

    # Wait a bit before listening again
    time.sleep(1)