#!/usr/bin/python3
#
# Author: Joao H de A Franco (jhafranco@acm.org)
#
# Description: Simplified DES implementation in Python 3
#
# Date: 2012-02-10
#
# License: Attribution-NonCommercial-ShareAlike 3.0 Unported
#          (CC BY-NC-SA 3.0)
#===========================================================
import random
from sys import exit
from time import time
 
KeyLength = 10
SubKeyLength = 8
DataLength = 8
FLength = 4
 
# Tables for initial and final permutations (b1, b2, b3, ... b8)
IPtable = (2, 6, 3, 1, 4, 8, 5, 7)
FPtable = (4, 1, 3, 5, 7, 2, 8, 6)
 
# Tables for subkey generation (k1, k2, k3, ... k10)
P10table = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8table = (6, 3, 7, 4, 8, 5, 10, 9)
 
# Tables for the fk function
EPtable = (4, 1, 2, 3, 2, 3, 4, 1)
S0table = (1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 3, 2)
S1table = (0, 1, 2, 3, 2, 0, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3)
P4table = (2, 4, 3, 1)
 
def perm(inputByte, permTable):
    """Permute input byte according to permutation table"""
    outputByte = 0
    for index, elem in enumerate(permTable):
        if index >= elem:
            outputByte |= (inputByte & (128 >> (elem - 1))) >> (index - (elem - 1))
        else:
            outputByte |= (inputByte & (128 >> (elem - 1))) << ((elem - 1) - index)
    return outputByte
 
def ip(inputByte):
    """Perform the initial permutation on data"""
    return perm(inputByte, IPtable)
 
def fp(inputByte):
    """Perform the final permutation on data"""
    return perm(inputByte, FPtable)
 
def swapNibbles(inputByte):
    """Swap the two nibbles of data"""
    return (inputByte << 4 | inputByte >> 4) & 0xff
 
def keyGen(key):
    """Generate the two required subkeys"""
    def leftShift(keyBitList):
        """Perform a circular left shift on the first and second five bits"""
        shiftedKey = [None] * KeyLength
        shiftedKey[0:9] = keyBitList[1:10]
        shiftedKey[4] = keyBitList[0]
        shiftedKey[9] = keyBitList[5]
        return shiftedKey
 
    # Converts input key (integer) into a list of binary digits
    keyList = [(key & 1 << i) >> i for i in reversed(range(KeyLength))]
    permKeyList = [None] * KeyLength
    for index, elem in enumerate(P10table):
        permKeyList[index] = keyList[elem - 1]
    shiftedOnceKey = leftShift(permKeyList)
    shiftedTwiceKey = leftShift(leftShift(shiftedOnceKey))
    subKey1 = subKey2 = 0
    for index, elem in enumerate(P8table):
        subKey1 += (128 >> index) * shiftedOnceKey[elem - 1]
        subKey2 += (128 >> index) * shiftedTwiceKey[elem - 1]
    return (subKey1, subKey2)
 
def fk(subKey, inputData):
    """Apply Feistel function on data with given subkey"""
    def F(sKey, rightNibble):
        aux = sKey ^ perm(swapNibbles(rightNibble), EPtable)
        index1 = ((aux & 0x80) >> 4) + ((aux & 0x40) >> 5) + \
                 ((aux & 0x20) >> 5) + ((aux & 0x10) >> 2)
        index2 = ((aux & 0x08) >> 0) + ((aux & 0x04) >> 1) + \
                 ((aux & 0x02) >> 1) + ((aux & 0x01) << 2)
        sboxOutputs = swapNibbles((S0table[index1] << 2) + S1table[index2])
        return perm(sboxOutputs, P4table)
 
    leftNibble, rightNibble = inputData & 0xf0, inputData & 0x0f
    return (leftNibble ^ F(subKey, rightNibble)) | rightNibble
 
def encrypt(key, plaintext):
    """Encrypt plaintext with given key"""
    data = fk(keyGen(key)[0], ip(plaintext))
    return fp(fk(keyGen(key)[1], swapNibbles(data)))

def encrypt_list(key, plaintext):
    """Encrypt plaintext with given key

    Args:
        key (binary): Un nombre binair de 10 bits
        plaintext (str): Le message à chiffrer

    Returns:
        list: la liste des caractères chiffrés
    """
    data = []
    plaintext_int_list = [ord(char) for char in plaintext_str]
    for i in range(len(plaintext)):
        data.append(encrypt(key, plaintext_int_list[i]))
    return data

def encrypt_list_double(key, key2, plaintext):
    """Encrypt plaintext with given key

    Args:
        key (binary): Un nombre binair de 10 bits
        plaintext (str): Le message à chiffrer

    Returns:
        list: la liste des caractères chiffrés
    """
    data = []
    plaintext_int_list = [ord(char) for char in plaintext_str]
    for i in range(len(plaintext)):
        data.append(encrypt(key2, encrypt(key, plaintext_int_list[i])))
    return data
 
def decrypt(key, ciphertext):
    """Decrypt ciphertext with given key"""
    data = fk(keyGen(key)[1], ip(ciphertext))
    return fp(fk(keyGen(key)[0], swapNibbles(data)))

def decrypt_list(key, ciphertext):
    """Decrypt ciphertext with given key

    Args:
        key (binary): Un nombre binair de 10 bits
        ciphertext (list): La liste des caractères chiffrés

    Returns:
        str: Le message déchiffré
    """
    data = []
    for i in range(len(ciphertext)):
        data.append(decrypt(key, ciphertext[i]))
    return data

def decrypt_list_double(key, key2, ciphertext):
    """Decrypt ciphertext with given key

    Args:
        key (binary): Un nombre binair de 10 bits
        ciphertext (list): La liste des caractères chiffrés

    Returns:
        str: Le message déchiffré
    """
    data = []
    for i in range(len(ciphertext)):
        data.append(decrypt(key, decrypt(key2, ciphertext[i])))
    return data

def text_to_binary_list(input_string):
    """Convert a string to a list of binary numbers"""
    return [ord(char) for char in input_string]

def binary_list_to_text(binary_list):
    """Convert a list of binary numbers to a string"""
    return ''.join(chr(char) for char in binary_list)

if __name__ == '__main__':
    # Test vectors described in "Simplified DES (SDES)"
    # (http://www2.kinneret.ac.il/mjmay/ise328/328-Assignment1-SDES.pdf)
 
    try:
        assert encrypt(0b0000000000, 0b10101010) == 0b00010001
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b0000000000, 0b10101010), "Expected: ", 0b00010001)
        exit(1)
    try:
        assert encrypt(0b1110001110, 0b10101010) == 0b11001010
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1110001110, 0b10101010), "Expected: ", 0b11001010)
        exit(1)
    try:
        assert encrypt(0b1110001110, 0b01010101) == 0b01110000
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1110001110, 0b01010101), "Expected: ", 0b01110000)
        exit(1)
    try:
        assert encrypt(0b1111111111, 0b10101010) == 0b00000100
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1111111111, 0b10101010), "Expected: ", 0b00000100)
        exit(1)
 
def cassage_brutal_simple(message_clair, message_chiffre):
    for i in range(2**10):
        trouvee = all(decrypt(i, mc) == mcl for mc, mcl in zip(message_chiffre, message_clair))

        if trouvee == True:
            return i
    return None

def cassage_brutal(message_clair, message_chiffre):
    for i in range(2**10):
        for j in range(2**10):
            trouvee = all(decrypt(j, decrypt(i, mc)) == mcl for mc, mcl in zip(message_chiffre, message_clair))
            if trouvee:
                return i, j
                
    return None


def cassage_inteligent(message_chiffre, message_clair):
    for i in range(2**10):
        for j in range(2**10):
            sub_chiffre = message_chiffre[:3]
            sub_clair = message_clair[:3]
            trouvee = all(decrypt(j, mc) == encrypt(i,mcl) for mc, mcl in zip(sub_chiffre, sub_clair))
            if trouvee:
                return i, j
    return None




# Cryptage avec 2 clés
for i in range(1):
    # Convertir la chaîne en une liste d'entiers
    plaintext_str = "Hello, world!"
    key = 0b1010101010 # 682
    key2 = 0b1110001110 # 910
    key3 = 0b0000000011 # 3


    # Chiffrer
    ciphertext = encrypt_list(key, plaintext_str)
    print("Message chiffré a une clé:", ciphertext)

    ciphertext_double = encrypt_list_double(key, key2, plaintext_str)
    print("Message chiffré a deux clés:", ciphertext_double)

    # Déchiffrer
    plaintext_result = binary_list_to_text(decrypt_list(key, ciphertext))
    print("Message déchiffré:", plaintext_result)

    plaintext_result_double = binary_list_to_text(decrypt_list_double(key, key2, ciphertext_double))
    print("Message déchiffré avec deux clés:", plaintext_result_double)

    # Attaque par force brute
    print("Attaque par force brute pour 1 cryptage...")
    print(cassage_brutal_simple(text_to_binary_list(plaintext_str), ciphertext))
    print("Attaque par force brute brutal pour 2 cryptages...")
    time_start_brutal = time()
    print(cassage_brutal(text_to_binary_list(plaintext_str), ciphertext_double))
    time_end_brutal = time()
    print("Temps d'exécution de la force brute brutal: ", time_end_brutal - time_start_brutal)
    print("Attaque par force brute inteligente pour 2 cryptages...")
    time_start_inteligent = time()
    keyres, keyres2 = cassage_inteligent(ciphertext_double, text_to_binary_list(plaintext_str))
    time_end_inteligent = time()
    print("Message déchiffré par cassage inteligent:", binary_list_to_text(decrypt_list_double(keyres, keyres2, ciphertext_double)))
    print("Temps d'exécution de la force brute inteligente: ", time_end_inteligent - time_start_inteligent)