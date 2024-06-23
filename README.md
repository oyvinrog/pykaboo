# Pykaboo

## Description

Hide and unhide files in images using steganography.

This is a simple script that allows you to hide and unhide files in images using steganography.

The hide function in the provided Python script uses a technique called Least Significant Bit (LSB) steganography to hide files within an image.

Simply right click the image file you
want to use for storage, and select "Hide with Pykaboo". Then just select all of the
files you want to hide.

To unhide a file, simply right click the file you want to unhide and select "Unhide with Pykaboo".

## Example of LSB

Example with an Image
Let's use a simple grayscale image where each pixel is represented by an 8-bit value (0 to 255):

Original Pixel Values: 10110101, 11001100, 10010011
Binary of Hidden Message: 010 (representing the letter 'A')
Step-by-Step Embedding:

Replace the LSB of the first pixel with the first bit of the message:
Original: 10110101
New: 10110100 (last bit changed from 1 to 0)

Replace the LSB of the second pixel with the second bit of the message:
Original: 11001100
New: 11001101 (last bit changed from 0 to 1)

Replace the LSB of the third pixel with the third bit of the message:
Original: 10010011
New: 10010010 (last bit changed from 1 to 0)

## Roadmap

Include AES encryption and password protection.