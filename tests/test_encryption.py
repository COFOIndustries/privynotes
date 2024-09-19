import unittest
from encryption import EncryptionHandler

class TestEncryptionHandler(unittest.TestCase):
    def setUp(self):
        self.encryption = EncryptionHandler()
        self.password = 'testpassword'
        self.encryption.set_key(self.password)
        self.sample_text = 'This is a test note.'

    def test_encryption_and_decryption(self):
        encrypted = self.encryption.encrypt(self.sample_text)
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(self.sample_text, decrypted)

    def test_incorrect_key(self):
        encrypted = self.encryption.encrypt(self.sample_text)
        self.encryption.set_key('wrongpassword')
        with self.assertRaises(ValueError):
            self.encryption.decrypt(encrypted)

if __name__ == '__main__':
    unittest.main()
