# pip install pyaudio

import pyaudio 

import wave

def capture_audio():
    # Set up audio stream
    p = pyaudio.PyAudio()

    # List all audio devices
    # print("Available audio devices:")
    # for i in range(p.get_device_count()):
    #     device_info = p.get_device_info_by_index(i)
    #     print(f"Index {i}: {device_info['name']} - Input Channels: {device_info['maxInputChannels']}")

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    print("Recording...")
    frames = []

    try:
        while True:
            data = stream.read(1024)
            frames.append(data)

    except KeyboardInterrupt:
        print("Recording stopped.")
        stream.stop_stream()
        stream.close()
        p.terminate()

    return b''.join(frames)

def to_wave(): 

    # Example: Raw byte string (replace with your actual byte string data)
    audio_data = capture_audio()  # This should be your actual byte string data

    # Set the parameters for the .wav file
    CHANNELS = 1  # Mono audio (1 channel)
    SAMPWIDTH = 2  # Sample width in bytes (for 16-bit PCM, this is 2 bytes)
    RATE = 16000  # Sample rate (44100 samples per second, common for audio)

    # Create a new wave file
    with wave.open("output.wav", "wb") as wf:
        wf.setnchannels(CHANNELS)  # Set the number of channels (1 for mono)
        wf.setsampwidth(SAMPWIDTH)  # Set the sample width (2 bytes for 16-bit)
        wf.setframerate(RATE)  # Set the sample rate (samples per second)
        wf.writeframes(audio_data)  # Write the byte string to the .wav file

    print("Byte string successfully saved as 'output.wav'.")

to_wave() 