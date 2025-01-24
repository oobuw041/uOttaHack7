import pyaudio

def capture_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    print("Recording...")
    frames = []

    # Capture audio for a specified duration (e.g., 5 seconds)
    for _ in range(0, int(16000 / 1024 * 5)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Return the captured audio frames (you can modify this to return a stream or file if needed)
    return frames
