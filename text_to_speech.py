import pyttsx3


class TextToSpeech:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.voices = self.engine.getProperty("voices")

        # Default settings
        self.current_voice = 0
        self.current_rate = 150
        self.current_volume = 1.0

        self.engine.setProperty("voice", self.voices[self.current_voice].id)
        self.engine.setProperty("rate", self.current_rate)
        self.engine.setProperty("volume", self.current_volume)

    # ----------------------------
    # Speak Text
    # ----------------------------
    def speak(self, text):

        if text.strip():

            self.engine.say(text)

            self.engine.runAndWait()

    # ----------------------------
    # Set Voice
    # ----------------------------
    def set_voice(self, index):

        if 0 <= index < len(self.voices):

            self.current_voice = index

            self.engine.setProperty(
                "voice",
                self.voices[index].id
            )

    # ----------------------------
    # Set Speed
    # ----------------------------
    def set_rate(self, rate):

        self.current_rate = rate

        self.engine.setProperty("rate", rate)

    # ----------------------------
    # Set Volume
    # ----------------------------
    def set_volume(self, volume):

        self.current_volume = volume

        self.engine.setProperty("volume", volume)

    # ----------------------------
    # Get Voices
    # ----------------------------
    def get_voice_names(self):

        names = []

        for voice in self.voices:

            names.append(voice.name)

        return names


if __name__ == "__main__":

    tts = TextToSpeech()

    print("Available Voices:\n")

    for i, name in enumerate(tts.get_voice_names()):

        print(i, "-", name)

    tts.speak("Welcome to your Voice to Text and Text to Voice project.")