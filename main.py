from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import StringProperty
from numpy import product


class MainWindow(Screen):
    state = StringProperty('normal') # 第一種方法將變數傳到kv檔

class SecondWindow(Screen):
    # def __init__(self, **kwargs):  # 第二種方法將變數傳到kv檔
    #     super(SecondWindow, self).__init__(**kwargs)
    #     self.myvar = 'yoyoyo'
    product_name = StringProperty('')
    def save(self, text):
        # 針對傳入的text進行處理
        self.product_name = text
        print(text)
        

class ThirdWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('my.kv')

class MyMainApp(App):
    def build(self):  # __init__
        return kv
    


if __name__ == "__main__":
    MyMainApp().run()