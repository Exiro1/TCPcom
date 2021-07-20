import time
from random import random

from TCPcom import TCPCOM, encode_data
import numpy as np


def start():
    c = TCPCOM()

    data = np.array(
        [12000, 56.25, -356, 1003, 23.56, 23.89, 6687, 32.56, -1200, 68.72, 48.63, 2963, 0, 1, 0, 1, 0, 1, 0, 1,
         0, 1, 0, 3, 2])
    while 1:
        if c.connected:
            recevied = c.read()
            c.send_data(encode_data(rand_data()))
        else:
            c.connect()
        time.sleep(1)

    c.disconnect()

def rand_data():
    data = np.array([])
    for i in range(12):
        data =np.append(data, np.random.rand()*1000)
    for i in range(11):
        data = np.append(data, np.random.randint(2))
    data =np.append(data,np.random.randint(1,8))
    data =np.append(data,np.random.randint(0,8))
    data[10] = data[10] / 5
    return data

if __name__ == '__main__':
    start()