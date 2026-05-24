from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


BLOCK_SIZE = AES.block_size


def derive_key(password: str) -> bytes:
    hash_obj = SHA256.new()
    hash_obj.update(password.encode("utf-8"))
    return hash_obj.digest()


def encrypt_ecb(data: bytes, password: str) -> bytes:
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(data, BLOCK_SIZE))


def decrypt_ecb(encrypted_data: bytes, password: str) -> bytes:
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(encrypted_data), BLOCK_SIZE)


def encrypt_cbc(data: bytes, password: str) -> tuple[bytes, bytes]:
    key = derive_key(password)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, BLOCK_SIZE))
    return encrypted_data, iv


def decrypt_cbc(encrypted_data: bytes, password: str, iv: bytes) -> bytes:
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data), BLOCK_SIZE)