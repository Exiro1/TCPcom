import getopt
import os
import sys
import threading
import time
from tkinter import Tk

import numpy as np
import serial

from CANcom import VESC
from TCPcom import TCPCOM, encode_data
from dashboard import Dashboard

# liste stockant les valeurs reçu (par le matlab et l'arduino volant)
lastmsgTCP = [0, 0, 0, 0, 0, 0, 0]
lastmsgUART = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

stop = False


# export DISPLAY=:0.0
# python3 home/pi/tmp/pycharm_project_130/PV3eRasp.py -i 46.105.28.70 -p 11000

def start(IP, PORT):
    # configuration du module CAN
    os.system("sudo ip link set can0 up type can bitrate 500000")
    os.system("sudo ifconfig can0 txqueuelen 65536")

    c = TCPCOM(IP, PORT)
    vesc = VESC(0, 1030)

    # lancement du thread d'écoute du port CAN
    listen_can_thr = threading.Thread(target=vesc.listen_can_thread)
    listen_can_thr.start()
    # lancement du thread d'écoute du port UART
    listen_uart_thr = threading.Thread(target=listen_uart_thread)
    listen_uart_thr.start()

    # (pour tester)
    data = rand_data()

    #lancement de l'affichage
    window = Tk()
    dash = Dashboard(window, data)

    tic = time.time() * 1000


    time_between_update = 1000 # temps entre chaque envoi de données au serveur (ms)
    while not dash.stop:
        if c.connected:
            recevied = c.read()
            if recevied is not None:
                on_receive(recevied)

        # recuperer les données ici
        dash.data = get_data(vesc, c)

        # envoi des données toutes les secondes
        if time.time() * 1000 - tic > time_between_update:
            tic = time.time() * 1000
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
    global stop
    stop = True
    listen_can_thr.join()
    print("thread can ended")
    listen_uart_thr.join()
    print("thread uart ended")


# ecoute du port UART et décodage des valeurs (il faudra peut etre change '/dev/ttyUSB0' en fonction du port utilisé)
def listen_uart_thread():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    while not stop:
        incom = bytearray()
        if ser.in_waiting > 0:
            start = ser.readline()
            boo = ser.read();
            boo2 = ser.read()
            speed = ser.read()
            speed2 = ser.read()
            dist = ser.read()
            dist2 = ser.read()
            pot = ser.read()
            pot2 = ser.read()
            mode = ser.read()
            mode2 = ser.read()
            lastmsgUART[2] = (boo[0] >> 0) & 0x01
            lastmsgUART[3] = (boo[0] >> 1) & 0x01
            lastmsgUART[4] = (boo[0] >> 2) & 0x01
            lastmsgUART[5] = (boo[0] >> 3) & 0x01
            lastmsgUART[6] = (boo[0] >> 4) & 0x01
            lastmsgUART[7] = (boo[0] >> 5) & 0x01
            lastmsgUART[8] = (boo[0] >> 6) & 0x01
            lastmsgUART[9] = (boo[0] >> 7) & 0x01
            lastmsgUART[10] = (boo2[0] >> 0) & 0x01
            lastmsgUART[11] = (boo2[0] >> 1) & 0x01
            lastmsgUART[12] = (boo2[0] >> 2) & 0x01
            lastmsgUART[13] = (boo2[0] >> 3) & 0x01
            lastmsgUART[14] = (boo2[0] >> 4) & 0x01
            lastmsgUART[15] = (boo2[0] >> 5) & 0x01
            lastmsgUART[0] = toInt16(speed[0] << 8 | speed2[0]) / 10.0
            lastmsgUART[1] = toInt16(dist[0] << 8 | dist2[0])
            lastmsgUART[16] = toInt16(pot[0] << 8 | pot2[0])
            lastmsgUART[17] = toInt16(mode[0] << 8 | mode2[0])


# genere des données aléatoire (pour tester)
def rand_data():
    data = np.array([])
    for i in range(12):
        data = np.append(data, np.random.rand() * 1000)
    for i in range(16):
        data = np.append(data, np.random.randint(2))
    data = np.append(data, np.random.randint(1, 8))
    data = np.append(data, np.random.randint(0, 8))
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
    data = np.append(data, np.random.rand() * 10 - 5)
    data = np.append(data, np.random.rand() * 10 - 5)
    data = np.append(data, np.random.rand() * 10 - 5)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 100)
    data = np.append(data, np.random.rand() * 100)

    return data


# décodage des données reçu par le matlab
# à noter que matlab envoi les données dans le format little-endian
# j'utilise partout ailleurs le big-endian
def on_receive(msg):
    arr = bytearray(msg)
    if len(arr) >= 13:
        lastmsgTCP[0] = arr[1] << 8 | arr[0]
        lastmsgTCP[1] = 0.1 * (arr[3] << 8 | arr[2])
        lastmsgTCP[2] = arr[5] << 8 | arr[4]
        lastmsgTCP[3] = 0.1 * (toInt16(arr[7] << 8 | arr[6]))
        lastmsgTCP[4] = 0.1 * (toInt16(arr[9] << 8 | arr[8]))
        lastmsgTCP[5] = 0.1 * (toInt16(arr[11] << 8 | arr[10]))
        lastmsgTCP[6] = arr[13] << 8 | arr[12]

# transfome un entier 16 bits en un int (32 bits)
def toInt16(value):
    vint = int(value)
    if vint >> 15 == 1:
        toadd = int(-1)
        toadd = toadd - pow(2, 16) + 1
        vint |= toadd
    return vint


# fonction qui arrange toutes les données récuperer dans une liste
def get_data(vesc, tcp):
    newdata = rand_data()

    newdata[6] = vesc.rpm
    newdata[8] = vesc.torque
    newdata[9] = vesc.temp_fet
    newdata[25] = 0
    if tcp.connected:
        newdata[25] = 1
    newdata[10] = lastmsgUART[0]
    newdata[11] = lastmsgUART[1]
    newdata[12] = lastmsgUART[2]
    newdata[13] = lastmsgUART[3]
    newdata[14] = lastmsgUART[4]
    newdata[15] = lastmsgUART[5]
    newdata[16] = lastmsgUART[6]
    newdata[17] = lastmsgUART[7]
    newdata[18] = lastmsgUART[8]
    newdata[19] = lastmsgUART[9]
    newdata[20] = lastmsgUART[10]
    newdata[21] = lastmsgUART[11]
    newdata[22] = lastmsgUART[12]
    newdata[23] = lastmsgUART[13]
    newdata[24] = lastmsgUART[14]
    newdata[27] = lastmsgUART[15]
    newdata[28] = lastmsgUART[16]
    newdata[29] = lastmsgUART[17]

    newdata[35] = lastmsgTCP[0]
    newdata[37] = lastmsgTCP[1]
    newdata[38] = lastmsgTCP[2]
    newdata[39] = lastmsgTCP[3]
    newdata[40] = lastmsgTCP[4]
    newdata[41] = lastmsgTCP[5]
    newdata[42] = lastmsgTCP[6]

    newdata[43] = vesc.temp_mot
    newdata[44] = vesc.vin
    newdata[45] = vesc.current
    newdata[46] = vesc.wath

    return newdata


if __name__ == '__main__':
    port = None
    ip = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:p:", ["ip=", "port="])
    except getopt.GetoptError:
        print('PV3eRasp.py -i <IP> -p <PORT>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('test.py PV3eRasp.py -i <IP> -p <PORT>')
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = arg
    if port is not None and ip is not None:
        start(ip, int(port))
    else:
        print('PV3eRasp.py -i <IP> -p <PORT>')
        sys.exit()
