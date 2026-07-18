import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr


class SpeechToText:

    def __init__(self):
        self.sample_rate = 44100
        self.duration = 5

    def listen(self):

        print("🎤 Speak now...")

        recording = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        write("recording.wav", self.sample_rate, recording)

        recognizer = sr.Recognizer()

        with sr.AudioFile("recording.wav") as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text

        except sr.UnknownValueError:
            print("Could not understand audio.")

        except sr.RequestError as e:
            print("Recognition Error:", e)

        return ""