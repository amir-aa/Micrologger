from Crypto.Cipher import AES, ARC4
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def rc4_encrypt(message, key):
    cipher = ARC4.new(key)
    ciphertext = cipher.encrypt(message.encode())
    return ciphertext

def rc4_decrypt(ciphertext, key):
    cipher = ARC4.new(key)
    decrypted_message = cipher.decrypt(ciphertext)
    return decrypted_message.decode()



def aes_encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext, cipher.iv

def aes_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Example usage:
key_aes = get_random_bytes(32)  # 128-bit key
message = "Hello, AES!"

ciphertext_aes, iv_aes = aes_encrypt(message, key_aes)
decrypted_message_aes = aes_decrypt(ciphertext_aes, key_aes, iv_aes)

print(f"Original Message: {message}")
print(f"Ciphertext (AES): {ciphertext_aes}")
print(f"Decrypted Message (AES): {decrypted_message_aes}")


# Example usage:
key_rc4 = get_random_bytes(16)  # 128-bit key
message = "Hello, RC4!"

ciphertext_rc4 = rc4_encrypt(message, key_rc4)
decrypted_message_rc4 = rc4_decrypt(ciphertext_rc4, key_rc4)

print(f"Original Message: {message}")
print(f"Ciphertext (RC4): {ciphertext_rc4.hex()}")
print(f"Decrypted Message (RC4): {decrypted_message_rc4}")
