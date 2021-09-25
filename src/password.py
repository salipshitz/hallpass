import os.path
from cryptography.fernet import Fernet

from include import STORAGE_LOCATION


pwd: bytes = b''
fernet: Fernet = None

def load():
    global pwd

    with open(STORAGE_LOCATION + "pwd.txt", 'rb') as f:
        pwd = f.read()


def write(new_pwd: str):
    global pwd
    global fernet

    if fernet is None:
        if os.path.exists(STORAGE_LOCATION + "pwdkey.key"):
            with open(STORAGE_LOCATION + "pwdkey.key", 'rb') as pwdkey:
                key = pwdkey.read()
                fernet = Fernet(key)
        else:
            key = Fernet.generate_key()
            with open(STORAGE_LOCATION + "pwdkey.key", 'wb') as pwdkey:
                pwdkey.write(Fernet.generate_key())
            fernet = Fernet(key)

    pwd = fernet.encrypt(new_pwd.encode('utf-8'))
    with open(STORAGE_LOCATION + "pwd.txt", 'wb') as f:
        f.write(pwd)


def verify(test_pwd: str) -> bool:
    global fernet

    if fernet is None:
        with open(STORAGE_LOCATION + "pwdkey.key", 'rb') as pwdkey:
            key = pwdkey.read()
        fernet = Fernet(key)
    decrypted = fernet.decrypt(pwd).decode('utf-8')
    return test_pwd == decrypted


def isempty() -> bool:
    return pwd == b''
