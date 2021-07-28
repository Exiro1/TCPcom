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



lastmsg = [0,0,0,0,0,0,0]
# export DISPLAY=:0.0
# python3 home/pi/tmp/pycharm_project_130/PV3eRasp.py -i 46.105.28.70 -p 11000
def start(IP,PORT):

    #pour execution depuis pc
    os.system("export DISPLAY=:0.0")

    #configuration du module CAN
    os.system("sudo ip link set can0 up type can bitrate 500000")
    os.system("sudo ifconfig can0 txqueuelen 65536")

    c = TCPCOM(IP, PORT)
    vesc = VESC(0,1030)

    #lancement du thread d'écoute du port CAN
    listen_thr = threading.Thread(target=vesc.listen_thread)
    listen_thr.start()

    data = rand_data()

    window = Tk()
    dash = Dashboard(window,data)

    tic = time.time()*1000

    while not dash.stop:
        if c.connected:
            recevied = c.read()
            if recevied is not None:
                on_receive(recevied)

        # recuperer les données ici
        dash.data = get_data(vesc,c)

        # envoi des données toutes les secondes
        if time.time()*1000-tic > 1000:
            tic = time.time()*1000
            if c.connected:
                c.send_data(encode_data(dash.data))
            else:
                c.connect()
        if dash.master is None:
            continue
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
    for i in range(16):
        data = np.append(data, np.random.randint(2))
    data =np.append(data,np.random.randint(1,8))
    data =np.append(data,np.random.randint(0,8))
    data[10] = data[10] / 5

    data = np.append(data, np.random.rand() * 1000)
    data = np.append(data, np.random.rand() * 1000)
    data = np.append(data, np.random.rand() * 1000)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 1000)
    data = np.append(data, np.random.randint(20))
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.randint(20))
    data = np.append(data, np.random.rand() * 10-5)
    data = np.append(data, np.random.rand() * 10-5)
    data = np.append(data, np.random.rand() * 10-5)
    data = np.append(data, np.random.rand() * 100)

    return data

def on_receive(msg):
    arr = bytearray(msg)
    lastmsg[0] = arr[1] << 8 | arr[0]
    lastmsg[1] = 0.1*(arr[3] << 8 | arr[2])
    lastmsg[2] = arr[5] << 8 | arr[4]
    lastmsg[3] = 0.1*(toInt16(arr[7] << 8 | arr[6]))
    lastmsg[4] = 0.1*(toInt16(arr[9] << 8 | arr[8]))
    lastmsg[5] = 0.1*(toInt16(arr[11] << 8 | arr[10]))
    lastmsg[6] = arr[13] << 8 | arr[12]


def toInt16(value):
    vint = int(value)
    if vint >> 15 == 1:
        toadd = int(-1)
        toadd =toadd - pow(2,16) + 1
        vint |= toadd
    return vint

def get_data(vesc, tcp):
    newdata = rand_data()

    newdata[6] = vesc.rpm
    newdata[8] = vesc.torque
    newdata[9] = vesc.temp_mot
    newdata[25] = 0
    if tcp.connected:
        newdata[25] = 1

    newdata[35] = lastmsg[0]
    newdata[37] = lastmsg[1]
    newdata[38] = lastmsg[2]
    newdata[39] = lastmsg[3]
    newdata[40] = lastmsg[4]
    newdata[41] = lastmsg[5]
    newdata[42] = lastmsg[6]
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