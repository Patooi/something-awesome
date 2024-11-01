import bcrypt
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def hash_master_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return (hashed, salt)


def compare_master_password(hashed, password, salt):
    new_hash = bcrypt.hashpw(password, salt)
    return new_hash == hashed


def encrypt_password(master_password, password):
    salt = bcrypt.gensalt()

    key_length = 32
    iterations = 10000
    key = hashlib.pbkdf2_hmac(
        "sha256", master_password.encode(), salt, iterations, key_length
    )

    iv = get_random_bytes(12)

    cipher = AES.new(key, AES.MODE_GCM, iv)

    ciphertext, tag = cipher.encrypt_and_digest(password.encode())

    return (ciphertext, salt, tag, iv)


def decrypt_password(iv, salt, tag, ciphertext, master_password):
    key_length = 32
    iterations = 10000

    key = hashlib.pbkdf2_hmac(
        "sha256", master_password.encode(), salt, iterations, key_length
    )

    cipher = AES.new(key, AES.MODE_GCM, iv)

    password = cipher.decrypt_and_verify(ciphertext, tag)

    return password


ciphertext, salt, tag, iv = encrypt_password("master", "mypassword")
password = decrypt_password(iv, salt, tag, ciphertext, "master")
print(password)
