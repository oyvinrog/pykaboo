
# Reproduce known issue
from pykaboo import hide

image_file = r"C:\scripts\steganodrive\playground\pic2.png"
# add  folder path to the files to hide
files_to_hide = [r"C:\scripts\steganodrive\playground\pic1.png",
                 r"C:\scripts\steganodrive\playground\tekst2.txt",
                 r"C:\scripts\steganodrive\playground\test.txt"]

stego_image = hide(image_file, files_to_hide)