# player.py
import os

class MediaPlayer:
    def __init__(self, media_path):
        self.media_path = media_path
        self.is_playing = False

    def play(self):
        if not self.is_playing:
            print(f"Playing media from {self.media_path}...")
            # Hier müsstest du die Logik implementieren, um Medien tatsächlich abzuspielen
            self.is_playing = True
        else:
            print("Media wird bereits abgespielt.")

    def pause(self):
        if self.is_playing:
            print("Media wird pausiert...")
            # Implementiere die Pause-Funktionalität hier
            self.is_playing = False
        else:
            print("Keine Medien zum Pausieren.")

    def stop(self):
        if self.is_playing:
            print("Media wird gestoppt...")
            # Implementiere die Stop-Funktionalität hier
            self.is_playing = False
        else:
            print("Keine Medien zum Stoppen.")
