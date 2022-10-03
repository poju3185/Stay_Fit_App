import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy_garden.zbarcam import ZBarCam

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
        

class ThirdWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_string(
'''
#:import Label kivy.uix.label.Label
#:import SlideTransition kivy.uix.screenmanager.SlideTransition

WindowManager:
    MainWindow:
    SecondWindow:
    ThirdWindow:
        

<MainWindow>:
    name: "main"  # (在python) name = "main"
    id: MainWindow

        
    Button:
        text: "Camera"
        size_hint: .3, .3
        on_release: 
            app.root.current = "second"
            root.manager.transition.direction = "left"


<SecondWindow>:
    name: "second"
    id: SecondWindow

    BoxLayout:
        orientation: 'vertical'
        ZBarCam:
            id: qrcodecam
            decoded_text: ''.join([str(symbol.data.decode('utf-8')) for symbol in qrcodecam.symbols])
        Label:
            id: qrcode
            size_hint: None, None
            size: self.texture_size[0], 50
            text:'' if qrcodecam.decoded_text == '' else 'success'

        Button:
            size_hint: .3, .3
            text: 'confrim'
            on_press:
                # 做了三件事 1. 切換到"third"視窗 2. 用save()函數把掃到的raw text傳回python 3. 把處理過的商品名稱預先傳到"third"的label_text.text中
                if qrcode.text != '': app.root.current = "third"; root.save(qrcodecam.decoded_text); root.manager.screens[2].ids.label_text.text = root.product_name

    Button:
        size_hint: .1, .1
        text: "Go Back"
        on_release: 
            app.root.current = "main"
            root.manager.transition.direction = "right"
    
            
<ThirdWindow>:
    name: "third"
    id: ThirdWindow
    text: ''


    Label:
        id: label_text
        text: root.text

    
    Button:
        size_hint: .1, .1
        text: "Done"
        on_release: 
            app.root.current = "second"
            root.manager.transition.direction = "left"

'''
)

class MyMainApp(App):
    def build(self):  # __init__
        return kv
    


if __name__ == "__main__":
    MyMainApp().run()