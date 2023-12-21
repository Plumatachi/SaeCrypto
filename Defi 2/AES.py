import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
aled = open("./Defi 2/arsene_lupin_extrait.txt", "r")
text = aled.read()

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))

file_out = open("./Defi 2/encrypted.bin", "wb")
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
file_out.close()

file_in = open("./Defi 2/encrypted.bin", "rb")
nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
file_in.close()

# let's assume that the key is somehow available again
time1 = time.time()
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)
print(f"{time.time()-time1} seconds")
