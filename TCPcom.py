import socket
import sys
import time
import numpy as np


# encode les données des capteurs afin de les transmettre au serveur
# exemple d'utilisation : send_data( encode_data( data ) )
# où data est une np.array des valeurs dans l'ordre spécifié par le fichier excel donnéePV3e.xlsx

def append_uint(data, value, len, mult=1):
    v = np.uint32(value * mult)
    for i in range(len):
        data.append((v >> (len - i - 1) * 8) & 0xff)


def append_int(data, value, len, mult=1):
    v = np.int32(value * mult)
    for i in range(len):
        data.append(np.uint8((v >> (len - i - 1) * 8) & 0xff))

# si il y a besoin d'ajouter des données à envoyer c'est ici qu'il faut le faire
# il faudra aussi modifier le matlab pour qu'il traite ces nouvelles données
def encode_data(data):
    encoded = bytearray()

    append_uint(encoded, data[0], 2)

    append_int(encoded, data[1], 2, 100)

    append_int(encoded, data[2], 2)

    append_uint(encoded, data[3], 2)

    append_uint(encoded, data[4], 2, 100)

    append_uint(encoded, data[5], 2, 100)

    append_uint(encoded, data[6], 2)

    append_uint(encoded, data[7], 2, 100)

    append_int(encoded, data[8], 2)

    append_int(encoded, data[9], 2, 100)

    append_int(encoded, data[10], 2, 100)

    append_uint(encoded, data[11], 2)

    boo = 0x00 | np.uint8(data[12]) | np.uint8(data[13]) << 1 | np.uint8(data[14]) << 2 \
          | np.uint8(data[15]) << 3 | np.uint8(data[16]) << 4 | np.uint8(data[17]) << 5 | np.uint8(data[18]) << 6 \
          | np.uint8(data[19]) << 7
    encoded.append(boo)

    boo = 0x00 | np.uint8(data[20]) | np.uint8(data[21]) << 1 | np.uint8(data[22]) << 2 \
          | np.uint8(data[23]) << 3 | np.uint8(data[24]) << 4 | np.uint8(data[25]) << 5 | np.uint8(data[26]) << 6 \
          | np.uint8(data[27]) << 7
    encoded.append(boo)

    append_uint(encoded, data[28], 1)

    append_uint(encoded, data[29], 1)

    # ajouter ici
    # si valeur non signée : append_uint(encoded, <valeur>, facteur)
    # si valeur signée : append_int(encoded, <valeur>, facteur)

    return encoded


class TCPCOM:

    def __init__(self, IP,PORT):
        self.connected = False
        self.HOST = IP
        self.PORT = PORT
        self.client = None

        while not self.connect():
            time.sleep(1)

    # retourne les infos reçu (None si rien à été reçu)
    def read(self):
        try:
            msg = self.client.recv(4096)
        except socket.timeout as e:
            err = e.args[0]
            # this next if/else is a bit redundant, but illustrates how the
            # timeout exception is setup
            if err == 'timed out':
                print('TO')
            else:
                print(e)
        except socket.error as e:
            pass
        else:
            if len(msg) == 0:
                print('server disconnected')
                self.connected = False
            else:
                print(f'data recvd : {msg} \n')
                return msg
        return None

    # essaye de se connecter au serveur
    # retourne True si le raspberry est connecté au serveur
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.HOST, self.PORT))
        except socket.error as e:
            print(f'impossible de se connecter {e}')
            return False

        self.connected = True
        self.client.setblocking(False)
        print('Connection ' + self.HOST + ':' + str(self.PORT) + ' .....SUCCESS')
        message = 'RASP\n'.encode()
        self.send_data(message)
        return True

    # envoie des données encodées au serveur
    def send_data(self, data):
        try:
            n = self.client.send(data)
        except socket.error as e:
            print(e)
            return False

        if n != len(data):
            print('Error sending data.')
        else:
            print('Data sent.')
        return True

    # deconnecte le raspberry du serveur
    def disconnect(self):
        self.send_data('END'.encode())
        print('Disconnection.')
        self.client.close()
