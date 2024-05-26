from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome import Random
import base64
import hashlib
from Cryptodome.Util.Padding import unpad
import base64
from werkzeug.datastructures import FileStorage
import cv2
import numpy as np

def encrypt(data, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(data.encode('utf-8'), AES.block_size)  # Encode data and pad it
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.urlsafe_b64encode(iv + cipher.encrypt(raw))




def decrypt(encrypted_data, password):
    try:
        private_key = hashlib.sha256(password.encode("utf-8")).digest()
        encrypted_data = base64.urlsafe_b64decode(encrypted_data)
        iv = encrypted_data[:AES.block_size]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        re=1
        return re



