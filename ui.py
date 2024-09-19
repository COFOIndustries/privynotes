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
            elif command == 'search':
                self.search_notes()
            elif command.startswith('export'):
                parts = command.split()
                if len(parts) == 2 and parts[1].isdigit():
                    self.export_note_content(int(parts[1]))
                else:
                    print("Usage: export <note_id>")
            elif command == 'reset_password':
                self.reset_password()
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

    def search_notes(self):
        search_term = input("Enter a search term (title, tags, or content): ").strip()
        notes = self.storage.get_all_notes()

        for note_id, title, tags in notes:
            content = self.encryption.decrypt(self.storage.load_note_content(note_id))
            if search_term.lower() in title.lower() or search_term.lower() in tags.lower() or search_term.lower() in content.lower():
                print(f"Found in Note ID: {note_id}, Title: {title}, Tags: {tags}")

    def export_note_content(self, note_id):
        encrypted_content = self.storage.load_note_content(note_id)
        if not encrypted_content:
            print("Note not found.")
            return
        content = self.encryption.decrypt(encrypted_content)
        export_format = input("Export as (txt/md): ").strip().lower()

        if export_format not in ['txt', 'md']:
            print("Invalid format.")
            return

        filename = f'note_{note_id}.{export_format}'
        with open(filename, 'w') as f:
            f.write(content)

        print(f"Note exported as {filename}.")

    def reset_password(self):
        old_password = input("Enter your current master password: ").strip()
        old_hash = self.encryption.get_hash(old_password)

        with open('master.hash', 'r') as f:
            saved_hash = f.read()

        if old_hash != saved_hash:
            print("Incorrect password.")
            return

        # Set a new password
        new_password = input("Set your new master password: ").strip()
        confirm_password = input("Confirm your new master password: ").strip()

        if new_password != confirm_password:
            print("Passwords do not match.")
            return

        print(f"Password strength: {self.check_password_strength(new_password)}")
        new_hash = self.encryption.get_hash(new_password)

        with open('master.hash', 'w') as f:
            f.write(new_hash)

        print("Password reset successfully.")

    def check_password_strength(self, password):
        if len(password) < 8:
            return "Weak"
        if any(char.isdigit() for char in password) and any(char.isalpha() for char in password):
            return "Medium"
        if len(password) >= 12 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password):
            return "Strong"
        return "Weak"

    def print_help(self):
        print("""
Available Commands:
  new                Create a new note
  edit <note_id>     Edit an existing note
  delete <note_id>   Delete a note
  list               View a list of saved notes
  search             Search notes by title, tags, or content
  export <note_id>   Export a note as txt or md
  reset_password     Reset your master password
  help               Show this help message
  exit               Exit the application
""")
