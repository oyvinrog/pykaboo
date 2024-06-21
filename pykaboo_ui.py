"""

Please run pykaboo.reg to create the registry entries for the context menu in
Windows

TODO:
- AES encryption with password to lock/unlock
- It will also know the original filename


"""
import sys
import os
from tkinter import Tk, filedialog
from pykaboo import hide, unhide
import logging

# Configure logging to file
logging.basicConfig(filename='pykaboo.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def select_image():
    root = Tk()
    root.withdraw()  # Hide the main window
    image_path = filedialog.askopenfilename(title="Select an image file", 
                                            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    return image_path

def main():
    logging.info("Starting Pykaboo")
    logging.info(f"Arguments: {sys.argv}")
    if len(sys.argv) != 3:
        logging.error("Incorrect usage. Expected two arguments.")
        print("Usage: python pykaboo_ui.py <hide/unhide> <file>")
        sys.exit(1)

    operation = sys.argv[1]
    file_path = sys.argv[2]

    if operation == "hide":
        img_path = select_image()
        if not img_path:
            logging.warning("No image selected. Exiting.")
            print("No image selected. Exiting.")
            sys.exit(1)
        try:
            logging.info(f"Hiding data in {img_path} with {file_path}")
            result = hide(img_path, file_path)
            logging.info(f"Data hidden in {result}")
            print(f"Data hidden in {result}")
        except Exception as e:
            logging.error(f"An error occurred: {e} on line {e.__traceback__.tb_lineno}")
            print(f"An error occurred: {e}")
    elif operation == "unhide":
        try:
            logging.info(f"Unhiding data from {file_path}")
            result = unhide(file_path, "unhidden_file.txt")
            logging.info(f"Data retrieved from {result}")
            print(f"Data retrieved from {result}")
        except Exception as e:
            logging.error(f"An error occurred: {e} on line {e.__traceback__.tb_lineno}")
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
