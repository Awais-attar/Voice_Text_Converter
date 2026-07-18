import tkinter as tk
from tkinter import filedialog
import threading

from text_to_speech import TextToSpeech
from speech_to_text import SpeechToText


class VoiceApp:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Voice to Text & Text to Voice")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.tts = TextToSpeech()
        self.stt = SpeechToText()

        # ---------------- Title ----------------
        title = tk.Label(
            self.root,
            text="🎙 Voice to Text & Text to Voice",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        # ---------------- Text Box ----------------
        self.text_box = tk.Text(
            self.root,
            width=90,
            height=16,
            font=("Arial", 12),
            wrap="word"
        )
        self.text_box.pack(pady=10)

        # ---------------- Buttons ----------------
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🎤 Listen", width=12,
                  command=self.start_listening).grid(row=0, column=0, padx=5)

        tk.Button(button_frame, text="🔊 Speak", width=12,
                  command=self.speak_text).grid(row=0, column=1, padx=5)

        tk.Button(button_frame, text="📂 Open", width=12,
                  command=self.open_file).grid(row=0, column=2, padx=5)

        tk.Button(button_frame, text="💾 Save", width=12,
                  command=self.save_file).grid(row=0, column=3, padx=5)

        tk.Button(button_frame, text="🗑 Clear", width=12,
                  command=self.clear_text).grid(row=0, column=4, padx=5)

        tk.Button(button_frame, text="📋 Copy", width=12,
                  command=self.copy_text).grid(row=0, column=5, padx=5)

        # ---------------- Voice Settings ----------------
        settings = tk.LabelFrame(
            self.root,
            text="Voice Settings",
            padx=10,
            pady=10
        )
        settings.pack(fill="x", padx=20, pady=15)

        # Voice Dropdown
        tk.Label(settings, text="Voice").grid(row=0, column=0, sticky="w")

        self.voice_names = self.tts.get_voice_names()

        self.voice_var = tk.StringVar()
        self.voice_var.set(self.voice_names[0])

        self.voice_menu = tk.OptionMenu(
            settings,
            self.voice_var,
            *self.voice_names,
            command=self.change_voice
        )

        self.voice_menu.grid(row=0, column=1, padx=10)

        # Speed Slider
        tk.Label(settings, text="Speed").grid(row=1, column=0, sticky="w")

        self.speed_slider = tk.Scale(
            settings,
            from_=50,
            to=300,
            orient="horizontal",
            length=250,
            command=self.change_speed
        )

        self.speed_slider.set(150)

        self.speed_slider.grid(row=1, column=1)

        # Volume Slider
        tk.Label(settings, text="Volume").grid(row=2, column=0, sticky="w")

        self.volume_slider = tk.Scale(
            settings,
            from_=0,
            to=100,
            orient="horizontal",
            length=250,
            command=self.change_volume
        )

        self.volume_slider.set(100)

        self.volume_slider.grid(row=2, column=1)

        # ---------------- Status ----------------
        self.status = tk.Label(
            self.root,
            text="Status : Ready",
            fg="blue",
            font=("Arial", 11)
        )
        self.status.pack(pady=10)

        self.root.mainloop()

    # ---------------- Speak ----------------
    def speak_text(self):

        text = self.text_box.get("1.0", tk.END)

        if text.strip():

            self.status.config(text="Status : Speaking...")

            self.tts.speak(text)

            self.status.config(text="Status : Ready")

        else:

            self.status.config(text="Status : Text Box Empty")

    # ---------------- Listen ----------------
    def start_listening(self):

        thread = threading.Thread(target=self.listen_voice)
        thread.daemon = True
        thread.start()

        # ---------------- Listen ----------------
    def start_listening(self):

        thread = threading.Thread(target=self.listen_voice)
        thread.daemon = True
        thread.start()

    def listen_voice(self):

        self.status.config(text="Status : Listening...")

        text = self.stt.listen()

        if text:

            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, text)

            self.status.config(text="Status : Speaking recognized text...")

            speak_thread = threading.Thread(
                target=self.tts.speak,
                args=(text,)
            )
            speak_thread.daemon = True
            speak_thread.start()

            self.status.config(text="Status : Ready")

        else:

            self.status.config(text="Status : Recognition Failed")

    # ---------------- File ----------------
    def open_file(self):

        file = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")]
        )

        if file:

            with open(file, "r", encoding="utf-8") as f:

                data = f.read()

            self.text_box.delete("1.0", tk.END)

            self.text_box.insert(tk.END, data)

            self.status.config(text="Status : File Opened")

    def save_file(self):

        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if file:

            with open(file, "w", encoding="utf-8") as f:

                f.write(self.text_box.get("1.0", tk.END))

            self.status.config(text="Status : File Saved")

    # ---------------- Text ----------------
    def clear_text(self):

        self.text_box.delete("1.0", tk.END)

        self.status.config(text="Status : Text Cleared")

    def copy_text(self):

        text = self.text_box.get("1.0", tk.END)

        if text.strip():

            self.root.clipboard_clear()

            self.root.clipboard_append(text)

            self.status.config(text="Status : Text Copied")

        else:

            self.status.config(text="Status : Nothing To Copy")

    # ---------------- Voice Settings ----------------
    def change_voice(self, selected):

        index = self.voice_names.index(selected)

        self.tts.set_voice(index)

        self.status.config(text=f"Status : Voice changed to {selected}")

    def change_speed(self, value):

        self.tts.set_rate(int(value))

    def change_volume(self, value):

        self.tts.set_volume(int(value) / 100)


if __name__ == "__main__":
    VoiceApp()