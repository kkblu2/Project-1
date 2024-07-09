from cryptography.fernet import Fernet
import os
import sys
import getpass
import hashlib

class FileEncryptor:
    def __init__(self):
        self.key_file = "Secret.key"
        self.salt_file = "Salt.bin"

    def generate_key(self, password):
        salt = os.urandom(16)
        with open(self.salt_file, "wb") as salt_file:
            salt_file.write(salt)
        
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)

    def load_key(self, password):
        with open(self.salt_file, "rb") as salt_file:
            salt = salt_file.read()
        
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return key

    def encrypt_file(self, filename, key):
        f = Fernet(key)
        with open(filename, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        
        encrypted_filename = f"encrypted_{filename}"
        with open(encrypted_filename, "wb") as file:
            file.write(encrypted_data)
        
        return encrypted_filename

    def decrypt_file(self, filename, key):
        f = Fernet(key)
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        
        try:
            decrypted_data = f.decrypt(encrypted_data)
        except:
            print("Decryption failed. Invalid key or corrupted file.")
            return None

        decrypted_filename = filename.replace("encrypted_", "decrypted_")
        with open(decrypted_filename, "wb") as file:
            file.write(decrypted_data)
        
        return decrypted_filename

    def encrypt_folder(self, folder_path, key):
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    encrypted_file = self.encrypt_file(file_path, key)
                    print(f"Encrypted: {file_path} -> {encrypted_file}")
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to encrypt {file_path}: {str(e)}")

    def decrypt_folder(self, folder_path, key):
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.startswith("encrypted_"):
                    file_path = os.path.join(root, file)
                    try:
                        decrypted_file = self.decrypt_file(file_path, key)
                        if decrypted_file:
                            print(f"Decrypted: {file_path} -> {decrypted_file}")
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Failed to decrypt {file_path}: {str(e)}")

def main():
    encryptor = FileEncryptor()

    while True:
        print("\n--- File Encryption and Decryption Tool ---")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Encrypt a folder")
        print("4. Decrypt a folder")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            filename = input("Enter the file name to encrypt: ")
            if os.path.exists(filename):
                password = getpass.getpass("Enter encryption password: ")
                encryptor.generate_key(password)
                key = encryptor.load_key(password)
                encrypted_file = encryptor.encrypt_file(filename, key)
                print(f"File encrypted successfully: {encrypted_file}")
            else:
                print(f"File '{filename}' not found.")

        elif choice == '2':
            filename = input("Enter the file name to decrypt: ")
            if os.path.exists(filename):
                password = getpass.getpass("Enter decryption password: ")
                key = encryptor.load_key(password)
                decrypted_file = encryptor.decrypt_file(filename, key)
                if decrypted_file:
                    print(f"File decrypted successfully: {decrypted_file}")
            else:
                print(f"File '{filename}' not found.")

        elif choice == '3':
            folder_path = input("Enter the folder path to encrypt: ")
            if os.path.isdir(folder_path):
                password = getpass.getpass("Enter encryption password: ")
                encryptor.generate_key(password)
                key = encryptor.load_key(password)
                encryptor.encrypt_folder(folder_path, key)
                print("Folder encryption completed.")
            else:
                print(f"Folder '{folder_path}' not found.")

        elif choice == '4':
            folder_path = input("Enter the folder path to decrypt: ")
            if os.path.isdir(folder_path):
                password = getpass.getpass("Enter decryption password: ")
                key = encryptor.load_key(password)
                encryptor.decrypt_folder(folder_path, key)
                print("Folder decryption completed.")
            else:
                print(f"Folder '{folder_path}' not found.")

        elif choice == '5':
            print("Thank you for using the File Encryption and Decryption Tool. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
