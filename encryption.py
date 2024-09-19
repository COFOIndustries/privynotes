from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

class EncryptionHandler:
    def __init__(self):
        self.key = None

    def set_key(self, password):
        print("Generating encryption key...")
        self.key = self.get_hash(password).encode('utf-8')
        print("Key generated successfully.")

    def encrypt(self, data):
        print("Encrypting note...")
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        print("Encryption complete.")
        return cipher.nonce + tag + ciphertext

    def decrypt(self, data):
        print("Decrypting note...")
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        print("Decryption complete.")
        return decrypted_data.decode('utf-8')

    def get_hash(self, password):
        """Generates a SHA-256 hash of the password to be used as the key."""
        hasher = SHA256.new(password.encode('utf-8'))
        return hasher.hexdigest()

