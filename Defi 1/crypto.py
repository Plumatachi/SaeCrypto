mot11 ="BDQE PG OTQYUZ EQ OMOTQ GZ FDQEAD"
mot12 ="MOODAOTQ M GZ MDNDQ FAGF DQOAGHQDF P'AD"
mot13 ="ZQ ZQSXUSQ BME XM VQGZQ BAGOQ RQGUXXG"
mot14 ="SDMZP QEF EAZ EQODQF YMXSDQ EM FMUXXQ YQZGQ"
mot15 ="DAZPQE QF OAXADQQE EAZF XQE NMUQE CG'UX BADFQ"
mot16 ="MZUEQQE QF EGODQQE, XQGDE EMHQGDE EAZF RADFQE."
mot17 ="YMUE MFFQZFUAZ M ZQ BME XQE ODACGQD,"
mot18 ="YQYQ EU XM RMUY FUDMUXXQ FQE QZFDMUXXQE,"
mot19 ="QZ MGOGZ OME FG ZQ PAUE EGOOAYNQD"
mot_C_cesar = mot11+"\n"+mot12+"\n"+mot13+"\n"+mot14+"\n"+mot15+"\n"+mot16+"\n"+mot17+"\n"+mot18+"\n"+mot19

def decrypt_cesar(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char.isalpha():
            shifted = ord(char) - shift
            if shifted < ord('A'):
                shifted += 26
            decrypted_char = chr(shifted)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

print("Décriptage en utilisant le chiffre de César")
print(decrypt_cesar(mot_C_cesar,12))
print("\nLe mot caché a retrouver est PANGRAMME\n\n")

mot21 = "AE IOW ZQBLNR WASIXQ WJR YKJ KGYUJAGY UU OXSLN TXRCUQYM"
mot22 = "IY IRCTQ HPNF RR RQBIIIGOFN XQ WTCEKK DQ OIH MHXDUDQW BAYNVUDQYM"
mot23 = "NR MRRPQD SU CXVMUQV HOHLWLQ CYT LRY GRQYMTRRY RPBMVXTVUES"
mot24 = "QF EXNFO UEHAMAEM RV MQEWPGR IRCTQ HTREOVRQ XE HUOYKIFGXXOA"
motall = mot21+"\n"+mot22+"\n"+mot23+"\n"+mot24
cle = "PANGRAMME"

def decrypt_vigenere(message,cle):
    # effectue le decalage en fonction de la cle sur les caracteres de message
    n = 0
    chiffre=''
    for c in message:
        if c.isalpha():
            k = ord(cle[n%len(cle)])-65
            chiffre += decrypt_cesar(c,k)
            n+=1
        else:
            chiffre += c
    return chiffre

print("Décriptage en utilisant le chiffre de Vigenere\n")
print(decrypt_vigenere(motall,cle))
print("\n\n")

indice = "LE VIF ZEPHYR JUBILE SUR LES KUMQUATS DU CLOWN GRACIEUX\nIL CACHE DANS LA REPETITION LE SECRET DE CES MURMURES MALHEUREUX\nNE GARDEZ DU PREMIER SOUFFLE QUE LES PREMIERES APPARITIONS\nET AINSI DEVOILEZ LE MESSAGE CACHE DERRIERE LA SUBSTITUTION"
mes = "EALOK, OKCT LOFX PLPSF! UF VKIF L ZKCASYA FTD: FUYXFEFDH"

def liste_mot_uni(message):
    l=[]
    for let in message:
        if let not in l and let.isalpha():
            l.append(let)
    return l

def create_dico(message):
    dico={}
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    liste_lettre = liste_mot_uni(message)
    for i in range(len(alphabet)):
        dico[liste_lettre[i]] = alphabet[i]
    return dico

def substitution(message,indice):
    vrai = ''
    dico = create_dico(indice)
    for c in message:
        if c.isalpha():
            if c in dico.keys():
                let = dico[c]
                vrai+=let
            else:
                vrai+=c
        else:
            vrai+=c
    return vrai

print(substitution(mes,indice))