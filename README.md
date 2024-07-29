# Pykaboo

This is a simple script that allows you to hide and unhide files in images using steganography.

Simply hold shift and right click the image file you
want to use for storage, and select "Hide with Pykaboo". Then just select all of the
files you want to hide.

![alt text](images/image.png)

The hide function in the provided script uses a technique to hide
data in the PNG metadata. Rather than embedding the data in the pixel values
of the image, it instead embeds the data in the metadata of the PNG file.

We use AES-256 encryption to encrypt the files, so you are safe if someone manages to understand that 
the files contain hidden information.

To unhide a file, simply right click the image you want to unhide and select "Unhide with Pykaboo".
