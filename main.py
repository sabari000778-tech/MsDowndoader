from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.utils import platform
import threading
import yt_dlp
import os


def get_download_path():
    if platform == "android":
        from android.storage import primary_external_storage_path
        return os.path.join(primary_external_storage_path(), "Download")
    return os.path.expanduser("~")


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.label = Label(
            text="Created by\n[b]Sabari[/b]",
            markup=True,
            font_size=52,
            halign="center",
            opacity=0,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.add_widget(self.label)
        self.add_widget(layout)
        Clock.schedule_once(self.start_animation, 0.5)

    def start_animation(self, dt):
        anim = (Animation(opacity=1, duration=1.5) +
                Animation(opacity=1, duration=1.0) +
                Animation(opacity=0, duration=1.0))
        anim.bind(on_complete=self.go_to_main)
        anim.start(self.label)

    def go_to_main(self, *args):
        self.manager.current = "main"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=30, spacing=20)

        layout.add_widget(Label(
            text="Ms Downloader",
            font_size=42,
            bold=True,
            size_hint_y=None,
            height=90,
            color=(0.2, 0.8, 0.2, 1)
        ))

        layout.add_widget(Label(
            text="Enter YouTube or Instagram URL:",
            font_size=28,
            size_hint_y=None,
            height=60
        ))

        self.url_input = TextInput(
            multiline=False,
            font_size=26,
            size_hint_y=None,
            height=70,
            hint_text="Paste URL here..."
        )
        layout.add_widget(self.url_input)

        self.status_label = Label(
            text="",
            font_size=26,
            size_hint_y=None,
            height=60,
            color=(0.2, 1, 0.2, 1)
        )
        layout.add_widget(self.status_label)

        btn = Button(
            text="Download",
            font_size=32,
            size_hint_y=None,
            height=80,
            background_color=(0, 0.6, 0, 1),
            bold=True
        )
        btn.bind(on_press=self.start_download)
        layout.add_widget(btn)

        layout.add_widget(Label(
            text="Created by Sabari",
            font_size=22,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=40
        ))

        self.add_widget(layout)

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "Please enter a URL!"
            self.status_label.color = (1, 0.3, 0.3, 1)
            return
        self.status_label.color = (0.2, 1, 0.2, 1)
        self.status_label.text = "Downloading... Please wait"
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, url):
        save_path = get_download_path()
        ydl_opts = {
            "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
            "format": "best",
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.text = "Download Complete! ✅"
            self.status_label.color = (0.2, 1, 0.2, 1)
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"
            self.status_label.color = (1, 0.3, 0.3, 1)


class MsDownloaderApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        return sm


if __name__ == "__main__":
    MsDownloaderApp().run()
