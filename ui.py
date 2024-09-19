class CommandLineInterface:
    def __init__(self, encryption_handler, storage_handler):
        self.encryption = encryption_handler
        self.storage = storage_handler

    def run(self):
        print("PrivyNotes CLI. Type 'help' for a list of commands.")
        while True:
            command = input("> ").strip()
            if command == 'new':
                self.create_note()
            elif command.startswith('edit'):
                parts = command.split()
                if len(parts) == 2 and parts[1].isdigit():
                    self.edit_note(int(parts[1]))
                else:
                    print("Usage: edit <note_id>")
            elif command.startswith('delete'):
                parts = command.split()
                if len(parts) == 2 and parts[1].isdigit():
                    self.delete_note(int(parts[1]))
                else:
                    print("Usage: delete <note_id>")
            elif command == 'list':
                self.list_notes()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                print("Exiting PrivyNotes.")
                break
            else:
                print("Unknown command. Type 'help' for a list of commands.")

    def create_note(self):
        title = input("Title: ").strip()
        tags = input("Tags (comma-separated): ").strip()
        print("Enter your note content. Type 'END' on a new line to finish.")
        lines = []
        while True:
            line = input()
            if line == 'END':
                break
            lines.append(line)
        content = '\n'.join(lines)
        encrypted_content = self.encryption.encrypt(content)
        note_id = self.storage.add_note_metadata(title, tags)
        self.storage.save_note_content(note_id, encrypted_content)
        print(f"Note '{title}' saved with ID {note_id}.")

    def edit_note(self, note_id):
        metadata = self.storage.cursor.execute(
            'SELECT title, tags FROM notes WHERE id = ?', (note_id,)
        ).fetchone()
        if not metadata:
            print("Note not found.")
            return
        title, tags = metadata
        encrypted_content = self.storage.load_note_content(note_id)
        if not encrypted_content:
            print("Note content not found.")
            return
        content = self.encryption.decrypt(encrypted_content)
        print(f"Editing Note ID {note_id}. Leave field blank to keep current value.")
        new_title = input(f"Title [{title}]: ").strip() or title
        new_tags = input(f"Tags [{tags}]: ").strip() or tags
        print("Enter your note content. Type 'END' on a new line to finish.")
        lines = []
        while True:
            line = input()
            if line == 'END':
                break
            lines.append(line)
        new_content = '\n'.join(lines) or content
        encrypted_content = self.encryption.encrypt(new_content)
        self.storage.update_note_metadata(note_id, new_title, new_tags)
        self.storage.save_note_content(note_id, encrypted_content)
        print(f"Note ID {note_id} updated.")

    def delete_note(self, note_id):
        confirm = input(f"Are you sure you want to delete note ID {note_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            self.storage.delete_note_metadata(note_id)
            self.storage.delete_note_content(note_id)
            print(f"Note ID {note_id} deleted.")
        else:
            print("Delete operation cancelled.")

    def list_notes(self):
        notes = self.storage.get_all_notes()
        if not notes:
            print("No notes found.")
            return
        print("Saved Notes:")
        for note in notes:
            note_id, title, tags = note
            print(f"ID: {note_id}, Title: {title}, Tags: {tags}")

    def print_help(self):
        print("""
Available Commands:
  new                Create a new note
  edit <note_id>     Edit an existing note
  delete <note_id>   Delete a note
  list               View a list of saved notes
  help               Show this help message
  exit               Exit the application
""")
