import unittest
import os
from storage import StorageHandler

class TestStorageHandler(unittest.TestCase):
    def setUp(self):
        # Use a test database
        self.storage = StorageHandler()
        self.storage.conn = sqlite3.connect(':memory:')
        self.storage.cursor = self.storage.conn.cursor()
        self.storage.create_table()

    def test_add_and_get_notes(self):
        note_id = self.storage.add_note_metadata('Test Note', 'test, note')
        notes = self.storage.get_all_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0][0], note_id)
        self.assertEqual(notes[0][1], 'Test Note')

    def test_delete_note_metadata(self):
        note_id = self.storage.add_note_metadata('Test Note', 'test, note')
        self.storage.delete_note_metadata(note_id)
        notes = self.storage.get_all_notes()
        self.assertEqual(len(notes), 0)

    def test_save_and_load_note_content(self):
        note_id = 1
        content = b'Test Content'
        self.storage.save_note_content(note_id, content)
        loaded_content = self.storage.load_note_content(note_id)
        self.assertEqual(content, loaded_content)
        self.storage.delete_note_content(note_id)
        loaded_content = self.storage.load_note_content(note_id)
        self.assertIsNone(loaded_content)

if __name__ == '__main__':
    unittest.main()
