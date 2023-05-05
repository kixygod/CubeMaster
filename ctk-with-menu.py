import tkinter as tk
import customtkinter
import os
from PIL import Image
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


# class Card(customtkinter.CTk):
#     def __init__(self, master, image_path, title, text):
#         super().__init__()

#         rubik_path = os.path.join(os.path.dirname(
#             os.path.realpath(__file__)), "rubik")

#         # Создаем место для фотографии
#         self.image = customtkinter.CTkImage(
#             Image.open(os.path.join(rubik_path, image_path)))
#         # customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
#         self.image_label = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image, image_path)),
#                                                   dark_image=Image.open(os.path.join(self.image, image_path)), size=(30, 30))
#         self.image_label.pack()

#         # Создаем заголовок
#         self.title_label = customtkinter.CTkLabel(
#             self, text=title, font=(tuple, 16, "bold"))
#         self.title_label.pack(pady=10)

#         # Создаем текст
#         self.text_label = customtkinter.CTkLabel(
#             self, text=text, font=(tuple, 12))
#         self.text_label.pack()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CubeMaster")
        self.geometry("1280x720")
        self.minsize(1280, 720)
        self.maxsize(1280, 720)
        self.resizable(False, False)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "icons")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(
            image_path, "CustomTkinter_logo_single.png")), size=(26, 26))

        self.timer_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "timer_dark.png")),
                                                  dark_image=Image.open(os.path.join(image_path, "timer_light.png")), size=(20, 20))
        self.tutorial_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "tutorial_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "tutorial_light.png")), size=(20, 20))
        self.about_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "about_dark.png")),
                                                  dark_image=Image.open(os.path.join(image_path, "about_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  CubeMaster", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Timer",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.timer_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tutorial",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.tutorial_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="About",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.about_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(
            row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # create scramble label
        self.scramble_generator = ScrambleGenerator()
        self.scramble_label = customtkinter.CTkLabel(
            self.home_frame, text="123", text_color=("gray10", "gray90"), font=(tuple, 30))
        self.scramble_label.grid(row=0, column=0, sticky="ew", pady=40)
        self.generate_scramble()
        self.scramble_label.after(0, self.generate_scramble)

        # create time label
        self.time_label = customtkinter.CTkLabel(
            self.home_frame, text="00:00.000", font=(tuple, 100))
        self.time_label.grid(row=1, column=0, sticky="nsew", pady=200)
        self.ao = customtkinter.CTkLabel(
            self.home_frame, text="Your average time ", font=(tuple, 15))
        self.ao.grid(row=2, column=0, sticky="nsew")

        # create vars for ao and latest solves
        self.start_time = 0
        self.elapsed_time = 0
        self.results = []
        self.timer_running = False
        self.bind("<space>", self.toggle_timer)

        # create listbox with your time
        self.listbox = tk.Listbox(
            self.navigation_frame, width=15, height=25, font=(tuple, 15), background='gray14', borderwidth=0, highlightthickness=0, selectbackground='gray14', fg='white')
        self.listbox.grid(row=4, column=0, sticky="ew")
        self.scrollbar = tk.Scrollbar(self.navigation_frame)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.upload_solves()

        # create second frame
        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        # rur = Card(self.second_frame, "rur.png", "R U R'", "123")
        # rur.pack()

        # create third frame
        self.third_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)
        self.about_title = customtkinter.CTkLabel(
            self.third_frame, text="CubeMaster", font=(tuple, 40), pady=40)
        self.about_title.grid(row=0, column=0, sticky="nsew")
        self.about_text = customtkinter.CTkLabel(
            self.third_frame, text=f"Добро пожаловать в приложение для сборки кубика!\nЭто приложение было создано на языке Python с использованием библиотеки Tkinter.\nОно предназначено для помощи в сборке кубика Рубика.\nВ приложении есть таймер, который позволяет отслеживать время, затраченное на сборку кубика.\nТаймер можно запустить и остановить в любой момент, а также сбросить его, чтобы начать заново.\nДостаточно просто нажать на пробел.\n Этот проект был создан в рамках учебного курса 'Объектно-ориентированное программирование'.\nОн помог мне лучше понять принципы ООП и научиться применять их на практике.\nНадеюсь, что это приложение поможет вам собрать кубик Рубика быстрее и более эффективно.\nСпасибо за использование моего приложения!", font=(tuple, 20))
        self.about_text.grid(row=1, column=0)

        # select default frame
        self.select_frame_by_name("home")

    # generate scramble
    def generate_scramble(self):
        scramble = self.scramble_generator.generate_scramble()
        self.scramble_label.configure(text=scramble, font=(tuple, 30))

    # add solve to the file and table
    def add_solve(self, time):
        self.file = open("solves.txt", "a+")
        self.file.write(f"{self.listbox.size()+1} : {time}\n")
        self.listbox.insert(tk.END, f"{self.listbox.size()+1} : {time}")

    # upload all solves from file to the app
    def upload_solves(self):
        with open("solves.txt", "r") as file:
            # Читаем строки из файла и добавляем их в Listbox
            for line in file:
                self.listbox.insert(tk.END, line.strip())

    # func for start/stop timer
    def toggle_timer(self, event):
        if self.timer_running:
            self.stop_timer()
            self.generate_scramble()
        else:
            self.start_timer()

    # start time
    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    # func to get average of all your solves
    def average(self, lst):
        if len(lst) == 0:
            return str(0)
        else:
            av = sum(lst) / len(lst)
            self.ao.configure(text=f"Your average time {av:.3f}")

    # stop time
    def stop_timer(self):
        self.timer_running = False
        self.elapsed_time = time.time() - self.start_time
        time_str = self.format_time(self.elapsed_time)
        self.time_label.configure(text=time_str)
        self.results.append(self.elapsed_time)
        self.add_solve(time_str)
        self.average(self.results)

    # update timer in real time
    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            time_str = self.format_time(elapsed_time)
            self.time_label.configure(text=time_str)
            self.home_frame.after(50, self.update_timer)

    # to render time on screen
    def format_time(self, elapsed_time):
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        millis = int((elapsed_time - seconds) * 1000) % 1000
        return f"{minutes:02d}:{seconds:02d}.{millis:03d}"

    # func to switch between screens
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    # open home
    def home_button_event(self):
        self.select_frame_by_name("home")

    # open second screen
    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    # open third screen
    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    # func to change theme
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
