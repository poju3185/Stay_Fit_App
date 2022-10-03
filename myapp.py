from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
# These are for the camera
from kivy.lang import Builder
from kivy.uix.camera import Camera

class SayHello(App):
    def build(self):
        self.window = GridLayout()
        #add widgets to window

        return Builder.load_file("cam.kv")


if __name__ == "__main__":
    SayHello().run()