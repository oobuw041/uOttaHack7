import pyaudio
import speech_recognition as sr
from googletrans import Translator


def capture_and_translate():
    # Initialiser le microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        try:
            # Capturer l'audio
            audio = recognizer.listen(source)
            print("Traitement en cours...")

            # Reconnaître la voix (langue par défaut : anglais)
            text = recognizer.recognize_google(audio, language='en-US')
            print(f"Texte reconnu : {text}")

            # Traduire en français
            translator = Translator()
            translated_text = translator.translate(text, src='en', dest='es').text
            print(f"Texte traduit : {translated_text}")

        except sr.UnknownValueError:
            print("Je n'ai pas pu comprendre l'audio.")
        except sr.RequestError as e:
            print(f"Erreur de reconnaissance vocale : {e}")


# Exécuter la fonction
if __name__ == "__main__":
    capture_and_translate()