import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64encode, b64decode

# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
# https://medium.com/quick-code/aes-implementation-in-python-a82f582f51c2


class AESCipher():
    def __init__(self, file_string=None):
        self.block_size = AES.block_size
        self.ciphertext = None
        self.tag = None
        self.nonce = None
        self.file_string = file_string

    def encrypt(self, password, encryption_key=""):
        password = self.__pad(password)
        key = hashlib.sha256(encryption_key.encode()).digest()
        self.key = key
        cipher = AES.new(key, AES.MODE_EAX)
        self.ciphertext, self.tag = cipher.encrypt_and_digest(password.encode())
        self.nonce = cipher.nonce
        return (self.ciphertext, self.tag, self.nonce)

    def decrypt(self, encryption_key=""):
        if self.ciphertext is None:
            raise AttributeError("Password was not loaded yet")
        key = hashlib.sha256(encryption_key.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX, self.nonce)
        password = cipher.decrypt_and_verify(self.ciphertext, self.tag).decode("utf-8")
        return self.__unpad(password)

    def save(self, file_string=None):
        if self.ciphertext is None:
            raise AttributeError("Password was not encrypted yet")
        elif file_string is not None:
            self.file_string = file_string
        with open(self.file_string, mode="wb") as file_out:
            [file_out.write(x) for x in (self.tag, self.ciphertext, self.nonce)]

    def load(self, file_string=None):
        if file_string is not None:
            self.file_string = file_string
        with open(self.file_string, mode="rb") as file_in:
            self.tag, self.ciphertext, self.nonce = [file_in.read(x) for x in (16, 32, 16)]

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]

class SHA256Hash():
    def __init__(self, plain_text, file_string=None):
        self.hash = self.__hash(plain_text)
        self.file_string = file_string
        
    def check_text(self, plain_text):
        return self.hash == self.__hash(plain_text)

    def save(self, file_string=None):
        if file_string is not None:
            self.file_string = file_string
        with open(self.file_string, mode="wb") as file_out:
            file_out.write(self.hash)

    def load(self, file_string=None):
        if file_string is not None:
            self.file_string = file_string
        with open(self.file_string, mode="rb") as file_in:
            self.hash = file_in.read(-1)

    def __hash(self, plain_text):
        return hashlib.sha256(plain_text.encode()).digest()

def test():
    FILE = "data/account/mypass.bin"

    mypass = AESCipher(FILE)
    mypass.encrypt("thisismypassword!", "thisismyprotectionpassword")
    mypass.save()

if __name__ == "__main__":
    test()
