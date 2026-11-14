import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time
import asyncio

words_by_level = {
    "easy": ["кошка", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "красный"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}


def record_voice():
    duration = 3
    sample_rate = 44100

    print("Speak...")
    recording = sd.rec(int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16")
    sd.wait()

    wav.write("answer.wav", sample_rate, recording)

    recognizer = sr.Recognizer()
    with sr.AudioFile("answer.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        return text.lower()
    except:
        return
    




async def translate_word(word):
    translator = Translator()
    result = await translator.translate(word, src="ru", dest="en")
    return result.text.lower()




def choose_level():
    print("CHOSSE THE LEVEL: 1 — easy  2 — medium  3 — hard ")

    choice = input(" Your choice: ")

    if choice == "1":
        return "easy"
    elif choice == "2":
        return "medium"
    elif choice == "3":
        return "hard"
    else:
        print("Easy by default")
        return "easy"



def game():
    print("VOICE TRANSLATOR GAME Say the translation of the word in English. You have 3 attempts. For the correct answer +10 points")

    level = choose_level()
    mistakes = 0
    score = 0

    while mistakes < 3:
        word = random.choice(words_by_level[level])

        print("\n------------------------")
        print(f"🇷🇺 Word: {word}")
        print(f"Mistakes: {mistakes}/3")
        print(f"Scores: {score}")

        correct = asyncio.run(translate_word(word))

        time.sleep(1)
        user = record_voice()

        print(f"You said: {user}")
        print(f"Correct: {correct}")

        if user == correct:
            print("Correct!")
            score += 10
        else:
            print("Wrong!")
            mistakes += 1

    print(" GAME OVER ")




    print(f"Result: {score} points")
    if score >= 40:
        print("GREAT!")
    elif score >= 20:
        print("Not bad!")
    else:
        print("Still need to train!")


game()
