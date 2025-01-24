import azure.cognitiveservices.speech as speechsdk
from audio_capture import capture_audio

def recognize_speech(audio_frames):
    speech_key = "ASUUqMVUMM7DtECn3HmazhYFt5aiXUji0YbCvsZU35C6mXUOAaqTJQQJ99BAACYeBjFXJ3w3AAAYACOGJY6H"
    region = "eastus"
    
    # Set up the speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    

    
    result = speech_recognizer.recognize_once()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return None
