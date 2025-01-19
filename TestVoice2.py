import speech_recognition as sr
from googletrans import Translator
import pyttsx3


def capture_and_translate():
    engine = pyttsx3.init()

    # Récupérer la liste des voix disponibles
    voices = engine.getProperty('voices')

    # Lister toutes les voix disponibles
    for index, voice in enumerate(voices):
        print(f"Index {index}: {voice.name} - ID: {voice.id}")

    # Initialiser le microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak now...")
        try:
            # Capturer l'audio
            audio = recognizer.listen(source)
            print("Processing in progress...")

            # Reconnaître la voix (langue par défaut : anglais)
            text = recognizer.recognize_google(audio, language='en-US')
            print(f"Recognized text : {text}")

            # Traduire en français
            translator = Translator()
            translated_text = translator.translate(text, src='en', dest='zh-CN').text
            print(f"Translated text : {translated_text}")

            engine.setProperty('voice', voices[2].id)

            engine.say(translated_text)
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Voice recognition error : {e}")


# Exécuter la fonction
if __name__ == "__main__":
    capture_and_translate()