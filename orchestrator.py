#send.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
import random
from database import *
from image_trimmer import split_image_by_red_line
from Central_processing import image_process_and_reply

def delay(min_delay=1.5, max_delay=2.5):
    """Adds a human-like delay."""  
    time.sleep(random.uniform(min_delay, max_delay))

def scrap_the_chat(driver):
        print("📲 Opening chat for all contacts")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='pane-side']")))
        
        try:
            unread_tab = WebDriverWait(driver , 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'unread message')]/../..")))
            driver.execute_script("arguments[0].style.borderBottom = '2px solid red'", unread_tab)   

        except:
            today_tab = WebDriverWait(driver , 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Today')]/../..")))
            driver.execute_script("arguments[0].style.borderBottom = '2px solid red'", today_tab)

        #Lets find the client name

        element = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"][data-tab="6"][role="button"]')
        target = element.find_element(By.TAG_NAME, "span")

        client_name = target.text

        print(f"Client name is {client_name}")

        driver.save_screenshot("chat.png") 

        split_image_by_red_line("chat.png" , "unread_chat_area.png")

        delay()

        previous_data = get_chat_data_by_client(client_name)

        print("reached here")
        image_process_and_reply(driver , "unread_chat_area.png" , client_name , None)
            
            
def unread_chat_auto(driver):

        try:
                container = driver.find_element(By.CSS_SELECTOR, "div[aria-label='chat-list-filters']")
        except:
                print("Could not find the unread messages tab. Try again later.")

        while True:

                print("The core logic is hidden due to cloning issues")
                print("All rights reserved")
                print("Mail to : Rjsumit151@gmail.com for hidden part")
                print("Whatsapp : +91 94603 57477")
                
        print("Replied the chats succesfully")  