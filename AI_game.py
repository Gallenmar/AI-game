import tkinter as tk
from tkinter import ttk

import random
import MiniMaksa
import alphaBeta
from spele import evaluate_turn


def widget_cleanup_decorator(func):
    def wrapper(self, *args, **kwargs):
        for widget in self.master.winfo_children():
            widget.destroy()
        result = func(self, *args, **kwargs)
        return result
    return wrapper

def add_back_button_decorator(func):
    def wrapper(self, *args, **kwargs):
        self.back_button = ttk.Button(self.master, text="Uz sākumu", style="Back.TButton", command=self.main_view)
        self.back_button.place(relx=0, rely=0, anchor="nw")
        result = func(self, *args, **kwargs)
        return result
    return wrapper

class HandleViewsMeta(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and attr_name.find("view") != -1:
                attrs[attr_name] = widget_cleanup_decorator(attr_value)

            if callable(attr_value) and attr_name.find("view") != -1 and attr_name.startswith("main_view") != True:
                attrs[attr_name] = widget_cleanup_decorator(add_back_button_decorator(attr_value))

        return super().__new__(cls, name, bases, attrs)


class AI_Game(metaclass=HandleViewsMeta):
    def __init__(self, master):
        self.master = master
        self.master.title("Mākslīgā intelekta spēle")
        self.master.maxsize(800, 600)
        self.master.geometry("800x600")
        self.master.configure(bg="#ffffff")

        self.style = ttk.Style()
        self.style.configure(
            "Title.TLabel",
            foreground="midnight blue",
            background="white",
            font=("Helvetica", 24, "bold"),
            padding=10
        )
        self.style.configure(
            "Info.TLabel",
            foreground="black",
            background="white",
            font=("Helvetica", 12),
            padding=10
        )
        self.style.configure(
            "Main.TButton",
            foreground="midnight blue",
            background="white",
            font=("Helvetica", 16, "bold"),
            padding=10
        )
        self.style.configure(
            "Back.TButton",
            foreground="red",
            background="white",
            font=("Helvetica", 16, "bold"),
            padding=10
        )
        
        self.human_number = 0
        self.human_points = 0
        self.computer_points = 0
        self.bank_points = 0
        self.current_number = 0
        self.dzilums = 7

        self.alpha_beta_human_number_input_flag = False
        self.min_max_human_number_input_flag = False

        self.main_view()

    def main_view(self):
        self.cleanup_game()

        self.title_label = ttk.Label(self.master, text="Grupas 38 spēle", style="Title.TLabel")
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")

        self.title_label = ttk.Label(self.master, text="Spēle realizēta ar min/max un alpha/beta algoritmiem", style="Info.TLabel")
        self.title_label.place(relx=0.5, rely=0.4, anchor="center")

        self.choose_game_mode_button = ttk.Button(self.master, text="Izvēlēties spēles viedu", style="Main.TButton", command=self.choose_game_mode_view)
        self.choose_game_mode_button.place(relx=0.5, rely=0.5, anchor="center")

        self.settings_button = ttk.Button(self.master, text="Iestatījumi", style="Main.TButton", command=self.settings_view)
        self.settings_button.place(relx=0.5, rely=0.6, anchor="center")

    def choose_game_mode_view(self):
        self.gamemode_label = ttk.Label(self.master, text="Izvēlēties spēles veidu", style="Info.TLabel")
        self.gamemode_label.place(relx=0.5, rely=0.3, anchor="center")

        self.alpha_beta_button = ttk.Button(self.master, text="Alpha/Beta", style="Main.TButton", command=self.alpha_beta_view)
        self.alpha_beta_button.place(relx=0.3, rely=0.5, anchor="center")

        self.min_max_button = ttk.Button(self.master, text="Min/Max", style="Main.TButton", command=self.min_max_view)
        self.min_max_button.place(relx=0.7, rely=0.5, anchor="center")

    def settings_view(self):
        self.dark_mode_button = ttk.Button(self.master, text="Tumšais režīms", style="Main.TButton", command=self.handle_dark_mode)
        self.dark_mode_button.place(relx=0.5, rely=0.5, anchor="center")

    def handle_dark_mode(self):
        self.master.configure(bg="#696969")
        self.style.configure(
            "Title.TLabel",
            foreground="#7E8EFA",
            background="#68696E",
            font=("Helvetica", 24, "bold"),
            padding=10
        )
        self.style.configure(
            "Info.TLabel",
            foreground="#BDC5FC",
            background="#68696E",
            font=("Helvetica", 12),
            padding=10
        )
        self.style.configure(
            "Main.TButton",
            foreground="#7E8EFA",
            background="#68696E",
            font=("Helvetica", 16, "bold"),
            padding=10
        )
        self.style.configure(
            "Back.TButton",
            foreground="#FB0303",
            background="#68696E",
            font=("Helvetica", 16, "bold"),
            padding=10
        )


    def alpha_beta_view(self):
        self.current_number_display = tk.StringVar()
        self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))

        self.human_number_display = tk.StringVar()
        self.human_number_display.set("Izvēlētais skaitlis ir: " + str(self.human_number))
        
        self.current_number_label = ttk.Label(self.master, textvariable=self.current_number_display, style="Info.TLabel")
        self.current_number_label.place(relx=0.8, rely=0.1, anchor="center")

        self.human_number_input_label = ttk.Label(self.master, text="Izvēlieties skaitli no 25 līdz 40", style="Info.TLabel")
        self.human_number_input_label.place(relx=0.5, rely=0.2, anchor="center")

        self.human_number_label = ttk.Label(self.master, textvariable=self.human_number_display, style="Info.TLabel")
        self.human_number_label.place(relx=0.1, rely=0.2, anchor="center")

        self.human_number_input = tk.Scale(self.master, from_=25, to=40, orient=tk.HORIZONTAL, length=300)
        self.human_number_input.place(relx=0.5, rely=0.3, anchor="center")

        self.multiplier_input_label = ttk.Label(self.master, text="Izvēlieties ar ko reizināt (2, 3 vai 4)", style="Info.TLabel")
        self.multiplier_input_label.place(relx=0.5, rely=0.4, anchor="center")

        self.multiplier_input = tk.Scale(self.master, from_=2, to=4, orient=tk.HORIZONTAL, length=300)
        self.multiplier_input.place(relx=0.5, rely=0.5, anchor="center")

        self.user_submit_button = ttk.Button(self.master, text="Ievadīt", style="Main.TButton", command=self.handle_alpha_beta)
        self.user_submit_button.place(relx=0.5, rely=0.6, anchor="center")

        self.alpha_beta_text_box = tk.Text(self.master, width=90, height=10, bd=1, relief="solid")
        self.alpha_beta_text_box.insert(tk.END, "Spēles gaita")
        self.alpha_beta_text_box.place(relx=0.5, rely=0.8, anchor="center")

    def min_max_view(self):
        self.current_number_display = tk.StringVar()
        self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
        
        self.human_number_display = tk.StringVar()
        self.human_number_display.set("Izvēlētais skaitlis ir: " + str(self.human_number))

        self.current_number_label = ttk.Label(self.master, textvariable=self.current_number_display, style="Info.TLabel")
        self.current_number_label.place(relx=0.8, rely=0.1, anchor="center")

        self.human_number_input_label = ttk.Label(self.master, text="Izvēlieties skaitli no 25 līdz 40", style="Info.TLabel")
        self.human_number_input_label.place(relx=0.5, rely=0.2, anchor="center")

        self.human_number_label = ttk.Label(self.master, textvariable=self.human_number_display, style="Info.TLabel")
        self.human_number_label.place(relx=0.1, rely=0.2, anchor="center")

        self.human_number_input = tk.Scale(self.master, from_=25, to=40, orient=tk.HORIZONTAL, length=300)
        self.human_number_input.place(relx=0.5, rely=0.3, anchor="center")

        self.multiplier_input_label = ttk.Label(self.master, text="Izvēlieties ar ko reizināt (2, 3 vai 4)", style="Info.TLabel")
        self.multiplier_input_label.place(relx=0.5, rely=0.4, anchor="center")

        self.multiplier_input = tk.Scale(self.master, from_=2, to=4, orient=tk.HORIZONTAL, length=300)
        self.multiplier_input.place(relx=0.5, rely=0.5, anchor="center")

        self.user_submit_button = ttk.Button(self.master, text="Ievadīt", style="Main.TButton", command=self.handle_min_max)
        self.user_submit_button.place(relx=0.5, rely=0.6, anchor="center")

        self.min_max_text_box = tk.Text(self.master, width=90, height=10, bd=1, relief="solid")
        self.min_max_text_box.insert(tk.END, "Spēles gaita")
        self.min_max_text_box.place(relx=0.5, rely=0.8, anchor="center")

    def handle_alpha_beta(self):
        if self.alpha_beta_human_number_input_flag == False:
            self.human_number = int(self.human_number_input.get())
            self.human_number_display.set("Izvēlētais skaitlis ir: " + str(self.human_number))
            self.current_number = self.human_number
            self.alpha_beta_human_number_input_flag = True

        self.handle_game_logic("alpha_beta", self.alpha_beta_text_box)

    def handle_min_max(self):
        if self.min_max_human_number_input_flag == False:
            self.human_number = int(self.human_number_input.get())
            self.human_number_display.set("Izvēlētais skaitlis ir: " + str(self.human_number))
            self.current_number = self.human_number
            self.min_max_human_number_input_flag = True

        self.handle_game_logic("min_max", self.min_max_text_box)

    def handle_game_logic(self, gamemode, text_box):
        self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
        self.multiplier = int(self.multiplier_input.get())
        text_box.insert(tk.END, "\nCilvēks izvēlējās reizināt ar: " + str(self.multiplier))

        self.current_number *= self.multiplier
        text_box.insert(tk.END, "\nPašreizējais skaitlis: : " + str(self.current_number))

        if self.current_number % 2 == 0:
            self.human_points -= 1
        else:
            self.human_points += 1

        if self.current_number % 10 == 0 or self.current_number % 10 == 5:
            self.bank_points += 1

        text_box.insert(tk.END, "\nCilvēka punkti: " + str(self.human_points))
        text_box.insert(tk.END, "\nDatora punkti: " + str(self.computer_points))
        text_box.insert(tk.END, "\nBankas punkti: " + str(self.bank_points))
        text_box.see("end")

        # self.evaluation_result = evaluate_turn(self.current_number, self.human_points, self.computer_points, self.bank_points)
        # if self.evaluation_result == -1:
        #     text_box.insert(tk.END, "\nGājiens bija slikts.")
        # elif self.evaluation_result == 0:
        #     text_box.insert(tk.END, "\nGājiens bija viduvējs.")
        # else:
        #     text_box.insert(tk.END, "\nGājiens bija labs.")

        self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
        if self.current_number >= 5000:
            self.end_round(text_box, False)
            self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
            return

        text_box.insert(tk.END, "\nDatora gājiens.")
        
        if gamemode == "alpha_beta":
            self.computer_multiplier = alphaBeta.AlphaBetaIzvele(self.current_number, self.human_points, self.computer_points, self.bank_points, self.dzilums)

        if gamemode == "min_max":
            self.computer_multiplier = MiniMaksa.MiniMaxIzvele(self.current_number, self.human_points, self.computer_points, self.bank_points, self.dzilums)

        text_box.insert(tk.END, "\nDators izvēlējās reizināt ar: " + str(self.computer_multiplier))
        self.current_number *= self.computer_multiplier
        text_box.insert(tk.END, "\nPašreizējais skaitlis: : " + str(self.current_number))
        

        if self.current_number % 2 == 0:
            self.computer_points -= 1
        else:
            self.computer_points += 1

        if self.current_number % 10 == 0 or self.current_number % 10 == 5:
            self.bank_points += 1

        text_box.insert(tk.END, "\nCilvēka punkti: " + str(self.human_points))
        text_box.insert(tk.END, "\nDatora punkti: " + str(self.computer_points))
        text_box.insert(tk.END, "\nBankas punkti: " + str(self.bank_points))
        text_box.see("end")

        # self.evaluation_result = evaluate_turn(self.current_number, self.human_points, self.computer_points, self.bank_points)
        # if self.evaluation_result == -1:
        #     text_box.insert(tk.END, "\nDatora gājiens bija slikts.")
        # elif self.evaluation_result == 0:
        #     text_box.insert(tk.END, "\nDatora gājiens bija viduvējs.")
        # else:
        #     text_box.insert(tk.END, "\nDatora gājiens bija labs.")

        self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
        if self.current_number >= 5000:
            self.end_round(text_box, True)
            self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
            return
        text_box.see("end")

    def end_round(self, text_box, computer_win):
        if computer_win:
            self.computer_points += self.bank_points
        else:
            self.human_points += self.bank_points

        text_box.insert(tk.END, "\nBeigas!")
        text_box.insert(tk.END, "\nCilvēka punkti: " + str(self.human_points))
        text_box.insert(tk.END, "\nDatora punkti: " + str(self.computer_points))

        if self.human_points > self.computer_points:
            text_box.insert(tk.END, "\nCilvēks uzvar!")
        elif self.human_points < self.computer_points:
            text_box.insert(tk.END, "\nDators uzvar!")
        else:
            text_box.insert(tk.END, "\nNeizšķirts rezultāts!")

        text_box.insert(tk.END, "\n-----------------\n")
        self.cleanup_game()
        self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
        self.human_number_display.set("Izvēlētais skaitlis ir: " + str(self.human_number))
        text_box.see("end")

    def cleanup_game(self):
        self.human_number = 0
        self.human_points = 0
        self.computer_points = 0
        self.bank_points = 0
        self.current_number = 0
        self.alpha_beta_human_number_input_flag = False
        self.min_max_human_number_input_flag = False


root = tk.Tk()
ai_game = AI_Game(root)
root.mainloop()