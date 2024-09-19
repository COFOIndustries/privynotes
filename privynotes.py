#PrivyTools Made by CofoIndustries. --v 1.1
import getpass
import hashlib
import os

from encryption import EncryptionHandler
from storage import StorageHandler
from ui import CommandLineInterface

def main():
    # Initialize storage and encryption handlers
    storage = StorageHandler()
    encryption = EncryptionHandler()
    
    # Check if master password is set
    if not os.path.exists('master.hash'):
        print("Welcome to PrivyNotes!")
        master_password = getpass.getpass("Set your master password: ")
        confirm_password = getpass.getpass("Confirm your master password: ")
        
        if master_password != confirm_password:
            print("Passwords do not match. Exiting.")
            return
        
        # Hash and save the master password hash
        master_hash = hashlib.sha256(master_password.encode()).hexdigest()
        with open('master.hash', 'w') as f:
            f.write(master_hash)
    else:
        master_password = getpass.getpass("Enter your master password: ")
        master_hash = hashlib.sha256(master_password.encode()).hexdigest()
        with open('master.hash', 'r') as f:
            saved_hash = f.read()
        if master_hash != saved_hash:
            print("Incorrect master password. Exiting.")
            return
    
    # Initialize encryption with the master password
    encryption.set_key(master_password)
#FailSafe passwd reset
    def reset_password():
    # Get the old password and verify it
    old_password = getpass.getpass("Enter your current master password: ")
    old_hash = hashlib.sha256(old_password.encode()).hexdigest()
    
    with open('master.hash', 'r') as f:
        saved_hash = f.read()
        
    if old_hash != saved_hash:
        print("Incorrect password.")
        return
    
    # Set a new password
    new_password = getpass.getpass("Set your new master password: ")
    confirm_password = getpass.getpass("Confirm your new master password: ")
    
    if new_password != confirm_password:
        print("Passwords do not match.")
        return
    
    new_hash = hashlib.sha256(new_password.encode()).hexdigest()
    with open('master.hash', 'w') as f:
        f.write(new_hash)
    
    print("Password reset successfully.")
    
    # Initialize the UI
    cli = CommandLineInterface(encryption, storage)
    cli.run()

if __name__ == "__main__":
    main()
