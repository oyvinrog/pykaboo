from PIL import Image
import numpy as np
import logging
import os
import png

# Configure logging to file and console with full trace
logging.basicConfig(filename='pykaboo.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()  # Create console handler
console_handler.setLevel(logging.DEBUG)  # Set level to DEBUG for full trace
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Define the same formatter
console_handler.setFormatter(formatter)  # Set formatter to console handler
logging.getLogger().addHandler(console_handler)  # Add console handler to the root logger

def hide(img, source_files):
    logging.info(f"Hiding data in {img} with {source_files}")
    reader = png.Reader(filename=img)
    w, h, pixels, metadata = reader.read_flat()

    # Filter out unsupported metadata keys
    supported_keys = {'greyscale', 'alpha', 'bitdepth', 'color_type', 'interlace'}
    filtered_metadata = {key: metadata[key] for key in supported_keys if key in metadata}

    all_data = bytearray()
    metadata_content = ""
    for file in source_files:
        with open(file, 'rb') as f:
            file_data = f.read()
            metadata_content += f"{os.path.basename(file)}:{len(file_data)};"
            all_data.extend(file_data)

    metadata_content += "end"
    metadata_bytes = metadata_content.encode()
    data_bytes = metadata_bytes + all_data

    custom_chunk_type = b"tEXt"
    custom_chunk_data = b"hidden_data\x00" + data_bytes
    output_filename = f"stego_{os.path.basename(img)}"

    with open(output_filename, 'wb') as output_file:
        # Initialize the writer with filtered metadata and write the PNG file
        writer = png.Writer(width=w, height=h, **filtered_metadata)
        writer.write_array(output_file, pixels)

        # Write the custom tEXt chunk after the IDAT chunk
        png.write_chunk(output_file, custom_chunk_type, custom_chunk_data)
        # Write the IEND chunk
        png.write_chunk(output_file, b'IEND', b'')

    logging.info(f"Data hidden successfully in {output_filename}")
    return output_filename

# STOPPET HER!!! FÅ DEN TIL Å FUNGERE ORDENTLIG!!
def unhide(img, output_folder):
    logging.info(f"Starting to unhide data from {img}")
    
    with open(img, 'rb') as f:
        content = f.read()
    
    # Search for the tEXt chunk with the hidden data
    search_marker = b'tEXt'
    hidden_data_marker = b'hidden_data\x00'
    
    index = content.find(search_marker)
    while index != -1:
        start_index = index + len(search_marker)
        if content[start_index:start_index + len(hidden_data_marker)] == hidden_data_marker:
            data_chunk = content[start_index + len(hidden_data_marker):]
            logging.info("Hidden data chunk found")
            break
        index = content.find(search_marker, index + 1)
    else:
        logging.error("No hidden data found")
        raise ValueError("No hidden data found")
    
    metadata_end = data_chunk.find(b'end')
    if metadata_end == -1:
        logging.error("End of metadata not found")
        raise ValueError("End of metadata not found")
    
    metadata_content = data_chunk[:metadata_end].decode()
    logging.info(f"Metadata content: {metadata_content}")
    
    files_info = [info.split(':') for info in metadata_content.split(';') if info and info != 'end']
    logging.info(f"Files info: {files_info}")
    
    offset = metadata_end + len(b'end')
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename, size in files_info:
        size = int(size)
        file_data = data_chunk[offset:offset + size]
        offset += size
        
        logging.info(f"Extracting {filename} of size {size} bytes")
        
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'wb') as f:
            f.write(file_data)
        logging.info(f"File extracted: {output_path}")
    
    logging.info(f"Data extracted successfully to {output_folder}")
    return output_folder

def create_test_file():
    with open("test_file.txt", "w") as f:
        f.write("This is a test file.")

    with open("another_file.txt", "w") as f:
        f.write("This is another test file.")

def create_red_image():
    # Create an image with red color
    img = Image.new('RGB', (100, 100), "red")
    img.save('red_image.png')

def create_blue_image():
    # Create an image with blue color
    img = Image.new('RGB', (100, 100), "blue")
    img.save('blue_image.png')

def test():

    create_test_file()
    create_red_image()
    create_blue_image()

    # Hide the data from multiple files
    stego_image = hide("red_image.png", ["test_file.txt", "another_file.txt", "blue_image.png"])
    print(f"Data hidden in {stego_image}")

    # Unhide the data to a specific folder
    output_folder = unhide(stego_image, "extracted_files")
    print(f"Data extracted to folder {output_folder}")

if __name__ == "__main__":

    test()
