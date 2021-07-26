import getopt
import os
import sys
import threading
import time
from random import random
from tkinter import Tk


from TCPcom import TCPCOM, encode_data
import numpy as np
from CANcom import VESC
from dashboard import Dashboard

# export DISPLAY=:0.0
# python3 home/pi/tmp/pycharm_project_130/PV3eRasp.py -i 46.105.28.70 -p 11000
def start(IP,PORT):

    os.system("export DISPLAY=:0.0")
    os.system("sudo ip link set can0 up type can bitrate 500000")
    os.system("sudo ifconfig can0 txqueuelen 65536")

    c = TCPCOM(IP, PORT)
    vesc = VESC(0,1)

    #start CAN listening thread
    listen_thr = threading.Thread(target=vesc.listen_thread)
    listen_thr.start()
    data = np.array(
        [12000, 56.25, -356, 1003, 23.56, 23.89, 6687, 32.56, -1200, 68.72, 48.63, 2963, 0, 1, 0, 1, 0, 1, 0, 1,
         0, 1, 0, 3, 2])
    data = rand_data()

    window = Tk()
    dash = Dashboard(window,rand_data())


    tic = time.time()*1000

    while not dash.stop:
        # recuperer les données ici
        dash.data = get_data(vesc,c)

        if time.time()*1000-tic > 1000:
            tic = time.time()*1000
            if c.connected:
                recevied = c.read()
                c.send_data(encode_data(dash.data))
            else:
                c.connect()

        dash.master.update_idletasks()
        dash.master.update()
    c.disconnect()
    vesc.stop = True
    listen_thr.join()


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

    data = np.append(data, np.random.rand() * 1000)
    data = np.append(data, np.random.rand() * 1000)
    data = np.append(data, np.random.randint(2))
    data = np.append(data, np.random.rand() * 1000)
    data = np.append(data, np.random.randint(2))
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.randint(2))
    data = np.append(data, np.random.randint(2))
    data = np.append(data, np.random.rand() * 1000)
    data = np.append(data, np.random.randint(2))
    data = np.append(data, np.random.randint(20))
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.randint(20))
    data = np.append(data, np.random.rand() * 10-5)
    data = np.append(data, np.random.rand() * 10-5)
    data = np.append(data, np.random.rand() * 10-5)
    data = np.append(data, np.random.rand() * 100)

    return data


def get_data(vesc, tcp):
    newdata = rand_data()

    newdata[6] = vesc.rpm
    newdata[8] = vesc.torque
    newdata[9] = vesc.temp_mot
    newdata[31] = 0
    if tcp.connected:
        newdata[31] = 1


    return newdata




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