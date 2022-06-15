import datetime
import time
import browser as browser
import config as cnfg
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

count = 0
retro_values_list = list()

#driver = webdriver.Chrome()
#driver.maximize_window()

def retro_data(driver):
    global count, retro_values_list
    retro_but = driver.find_element(by=By.XPATH, value=cnfg.retro_bt)
    retro_but.click()
    slider = driver.find_element(by=By.XPATH, value="//div[@class='knob--458ea enabled--ba5b8']")
    help = driver.find_element(by=By.XPATH, value="//div[@class='right-stub--4fc34']")
    action = ActionChains(driver)
    action.drag_and_drop(slider,help).perform()
    wait = WebDriverWait(driver, 60)
    elm = wait.until(lambda x: x.find_element(by=By.XPATH, value="//div[@class='text--27a51' and contains(text(), 'ДЕЛАЙТЕ')]"))
    text = elm.text
    # text = driver.find_element(by=By.XPATH, value="//div[@class='text--27a51']").text
    first_txt = text[: text.find(' ')]
    if first_txt == 'ДЕЛАЙТЕ' or 'СТАВКИ' or 'СТАВОК':
        values = driver.find_elements(by=By.XPATH, value="//div[@class='recent-numbers--834df']//div[contains(@class, 'single-number--43778')]")
        for i in values:
            buff = i.get_attribute('data-role')
            last_txt = buff[buff.find('-') + 1:]
            retro_values_list.append(int(last_txt))
            #print(last_txt)
            count += 1
        other_values = driver.find_elements(by=By.XPATH, value="//div[contains(@class, 'statistics--adb67')]//div[contains(@class, 'single-number--43778')]")
        for i in other_values:
            buff = i.get_attribute('data-role')
            last_txt = buff[buff.find('-') + 1:]
            retro_values_list.append(int(last_txt))
            #print(last_txt)
            count += 1
    #print(count)
    return retro_values_list

#driver.get("https://www.favbet.com/ru/live-casino/show-game/evolution/lightning-roulette/?playMode=real")
#wait = WebDriverWait(driver, 60)
#elm = wait.until(lambda x: x.find_element(by=By.XPATH, value="//iframe[@class='GameIframe_iframe__1hYPa LocalGameFrame_iframe__1w516']"))
#driver.switch_to.frame(elm)
#camera_bt = wait.until(lambda x: x.find_element(by=By.XPATH, value="//button[@data-role='video-button']"))
#camera_bt.click()
