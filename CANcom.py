import time
import can




class VESC:

    def __init__(self):
        self.id = 22;
        can_interface = 'can0'
        self.bus = can.interface.Bus(can_interface, bustype='socketcan_native')
        self.stop = False

    def write(self, id, data, extended=False):
        msg = can.Message(arbitration_id=id, data=data, extended_id=extended)
        self.bus.send(msg)

    def decode(self, msg):
        id = msg.arbitration_id
        array = msg.data
        array.reverse()
        dlc = msg.dlc
        if id & 0xFF00 == 0x900:
            print("PACKET 1")
            self.rpm = array[7] << 24 | array[6] << 16 | array[5] << 8 | array[4]
            print("RPM : " + str(self.rpm))
            self.current = array[3] << 8 | array[2]
            print("current : " + str(self.current))
            self.dutyc = (array[1] << 8 | array[0]) / 1000.0
            print("duty Cycle : " + str(self.dutyc))
        if id & 0xFF00 == 0xe00:
            print("PACKET 2")
            self.amph = array[7] << 24 | array[6] << 16 | array[5] << 8 | array[4]
            self.amph = self.amph / 1000
            print("AMP_H : " + str(self.amph))
            self.amphc = array[3] << 24 | array[2] << 16 | array[1] << 8 | array[0]
            self.amphc = self.amphc / 1000
            print("AMP_HC : " + str(self.amphc))
        if id & 0xFF00 == 0xf00:
            print("PACKET 3")
            self.wath = array[7] << 24 | array[6] << 16 | array[5] << 8 | array[4]
            self.wath = self.wath / 1000
            print("WATT_H : " + str(self.wath))
            self.wathc = array[3] << 24 | array[2] << 16 | array[1] << 8 | array[0]
            self.wathc = self.wathc / 1000
            print("WATT_HC : " + str(self.wathc))
        if id & 0xFF00 == 0x1000:
            print("PACKET 4")
            self.temp_fet = (array[7] << 8 | array[6]) * 0.1
            print("Temp fet : " + str(self.temp_fet))
            self.temp_mot = (array[5] << 8 | array[4]) * 0.1
            print("Temp motor : " + str(self.temp_mot))
            self.curr_in = (array[3] << 8 | array[2]) * 0.1
            print("Current in : " + str(self.curr_in))
            self.pid_pos = (array[1] << 8 | array[0]) * 0.5
            print("pid pos : " + str(self.pid_pos))
        if id & 0xFF00 == 0x1b00:
            print("PACKET 5")
            self.tacho = array[7] << 24 | array[6] << 16 | array[5] << 8 | array[4]
            print("TACHO : " + str(self.tacho))
            self.vin = (array[3] << 8 | array[2]) * 0.1
            print("VIN : " + str(self.vin))

        print("\n")

    def listen_thread(self):
        while not self.stop:
            message = self.bus.recv(1.0)  # Timeout in seconds.
            if message is None:
                print('Timeout occurred, no message.')
            self.decode(message)







