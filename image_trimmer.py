import cv2
import numpy as np
from PIL import Image
import sys

def split_image_by_red_line(image_path, output_path="bottom_right_half.png"):
    """
    Finds a single horizontal red line in an image, then crops and saves
    the portion of the image below and to the right of the line's starting point.

    Args:
        image_path (str): The path to the input image file.
        output_path (str): The path where the cropped section will be saved.
    """
    
    print("The core logic is hidden due to cloning issues")
    print("All rights reserved")
    print("Mail to : Rjsumit151@gmail.com for hidden part")
    print("Whatsapp : +91 94603 57477")

if __name__ == "__main__":

    input_file = "chat.png"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
    split_image_by_red_line(input_file, "bottom_right_half.png")


