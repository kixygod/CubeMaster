import tkinter as tk
import customtkinter as ctk
from tkinter import *
import random
import time


class ScrambleGenerator:
    def __init__(self):
        self.moves = ["U", "U'", "U2", "D", "D'", "D2", "R", "R'",
                      "R2", "L", "L'", "L2", "F", "F'", "F2", "B", "B'", "B2"]

    def generate_scramble(self):
        scramble = ""
        prev_move = ""
        for i in range(20):
            move = random.choice(self.moves)
            while move[0] == prev_move:
                move = random.choice(self.moves)
            scramble += move + " "
            prev_move = move[0]
        return scramble.strip()


class SpeedcubingApp:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.window = ctk.CTk()
        self.window.title("Speedcubing Timer")

        self.scramble_generator = ScrambleGenerator()
        self.scramble_label = ctk.CTkLabel(self.window, text="")
        self.scramble_label.pack()

        self.time_label = ctk.CTkLabel(
            self.window, text="00:00.000", font=("Arial", 70))
        self.time_label.pack()

        self.ao = ctk.CTkLabel(
            self.window, text="Your average time ", font=("Arial", 15))
        self.ao.pack()

        self.start_time = 0
        self.elapsed_time = 0
        self.results = []
        self.timer_running = False
        self.window.bind("<space>", self.toggle_timer)

        self.generate_scramble()
        self.scramble_label.after(0, self.generate_scramble)

        self.listbox = tk.Listbox(
            self.window, width=100, height=25, font=("Arial", 20), background='gray14', borderwidth=0, highlightthickness=0, selectbackground='gray14', fg='white')
        self.listbox.pack()

        self.scrollbar = tk.Scrollbar(self.window)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.window.mainloop()

    def add_solve(self, time):
        self.listbox.insert(tk.END, f"{self.listbox.size()+1} : {time}")

    def toggle_timer(self, event):
        if self.timer_running:
            self.stop_timer()
            self.generate_scramble()
        else:
            self.start_timer()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def average(self, lst):
        if len(lst) == 0:
            return str(0)
        else:
            av = sum(lst) / len(lst)
            self.ao.configure(text=f"Your average time {av:.3f}")

    def stop_timer(self):
        self.timer_running = False
        self.elapsed_time = time.time() - self.start_time
        time_str = self.format_time(self.elapsed_time)
        self.time_label.configure(text=time_str)
        self.results.append(self.elapsed_time)
        self.add_solve(time_str)
        self.average(self.results)

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            time_str = self.format_time(elapsed_time)
            self.time_label.configure(text=time_str)
            self.window.after(50, self.update_timer)

    def generate_scramble(self):
        scramble = self.scramble_generator.generate_scramble()
        self.scramble_label.configure(text=scramble, font=("Arial", 20))

    def format_time(self, elapsed_time):
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        millis = int((elapsed_time - seconds) * 1000) % 1000
        return f"{minutes:02d}:{seconds:02d}.{millis:03d}"


app = SpeedcubingApp()
