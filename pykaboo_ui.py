"""
see README.md for more info

Please run pykaboo.reg to create the registry entries for the context menu in
Windows

TODO:
- AES encryption with password to lock/unlock
- It will also know the original filename


"""
import sys
import os
from tkinter import Tk, filedialog
from tkinter.simpledialog import askstring
from pykaboo import hide, unhide
import logging

# Configure logging
logging.basicConfig(filename='pykaboo.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def select_files():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(title="Select files to hide", 
                                             filetypes=[("All files", "*.*")])
    return file_paths

def get_password():
    root = Tk()
    root.withdraw()  # Hide the main window
    password = askstring("Password", "Enter password:", show='*')
    return password

def main():
    logging.info("Starting Pykaboo")
    logging.info(f"Arguments: {sys.argv}")
    if len(sys.argv) != 3:
        logging.error("Incorrect usage. Expected two arguments.")
        print("Usage: python pykaboo_ui.py <hide/unhide> <image_file>")
        sys.exit(1)

    operation = sys.argv[1]
    image_path = sys.argv[2]
    password = get_password()
    if not password:
        logging.warning("No password provided. Exiting.")
        print("No password provided. Exiting.")
        sys.exit(1)

    if operation == "hide":
        file_paths = select_files()
        if not file_paths:
            logging.warning("No files selected. Exiting.")
            print("No files selected. Exiting.")
            sys.exit(1)
        try:
            logging.info(f"Hiding files {file_paths} in {image_path}")
            result = hide(image_path, file_paths, password)
            logging.info(f"Data hidden in {result}")
            print(f"Data hidden in {result}")
        except Exception as e:
            logging.error(f"An error occurred: {e} on line {e.__traceback__.tb_lineno}")
            print(f"An error occurred: {e}")
    elif operation == "unhide":
        try:
            logging.info(f"Unhiding data from {image_path}")
            result = unhide(image_path, "unhidden_files", password)
            logging.info(f"Data retrieved from {result}")
            print(f"Data retrieved from {result}")
        except Exception as e:
            logging.error(f"An error occurred: {e} on line {e.__traceback__.tb_lineno}")
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
