import os
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver import ChromeOptions, DesiredCapabilities
import random
from app.simulation.main_logic import RetroperspectiveClass
#from xvfbwrapper import Xvfb
from pyvirtualdisplay import Display

TZ = "Europe/Kiev"
basedir = os.path.abspath(os.path.dirname(__file__))
#username = 'speedsolver99@gmail.com'
#password = '1q2w3e4r5t6Y'
scheduler = BackgroundScheduler(timezone=TZ)
scheduler.start()

min_line = [1,4,7,10,13,16,19,22,25,28,31,34]
middle_line = [2,5,8,11,14,17,20,23,26,29,32,35]
max_line = [3,6,9,12,15,18,21,24,27,30,33,36]
first12 = [1,2,3,4,5,6,7,8,9,10,11,12]
second12 = [13,14,15,16,17,18,19,20,21,22,23,24]
third12 = [25,26,27,28,29,30,31,32,33,34,35,36]
red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
black = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]


#double_bt = "//button[@data-role='double-button']"
double_bt = "//div[@class='doubleRepeatButtonWrapper--55420']"
email_field = "//input[@type='email']"
password_field = "//input[@type='password']"
balance_field = "//span[@data-role='balance-label__value']"
#balance_field = "//span[@class='User_balance__3bk4d']"
game_iframe = "//iframe[@class='GameIframe_iframe__1hYPa LocalGameFrame_iframe__1w516']"
video_mode_bt = "//button[@data-role='video-button']"
info_text_field = "//div[@class='text--27a51']"
bet_4_bt = "//div[@data-value='4']"
bet_10_bt = "//div[@data-value='10']"
bet_20_bt = "//div[@data-value='20']"
bet_100_bt = "//div[@data-value='100']"
bet_500_bt = "//div[@data-value='500']"
bet_2000_bt = "//div[@data-value='2000']"
retro_bt = "//div[@data-role='paginator-item-numbers']"
#no_balance_bet = 'Ставка'
#bet_info_field = ''
bet_information_dict = {}
user_bot_last_state = {}
admin_id = 1
verification_code = 5692
drivers_dict = dict()
retro_dict = dict()
windows_dict = dict()

online_users = ["Нет пользователей онлайн"]

def generate_verification_code():
    global verification_code
    number = random.randrange(1000,9999)
    verification_code = number


def add_retro(username, fav_username, fav_password):
    global retro_dict
    if username in retro_dict:
        return retro_dict[username]
    else:
        retro = RetroperspectiveClass(username, fav_username, fav_password)
        retro_dict[username] = retro
        return retro


def delete_retro(username):
    global retro_dict
    if username in retro_dict:
        retro_dict.pop(username)


def delete_webdriver(username):
    global drivers_dict, windows_dict
    if username in drivers_dict:
        drivers_dict[username].get("https://www.favbet.com/ru/live-casino/")
        #windows_dict[username].stop()
        #windows_dict[username].stop()
        drivers_dict[username].quit()
        drivers_dict.pop(username)

#For real project
def add_webdriver1(username):
    global drivers_dict, windows_dict
    if username in drivers_dict:
        return drivers_dict[username]
    else:
        chrome_option = ChromeOptions()
        chrome_option.add_extension("proxy.zip")
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "80.0_VNC",
            "screenResolution": "1920x1080x24",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False
            }
        }
        driver = webdriver.Remote(
            command_executor='http://selenoid:4444/wd/hub',
            options=chrome_option,
            desired_capabilities=capabilities)
        driver.maximize_window()
        drivers_dict[username] = driver
        return drivers_dict[username]

#For debug
def add_webdriver(username):
    global drivers_dict, windows_dict
    if username in drivers_dict:
        return drivers_dict[username]
    else:
        chrome_option = ChromeOptions()
        executable_path = "/usr/bin/chromedriver"
        driver = webdriver.Chrome()
        driver.maximize_window()
        drivers_dict[username] = driver
        return drivers_dict[username]


class Config(object):

    #Секретный ключ для шифровки страниц во избежание хакерских атак
    SECRET_KEY = 'fav_fav_bet_bet'
    #Расположение БД
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'ruketka.master@gmail.com'
    MAIL_PASSWORD = 'vgmfjsedblfirbps'
    ADMINS = ['ruketka.master@gmail.com']

