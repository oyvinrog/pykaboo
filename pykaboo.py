"""
Peekaboo is a simple steganography tool that allows you to hide data in an image and
 extract it later.

Usage: 

    hide(img, source_file) - Hide the data in the image
    unhide(img, output_filename) - Extract the data from the image


"""

from PIL import Image
import numpy as np
import logging

# Configure logging to file
logging.basicConfig(filename='pykaboo.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def hide(img, source_file):
    # Open the image
    logging.info(f"Hiding data in {img} with {source_file}")
    image = Image.open(img)
    logging.info(f"Image opened")
    img_array = np.array(image)
    logging.info(f"Image converted to numpy array")

    # Read the source file
    logging.info(f"Reading source file")
    with open(source_file, 'rb') as f:
        data = f.read()

    logging.info(f"Source file read")

    # Convert data to binary
    logging.info(f"Converting data to binary")
    binary_data = ''.join(format(byte, '08b') for byte in data)
    data_length = len(binary_data)

    # Check if the image is large enough to hold the data
    if data_length > img_array.size - 32:  # Account for the 32 bits used to store length
        raise ValueError("Image is too small to hide the data")
    
    logging.info(f"Data converted to binary")

    # Flatten the image array
    flat_img = img_array.flatten()

    # Embed data length
    for i in range(32):
        flat_img[i] = (flat_img[i] & 0xFE) | int(format(data_length, '032b')[i])

    # Embed data
    for i, bit in enumerate(binary_data):
        flat_img[i + 32] = (flat_img[i + 32] & 0xFE) | int(bit)

    # Reshape the array back to the original image shape
    stego_img = flat_img.reshape(img_array.shape)

    # Save the steganographic image
    stego_image = Image.fromarray(stego_img.astype(np.uint8))

    # extract the actual filename from output_filename
    import os
    actual_img = os.path.basename(img)
    logging.info(f"Steganographic image saved as stego_{actual_img}")

    output_filename = f"stego_{actual_img}"
    stego_image.save(output_filename)

    return output_filename

def unhide(img, output_filename):
    # Open the image and extract the data
    image = Image.open(img)
    img_array = np.array(image)
    flat_img = img_array.flatten()

    # Extract data length
    length_bits = ''.join(str(pixel & 1) for pixel in flat_img[:32])
    data_length = int(length_bits, 2)

    # Extract data
    hidden_bits = ''.join(str(pixel & 1) for pixel in flat_img[32:32 + data_length])
    
    # Convert bits to bytes
    hidden_bytes = bytes(int(hidden_bits[i:i+8], 2) for i in range(0, len(hidden_bits), 8))
    
    # Save the extracted data to a file
    with open(output_filename, 'wb') as f:
        f.write(hidden_bytes)

    return output_filename

# Example usage:

def create_test_file():
    with open("test_file.txt", "w") as f:
        f.write("This is a test file.")

def create_red_image():
    # Create an image with red color
    img = Image.new('RGB', (100, 100), "red")
    img.save('red_image.png')

def test():

    create_test_file()
    create_red_image()

    # Hide the data
    stego_image = hide("red_image.png", "test_file.txt")
    print(f"Data hidden in {stego_image}")

    # Unhide the data
    extracted_file = unhide(stego_image, "extracted_data.txt")
    print(f"Data extracted to {extracted_file}")