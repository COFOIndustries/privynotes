import unittest
from unittest.mock import patch
from ui import CommandLineInterface
from encryption import EncryptionHandler
from storage import StorageHandler

class TestCommandLineInterface(unittest.TestCase):
    def setUp(self):
        self.encryption = EncryptionHandler()
        self.encryption.set_key('testpassword')
        self.storage = StorageHandler()
        self.storage.conn = sqlite3.connect(':memory:')
        self.storage.cursor = self.storage.conn.cursor()
        self.storage.create_table()
        self.cli = CommandLineInterface(self.encryption, self.storage)

    @patch('builtins.input', side_effect=['Test Title', 'test, note', 'Test Content', 'END'])
    def test_create_note(self, mock_input):
        with patch('builtins.print') as mock_print:
            self.cli.create_note()
            mock_print.assert_any_call("Note 'Test Title' saved with ID 1.")

    @patch('builtins.input', side_effect=['y'])
    def test_delete_note(self, mock_input):
        self.storage.add_note_metadata('Test Note', 'test')
        with patch('builtins.print') as mock_print:
            self.cli.delete_note(1)
            mock_print.assert_any_call("Note ID 1 deleted.")

    def test_list_notes(self):
        self.storage.add_note_metadata('Test Note', 'test')
        with patch('builtins.print') as mock_print:
            self.cli.list_notes()
            mock_print.assert_any_call("ID: 1, Title: Test Note, Tags: test")

if __name__ == '__main__':
    unittest.main()
