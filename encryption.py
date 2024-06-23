from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def encrypt(password, data):
    # Generate a random salt
    salt = os.urandom(16)
    # Derive a key from the password
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    key = kdf.derive(password.encode())
    
    # Generate a random IV
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the data
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Create HMAC for integrity
    hmac = HMAC(key, hashes.SHA256(), backend=default_backend())
    hmac.update(encrypted_data)
    hmac_digest = hmac.finalize()
    
    # Return the salt, iv, hmac, and encrypted data
    return salt + iv + hmac_digest + encrypted_data

def decrypt(password, encrypted_bytes):
    # Extract salt, iv, and hmac from the input bytes
    salt = encrypted_bytes[:16]
    iv = encrypted_bytes[16:32]
    hmac_digest = encrypted_bytes[32:64]
    encrypted_data = encrypted_bytes[64:]
    
    # Derive the key from the password
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    key = kdf.derive(password.encode())
    
    # Verify HMAC for integrity
    hmac = HMAC(key, hashes.SHA256(), backend=default_backend())
    hmac.update(encrypted_data)
    hmac.verify(hmac_digest)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Unpad the data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    
    # Return the decrypted data
    return decrypted_data

# Example usage
#password = 'strongpassword'
#encrypt_file(password, 'plain.txt', 'encrypted.dat')
#decrypt_file(password, 'encrypted.dat', 'decrypted.txt')

def test():

    test = b"This is a test"
    password = "password"
    encrypted = encrypt(password, test)
    decrypted = decrypt(password, encrypted)
    print("Decrypted:  ", decrypted)

if __name__ == "__main__": 
    
    test()
