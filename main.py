
import os
import asyncio
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from groq import Groq
import edge_tts

# Speech recognition module import
try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.RECORD_AUDIO,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.CAMERA
    ])
except ImportError:
    pass

class JarvisApp(App):
    def build(self):
        self.is_active = False
        self.api_key = "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"
        self.client = Groq(api_key=self.api_key)
        self.recognizer = sr.Recognizer() if sr else None
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.status_label = Label(
            text="JARVIS: OFF\n(Tap button to activate Wake-Word)", 
            font_size='20sp', 
            halign='center'
        )
        layout.add_widget(self.status_label)
        
        self.toggle_btn = Button(
            text="POWER ON JARVIS", 
            font_size='20sp', 
            background_color=(0, 1, 0, 1),
            size_hint=(1, 0.3)
        )
        self.toggle_btn.bind(on_press=self.toggle_jarvis)
        layout.add_widget(self.toggle_btn)
        
        return layout

    def toggle_jarvis(self, instance):
        if not self.is_active:
            self.is_active = True
            self.toggle_btn.text = "POWER OFF JARVIS"
            self.toggle_btn.background_color = (1, 0, 0, 1)
            self.status_label.text = "JARVIS: LISTENING FOR 'HEY JARVIS'..."
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.is_active = False
            self.toggle_btn.text = "POWER ON JARVIS"
            self.toggle_btn.background_color = (0, 1, 0, 1)
            self.status_label.text = "JARVIS: SLEEPING 😴"

    def listen_loop(self):
        if not self.recognizer:
            return

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_active:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio, language="hi-IN")
                    text_lower = text.lower()
                    
                    # Wake-word check
                    if "jarvis" in text_lower or "जार्विस" in text_lower or "hey jarvis" in text_lower:
                        Clock.schedule_once(lambda dt: self.update_status(f"Heard Wake Word! Asking AI..."))
                        self.ask_jarvis(text)
                except Exception:
                    pass

    def ask_jarvis(self, user_text):
        if not self.is_active:
            return

        system_prompt = (
            "You are Jarvis, an ultra-sarcastic, street-smart Indian AI buddy. "
            "You speak in casual Hinglish with zero filter. Speak like a close friend who roasts naturally."
        )

        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ]
            )
            reply = response.choices[0].message.content
            Clock.schedule_once(lambda dt: self.update_status(f"Jarvis: {reply}"))
            asyncio.run(self.speak(reply))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f"Error: {str(e)}"))

    async def speak(self, text):
        voice = "hi-IN-MadhurNeural"
        output_file = "jarvis_speech.mp3"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    def update_status(self, text):
        self.status_label.text = text

if __name__ == "__main__":
    JarvisApp().run()
