# @Date:   2021-03-22T12:52:26+01:00
# @Last modified time: 2021-03-24T13:57:28+01:00

import math
# from includes.chrono import *
# from includes.test import Test
# from includes.track_2 import Track
from tkinter import *


# import fuel_cons_value_frame
# changes


class Dashboard:

    def kill(self):
        self.stop = True
        self.master.destroy()
        if self.updateID != 0:
            self.master.after_cancel(self.updateID)
        if self.upd_dash != 0:
            self.master.after_cancel(self.upd_dash)

    def update_dash(self):

        # VARIABLES DU DASHBOARD
        self.engine_rpm = float("{:.2f}".format(self.data[0]))
        self.engine_temp = float("{:.2f}".format(self.data[1]))  # °C
        self.temp_water = float("{:.2f}".format(self.data[2]))
        self._lambda = float("{:.2f}".format(self.data[3]))
        self.p_fuel = float("{:.2f}".format(self.data[4]))  # bars
        self.lipo = float("{:.2f}".format(self.data[5]))  # %
        self.motor_rpm = float("{:.2f}".format(self.data[6]))
        self.superc = float("{:.2f}".format(self.data[7]))
        self.motor_torque = float("{:.2f}".format(self.data[8]))
        self.motor_temp = float("{:.2f}".format(self.data[9]))
        self.speed = float("{:.2f}".format(self.data[10]))  # km/h
        self.distance = float("{:.2f}".format(self.data[11]))  # km

        self.fuel_mode = self.data[19]  # True si mode FUEL ON
        self.ice_clutch1 = self.data[23]  # True si ICE Clutch ON
        self.ice_clutch2 = self.data[24]  # False si ICE Clutch OFF
        self.connexion = self.data[25]  # True si état de connexion 3g OK
        self.gps = self.data[26]  # True si connexion GPS OK
        self.break_value = self.data[27]

        self.hybride_mode = self.data[28] == 3  # False si mode HY pas activé

        self.engine_torque = float("{:.2f}".format(self.data[30]))  # Nm
        self.fuel_cons = float("{:.2f}".format(self.data[31]))  # mL

        self.efficiency = float("{:.2f}".format(self.data[32]))  # km/L

        self.soc = float("{:.2f}".format(self.data[33]))  # %

        self.time = float("{:.2f}".format(self.data[34]))  # en millisecondes

        self.turn_regen = int(self.data[35])
        self.value_regen = int(self.data[36])  # en pourcent
        self.target_speed = float("{:.2f}".format(self.data[37]))  # en km
        self.turn_ice = int(self.data[38])
        self.race_delta = float("{:.2f}".format(self.data[39]))
        self.live_delta = float("{:.2f}".format(self.data[40]))
        self.n_1_delta = float("{:.2f}".format(self.data[41]))
        self.target_soc = float("{:.2f}".format(self.data[42]))

        # CONDITIONNEMENT
        # Mode Hybride
        if self.hybride_mode == 0:
            self.hy_background = "white"
            self.hy_police = "black"
        else:
            self.hy_background = "red"
            self.hy_police = "white"
        # Etat ICE Clutch engine
        if self.ice_clutch1 == 1:
            self.clutch1_background = "red"
            self.clutch1_value = "ON"
            self.clutch1_contour = "red"
        else:
            self.clutch1_background = "black"
            self.clutch1_contour = "white"
            self.clutch1_value = "OFF"
        # Etat ICE Clutch motor
        if self.ice_clutch2 == 1:
            self.clutch2_background = "red"
            self.clutch2_value = "ON"
            self.clutch2_contour = "red"
        else:
            self.clutch2_background = "black"
            self.clutch2_contour = "white"
            self.clutch2_value = "OFF"
        # Fuel mode
        if self.fuel_mode == 1:
            self.fuel_mode_value = "ON"
            self.fuel_mode_background = "red"
            self.fuel_mode_contour = "red"
        else:
            self.fuel_mode_value = "OFF"
            self.fuel_mode_background = "black"
            self.fuel_mode_contour = "white"
        # Etat connexion 3g
        if self.connexion == 1:
            self.etat_connexion_background = "#03FF00"
            self.etat_connexion_label = "black"
        else:
            self.etat_connexion_background = "red"
            self.etat_connexion_label = "white"
        # Etat connexion GPS
        if self.gps == 1:
            self.etat_gps_background = "#03FF00"
            self.etat_gps_label = "black"
        else:
            self.etat_gps_background = "red"
            self.etat_gps_label = "white"
        # Etat Breaks
        if self.break_value == 0:
            self.breaks_background = "black"
        else:
            self.breaks_background = "red"
        self.upd_dash = self.master.after(100, self.update_dash)

    def __init__(self, master, data):
        self.master = master
        self.updateID = 0
        self.upd_dash = 0
        self.stop = False
        self.data = data
        if master is None:
            return
        self.update_dash()

        # FENETRE PRINCIPALE
        self.width_screen = self.master.winfo_screenwidth() - 20  # -20 de highlightthickness=10
        self.height_screen = self.master.winfo_screenheight() - 20  # -20 de highlightthickness=10
        self.space = math.ceil(self.width_screen / 50)  # variable qui va espacer les différents cadres
        # self.space = self.width_screen/40
        self.master.geometry(f"{self.width_screen}x{self.height_screen}")
        self.master.configure(bg="black", highlightbackground=self.hy_background, highlightcolor=self.hy_background,
                              highlightthickness=10, padx=0, pady=0, borderwidth=0, relief="flat")

        # POLICES
        self.font_titre = ("Arial", int(self.space * 0.8), "bold")
        self.font_titre_donnees = ("Arial", int(self.space * 1.5), "bold")
        self.font_donnees = ("Arial", int(self.space * 1.75), "bold")
        self.font_vitesse = ("Arial", int(self.space * 2.5), "bold")
        self.font_hy = ("Arial", int(self.space * 2), "bold")
        self.font_etat_clutch = ("Arial", int(self.space * 1.2), "bold")
        self.font_titre_signaux = ("Arial", int(self.space * 1.2), "bold")

        self.master.attributes('-fullscreen', True)  # affichage plein écran
        self.master.bind("<Escape>", lambda e: self.kill())  # <ESC> pour pouvoir fermer le programe
        self.master.bind("<Button-1>", lambda e: self.kill())  # <CLIQUER> pour pouvoir fermer le programe
        self.master.bind("<Left>", lambda e: self.create_track())  # <Left> pour afficher le menu track
        self.master.bind("<Right>", lambda e: self.create_test())  # <Right> pour afficher le menu test

        # self.create_track()

    def __FrameDestroy(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def update_track(self):
        self.num_lap_label.configure(text="8/11")
        mode = 'ON'
        if self.fuel_mode == 0:
            mode = 'OFF'
        self.soc_value_label.configure(text=str(self.soc) + '%')

        self.state_label.configure(text=mode)

        self.master.configure(bg="black", highlightbackground=self.hy_background, highlightcolor=self.hy_background)

        if self.soc < self.target_soc:

            self.TSOC_part1.configure(bg="green", width=self.soc / 100 * self.TSOC_jauge_frame["width"],
                                      height=self.height_screen / 10 - self.space)
            self.TSOC_part1.grid(column=0, row=0)
            self.TSOC_part2.configure(bg="black",
                                      width=(self.target_soc - self.soc) / 100 * self.TSOC_jauge_frame[
                                          "width"],
                                      height=self.height_screen / 10 - self.space)
            self.TSOC_part2.grid(column=1, row=0)
            self.TSOC_part3.configure(bg="black",
                                      width=(100 - self.target_soc + 1) / 100 * self.TSOC_jauge_frame[
                                          "width"],
                                      height=self.height_screen / 10 - self.space)
            self.TSOC_part3.grid(column=3, row=0)
            self.TSOC_cursor_jauge_frame.configure(bg="white", width=0.01 * self.TSOC_jauge_frame["width"],
                                                   height=self.height_screen / 10 - self.space)
            self.TSOC_cursor_jauge_frame.grid(column=2, row=0)
        elif self.soc > self.target_soc:
            self.TSOC_part1.configure(bg="green",
                                      width=self.target_soc / 100 * self.TSOC_jauge_frame["width"],
                                      height=self.height_screen / 10 - self.space)
            self.TSOC_part1.grid(column=0, row=0)
            self.TSOC_part2.configure(bg="green",
                                      width=(self.soc - self.target_soc + 1) / 100 * self.TSOC_jauge_frame[
                                          "width"],
                                      height=self.height_screen / 10 - self.space)
            self.TSOC_part2.grid(column=2, row=0)
            self.TSOC_part3.configure(bg="black", width=(100 - self.soc) / 100 * self.TSOC_jauge_frame[
                "width"],
                                      height=self.height_screen / 10 - self.space)
            self.TSOC_part3.grid(column=3, row=0)
            self.TSOC_cursor_jauge_frame.configure(bg="white", width=0.01 * self.TSOC_jauge_frame["width"],
                                                   height=self.height_screen / 10 - self.space)
            self.TSOC_cursor_jauge_frame.grid(column=1, row=0)

        elif self.soc == self.target_soc:
            self.TSOC_part1.configure(bg="green", width=self.soc / 100 * self.TSOC_jauge_frame["width"],
                                      height=self.height_screen / 10 - self.space)
            self.TSOC_part1.grid(column=0, row=0)
            self.TSOC_part2.configure(bg="black", width=(100 - self.soc) / 100 * self.TSOC_jauge_frame[
                "width"],
                                      height=self.height_screen / 10 - self.space)
            self.TSOC_part2.grid(column=1, row=0)

            self.TSOC_part3.configure(width=0, bg='black')
            self.TSOC_part3.grid(column=3, row=0)

        self.TSOC_num_label.configure(text=str(self.target_soc) + '%')
        fg = 'green'
        if self.race_delta > 0:
            fg = 'red'
        self.num_raceD_label.configure(text=str(self.race_delta) + 's', fg=fg)
        fg = 'green'
        if self.live_delta > 0:
            fg = 'red'
        self.num_liveD_label.configure(text=str(self.live_delta) + 's', fg=fg)
        fg = 'green'
        if self.n_1_delta > 0:
            fg = 'red'
        self.nD_label.configure(text=str(self.n_1_delta) + 's', fg=fg)

        self.num_turn_regen_label.configure(text=str(self.turn_regen))

        self.num_speed_regen_label.configure(text=str(self.value_regen) + '%')

        self.int_speed_ICE_label.configure(text=str(int(self.target_speed)))

        self.dec_speed_ICE_label.configure(text="." + str(int(self.target_speed * 10 % 10)) + " km/h")

        self.mode_label.configure(bg=self.hy_background, fg=self.hy_police, font=self.font_hy)

        self.int_speed_label.configure(text=str(int(self.speed)))

        self.dec_speed_label.configure(text="." + str(int(self.speed * 10 % 10)) + " km/h")

        self.breaks_label.configure(bg=self.breaks_background)

        self.mode_label.configure(bg=self.hy_background)

        self.num_time_label.configure(text=str(self.time))

        self.num_turn_ICE_label.configure(text=str(self.turn_ice))

        self.updateID = self.master.after(200, self.update_track)

    def create_track(self):
        if self.updateID != 0:
            self.master.after_cancel(self.updateID)
        self.__FrameDestroy()

        self.master.columnconfigure(0, minsize=self.width_screen / 6)
        self.master.columnconfigure(1, minsize=self.width_screen / 6)
        self.master.columnconfigure(2, minsize=self.width_screen / 6)
        self.master.columnconfigure(3, minsize=self.width_screen / 6)
        self.master.columnconfigure(4, minsize=self.width_screen / 6)
        self.master.columnconfigure(5, minsize=self.width_screen / 6)

        self.master.rowconfigure(0, minsize=self.height_screen / 4)
        self.master.rowconfigure(1, minsize=self.height_screen / 4)
        self.master.rowconfigure(2, minsize=self.height_screen / 4)
        self.master.rowconfigure(3, minsize=self.space)
        self.master.rowconfigure(4, minsize=self.height_screen / 4 - self.space)

        self.lap_frame = Frame(self.master, width=self.width_screen / 6 - self.space,
                               height=self.height_screen / 4 - self.space)
        self.lap_frame.grid(column=0, row=0)
        self.lap_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.lap_frame.pack_propagate(0)

        self.lap_label = Label(self.lap_frame, text="LAP")
        self.lap_label.pack()
        self.lap_label.configure(bg=self.lap_frame["bg"], fg="white", font=("Arial 26 bold"))

        self.num_lap_label = Label(self.lap_frame, text="8/11")
        self.num_lap_label.pack(expand=True)
        self.num_lap_label.configure(bg=self.lap_frame["bg"], fg="yellow", font=("Arial 50 bold"))

        self.SOC_frame = LabelFrame(self.master, width=self.width_screen / 6 - self.space,
                                    height=self.height_screen / 4 - self.space)
        self.SOC_frame.grid(column=5, row=0)
        self.SOC_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.SOC_frame.pack_propagate(0)

        self.SOC_label = Label(self.SOC_frame, text="SOC")
        self.SOC_label.pack()
        self.SOC_label.configure(bg=self.SOC_frame["bg"], fg="white", font=("Arial 25 bold"))

        self.soc_value_label = Label(self.SOC_frame, text=str(self.soc) + '%')
        self.soc_value_label.pack(expand=True)
        self.soc_value_label.configure(bg=self.SOC_frame["bg"], fg="yellow", font=("Arial 50 bold"))

        self.TSOC_frame = Frame(self.master)
        self.TSOC_frame.grid(column=1, row=0, columnspan=4)
        self.TSOC_frame.configure(bg="black")

        self.TSOC_jauge_frame = Frame(self.TSOC_frame, width=4 * self.width_screen / 6 - self.space,
                                      height=self.height_screen / 10 - self.space)
        self.TSOC_jauge_frame.grid(column=0, row=0)
        self.TSOC_jauge_frame.configure(bg="black", highlightbackground="white", highlightthickness=4)

        if self.soc < self.target_soc:

            self.TSOC_part1 = Frame(self.TSOC_jauge_frame,
                                    width=self.soc / 100 * self.TSOC_jauge_frame["width"],
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part1.grid(column=0, row=0)
            self.TSOC_part1.configure(bg="green")

            self.TSOC_part2 = Frame(self.TSOC_jauge_frame,
                                    width=(self.target_soc - self.soc) / 100 * self.TSOC_jauge_frame[
                                        "width"],
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part2.grid(column=1, row=0)
            self.TSOC_part2.configure(bg="black")

            self.TSOC_part3 = Frame(self.TSOC_jauge_frame,
                                    width=(100 - self.target_soc + 1) / 100 * self.TSOC_jauge_frame[
                                        "width"],
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part3.grid(column=3, row=0)
            self.TSOC_part3.configure(bg="black")

            self.TSOC_cursor_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                 width=0.01 * self.TSOC_jauge_frame["width"],
                                                 height=self.height_screen / 10 - self.space)
            self.TSOC_cursor_jauge_frame.grid(column=2, row=0)
            self.TSOC_cursor_jauge_frame.configure(bg="white")

        elif self.soc > self.target_soc:
            self.TSOC_part1 = Frame(self.TSOC_jauge_frame,
                                    width=self.target_soc / 100 * self.TSOC_jauge_frame["width"],
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part1.grid(column=0, row=0)
            self.TSOC_part1.configure(bg="green")

            self.TSOC_part2 = Frame(self.TSOC_jauge_frame,
                                    width=(self.soc - self.target_soc + 1) / 100 * self.TSOC_jauge_frame[
                                        "width"],
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part2.grid(column=2, row=0)
            self.TSOC_part2.configure(bg="green")

            self.TSOC_part3 = Frame(self.TSOC_jauge_frame,
                                    width=(100 - self.soc) / 100 * self.TSOC_jauge_frame[
                                        "width"],
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part3.grid(column=3, row=0)
            self.TSOC_part3.configure(bg="black")

            self.TSOC_cursor_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                 width=0.01 * self.TSOC_jauge_frame["width"],
                                                 height=self.height_screen / 10 - self.space)
            self.TSOC_cursor_jauge_frame.grid(column=1, row=0)
            self.TSOC_cursor_jauge_frame.configure(bg="white")

        elif self.soc == self.target_soc:
            self.TSOC_part1 = Frame(self.TSOC_jauge_frame,
                                    width=self.soc / 100 * self.TSOC_jauge_frame["width"],
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part1.grid(column=0, row=0)
            self.TSOC_part1.configure(bg="green")

            self.TSOC_part2 = Frame(self.TSOC_jauge_frame,
                                    width=(100 - self.soc) / 100 * self.TSOC_jauge_frame[
                                        "width"],
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part2.grid(column=1, row=0)
            self.TSOC_part2.configure(bg="black")

            self.TSOC_part3 = Frame(self.TSOC_jauge_frame,
                                    width=0,
                                    height=self.height_screen / 10 - self.space)
            self.TSOC_part3.grid(column=3, row=0)
            self.TSOC_part3.configure(bg="black")

        self.TSOC_num_frame = Frame(self.TSOC_frame)
        self.TSOC_num_frame.grid(column=0, row=1, sticky='w')
        self.TSOC_num_frame.configure(bg="black")

        self.TSOC_title_label = Label(self.TSOC_num_frame, text='TARGET SOC ')
        self.TSOC_title_label.configure(font=("Arial 30 bold"), bg='black', fg='white')
        self.TSOC_title_label.grid(column=0, row=0, sticky='s')

        self.TSOC_num_label = Label(self.TSOC_num_frame, text=str(self.target_soc) + '%')
        self.TSOC_num_label.configure(font=("Arial 50 bold"), bg='black', fg='yellow')
        self.TSOC_num_label.grid(column=1, row=0)

        self.others_frame = LabelFrame(self.master, text="EMPTY", bd=3, width=self.width_screen / 6 - self.space,
                                       height=self.height_screen / 4 - self.space)
        self.others_frame.grid(column=0, row=1)
        self.others_frame.configure(bg="black", fg="white")

        self.deltas_frame = Frame(self.master, width=4 * self.width_screen / 6 - self.space * 2,
                                  height=self.height_screen / 4 - self.space)
        self.deltas_frame.grid(column=1, row=1, columnspan=4)
        self.deltas_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.deltas_frame.grid_propagate(0)

        self.liveD_frame = Frame(self.deltas_frame, width=self.width_screen * 2 / 9 - 2 - 2 * self.space / 3,
                                 height=self.height_screen / 4 - self.space - 4, bg='white')
        self.liveD_frame.grid(column=1, row=0)
        self.liveD_frame.pack_propagate(0)

        self.liveD_label = Label(self.liveD_frame, text='LIVE DELTA')
        self.liveD_label.configure(font=("Arial 25 bold"), bg='white', fg='black')
        self.liveD_label.pack()

        self.num_liveD_label = Label(self.liveD_frame, text=str(self.live_delta) + 's')
        self.num_liveD_label.configure(font=("Arial 40 bold"), bg='white', fg='red')
        self.num_liveD_label.pack(expand=True)

        self.raceD_frame = Frame(self.deltas_frame, width=self.width_screen * 2 / 9 - 2 - 2 * self.space / 3,
                                 height=self.height_screen / 4 - self.space - 4, bg='black')
        self.raceD_frame.grid(column=0, row=0)
        self.raceD_frame.pack_propagate(0)

        self.raceD_label = Label(self.raceD_frame, text='RACE DELTA')
        self.raceD_label.configure(font=("Arial 25 bold"), bg=self.deltas_frame["bg"], fg='white')
        self.raceD_label.pack()

        self.num_raceD_label = Label(self.raceD_frame, text=str(self.race_delta) + 's')
        self.num_raceD_label.configure(font=("Arial 40 bold"), bg=self.deltas_frame["bg"], fg='green')
        self.num_raceD_label.pack(expand=True)

        self.nD_frame = Frame(self.deltas_frame, width=self.width_screen * 2 / 9 - 2 - 2 * self.space / 3,
                              height=self.height_screen / 4 - self.space - 4, bg='black')
        self.nD_frame.grid(column=2, row=0)
        self.nD_frame.pack_propagate(0)

        self.nD_label = Label(self.nD_frame, text='N-1 DELTA')
        self.nD_label.configure(font=("Arial 25 bold"), bg=self.deltas_frame["bg"], fg='white')
        self.nD_label.pack()

        self.nD_label = Label(self.nD_frame, text=str(self.n_1_delta) + 's')
        self.nD_label.configure(font=("Arial 40 bold"), bg=self.deltas_frame["bg"], fg='green')
        self.nD_label.pack(expand=True)

        self.fuel_frame = Frame(self.master, width=self.width_screen / 6 - self.space,
                                height=self.height_screen / 4 - self.space)
        self.fuel_frame.grid(column=5, row=1)
        self.fuel_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.fuel_frame.pack_propagate(0)

        self.fuel_label = Label(self.fuel_frame, text="FUEL")
        self.fuel_label.pack()
        self.fuel_label.configure(bg=self.fuel_frame["bg"], fg="white", font=("Arial 25 bold"))

        self.state_label = Label(self.fuel_frame, text="ON")
        self.state_label.pack(expand=True)
        self.state_label.configure(bg=self.fuel_frame["bg"], fg="yellow", font=("Arial 50 bold"))

        self.regen_frame = Frame(self.master, width=3 * self.width_screen / 6 - self.space * 2,
                                 height=self.height_screen / 4 - self.space)
        self.regen_frame.grid(column=0, row=2, columnspan=3)
        self.regen_frame.configure(bg="black")
        self.regen_frame.grid_propagate(0)

        self.turn_regen_frame = Frame(self.regen_frame, width=self.width_screen / 8 - self.space,
                                      height=self.height_screen / 4 - self.space, bg='white')
        self.turn_regen_frame.grid(column=0, row=0)
        self.turn_regen_frame.pack_propagate(0)

        self.turn_regen_label = Label(self.turn_regen_frame, text='TURN')
        self.turn_regen_label.configure(font=("Arial 35 bold"), bg=self.turn_regen_frame["bg"])
        self.turn_regen_label.pack()

        self.num_turn_regen_label = Label(self.turn_regen_frame, text=str(self.turn_regen))
        self.num_turn_regen_label.configure(font=("Arial 80 bold"), bg=self.turn_regen_frame["bg"])
        self.num_turn_regen_label.pack(expand=True)

        self.speed_regen_frame = Frame(self.regen_frame, width=3 * self.width_screen / 8 - self.space,
                                       height=self.height_screen / 4 - self.space, bg=self.regen_frame["bg"])
        self.speed_regen_frame.grid(column=1, row=0)
        self.speed_regen_frame.configure(highlightbackground="white", highlightthickness=2)
        self.speed_regen_frame.pack_propagate(0)

        self.speed_regen_label = Label(self.speed_regen_frame, text='REGEN')
        self.speed_regen_label.configure(font=("Arial 30 bold"), bg=self.speed_regen_frame["bg"], fg="white")
        self.speed_regen_label.pack(anchor='nw')

        self.num_speed_regen_label = Label(self.speed_regen_frame, text=str(self.value_regen) + '%')
        self.num_speed_regen_label.configure(font=("Arial 50 bold"), bg=self.speed_regen_frame["bg"], fg="yellow")
        self.num_speed_regen_label.pack(expand=True)

        self.ICE_frame = Frame(self.master, width=3 * self.width_screen / 6 - self.space * 2,
                               height=self.height_screen / 4 - self.space,
                               bg='black')
        self.ICE_frame.grid(column=3, row=2, columnspan=3)
        self.ICE_frame.grid_propagate(0)

        self.turn_ICE_frame = Frame(self.ICE_frame, width=self.width_screen / 8 - self.space,
                                    height=self.height_screen / 4 - self.space,
                                    bg='white')
        self.turn_ICE_frame.grid(column=0, row=0)
        self.turn_ICE_frame.pack_propagate(0)

        self.turn_ICE_label = Label(self.turn_ICE_frame, text='TURN')
        self.turn_ICE_label.configure(font=("Arial 35 bold"), bg=self.turn_ICE_frame["bg"])
        self.turn_ICE_label.pack()

        self.num_turn_ICE_label = Label(self.turn_ICE_frame, text=str(self.turn_ice))
        self.num_turn_ICE_label.configure(font=("Arial 80 bold"), bg=self.turn_ICE_frame["bg"])
        self.num_turn_ICE_label.pack(expand=True)

        self.speed_ICE_frame = Frame(self.ICE_frame, width=3 * self.width_screen / 8 - self.space,
                                     height=self.height_screen / 4 - self.space, bg=self.ICE_frame["bg"])
        self.speed_ICE_frame.grid(column=1, row=0)
        self.speed_ICE_frame.configure(highlightbackground="white", highlightthickness=2)
        self.speed_ICE_frame.grid_propagate(0)
        # self.ICE_frame.columnconfigure(0, minsize=(3*self.width_screen/8-self.space)/2)

        self.speed_ICE_label = Label(self.speed_ICE_frame, text='ICE')
        self.speed_ICE_label.configure(font=("Arial 30 bold"), bg=self.speed_ICE_frame["bg"], fg="white")
        self.speed_ICE_label.grid(column=0, row=0)
        self.speed_ICE_frame.columnconfigure(0)

        self.int_speed_ICE_label = Label(self.speed_ICE_frame, text=str(int(self.target_speed)))
        self.int_speed_ICE_label.grid(row=1, column=5, sticky='ns')
        self.int_speed_ICE_label.configure(bg=self.speed_ICE_frame["bg"], fg="yellow", font=self.font_vitesse)
        self.dec_speed_ICE_label = Label(self.speed_ICE_frame,
                                         text="." + str(int(self.target_speed * 10 % 10)) + " km/h")
        self.dec_speed_ICE_label.grid(row=1, column=6)
        self.dec_speed_ICE_label.configure(bg=self.speed_ICE_frame["bg"], fg="yellow", font=("Arial 35 bold"))

        self.spacer_frame = Frame(self.master, width=self.width_screen, height=2)
        self.spacer_frame.grid(column=0, row=3, columnspan=6)
        self.spacer_frame.configure(bg="white")

        self.breaks_mode_frame = Frame(self.master, width=self.width_screen / 6,
                                       height=self.height_screen / 4 - self.space)
        self.breaks_mode_frame.grid(column=0, row=4)
        self.breaks_mode_frame.pack_propagate(0)
        self.breaks_mode_frame.configure(bg="black")

        self.breaks_label = Label(self.breaks_mode_frame, text="BRK")
        self.breaks_label.pack(expand=True)
        self.breaks_label.configure(bg=self.breaks_background, fg="white", font=("Arial 30 bold"))

        self.mode_label = Label(self.breaks_mode_frame, text="HY")
        self.mode_label.pack(anchor="sw", side=BOTTOM)
        self.mode_label.configure(bg=self.hy_background, fg=self.hy_police, font=self.font_hy)

        self.time_frame = Frame(self.master, width=3 * self.width_screen / 6,
                                height=self.height_screen / 4 - self.space)
        self.time_frame.grid(column=1, row=4, columnspan=3)
        self.time_frame.configure(bg="black")
        self.time_frame.pack_propagate(0)

        self.time_label = Label(self.time_frame, text="TIME")
        self.time_label.pack(anchor='nw')
        self.time_label.configure(bg=self.time_frame["bg"], fg="white", font=("Arial 25 bold"))

        self.num_time_label = Label(self.time_frame, text="00:02:11")
        self.num_time_label.pack(expand=True, anchor='nw')
        self.num_time_label.configure(bg=self.time_frame["bg"], fg="yellow", font=("Arial 90 bold"))

        self.speed_frame = Frame(self.master, width=2 * self.width_screen / 6 - self.space,
                                 height=self.height_screen / 4 - self.space)
        self.speed_frame.grid(column=4, row=4, columnspan=2)
        self.speed_frame.configure(bg="black")
        self.speed_frame.grid_propagate(0)

        self.speed_label = Label(self.speed_frame, text="SPEED")
        self.speed_label.grid(row=0, column=0)
        self.speed_label.configure(bg=self.speed_frame["bg"], fg="white", font=("Arial 25 bold"))

        self.int_speed_label = Label(self.speed_frame, text=str(int(self.speed)))
        self.int_speed_label.grid(row=1, column=0, sticky='ns')
        self.int_speed_label.configure(bg=self.speed_frame["bg"], fg="yellow", font=self.font_vitesse)
        self.dec_speed_label = Label(self.speed_frame, text="." + str(int(self.speed * 10 % 10)) + " km/h")
        self.dec_speed_label.grid(row=1, column=1)
        self.dec_speed_label.configure(bg=self.speed_frame["bg"], fg="yellow", font=("Arial 35 bold"))

        self.update_track()

    def update_test(self):

        # self.rpm_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
        #                       height=self.height_screen / 8 - self.space)

        self.master.configure(bg="black", highlightbackground=self.hy_background, highlightcolor=self.hy_background)

        self.hybride_mode_label.configure(bg=self.hy_background, fg=self.hy_police, font=self.font_hy)

        self.engine_torque_value_label.configure(text=self.engine_torque)

        self.engine_temp_value_label.configure(text=self.engine_temp)

        self.engine_rpm_value_label.configure(text=self.engine_rpm)
        self.engine_rpm_value_label.pack()

        self.p_fuel_value_label.configure(text=self.p_fuel)

        self.fuel_cons_value_label.configure(text=self.fuel_cons)

        self.rpm_motor_value_label.configure(text=self.motor_rpm)
        self.rpm_motor_value_label.pack()

        self.torque_motor_value_label.configure(text=self.motor_torque)

        self.motor_temp_value_label.configure(text=self.motor_temp)

        self.distance_value_label.configure(text=self.distance)

        self.efficiency_value_label.configure(text=self.efficiency)

        self.ice_clutch2_value_frame.configure(bg=self.clutch2_background, highlightbackground=self.clutch2_contour,
                                               highlightthickness=2)

        self.ice_clutch2_value_label.configure(text=self.clutch2_value, bg=self.ice_clutch2_value_frame["bg"])

        self.ice_clutch1_value_frame.configure(bg=self.clutch1_background, highlightbackground=self.clutch1_contour)

        self.ice_clutch1_value_label.configure(text=self.clutch1_value, bg=self.ice_clutch1_value_frame["bg"])
        # self.spacer ligne blanch

        self.fuel_mode_frame.configure(bg=self.fuel_mode_background, highlightbackground=self.fuel_mode_contour,
                                       highlightthickness=2)

        self.fuel_mode_label.configure(text=self.fuel_mode_value)

        self.fuel_mode_label.configure(bg=self.fuel_mode_frame["bg"])
        self.fuel_label.configure(bg=self.fuel_mode_frame["bg"])

        self.lipo_value_label.configure(text="%s%s" % (int(self.lipo) / 10, "%"))

        # 3G

        self.connexion_frame.configure(bg=self.etat_connexion_background)

        self.connexion_label.configure(bg=self.connexion_frame["bg"], fg=self.etat_connexion_label,
                                       font=self.font_titre_donnees)

        # GPS

        self.gps_frame.configure(bg=self.etat_gps_background)
        self.gps_frame.pack_propagate(0)

        self.gps_label.configure(bg=self.gps_frame["bg"], fg=self.etat_gps_label, font=self.font_titre_donnees)

        self.soc_value_label.configure(text=str(int(self.soc)) + '%')

        # Speed

        self.speed_value_label.configure(text=self.speed)

        self.updateID = self.master.after(200, self.update_test)

    def create_test(self):
        if self.updateID != 0:
            self.master.after_cancel(self.updateID)
        self.__FrameDestroy()
        self.master.rowconfigure(0, minsize=self.height_screen / 8)
        self.master.rowconfigure(1, minsize=self.height_screen / 8)
        self.master.rowconfigure(2, minsize=self.height_screen / 8)
        self.master.rowconfigure(3, minsize=self.height_screen / 8)
        self.master.rowconfigure(4, minsize=self.height_screen / 8)
        self.master.rowconfigure(5, minsize=self.height_screen / 8)
        self.master.rowconfigure(6, minsize=5)
        self.master.rowconfigure(7, minsize=self.height_screen / 8)
        self.master.rowconfigure(8, weight=2)

        self.master.columnconfigure(0, weight=1, minsize=0)
        self.master.columnconfigure(1, weight=1, minsize=self.width_screen / 8)
        self.master.columnconfigure(2, weight=4, minsize=0)
        self.master.columnconfigure(3, weight=1, minsize=0)
        self.master.columnconfigure(4, weight=1, minsize=0)
        self.master.columnconfigure(5, weight=4, minsize=0)
        self.master.columnconfigure(6, weight=1, minsize=self.width_screen / 4)
        self.master.columnconfigure(7, weight=1, minsize=0)

        self.hybride_mode_frame = Frame(self.master)
        self.hybride_mode_frame.grid(column=0, row=8)
        # self.hybride_mode_frame.pack_propagate(0)
        self.hybride_mode_frame.configure(bg="black")

        self.hybride_mode_label = Label(self.hybride_mode_frame, text="HY")
        self.hybride_mode_label.pack(anchor="sw", side=BOTTOM)
        self.hybride_mode_label.configure(bg=self.hy_background, fg=self.hy_police, font=self.font_hy)

        # engine RPM

        self.engine_rpm_frame = Frame(self.master)
        self.engine_rpm_frame.grid(column=0, row=0)
        self.engine_rpm_frame.configure(bg="black")
        # self.engine_rpm_frame.pack_propagate(0)

        self.engine_rpm_label = Label(self.engine_rpm_frame, text="Engine")
        self.engine_rpm_label.pack(side=RIGHT)
        self.engine_rpm_label.configure(bg=self.engine_rpm_frame["bg"], fg="white", font=self.font_titre)

        self.engine_rpm_frame = Frame(self.master)
        self.engine_rpm_frame.grid(column=1, row=0)
        self.engine_rpm_frame.configure(bg="black")
        # self.engine_rpm_frame.pack_propagate(0)

        self.engine_rpm_label = Label(self.engine_rpm_frame, text="RPM")
        self.engine_rpm_label.pack(side=LEFT)
        self.engine_rpm_label.configure(bg=self.engine_rpm_frame["bg"], fg="white", font=self.font_titre)

        self.engine_rpm_value_frame = Frame(self.master)
        self.engine_rpm_value_frame.grid(column=2, row=0)
        self.engine_rpm_value_frame.configure(bg="black")
        # self.engine_rpm_value_frame.pack_propagate(0)

        self.engine_rpm_value_label = Label(self.engine_rpm_value_frame, text=self.engine_rpm)
        self.engine_rpm_value_label.pack()
        self.engine_rpm_value_label.configure(bg=self.engine_rpm_value_frame["bg"], fg="yellow", font=self.font_donnees)
        self.rpm_frame = Frame(self.master)
        self.rpm_frame.grid(column=3, row=0)
        self.rpm_frame.configure(bg="black")
        # self.rpm_frame.pack_propagate(0)
        self.rpm_label = Label(self.rpm_frame, text="RPM")
        self.rpm_label.pack(anchor="w", side=LEFT)
        self.rpm_label.configure(bg=self.engine_rpm_value_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # engine Torque

        self.engine_torque_frame = Frame(self.master)
        self.engine_torque_frame.grid(column=0, row=1)
        self.engine_torque_frame.configure(bg="black")
        # self.engine_torque_frame.pack_propagate(0)

        self.engine_torque_label = Label(self.engine_torque_frame, text="Engine")
        self.engine_torque_label.pack(side=RIGHT)
        self.engine_torque_label.configure(bg=self.engine_torque_frame["bg"], fg="white", font=self.font_titre)

        self.engine_torque_frame = Frame(self.master)
        self.engine_torque_frame.grid(column=1, row=1)
        self.engine_torque_frame.configure(bg="black")
        # self.engine_torque_frame.pack_propagate(0)

        self.engine_torque_label = Label(self.engine_torque_frame, text="Torque")
        self.engine_torque_label.pack(side=LEFT)
        self.engine_torque_label.configure(bg=self.engine_torque_frame["bg"], fg="white", font=self.font_titre)

        self.engine_torque_value_frame = Frame(self.master)
        self.engine_torque_value_frame.grid(column=2, row=1)
        self.engine_torque_value_frame.configure(bg="black")
        # self.engine_torque_value_frame.pack_propagate(0)

        self.engine_torque_value_label = Label(self.engine_torque_value_frame, text=self.engine_torque)
        self.engine_torque_value_label.pack()
        self.engine_torque_value_label.configure(bg=self.engine_torque_value_frame["bg"], fg="yellow",
                                                 font=self.font_donnees)
        self.torque_frame = Frame(self.master)
        self.torque_frame.grid(column=3, row=1)
        self.torque_frame.configure(bg="black")
        # self.torque_frame.pack_propagate(0)
        self.torque_label = Label(self.torque_frame, text="Nm")
        self.torque_label.pack(anchor="w", side=LEFT)
        self.torque_label.configure(bg=self.engine_torque_value_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # engine Temp

        self.engine_temp_frame = Frame(self.master)
        self.engine_temp_frame.grid(column=0, row=2)
        self.engine_temp_frame.configure(bg="black")
        # self.engine_temp_frame.pack_propagate(0)

        self.engine_temp_label = Label(self.engine_temp_frame, text="Engine")
        self.engine_temp_label.pack(side=RIGHT)
        self.engine_temp_label.configure(bg=self.engine_temp_frame["bg"], fg="white", font=self.font_titre)

        self.engine_temp_frame = Frame(self.master)
        self.engine_temp_frame.grid(column=1, row=2)
        self.engine_temp_frame.configure(bg="black")
        # self.engine_temp_frame.pack_propagate(0)

        self.engine_temp_label = Label(self.engine_temp_frame, text="Temp.")
        self.engine_temp_label.pack(side=LEFT)
        self.engine_temp_label.configure(bg=self.engine_temp_frame["bg"], fg="white", font=self.font_titre)

        self.engine_temp_value_frame = Frame(self.master)
        self.engine_temp_value_frame.grid(column=2, row=2)
        self.engine_temp_value_frame.configure(bg="black")
        # self.engine_temp_value_frame.pack_propagate(0)

        self.engine_temp_value_label = Label(self.engine_temp_value_frame, text=self.engine_temp)
        self.engine_temp_value_label.pack()
        self.engine_temp_value_label.configure(bg=self.engine_temp_value_frame["bg"], fg="yellow",
                                               font=self.font_donnees)
        self.temp_frame = Frame(self.master)
        self.temp_frame.grid(column=3, row=2)
        self.temp_frame.configure(bg="black")
        # self.temp_frame.pack_propagate(0)
        self.temp_label = Label(self.temp_frame, text="°C")
        self.temp_label.pack(anchor="w", side=LEFT)
        self.temp_label.configure(bg=self.engine_temp_value_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # Pression fuel

        self.p_fuel_frame = Frame(self.master)
        self.p_fuel_frame.grid(column=0, row=3)
        self.p_fuel_frame.configure(bg="black")
        # self.p_fuel_frame.pack_propagate(0)

        self.p_fuel_label = Label(self.p_fuel_frame, text="P Fuel")
        self.p_fuel_label.pack(side=RIGHT)
        self.p_fuel_label.configure(bg=self.p_fuel_frame["bg"], fg="white", font=self.font_titre)

        self.p_fuel_value_frame = Frame(self.master)
        self.p_fuel_value_frame.grid(column=2, row=3)
        self.p_fuel_value_frame.configure(bg="black")
        # self.p_fuel_value_frame.pack_propagate(0)

        self.p_fuel_value_label = Label(self.p_fuel_value_frame, text=self.p_fuel)
        self.p_fuel_value_label.pack()
        self.p_fuel_value_label.configure(bg=self.p_fuel_value_frame["bg"], fg="yellow", font=self.font_donnees)
        self.p_fuel_unit_frame = Frame(self.master)
        self.p_fuel_unit_frame.grid(column=3, row=3)
        self.p_fuel_unit_frame.configure(bg="black")
        # self.p_fuel_unit_frame.pack_propagate(0)
        self.p_fuel_unit_label = Label(self.p_fuel_unit_frame, text="bars")
        self.p_fuel_unit_label.pack(anchor="w", side=LEFT)
        self.p_fuel_unit_label.configure(bg=self.p_fuel_unit_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # Fuel cons

        self.fuel_cons_frame = Frame(self.master)
        self.fuel_cons_frame.grid(column=0, row=4)
        self.fuel_cons_frame.configure(bg="black")
        # self.fuel_cons_frame.pack_propagate(0)

        self.fuel_cons_label = Label(self.fuel_cons_frame, text="Fuel")
        self.fuel_cons_label.pack(side=RIGHT)
        self.fuel_cons_label.configure(bg=self.fuel_cons_frame["bg"], fg="white", font=self.font_titre)

        self.fuel_cons_frame = Frame(self.master)
        self.fuel_cons_frame.grid(column=1, row=4)
        self.fuel_cons_frame.configure(bg="black")
        # self.fuel_cons_frame.pack_propagate(0)

        self.fuel_cons_label = Label(self.fuel_cons_frame, text="Cons.")
        self.fuel_cons_label.pack(side=LEFT)
        self.fuel_cons_label.configure(bg=self.fuel_cons_frame["bg"], fg="white", font=self.font_titre)

        self.fuel_cons_value_frame = Frame(self.master)
        self.fuel_cons_value_frame.grid(column=2, row=4)
        self.fuel_cons_value_frame.configure(bg="black")
        # self.fuel_cons_value_frame.pack_propagate(0)

        self.fuel_cons_value_label = Label(self.fuel_cons_value_frame, text=self.fuel_cons)
        self.fuel_cons_value_label.pack()
        self.fuel_cons_value_label.configure(bg=self.fuel_cons_value_frame["bg"], fg="yellow", font=self.font_donnees)
        self.fuel_frame = Frame(self.master)
        self.fuel_frame.grid(column=3, row=4)
        self.fuel_frame.configure(bg="black")
        # self.fuel_frame.pack_propagate(0)
        self.fuel_label = Label(self.fuel_frame, text="mL")
        self.fuel_label.pack(anchor="w", side=LEFT)
        self.fuel_label.configure(bg=self.fuel_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # ICE Clutch n°1

        self.ice_clutch1_frame = Frame(self.master)
        self.ice_clutch1_frame.grid(column=0, row=5)
        self.ice_clutch1_frame.configure(bg="black")
        # self.ice_clutch1_frame.pack_propagate(0)

        self.ice_clutch1_label = Label(self.ice_clutch1_frame, text="ICE")
        self.ice_clutch1_label.pack(side=RIGHT)
        self.ice_clutch1_label.configure(bg=self.ice_clutch1_frame["bg"], fg="white", font=self.font_titre)

        self.ice_clutch1_frame = Frame(self.master)
        self.ice_clutch1_frame.grid(column=1, row=5)
        self.ice_clutch1_frame.configure(bg="black")
        # self.ice_clutch1_frame.pack_propagate(0)

        self.ice_clutch1_label = Label(self.ice_clutch1_frame, text="Clutch")
        self.ice_clutch1_label.pack(side=LEFT)
        self.ice_clutch1_label.configure(bg=self.ice_clutch1_frame["bg"], fg="white", font=self.font_titre)

        self.ice_clutch1_value_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                                             height=self.height_screen / 8 - self.space)
        self.ice_clutch1_value_frame.grid(column=2, row=5, )
        self.ice_clutch1_value_frame.configure(bg=self.clutch1_background, highlightbackground=self.clutch1_contour,
                                               highlightthickness=2)
        self.ice_clutch1_value_frame.pack_propagate(0)

        self.ice_clutch1_value_label = Label(self.ice_clutch1_value_frame, text=self.clutch1_value, pady=100)
        self.ice_clutch1_value_label.pack()
        self.ice_clutch1_value_label.configure(bg=self.ice_clutch1_value_frame["bg"], fg="white",
                                               font=self.font_etat_clutch)

        # RPM Motor

        self.rpm_motor_frame = Frame(self.master)
        self.rpm_motor_frame.grid(column=4, row=0)
        self.rpm_motor_frame.configure(bg="black")
        # self.rpm_motor_frame.pack_propagate(0)

        self.rpm_motor_label = Label(self.rpm_motor_frame, text="RPM")
        self.rpm_motor_label.pack(side=RIGHT)
        self.rpm_motor_label.configure(bg=self.rpm_motor_frame["bg"], fg="white", font=self.font_titre)

        self.rpm_motor_frame = Frame(self.master)
        self.rpm_motor_frame.grid(column=5, row=0)
        self.rpm_motor_frame.configure(bg="black")
        # self.rpm_motor_frame.pack_propagate(0)

        self.rpm_motor_label = Label(self.rpm_motor_frame, text="Motor")
        self.rpm_motor_label.pack(side=LEFT)
        self.rpm_motor_label.configure(bg=self.rpm_motor_frame["bg"], fg="white", font=self.font_titre)

        self.rpm_motor_value_frame = Frame(self.master)
        self.rpm_motor_value_frame.grid(column=6, row=0)
        self.rpm_motor_value_frame.configure(bg="black")
        # self.rpm_motor_value_frame.pack_propagate(0)

        self.rpm_motor_value_label = Label(self.rpm_motor_value_frame, text=self.motor_rpm)
        self.rpm_motor_value_label.pack()
        self.rpm_motor_value_label.configure(bg=self.rpm_motor_value_frame["bg"], fg="yellow", font=self.font_donnees)
        self.rpm_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                               height=self.height_screen / 8 - self.space)
        self.rpm_frame.grid(column=7, row=0)
        self.rpm_frame.configure(bg="black")
        # self.rpm_frame.pack_propagate(0)
        self.rpm_label = Label(self.rpm_frame, text="RPM")
        self.rpm_label.pack(anchor="w", side=LEFT)
        self.rpm_label.configure(bg=self.engine_rpm_value_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # Motor Torque

        self.torque_motor_frame = Frame(self.master)
        self.torque_motor_frame.grid(column=4, row=1)
        self.torque_motor_frame.configure(bg="black")
        # self.torque_motor_frame.pack_propagate(0)

        self.torque_motor_label = Label(self.torque_motor_frame, text="Torque")
        self.torque_motor_label.pack(side=RIGHT)
        self.torque_motor_label.configure(bg=self.torque_motor_frame["bg"], fg="white", font=self.font_titre)

        self.torque_motor_frame = Frame(self.master)
        self.torque_motor_frame.grid(column=5, row=1)
        self.torque_motor_frame.configure(bg="black")
        # self.torque_motor_frame.pack_propagate(0)

        self.torque_motor_label = Label(self.torque_motor_frame, text="motor")
        self.torque_motor_label.pack(side=LEFT)
        self.torque_motor_label.configure(bg=self.torque_motor_frame["bg"], fg="white", font=self.font_titre)

        self.torque_motor_value_frame = Frame(self.master)
        self.torque_motor_value_frame.grid(column=6, row=1)
        self.torque_motor_value_frame.configure(bg="black")
        # self.torque_motor_value_frame.pack_propagate(0)

        self.torque_motor_value_label = Label(self.torque_motor_value_frame, text=self.motor_torque)
        self.torque_motor_value_label.pack()
        self.torque_motor_value_label.configure(bg=self.torque_motor_value_frame["bg"], fg="yellow",
                                                font=self.font_donnees)
        self.torque_frame = Frame(self.master)
        self.torque_frame.grid(column=7, row=1)
        self.torque_frame.configure(bg="black")
        # self.torque_frame.pack_propagate(0)
        self.torque_label = Label(self.torque_frame, text="Nm")
        self.torque_label.pack(anchor="w", side=LEFT)
        self.torque_label.configure(bg=self.torque_motor_value_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # Motor Temp

        self.motor_temp_frame = Frame(self.master)
        self.motor_temp_frame.grid(column=4, row=2)
        self.motor_temp_frame.configure(bg="black")
        # self.motor_temp_frame.pack_propagate(0)

        self.motor_temp_label = Label(self.motor_temp_frame, text="Motor")
        self.motor_temp_label.pack(side=RIGHT)
        self.motor_temp_label.configure(bg=self.motor_temp_frame["bg"], fg="white", font=self.font_titre)

        self.motor_temp_frame = Frame(self.master)
        self.motor_temp_frame.grid(column=5, row=2)
        self.motor_temp_frame.configure(bg="black")
        # self.motor_temp_frame.pack_propagate(0)

        self.motor_temp_label = Label(self.motor_temp_frame, text="Temp.")
        self.motor_temp_label.pack(side=LEFT)
        self.motor_temp_label.configure(bg=self.motor_temp_frame["bg"], fg="white", font=self.font_titre)

        self.motor_temp_value_frame = Frame(self.master)
        self.motor_temp_value_frame.grid(column=6, row=2)
        self.motor_temp_value_frame.configure(bg="black")
        # self.motor_temp_value_frame.pack_propagate(0)

        self.motor_temp_value_label = Label(self.motor_temp_value_frame, text=self.motor_temp)
        self.motor_temp_value_label.pack()
        self.motor_temp_value_label.configure(bg=self.motor_temp_value_frame["bg"], fg="yellow", font=self.font_donnees)
        self.temp_frame = Frame(self.master)
        self.temp_frame.grid(column=7, row=2)
        self.temp_frame.configure(bg="black")
        # self.temp_frame.pack_propagate(0)
        self.temp_label = Label(self.temp_frame, text="°C")
        self.temp_label.pack(anchor="w", side=LEFT)
        self.temp_label.configure(bg=self.motor_temp_value_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # Distance

        self.distance_frame = Frame(self.master)
        self.distance_frame.grid(column=5, row=3)
        self.distance_frame.configure(bg="black")
        # self.distance_frame.pack_propagate(0)

        self.distance_label = Label(self.distance_frame, text="Distance")
        self.distance_label.pack(side=RIGHT)
        self.distance_label.configure(bg=self.distance_frame["bg"], fg="white", font=self.font_titre)

        self.distance_value_frame = Frame(self.master)
        self.distance_value_frame.grid(column=6, row=3)
        self.distance_value_frame.configure(bg="black")
        # self.distance_value_frame.pack_propagate(0)

        self.distance_value_label = Label(self.distance_value_frame, text=self.distance)
        self.distance_value_label.pack()
        self.distance_value_label.configure(bg=self.distance_value_frame["bg"], fg="yellow", font=self.font_donnees)
        self.distance_unit_frame = Frame(self.master)
        self.distance_unit_frame.grid(column=7, row=3)
        self.distance_unit_frame.configure(bg="black")
        # self.distance_unit_frame.pack_propagate(0)
        self.distance_unit_label = Label(self.distance_unit_frame, text="km")
        self.distance_unit_label.pack(anchor="w", side=LEFT)
        self.distance_unit_label.configure(bg=self.distance_unit_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # Efficiency

        self.efficiency_frame = Frame(self.master)
        self.efficiency_frame.grid(column=5, row=4)
        self.efficiency_frame.configure(bg="black")
        # self.efficiency_frame.pack_propagate(0)

        self.efficiency_label = Label(self.efficiency_frame, text="Efficiency")
        self.efficiency_label.pack(side=RIGHT)
        self.efficiency_label.configure(bg=self.efficiency_frame["bg"], fg="white", font=self.font_titre)

        self.efficiency_value_frame = Frame(self.master)
        self.efficiency_value_frame.grid(column=6, row=4)
        self.efficiency_value_frame.configure(bg="black")
        # self.efficiency_value_frame.pack_propagate(0)

        self.efficiency_value_label = Label(self.efficiency_value_frame, text=self.efficiency)
        self.efficiency_value_label.pack()
        self.efficiency_value_label.configure(bg=self.efficiency_value_frame["bg"], fg="yellow", font=self.font_donnees)
        self.efficiency_unit_frame = Frame(self.master)
        self.efficiency_unit_frame.grid(column=7, row=4)
        self.efficiency_unit_frame.configure(bg="black")
        # self.efficiency_unit_frame.pack_propagate(0)
        self.efficiency_unit_label = Label(self.efficiency_unit_frame, text="km/L")
        self.efficiency_unit_label.pack(anchor="w", side=LEFT)
        self.efficiency_unit_label.configure(bg=self.efficiency_unit_frame["bg"], fg="yellow",
                                             font=self.font_titre_donnees)

        # ICE Clutch n°2

        self.ice_clutch2_frame = Frame(self.master)
        self.ice_clutch2_frame.grid(column=4, row=5)
        self.ice_clutch2_frame.configure(bg="black")
        # self.ice_clutch2_frame.pack_propagate(0)

        self.ice_clutch2_label = Label(self.ice_clutch2_frame, text="ICE")
        self.ice_clutch2_label.pack(side=RIGHT)
        self.ice_clutch2_label.configure(bg=self.ice_clutch2_frame["bg"], fg="white", font=self.font_titre)

        self.ice_clutch2_frame = Frame(self.master)
        self.ice_clutch2_frame.grid(column=5, row=5)
        self.ice_clutch2_frame.configure(bg="black")
        # self.ice_clutch2_frame.pack_propagate(0)

        self.ice_clutch2_label = Label(self.ice_clutch2_frame, text="Clutch")
        self.ice_clutch2_label.pack(side=LEFT)
        self.ice_clutch2_label.configure(bg=self.ice_clutch2_frame["bg"], fg="white", font=self.font_titre)

        self.ice_clutch2_value_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                                             height=self.height_screen / 8 - self.space)
        self.ice_clutch2_value_frame.grid(column=6, row=5)

        self.ice_clutch2_value_frame.configure(bg=self.clutch2_background, highlightbackground=self.clutch2_contour,
                                               highlightthickness=2)
        self.ice_clutch2_value_frame.pack_propagate(0)

        self.ice_clutch2_value_label = Label(self.ice_clutch2_value_frame, text=self.clutch2_value, pady=100)
        self.ice_clutch2_value_label.pack()
        self.ice_clutch2_value_label.configure(bg=self.ice_clutch2_value_frame["bg"], fg="white",
                                               font=self.font_etat_clutch)

        # self.spacer ligne blanche

        self.spacer_frame = Frame(self.master, width=self.width_screen, height=5)
        self.spacer_frame.grid(column=0, row=6, columnspan=8)
        self.spacer_frame.configure(bg="white")

        # Fuel mode

        self.fuel_mode_frame = Frame(self.master)
        self.fuel_mode_frame.grid(column=1, row=7, rowspan=8)
        self.fuel_mode_frame.configure(bg=self.fuel_mode_background, highlightbackground=self.fuel_mode_contour,
                                       highlightthickness=2)
        # self.fuel_mode_frame.pack_propagate(0)

        self.fuel_label = Label(self.fuel_mode_frame, text="FUEL")
        self.fuel_label.pack()
        self.fuel_label.configure(bg=self.fuel_mode_frame["bg"], fg="white", font=self.font_titre_signaux)

        self.fuel_mode_label = Label(self.fuel_mode_frame, text=self.fuel_mode_value)
        self.fuel_mode_label.pack(expand=True)
        self.fuel_mode_label.configure(bg=self.fuel_mode_frame["bg"], fg="yellow", font=self.font_donnees)

        # SOC

        self.soc_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                               height=self.height_screen / 5 - self.space)
        self.soc_frame.grid(column=2, row=7, rowspan=8)
        self.soc_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.soc_frame.pack_propagate(0)

        self.soc_label = Label(self.soc_frame, text="SOC")
        self.soc_label.pack()
        self.soc_label.configure(bg=self.soc_frame["bg"], fg="white", font=self.font_titre_signaux)

        self.soc_value_label = Label(self.soc_frame, text="%s%s" % (self.soc, "%"))
        self.soc_value_label.pack(expand=True)
        self.soc_value_label.configure(bg=self.soc_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # LIPO

        self.lipo_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                                height=self.height_screen / 5 - self.space)
        self.lipo_frame.grid(column=3, row=7, rowspan=8)
        self.lipo_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.lipo_frame.pack_propagate(0)

        self.lipo_label = Label(self.lipo_frame, text="LIPO")
        self.lipo_label.pack()
        self.lipo_label.configure(bg=self.lipo_frame["bg"], fg="white", font=self.font_titre_signaux)

        self.lipo_value_label = Label(self.lipo_frame, text="%s%s" % (self.lipo, "%"))
        self.lipo_value_label.pack(expand=True)
        self.lipo_value_label.configure(bg=self.lipo_frame["bg"], fg="yellow", font=self.font_titre_donnees)

        # 3G

        self.connexion_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                                     height=self.height_screen / 8 - self.space)
        self.connexion_frame.grid(column=5, row=7)

        self.connexion_frame.configure(bg=self.etat_connexion_background)
        self.connexion_frame.pack_propagate(0)

        self.connexion_label = Label(self.connexion_frame, text="3G")
        self.connexion_label.pack(pady=0.5 * self.space)
        self.connexion_label.configure(bg=self.connexion_frame["bg"], fg=self.etat_connexion_label,
                                       font=self.font_titre_donnees)

        # GPS

        self.gps_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                               height=self.height_screen / 8 - self.space)
        self.gps_frame.grid(column=5, row=8)
        self.gps_frame.configure(bg=self.etat_gps_background)
        self.gps_frame.pack_propagate(0)

        self.gps_label = Label(self.gps_frame, text="GPS")
        self.gps_label.pack(pady=0.5 * self.space)
        self.gps_label.configure(bg=self.gps_frame["bg"], fg=self.etat_gps_label, font=self.font_titre_donnees)

        # Speed

        self.speed_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                                 height=self.height_screen / 8 - self.space)
        self.speed_frame.grid(column=6, row=7)
        self.speed_frame.configure(bg="black")
        self.speed_frame.pack_propagate(0)

        self.speed_label = Label(self.speed_frame, text="SPEED")
        self.speed_label.pack(anchor=NW, side=LEFT)
        self.speed_label.configure(bg=self.speed_frame["bg"], fg="white", font=self.font_titre)

        self.speed_value_frame = Frame(self.master)
        self.speed_value_frame.grid(column=6, row=8)
        self.speed_value_frame.configure(bg="black")
        # self.speed_value_frame.pack_propagate(0)

        self.speed_value_label = Label(self.speed_value_frame, text=self.speed)
        self.speed_value_label.pack(expand=True, anchor=E, pady=0.5 * self.space)
        self.speed_value_label.configure(bg=self.speed_value_frame["bg"], fg="yellow", font=self.font_vitesse)

        self.speed_unit_frame = Frame(self.master, width=self.width_screen / 8 - self.space,
                                      height=self.height_screen / 8 - self.space)
        self.speed_unit_frame.grid(column=7, row=8)
        self.speed_unit_frame.configure(bg="black")
        self.speed_unit_frame.pack_propagate(0)

        self.speed_unit_label = Label(self.speed_unit_frame, text="km/h")
        self.speed_unit_label.pack(expand=True, anchor=W)
        self.speed_unit_label.configure(bg=self.speed_unit_frame["bg"], fg="yellow", font=self.font_titre_donnees)
        self.update_test()
