from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

file_path = "catalog.png"
sales_number = "+91 94603 57477"

def delay(min_delay=1.5, max_delay=2.5):
    """Adds a human-like delay."""  
    time.sleep(random.uniform(min_delay, max_delay))

def reply_to_the_chat(chat_data , driver):

    print("Replying to the chat")
    
    #First :read the output of the chat
    #Second : Wheter the client asked for the catalog or not 
    #Third : if he asks then we have to do three things: First send him the catalog , then send sales team the message that the client is interested
    #Fouth : if he tell some areas to improve then we also have to send them the message too
    #fifth if he/she asked for the meeting
    #normal reply should be given to him

    message_box = driver.find_element(By.CSS_SELECTOR, "div[aria-placeholder='Type a message']")
    message_box.click()
    delay()
    message_box.send_keys(chat_data['last_reply'])
    message_box.send_keys(Keys.ENTER)
    delay()

    if bool(chat_data["catalog"]):
        print("Client asked for product/service")
        #First send him the catalog

        try:    
                print("Sending the catalog")
                #To send the catalog
                #Step 1: Locate the attach button
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus-rounded']"))).click()
                time.sleep(1)

                print("plus section clicked")
                # Upload the file
                file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
                file_input.send_keys("/home/sumit/Downloads/catalog.png")
                time.sleep(2)

                print("reacher here")

                # Click the send button
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='wds-ic-send-filled']")))
                element.click()

                #To send the sales team message
                #find the search bar 
                container = driver.find_element(By.CSS_SELECTOR, "div[aria-label='chat-list-filters']")
                container.find_elements(By.TAG_NAME, "button")[0].click()
                delay()
                search_bar = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Search input textbox']")    
                search_bar.click()
                delay()
                search_bar.send_keys(sales_number)
                delay()
                search_bar.send_keys(Keys.ENTER)
                message_box = driver.find_element(By.CSS_SELECTOR, "div[aria-placeholder='Type a message']")
                message_box.click()
                delay()
                message_box.send_keys(f"""The client {chat_data["client_name"]} seems interested and asked for the catalog""")
                message_box.send_keys(Keys.ENTER)
                delay()

                
        except:
                print("Could not send message. Try again later.")

    elif chat_data["suggestions"] != "No":
            
            try:
                container = driver.find_element(By.CSS_SELECTOR, "div[aria-label='chat-list-filters']")
                container.find_elements(By.TAG_NAME, "button")[0].click()
                delay()
                search_bar = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Search input textbox']")    
                search_bar.click()
                delay()
                search_bar.send_keys(sales_number)
                delay()
                search_bar.send_keys(Keys.ENTER)
                delay()
                message_box = driver.find_element(By.CSS_SELECTOR, "div[aria-placeholder='Type a message']")
                message_box.click()
                delay()
                message_box.send_keys(f"""The client {chat_data["client_name"]} Suggested to improve the product/service : {chat_data["suggestions"]}""")

                message_box.send_keys(Keys.ENTER)
                delay()

            except:
                    print("Could not send message. Try again later.")

