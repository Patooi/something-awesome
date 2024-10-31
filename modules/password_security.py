import bcrypt
import hashlib
from Crypto.Cipher import AES


def hash_master_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return (hashed, salt)


def encrypt_password(master_password, password):
    salt = bcrypt.gensalt()

    key_length = 32
    iterations = 10000
    key = hashlib.pbkdf2_hmac(
        "sha256", master_password.encode("utf-8"), salt, iterations, key_length
    )

    cipher = AES.new(key, AES.MODE_EAX)
