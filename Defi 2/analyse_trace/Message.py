from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from scapy.all import *

def decrypt_aes_cbc(key, iv, ciphertext):
    """Permet de décrypter un message chiffré avec AES en mode CBC

    Args:
        key (String): la clé de chiffrement
        iv (String): le vercteur d'initialisation
        ciphertext (String): le message sans le vecteur d'initialisation

    Returns:
        String: Le message decrypté
    """
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message

def remove_iv_and_unpad(payload):
    """Permet de retirer le vecteur d'initialisation et de retirer le padding du message

    Args:
        payload (String): le contenu du packet

    Returns:
        String: un tuble contenant le vecteur d'initialisation et le message sans le padding
    """
    iv = payload[:16]
    encrypted_message = payload[16:]
    unpadded_message = encrypted_message
    return iv, unpadded_message

def decode_packet(packet, key64bits):
    """Permet de décoder un packet UDP et de le décrypter avec AES en mode CBC avec la clé key64bits et de le retourner en utf-8 si le port est 9999

    Args:
        packet (packet): le packet à décoder
        key64bits (String): la clé de 64 bits à utiliser pour le décryptage

    Returns:
        String: Le message décrypté en utf-8
    """
    key = int(key64bits, 2).to_bytes((len(key64bits) + 7) // 8, byteorder='big')
    key = key*4
    if packet.haslayer("UDP") and packet["UDP"].dport == 9999:
            payload = bytes(packet["UDP"].payload)
            iv, encrypted_message = remove_iv_and_unpad(payload)
            decrypted_message = decrypt_aes_cbc(key, iv, encrypted_message)
            decoded_message = decrypted_message.decode("utf-8")
            return decoded_message

# on récupère les packets
packets = rdpcap('./Defi 2/analyse_trace/trace_sae.cap')
# on récupère la clé de 64 bits qui été dans l'image roussignol2
key64bits = '1110011101101101001100010011111110010010101110011001000001001100'

for packetline in packets:
    message = decode_packet(packetline, key64bits)
    if message:
        print(message)
        continue