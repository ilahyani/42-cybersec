import argparse
import hmac
import hashlib
import os
import base64
from cryptography.fernet import Fernet

FERNET_KEY = os.environ.get("FERNET_KEY")

def ft_otp(args):
    if args.g:
        try:
            with open(args.g, 'r') as f:
                key = f.read().strip()
                if len(key) < 64:
                    exit(print("Key must be atleast 64 characters long"))
        except IOError:
            exit(print(f"Error: Could not read file {args.g}"))
        
        try:
            key_bytes = bytes.fromhex(key)
            cipher = Fernet(FERNET_KEY)
            encrypted_data = cipher.encrypt(key_bytes)
        except ValueError as e:
            exit(print(f"Invalid hexadecimal key: {e}"))
        
        try:
            with open('ft_otp.key', 'wb') as file:
                file.write(encrypted_data)
            print("Key was successfully saved in ft_otp.key")
        except Exception as e:
            exit(print(f"Failed to save key: {e}"))

    elif args.k:
        try:
            with open(args.k, 'rb') as file:
                encrypted_data = file.read()
                cipher = Fernet(FERNET_KEY)
                try:
                    key = cipher.decrypt(encrypted_data)
                except Exception as e:
                    exit(print("Invalid File"))
        except IOError:
            exit(print(f"Could not read file {args.k}"))

        try:
            with open('counter', 'r+') as file:
                content = file.read()
                counter = int(content) if content else 0
                file.seek(0)
                file.write(str(counter + 1))
        except FileNotFoundError:
            with open('counter', 'w') as file:
                counter = 0
                file.write('1')
        
        print('Hex secret:', key.hex())
        print('Counter:', counter)
        counter_bytes = counter.to_bytes(8, byteorder='big')

        hmac_digest = hmac.new(key, counter_bytes, hashlib.sha1).digest()

        offset = hmac_digest[-1] & 0x0f
        code_bytes = hmac_digest[offset:offset+4]
        code = int.from_bytes(code_bytes, byteorder='big') & 0x7fffffff
        otp = code % 10**6

        print(f"{otp:06d}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
        aaaaaaaa OTP?
    """)
    parser.add_argument('-g',type=str, help='Initial Password, a hexadecimal key of at least 64 characters')
    parser.add_argument('-k', type=str, help='Key to base the TOTP on')
    
    args = parser.parse_args()
    
    if not args.g and not args.k:
        exit(0)
    
    ft_otp(args)
