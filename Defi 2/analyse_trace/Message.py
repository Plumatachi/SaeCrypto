from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from scapy.all import *

def decrypt_aes_cbc(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message

def remove_iv_and_unpad(payload):
    # Assuming the IV is already present in the payload
    iv = payload[:16]
    encrypted_message = payload[16:]
    unpadded_message = encrypted_message
    return iv, unpadded_message

def decode_packet(packet, key64bits):
    key = int(key64bits, 2).to_bytes((len(key64bits) + 7) // 8, byteorder='big')
    key = key*4
    if packet.haslayer("UDP") and packet["UDP"].dport == 9999:
            payload = bytes(packet["UDP"].payload)
            iv, encrypted_message = remove_iv_and_unpad(payload)
            decrypted_message = decrypt_aes_cbc(key, iv, encrypted_message)
            decoded_message = decrypted_message.decode("utf-8")
            return decoded_message


packets = rdpcap('./Defi 2/analyse_trace/trace_sae.cap')
key64bits = '1110011101101101001100010011111110010010101110011001000001001100'

for packetline in packets:
    message = decode_packet(packetline, key64bits)
    if message:
        print(message)
        continue