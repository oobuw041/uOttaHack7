from audio_capture import capture_audio
from recognize_time import recognize_speech_with_timeout
from speech_recognition import recognize_speech
from translation import translate_text

# Capture audio
audio_frames = capture_audio()

# Recognize speech and get the transcribed text
recognized_text = recognize_speech(audio_frames)
if recognized_text:
    print(f"Recognized text: {recognized_text}")
    
    # Translate the recognized text
    translated_text = translate_text(recognized_text, "es")
    print(f"Translated text: {translated_text}")
else:
    print("No speech recognized.")
