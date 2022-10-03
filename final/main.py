from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from numpy import product
from kivy.uix.popup import Popup
import gspread
from kivy.core.window import Window
Window.clearcolor = (28/255, 28/255, 30/255, 1)
creds = gspread.service_account(filename='credential.json')
client = creds.open_by_url(
"https://docs.google.com/spreadsheets/d/1oT7JtM6lruaFktF_eNz310wBKo-xKJyrDSG-cYdXKuU/edit#gid=0")
ingredientsheet = client.worksheet("ingredient")
accountsheet = client.worksheet("account")
account_list = accountsheet.col_values(1)
password_list = accountsheet.col_values(2)
validaccount = 0
currentname = ["default"]
usersheet = client.worksheet(currentname[0])



#使用者登入畫面
class LoginPage(Screen):
    username = ObjectProperty("None")
    password = ObjectProperty(None)
    def press(self):
        if self.username.text in account_list:
            if self.password.text == password_list[account_list.index(self.username.text)]:
                validaccount = 1
            if validaccount == 0:
                # self.ids.Login.text = "Wrong Password"
                self.username.text = ""
                self.password.text = ""
            else:
                self.manager.current = "main"
                currentname[0] = self.username.text
        else:
            account_list.append(self.username.text)
            password_list.append(self.password.text)
            accountsheet.append_row([self.username.text, self.password.text]) 
            usersheet = client.add_worksheet(title=self.username.text, rows=100, cols=10)
            cell_list = usersheet.range('A1:L1')
            head = ["編號", "品牌/製作商",	"品名", "熱量 (Kcal/份)",	"熱量 (Kcal/100g)",
            	"碳水化合物(g)", "蛋白質(g)", "脂肪(g)", "鈉(mg)", "金額(NTD)",	"累積熱量",	"目標熱量"]
            for i in range(len(head)):
                cell_list[i].value = head[i]
            usersheet.update_cells(cell_list)
            usersheet.update("K2", "=SUM(D2:D100)", raw=False)
            usersheet.update("L2", "0")
            usersheet.update("K3", "=L2-K2", raw=False)
            currentname[0] = self.username.text
            validaccount = 1
            self.manager.current = "welcome"

class MainWindow(Screen):
    state = StringProperty('normal') # 第一種方法將變數傳到kv檔
    def refresh(self):
        usersheet = client.worksheet(currentname[0])
        #targetvalue = usersheet.acell('L2').value
        #currentvalue = usersheet.acell('K2').value
        #suplus = int(targetvalue) - int(currentvalue)
        self.ids.main_text.text =usersheet.acell('K3').value
        self.ids.target_kcal_shown.text = usersheet.acell('L2').value
        self.ids.consumed_kcal_shown.text = usersheet.acell('K2').value 

class SecondWindow(Screen):
    # def __init__(self, **kwargs):  # 第二種方法將變數傳到kv檔
    #     super(SecondWindow, self).__init__(**kwargs)
    #     self.myvar = 'yoyoyo'
    product_name = StringProperty('')
    def save(self, text):
        # 針對傳入的text進行處理
        usersheet = client.worksheet(currentname[0])
        self.product_name = text
        cell = ingredientsheet.find(text)
        valuelist = ingredientsheet.row_values(cell.row)
        usersheet.append_row(valuelist[1:], value_input_option='USER_ENTERED')
        print(valuelist[1])
        # mains.ids.main_text.text = usersheet.acell('K2').value + '//' + usersheet.acell('L2').value 
        # + ' kcal, remains ' + str(int(usersheet.acell('L2').value) - int(usersheet.acell('K2').value)) + ' kcal to consume'
        

class ThirdWindow(Screen):
    pass


class FourthWindow(Screen):
    item: ObjectProperty(None)
    calorie: ObjectProperty(None)
    quantity: ObjectProperty(None)
    price: ObjectProperty(None)

    def press(self):
        usersheet = client.worksheet(currentname[0])
        item = self.item.text
        calorie = self.calorie.text
        quantity = self.quantity.text
        price = self.price.text
        newlist = [0, 0, item, calorie, 0, 0, 0, 0, 0, price]
        ingredientsheet.append_row(newlist, value_input_option='USER_ENTERED')
        for i in range(int(quantity)):
            usersheet.append_row(newlist, value_input_option='USER_ENTERED')  # 新增在個人的sheet下
        mains = self.manager.get_screen("main")
        mains.ids.consumed_kcal_shown.text = usersheet.acell('K2').value
        # mains.ids.main_text.text = usersheet.acell('K2').value + '//' + usersheet.acell('L2').value 
        # + ' kcal, remains ' + str(int(usersheet.acell('L2').value) - int(usersheet.acell('K2').value)) + ' kcal to consume'
        self.item.text = ""
        self.calorie.text = ""
        self.quantity.text = ""
        self.price.text = ""
    

class FifthWindow(Screen):
    target = ObjectProperty(None)

    def press(self):
        usersheet = client.worksheet(currentname[0])
        target = self.target.text
        usersheet.update("L2", target)
        mains = self.manager.get_screen("main")
        # mains.ids.main_text.text = str(usersheet.acell('K3'))
        # mains.ids.target_kcal_shown.text = str(usersheet.acell('L2').value)
        # mains.ids.consumed_kcal_shown.text = str(usersheet.acell('K2').value )
        self.target.text = ""

class WelcomeWindow(Screen):
    pass
class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('my.kv')

class MyMainApp(App):
    def build(self):  # __init__
        return kv
    


if __name__ == "__main__":
    MyMainApp().run()