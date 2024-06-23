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
import os

# Configure logging to file
logging.basicConfig(filename='pykaboo.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def hide(img, source_files):
    logging.info(f"Hiding data in {img} with {source_files}")
    image = Image.open(img)
    img_array = np.array(image)

    # Prepare data with metadata
    all_data = bytearray()
    metadata = ""
    for file in source_files:
        with open(file, 'rb') as f:
            file_data = f.read()
            metadata += f"{os.path.basename(file)}:{len(file_data)};"
            all_data.extend(file_data)

    metadata += "end"  # End of metadata marker
    metadata_bytes = metadata.encode()
    binary_data = ''.join(format(byte, '08b') for byte in metadata_bytes + all_data)
    data_length = len(binary_data)

    if data_length > img_array.size - 32:
        raise ValueError("Image is too small to hide the data")

    flat_img = img_array.flatten()
    for i in range(32):
        flat_img[i] = (flat_img[i] & 0xFE) | int(format(data_length, '032b')[i])
    for i, bit in enumerate(binary_data):
        flat_img[i + 32] = (flat_img[i + 32] & 0xFE) | int(bit)

    stego_img = flat_img.reshape(img_array.shape)
    stego_image = Image.fromarray(stego_img.astype(np.uint8))
    output_filename = f"stego_{os.path.basename(img)}"
    stego_image.save(output_filename)

    return output_filename

def unhide(img, output_folder):
    image = Image.open(img)
    img_array = np.array(image)
    flat_img = img_array.flatten()

    length_bits = ''.join(str(pixel & 1) for pixel in flat_img[:32])
    data_length = int(length_bits, 2)
    hidden_bits = ''.join(str(pixel & 1) for pixel in flat_img[32:32 + data_length])
    hidden_bytes = bytes(int(hidden_bits[i:i+8], 2) for i in range(0, len(hidden_bits), 8))

    # Extract metadata
    metadata_end = hidden_bytes.find(b'end')
    metadata_content = hidden_bytes[:metadata_end].decode()
    files_info = [info.split(':') for info in metadata_content.split(';') if info]
    offset = metadata_end + 3  # +3 to move past 'end'

    # Extract files
    
    # create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename, size in files_info:
        size = int(size)
        file_data = hidden_bytes[offset:offset + size]
        offset += size
        with open(os.path.join(output_folder, filename), 'wb') as f:
            f.write(file_data)

    return output_folder

# Example usage:

def create_test_file():
    with open("test_file.txt", "w") as f:
        f.write("This is a test file.")

    with open("another_file.txt", "w") as f:
        f.write("This is another test file.")

def create_red_image():
    # Create an image with red color
    img = Image.new('RGB', (100, 100), "red")
    img.save('red_image.png')

def test():

    create_test_file()
    create_red_image()

    # Hide the data from multiple files
    stego_image = hide("red_image.png", ["test_file.txt", "another_file.txt"])
    print(f"Data hidden in {stego_image}")

    # Unhide the data to a specific folder
    output_folder = unhide(stego_image, "extracted_files")
    print(f"Data extracted to folder {output_folder}")

if __name__ == "__main__":

    test()
