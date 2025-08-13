from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from orchestrator import unread_chat_auto, delay
import time
import random

driver = None

def setup_driver():
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("detach", True)
        # Uncomment for background run:
        #options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ Chrome initialized")

        return driver

def wait_for_login(driver, timeout=120):
        print("Please scan the QR code from your WhatsApp app to log in ignore if done.")
        try:
                WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='pane-side']"))
                )
                print("Logged in successfully.")
        except:
                print("Login timeout. Make sure to scan the QR code in time.")
                driver.quit()

def close(driver):

        delay()
        driver.quit()


def main():
        
        driver = setup_driver()
        link = f"https://web.whatsapp.com/"

        try:
                driver.get(link)
                wait_for_login(driver)

        except:
                print("Enable to open whatsapp , Check your internet connection and try again later")

        delay()
        
        #It is made sure that the whatsapp is open now we can do automation

        try:
                unread_chat_auto(driver)
                delay()

        except:
                print("No new chats to load")
        
        time.sleep(2)
        close(driver)


if __name__ == "__main__":
        main()