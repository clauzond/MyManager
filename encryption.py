import hashlib
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
# https://medium.com/quick-code/aes-implementation-in-python-a82f582f51c2


class Password:
    def __init__(self):
        self.cipherstring = None

    def __str__(self):
        return self.cipherstring

    def encrypt(self, password, encryption_key=""):
        password = self.__pad(password)
        key = hashlib.sha256(encryption_key.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(password.encode())
        nonce = cipher.nonce
        self.cipherstring = b64encode(tag + nonce + ciphertext).decode('utf-8')
        return self.cipherstring

    def decrypt(self, encryption_key="", cipherstring=None):
        if cipherstring is not None:
            self.cipherstring = cipherstring
        elif self.cipherstring is None:
            raise AttributeError("Password was not loaded yet")
        cipherbytes = b64decode(self.cipherstring)
        tag = cipherbytes[:16]
        nonce = cipherbytes[16:32]
        ciphertext = cipherbytes[32:]
        key = hashlib.sha256(encryption_key.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        password = cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8")
        return self.__unpad(password)

    def __pad(self, plain_text):
        number_of_bytes_to_pad = AES.block_size - len(plain_text) % AES.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]


# def load(self, file_string=None):
#     if file_string is not None:
#         self.file_string = file_string
#     with open(self.file_string, mode="rb") as file_in:
#         self.hash = file_in.read(-1)

def encrypt_password(password, encryption_key=""):
    return Password().encrypt(password, encryption_key)


def decrypt_password(cipherstring="", encryption_key=""):
    return Password().decrypt(encryption_key, cipherstring)


def verify_hash(plain_text, _hash):
    return _hash == hash_text(plain_text)


def hash_text(plain_text):
    return hashlib.sha256(plain_text.encode()).digest()


def encrypt_dictionnary(dic, encryption_key=""):
    for key in dic:
        dic[key] = encrypt_password(dic[key], encryption_key)
    return dic

def decrypt_dictionnary(dic, encryption_key=""):
    for key in dic:
        dic[key] = decrypt_password(dic[key], encryption_key)
    return dic

if __name__ == "__main__":
    ...