import os
import time
import random
import re
import io
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import PIL.Image 
import json 
from database import *
from reply_job import reply_to_the_chat
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
load_dotenv()

class HiddenPrints:
    """Context manager to suppress print statements."""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = io.StringIO()
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout

def send_message(message , driver):

        try:    
                message_box = driver.find_element(By.CSS_SELECTOR, "div[aria-placeholder='Type a message']")
                message_box.click()
                time.sleep(2)
                message_box.send_keys(message)
                message_box.send_keys(Keys.ENTER)

        except:

                print("Could not send message. Try again later.")

def human_delay(min_delay=0.5, max_delay=1.5):
    """Adds a human-like delay."""
    time.sleep(random.uniform(min_delay, max_delay))

class GeminiImageAnalyzer:
    """
    GeminiImageAnalyzer class for analyzing images using the Google Gemini API.
    Provides detailed descriptions of images and reports token usage.
    """

    def __init__(self):
        
        self.system_prompt_image_analysis = """
            You are a highly observant image analysis assistant.
            Process the visual information to fulfill the user's request.
            """

        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in your .env file.")
        
        genai.configure(api_key=gemini_api_key)
        
        
        self.model_name = "models/gemini-1.5-flash-latest" 
        try:
            self.llm_client = genai.GenerativeModel(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini model '{self.model_name}': {e}")

    def analyze_image(self, image_path: str, user_query: str = "") -> str:
        """
        Analyzes an image and provides a description based on an optional user query.
        Returns the generated description string.
        """
        try:
            try:
                img = PIL.Image.open(image_path)
            except FileNotFoundError:
                print(f"Error: Image file not found at '{image_path}'")
                return None
            except Exception as e:
                print(f"Error loading image '{image_path}': {e}")
                return None

            
            contents_parts = [
                img,
                {"text": self.system_prompt_image_analysis} # Use the image analysis prompt
            ]
            if user_query: # Add user's specific question about the image
                contents_parts.append({"text": user_query})
            
            with HiddenPrints(): 
                response = self.llm_client.generate_content(
                    contents=contents_parts,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.2,
                        max_output_tokens=2000 
                    ),
            
                )
            
            if hasattr(response, 'usage_metadata'):
                prompt_tokens = response.usage_metadata.prompt_token_count
                output_tokens = response.usage_metadata.candidates_token_count
                total_tokens = response.usage_metadata.total_token_count
                
                print(f"\n✨ Gemini Token Usage for Image Analysis:")
                print(f"  - Prompt Tokens (including image and text prompt): {prompt_tokens}")
                print(f"  - Output Tokens: {output_tokens}")
                print(f"  - Total Tokens: {total_tokens}")
            else:
                print("⚠️ Could not retrieve token usage metadata.")

            return self._clean_response(response.text.strip())

        except Exception as e:
            print(f"AI Error during image analysis with Gemini: {e}")
            return None

    def _clean_response(self, text: str) -> str:
        """Cleans the response text by removing specific XML-like tags and Markdown code blocks."""
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

def image_process_and_reply(driver ,chat_image_path , client_name , previous_data : str):

    print("\n--- Starting GeminiImageAnalyzer ---")
    image_analyzer = GeminiImageAnalyzer()
    
    if os.path.exists(chat_image_path):
        print(f"\n--- Analyzing '{chat_image_path}' for chat details ---")

        # The detailed user query instructing Gemini on what to extract and in what format
        query = f"""

         The Query part is hidden due to cloning issues 
         All rights reserved
         Mail to : Rjsumit151@gmail.com for hidden part 
         Whatsapp : +91 94603 57477
        """

        json_output_str = image_analyzer.analyze_image(chat_image_path, user_query=query)

        setup_database()  # Only needed once, or on app start

        if json_output_str:
            try:
                cleaned_str = json_output_str.strip()
                if cleaned_str.startswith("```json"):
                    cleaned_str = cleaned_str.replace("```json", "").replace("```", "").strip()
                
                chat_data = json.loads(cleaned_str)
                print(chat_data)
                print("Chat data stored/updated in the database. now giving reply to it")
                reply_to_the_chat(chat_data , driver)
                insert_or_update_chat_data(chat_data)

            except json.JSONDecodeError as e:
                print("❌ JSON Decode Error:", e)
                print("🔎 Offending string:\n", json_output_str)
            except Exception as e:
                print(f"❌ Other error: {e}")

            export_to_csv()
    else:
        print(f"Error: Image file '{chat_image_path}' not found. Please ensure it's in the same directory as this script.")