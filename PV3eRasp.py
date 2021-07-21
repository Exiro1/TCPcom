import getopt
import sys
import time
from random import random
from tkinter import Tk

from TCPcom import TCPCOM, encode_data
import numpy as np

from dashboard import Dashboard


def start(IP,PORT):
    c = TCPCOM(IP, PORT)

    window = Tk()
    dash = Dashboard(window,rand_data())

    data = np.array(
        [12000, 56.25, -356, 1003, 23.56, 23.89, 6687, 32.56, -1200, 68.72, 48.63, 2963, 0, 1, 0, 1, 0, 1, 0, 1,
         0, 1, 0, 3, 2])

    while not dash.stop:
        if c.connected:
            recevied = c.read()
            dash.data = rand_data();
            c.send_data(encode_data(dash.data))
        else:
            c.connect()
        dash.master.update_idletasks()
        dash.master.update()
        time.sleep(1)
    c.disconnect()



# genere des dnnées aléatoire (pour tester)
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
    port = None
    ip = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:p:", ["ip=", "port="])
    except getopt.GetoptError:
        print('PV3eRasp.py -ip <IP> -port <PORT>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('test.py PV3eRasp.py -ip <IP> -port <PORT>')
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = arg
    if port is not None and ip is not None:
        start(ip, int(port))
    else:
        print('PV3eRasp.py -ip <IP> -port <PORT>')
        sys.exit()