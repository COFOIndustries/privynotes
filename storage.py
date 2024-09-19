import sqlite3
import os

class StorageHandler:
    def __init__(self):
        self.conn = sqlite3.connect('notes.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        if not os.path.exists('notes'):
            os.makedirs('notes')

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                tags TEXT
            )
        ''')
        self.conn.commit()

    def add_note_metadata(self, title, tags):
        self.cursor.execute('''
            INSERT INTO notes (title, tags) VALUES (?, ?)
        ''', (title, tags))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_note_metadata(self, note_id, title, tags):
        self.cursor.execute('''
            UPDATE notes SET title = ?, tags = ? WHERE id = ?
        ''', (title, tags, note_id))
        self.conn.commit()

    def delete_note_metadata(self, note_id):
        self.cursor.execute('''
            DELETE FROM notes WHERE id = ?
        ''', (note_id,))
        self.conn.commit()

    def get_all_notes(self):
        self.cursor.execute('SELECT id, title, tags FROM notes')
        return self.cursor.fetchall()

    def save_note_content(self, note_id, encrypted_content):
        with open(f'notes/{note_id}.note', 'wb') as f:
            f.write(encrypted_content)

    def load_note_content(self, note_id):
        try:
            with open(f'notes/{note_id}.note', 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def delete_note_content(self, note_id):
        os.remove(f'notes/{note_id}.note')
