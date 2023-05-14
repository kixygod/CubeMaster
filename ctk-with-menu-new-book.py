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


class Card(customtkinter.CTkFrame):
    def __init__(self, master, image_name, text):
        super().__init__(master)
        rubik_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "rubik")
        self.image = customtkinter.CTkImage(light_image=Image.open(os.path.join(rubik_path, image_name)),
                                            dark_image=Image.open(os.path.join(rubik_path, image_name)), size=(60, 60))
        # self.label_image = tk.Label(self, image=self.image)
        self.label_image = customtkinter.CTkButton(self.master, corner_radius=0, height=0, border_spacing=10, text=text, font=(tuple, 20),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.image, anchor="n")
        self.label_image.pack()


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        if image == None:
            label = customtkinter.CTkLabel(
                self, text=item, font=(tuple, 30), image=image, compound="left", padx=5, anchor="w")
        else:
            label = customtkinter.CTkLabel(
                self, text=item, font=(tuple, 20), image=image, compound="left", padx=5, anchor="w")
        # button = customtkinter.CTkButton(
        #     self, text="Command", width=100, height=24)
        label.grid(row=len(self.label_list),
                   column=0, pady=(0, 10), sticky="w")
        # button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        # self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


class ScrollingFrame(customtkinter.CTkFrame):
    def __init__(self, master, images):
        super().__init__(master)
        self.canvas = customtkinter.CTkCanvas(self)
        self.scrollbar = customtkinter.CTkScrollbar(
            self, command=self.canvas.yview)
        self.scrollable_frame = customtkinter.CTkFrame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        for image in images:
            image_label = Card(
                self.scrollable_frame, image["path"], image["text"])
            # image_label.pack(pady=0)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


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
            self.navigation_frame, width=15, height=25, font=(tuple, 15), background='gray20', borderwidth=0, highlightthickness=0, selectbackground='gray14', fg='white')
        self.listbox.grid(row=4, column=0, sticky="ew")
        self.scrollbar = tk.Scrollbar(self.navigation_frame)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.upload_solves()

        # create second frame
        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")

        self.images = [["rur.png", "R U R'"], ["fuf.png", "F' U' F"], ["urur.png", "U R U' R'"],
                       ["ufuf.png", "U' F' U F"],
                       ["urururur.png", "(U' R U') (R' U R) U R'"],
                       ["ufufufuf.png", "(U F' U) (F U' F') U' F"],
                       ["urururur'.png", "(U' R U) (R' U R) U R'"],
                       ["ufufufuf'.png", "(U F' U') (F U' F') U' F"], [
            "dru2rdrur.png", "d (R' U2 R) d' (R U R')"],
            ["uru2rdrur.png", "U' (R U2 R') d (R' U' R)"], [
            "rurudrur'.png", "(R U' R' U) d (R' U' R)"],
            ["fufudfuf'.png", "(F' U F U') d' (F U F')"], [
            "ufu2fufu2f'.png", "(U F' U2 F) (U F' U2 F)"],
            ["uru2ruru2r'.png", "(U' R U2 R') (U' R U2 R')"], [
            "ufufufu2f.png", "(U F' U' F) (U F' U2 F)"],
            ["urururu2r'.png", "(U' R U R') (U' R U2 R')"],
            ["ru2r'u'rur'.png", "(R U2 R' U') (R U R')"],
            ["f'u2fuf'u'f.png", "(F' U2 F U) (F' U' F)"],
            ["uru2r'uru'r'.png", "(U R U2 R') (U R U' R')"],
            ["u'f'u2fu'f'uf.png", "(U' F' U2 F) (U' F' U F)"],
            ["u2rur'uru'r'.png", "U2 (R U R' U) (R U' R')"],
            ["u2f'u'fu'f'uf.png", "U2 (F' U' F U') (F' U F)"],
            ["rur'u'u'rur'u'rur'.png", "(R U R' U') U' (R U R' U') (R U R')"],
            ["y'r'u'ruur'u'rur'u'r.png",
                "y' (R' U' R U) U (R' U' R U) (R' U' R)"],
            ["uf'ufuf'u2f.png", "(U F' U F) (U F' U2 F)"],
            ["u'ru'r'u'ru2r'.png", "(U' R U' R') (U' R U2 R')"],
            ["uf'u'fd'fuf'.png", "(U F' U' F) (d' F U F')"],
            ["u'rur'dr'u'r.png", "(U' R U R') (d R' U' R)"],
            ["ru'r'dr'ur.png", "(R U' R') (d R' U R)"],
            ["rur'u'rur'u'rur'.png", "(R U R' U') (R U R' U') (R U R')"],
            ["uru'r'u'f'uf.png", "(U R U' R') (U' F' U F)"],
            ["u'f'ufuru'r'.png", "(U' F' U F) (U R U' R')"],
            ["f'ufu'f'uf.png", "(F' U F) (U' F' U F)"],
            ["ru'r'uru'r'.png", "(R U' R') (U R U' R')"],
            ["rur'u'rur'.png", "(R U R') (U' R U R')"],
            ["f'u'fuf'u'f.png", "(F' U' F) (U F' U' F)"],
            ["ru'r'uru2r'uru'r.png", "(R U' R' U) R U2 R' (U R U' R')"],
            ["ru'r'u'rur'u'ru2r'.png", "(R U' R' U') (R U R' U') (R U2 R')"],
            ["rur'u'ru'r'udr'u'r.png", "(R U R' U') (R U' R') U d (R' U' R)"],
            ["ru'r'dr'u'ru'r'u'r.png", "(R U' R') d (R' U' R U') (R' U' R)"],
            ["ru'r'dr'u2rur'u2r.png", "(R U' R' d R' U2 R) (U R' U2 R)"],
            ["r'u2rur'ur.png", "(R' U2 R) U (R' U R)"],
            ["ru2r'u'ru'r'.png", "(R U2 R') U' (R U' R')"],
            ["f'rur'u'r'fr.png", "F' (r U R' U') (r' F R)"],
            ["rur'u'r'frf'.png", "(r U R' U') (r' F R F')"],
            ["ru2r2'u'r2u'r2'u2r.png", "R U2 (R2' U' R2 U') (R2' U2 R)"],
            ["rur'uru'r'uru2r'.png", "(R U R') U (R U' R') U (R U2 R')"],
            ["r2dr'u2rd'r'u2r'.png", "R2 D (R' U2 R) D' (R' U2 R')"],
            ["ru2r'r'frf'u2r'frf'.png",
                "(R U2 R') (R' F R F') U2 (R' F R F')"],
            ["frur'u'f'frur'u'f'.png", "F (R U R' U') F' f (R U R' U') f'"],
            ["frur'u'f'ufrur'u'f'.png", "f (R U R' U') f' U F (R U R' U') F'"],
            ["frur'u'f'u'frur'u'f'.png",
                "f (R U R' U') f' U' F (R U R' U') F'"],
            ["murur'u'm'r'frf'.png", "M U (R U R' U') M' (R' F R F')"],
            ["frur'uy'r'u2r'frf'.png", "F (R U R' U) y' R' U2 (R' F R F')"],
            ["rur'ur'frf'u2r'frf'.png",
                "(R U R' U) (R' F R F') U2 (R' F R F')"],
            ["murur'u'm2uru'r'.png", "M U (R U R' U') M2 (U R U' r')"],
            ["rur'u'm'uru'r'.png", "(R U R' U') M' (U R U' r')"],
            ["m'u'mu2'm'u'm.png", "M' U' M U2' M' U' M"],
            ["ru2'r2u'ru'r'u2frf'.png", "R U2 R2 (U' R U' R') U2 (F R F')"],
            ["rur'urd'ru'r'f'.png", "(R U R' U) R d' R U' R' F'"],
            ["frur'u'rur'u'f'.png", "f (R U R' U') (R U R' U') f'"],
            ["frur'u'rf'rur'u'r'.png", "F (R U R' U') R F' (r U R' U') r'"],
            ["frur'u'f'.png", "F (R U R' U') F'"],
            ["rur'u'r'frf''.png", "(R U R' U') (R' F R F')"],
            ["r'frur'u'f'ur.png", "R' F (R U R' U') F' U R"],
            ["lf'l'u'lufu'l'.png", "L F' (L' U' L U) F U' L'"],
            ["r'frur'f'ry'ru'r'.png", "(R' F R) U (R' F' R) y' (R U' R')"],
            ["furu'r2f'ruru'r'.png", "F (U R U' R2) F' (R U R U' R')"],
            ["rur'rur'u'ru'r'.png", "r U r' (R U R' U') r U' r'"],
            ["i'u'i;'u';ui'ui.png", "l' U' l (L' U' L U) l' U l"],
            ["r'u'r'frf'ur.png", "R' U' (R' F R F') U R"],
            ["rur'u'xd'r'uru'dx'.png", "(R U R' U') x D' R' U R U' D x'"],
            ["rur'uru'r'u'r'frf'.png", "(R U R' U) (R U' R' U') (R' F R F')"],
            ["l'u'lu'l'ululf'l'f.png", "(L' U' L U') (L' U L U) (L F' L' F)"],
            ["frur'u'f''.png", "f (R U R' U') f'"],
            ["f'l'u'luf.png", "f' (L' U' L U) f"],
            ["r'u'furu'r'f'r.png", "R' U' F U R U' R' F' R"],
            ["furu'f'rur'u'r'.png", "F U R U' F' r U R' U' r'"],
            ["ru2r'r'frf'ru2r'.png", "(R U2 R') (R' F R F') (R U2 R')"],
            ["fr'f'ruru'r'.png", "F R' F' R U R U' R'"],
            ["r'u2rur'ur''.png", "r' U2 (R U R' U) r"],
            ["ru2r'u'ru'r''.png", "r U2 R' U' R U' r'"],
            ["frur'u'rur'u'f''.png", "F (R U R' U') (R U R' U') F'"],
            ["f'l'u'lul'u'luf.png", "F' (L' U' L U) (L' U' L U) F"],
            ["r'fr2b'r2'f'r2br'.png", "R' F R2 B' R2' F' R2 B R'"],
            ["r'fr'f'r2u2yr'frf'.png", "(R' F R' F') R2 U2 y (R' F R F')"],
            ["l'u'lu'l'ulu'l'u2l.png", "(l' U' L U') (L' U L U') L' U2 l"],
            ["rur'uru'r'uru2'r'.png", "(r U R' U) (R U' R' U) R U2' r'"],
            ["f'l'u'lufyfrur'u2'f'.png",
                "F' (L' U' L U) F y F (R U R' U') F'"],
            ["frur'u'f'ufrur'u'f''.png",
                "F (R U R' U') F' U F (R U R' U') F'"],
            ["rur'uru2r'.png", "(r U R' U) R U2 r'"],
            ["r'u'ru'r'u2r.png", "r' U' R U' R' U2 r"],
            ["rur'ur'frf'ru2r'.png", "(R U R' U) (R' F R F') R U2 R'"],
            ["rur'u'r'fr2ur'u'f'.png", "(R U R' U') R' F R2 U R' U' F'"],
            ["rur'u'ru'r'f'u'frur'.png",
                "(R U R' U') R U' R' F' U' (F R U R')"],
            ["r'frf'r'frf'rur'u'rur'.png",
                "(R' F R F') (R' F R F') (R U R' U') (R U R')"],
            ["rur'uru2r'frur'u'f'.png", "(R U R' U) R U2 R' F (R U R' U') F'"],
            ["lf'l'fl'u2ldrur'.png", "(L F' L' F) L' U2 L d (R U R')"],
            ["m2um2u2m2um2.png", "(M2 U M2) U2 (M2 U M2)"],
            ["r'u'r2urur'u'ruru'ru'r'u2.png",
                "R' U' R2 U (R U R' U') R U R U' R U' R' U2"],
            ["r2u'r'u'rururu'r.png", "R2 U' (R' U' R) U R U (R U' R)"],
            ["r'ur'u'r'u'r'urur2.png", "(R' U R' U') R' U' (R' U R) U R2"],
            ["xz'r2u2r'd'ru2r'dr'zx'.png",
                "x z' R2 U2 (R' D' R) U2 (R' D R') z x'"],
            ["xr2d2rur'd2ru'rx'.png", "x R2 D2 (R U R') D2 (R U' R) x'"],
            ["r2ur'u'yrur'u'rur'u'rur'y'ru'r2'.png",
                "R2 U R' U' y (R U R' U') (R U R' U') (R U R') y' (R U' R2')"],
            ["rur'u'r'fr2u'r'u'rur'f'.png",
                "(R U R' U') R' F R2 U' R' U' R U R' F'"],
            ["fru'r'u'rur'f'rur'u'r'frf'.png",
                "(F R U' R') U' (R U R' F') (R U R' U') (R' F R F')"],
            ["u'r'uru'r2f'u'fuxrur'u'r2x'.png",
                "U' (R' U R U') R2 (F' U' F U) x (R U R' U') R2 x'"],
            ["r'ur'u'yr'dr'd'r2y2'r'b'rbr.png",
                "(R' U R' U') y (R' D R' D') R2 y' (R' B' R B R)"],
            ["l'u'lfl'u'lulf'l2ulu.png",
                "L' U' L F (L' U' L U) L F' L2 U L U"],
            ["ruru'f'rur'u'r'fr2u'r'u'.png",
                "R U R' F' (R U R' U') R' F R2 U' R' U'"],
            ["lu2l'u2lf'l'u'lulfl2u.png",
                "(L U2 L') U2 L F' (L' U' L U) L F L2 U"],
            ["r'u2ru2r'frur'u'r'f'r2u'.png",
                "(R' U2 R) U2 R' F (R U R' U') R' F' R2 U'"],
            ["rur'urur'f'rur'u'r'fr2u'r'u2ru'r'.png",
                "(R U R' U) (R U R' F') (R U R' U') R' F R2 U' R' U2 (R U' R')"],
            ["r'uru'r'f'u'frur'fr'f'ru'r.png",
                "(R' U R U') R' (F' U' F) (R U R' F) R' F' (R U' R)"],
            ["yr2'ur'ur'u'ru'r2y'r'ur.png",
                "y R2' u (R' U R' U') (R u' R2) y' (R' U R)"],
            ["r'u'ryr2ur'uru'ru'r2.png",
                "(R' U' R) y R2 u (R' U R U') (R u' R2)"],
            ["yr2'u'ru'rur'ur2yru'r'.png",
                "y R2' u' R U' (R U R' u) R2 y (R U' R')"],
            ["y2rur'y'r2u'ru'r'ur'ur2.png",
                "y2 (R U R') y' (R2 u' R) U' (R' U R') u R2"]
        ]
        self.titles = ["F2L", "1. Basic cases", "2. Corner and edge in top", "3. Corner pointing up, edge in top",
                       "4. Corner in top, edge in middle", "5. Corner in bottom, edge in top", "6. Corner in bottom, edge in middle", "OLL", "Crosses", "Dots", "All Corners", "Lines", "Ts", "Zs", "Big Ls", "Cs", "Ws", "Ps", "Squares", "Little Ls", "Other shapes", "PLL", "Edges only", "Corners only", "Edges and corners"]

        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(
            self.second_frame, corner_radius=0)
        self.scrollable_label_button_frame.pack(expand=True, fill="both")

        self.title_index = 0

        self.scrollable_label_button_frame.add_item(
            self.titles[self.title_index], image=None)
        self.title_index += 1

        for i in range(len(self.images)):
            if i in [0, 4, 16, 24, 30, 36, 41, 48, 56, 58, 62, 64, 66, 70, 72, 74, 78, 82, 88, 98, 102, 105]:
                if i in [41, 98]:
                    self.scrollable_label_button_frame.add_item(
                        self.titles[self.title_index], image=None)
                    self.title_index += 1
                self.scrollable_label_button_frame.add_item(
                    self.titles[self.title_index], image=None)
                self.title_index += 1
            self.scrollable_label_button_frame.add_item(self.images[i][1], image=customtkinter.CTkImage(
                Image.open(os.path.join(current_dir, "rubik", self.images[i][0])), size=(80, 80)))
            print(i)

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
        if customtkinter.get_appearance_mode() == "Light":
            self.listbox.config(background='gray90', fg='black')
        elif customtkinter.get_appearance_mode() == "System":
            if customtkinter.get_appearance_mode() == "Light":
                self.listbox.config(background='gray90', fg='black')
            else:
                self.listbox.config(background='gray20', fg='white')
        else:
            self.listbox.config(background='gray20', fg='white')


if __name__ == "__main__":
    app = App()
    app.mainloop()
