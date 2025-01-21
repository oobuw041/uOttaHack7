import azure.cognitiveservices.speech as speechsdk
import time

def recognize_speech_with_timeout(silence_timeout=5):
    speech_key = "ASUUqMVUMM7DtECn3HmazhYFt5aiXUji0YbCvsZU35C6mXUOAaqTJQQJ99BAACYeBjFXJ3w3AAAYACOGJY6H"
    region = "eastus"

    # Configure the speech service
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create the speech recognizer
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Variable to track the last time speech was recognized
    last_speech_time = time.time()

    # Callback for recognized events
    def recognized_callback(event):
        nonlocal last_speech_time
        print(f"Recognized: {event.result.text}")
        last_speech_time = time.time()  # Update the last speech time

    # Connect the callback to the recognized event
    speech_recognizer.recognized.connect(recognized_callback)

    # Start continuous recognition
    print("Starting continuous recognition...")
    speech_recognizer.start_continuous_recognition()

    while True:
        # Check if silence timeout is reached
        if time.time() - last_speech_time > silence_timeout:
            print("Silence detected. Stopping recognition...")
            speech_recognizer.stop_continuous_recognition()
            break

# Run the recognition with a 5-second silence timeout
recognize_speech_with_timeout(silence_timeout=5)
