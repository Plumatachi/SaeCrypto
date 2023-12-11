# Analyse de trace réseau - SAE3.04 Crypto

Cette archive contient une trace d'échange réseau au format `.cap`. Vous pouvez par exemple visualiser le détail des paquets à l'aide d'un outil comme `wireshark`.

Cette trace contient des messages correspondant à des échanges entre Alice et Bob utilisant le protocole `plutotBonneConfidentialité`. La partie *asymétrique* du protocole (échange de la clé de session) a déjà eu lieu. Ils utilisent maintenant cette clé afin de chiffrer *symétriquement* leur communication grâce à l'algorithme `AES-256`. Vous avez normalement récupéré une partie de la clé, de taille 64 bits, à l'étape précédente. Il vous suffira de répliquer **4 fois** cette clé afin d'obtenir la clé utilisée par Alice et Bob.

Le but de cette partie est non seulement de **retrouver les messages originaux échangés** mais également de fournir une méthode **automatique** (ie un programme python) afin de pouvoir les extraire d'une capture d'échange réseau éventuellement plus large.

Voici quelques indices vous permettant d'identifier les messages et de les déchiffrer:

* le protocole `plutotBonneConfidentialite` est un protocole applicatif et utilise UDP sur le port 9999.
* avant d'être envoyé, on ajoute en tête du message le vecteur d'initialisation (16 octets) utilisé par `AES`.
* le protocole AES est utilisé en mode CBC. Cela implique que la taille des messages envoyés doit être un multiple de la taille des blocs, soit un multiple de $128$ bits. Pour cela, un mécanisme de *remplissage* (padding) est utilisé. Il s'agit de **PKCS7** (présent dans la bibliothèque python `cryptography` par exemple).

Il vous est conseillé d'utiliser `scapy` pour décortiquer les paquets, mais ce n'est pas une obligation.
