import tkinter as tk
from tkinter import ttk

import random
import MiniMaksa
import alphaBeta
# from spele import evaluate_turn


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

        self.style = ttk.Style()
        self.handle_light_mode()

        self.human_number = 0
        self.human_points = 0
        self.computer_points = 0
        self.bank_points = 0
        self.current_number = 0
        self.dzilums = 7

        self.alpha_beta_human_number_input_flag = False
        self.min_max_human_number_input_flag = False
        self.turn_order = "human"

        self.main_view()
    
    def handle_light_mode(self):
        self.mode = "light"
        self.master.configure(bg="#ffffff")
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
            "Winner.TLabel",
            foreground="blue",
            background="white",
            font=("Helvetica", 16, "bold"),
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
        self.settings_view()

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
        if (self.mode == "light"):
            self.dark_mode_button = ttk.Button(self.master, text="Tumšais režīms", style="Main.TButton", command=self.handle_dark_mode)
            self.dark_mode_button.place(relx=0.5, rely=0.5, anchor="center")
            
        elif (self.mode == "dark"):
            self.dark_mode_button = ttk.Button(self.master, text="Gaišais režīms", style="Main.TButton", command=self.handle_light_mode)
            self.dark_mode_button.place(relx=0.5, rely=0.5, anchor="center")
            

    def handle_dark_mode(self):
        self.mode = "dark"
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
        self.settings_view()

    def game_display_layout(self):
        self.current_number_display = tk.StringVar()
        self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
        
        self.current_number_label = ttk.Label(self.master, textvariable=self.current_number_display, style="Info.TLabel")
        self.current_number_label.place(relx=0.2, rely=0.2, anchor="center")

        self.human_points_display = tk.StringVar()
        self.human_points_display.set("Cilvēka punkti: " + str(self.human_points))
        
        self.human_points_label = ttk.Label(self.master, textvariable=self.human_points_display, style="Info.TLabel")
        self.human_points_label.place(relx=0.2, rely=0.4, anchor="center")

        self.computer_points_display = tk.StringVar()
        self.computer_points_display.set("Datora punkti: " + str(self.computer_points))
        
        self.computer_points_label = ttk.Label(self.master, textvariable=self.computer_points_display, style="Info.TLabel")
        self.computer_points_label.place(relx=0.2, rely=0.5, anchor="center")

        self.bank_points_display = tk.StringVar()
        self.bank_points_display.set("Punkti bankā: " + str(self.bank_points))
        
        self.bank_points_label = ttk.Label(self.master, textvariable=self.bank_points_display, style="Info.TLabel")
        self.bank_points_label.place(relx=0.2, rely=0.6, anchor="center")

        self.turn_order_display = tk.StringVar()
        self.turn_order_display.set("Gājies būs: " + ("cilvēkam" if self.turn_order == "human" else "datoram"))
        
        self.turn_order_label = ttk.Label(self.master, textvariable=self.turn_order_display, style="Info.TLabel")
        self.turn_order_label.place(relx=0.85, rely=0.3, anchor="center")

        self.winner_display = tk.StringVar()
        self.winner_display.set("")
        
        self.winner_label = ttk.Label(self.master, textvariable=self.winner_display, style="Winner.TLabel")
        self.winner_label.place(relx=0.85, rely=0.5, anchor="center")


        self.human_number_display = tk.StringVar()
        self.human_number_display.set("Izvēlētais skaitlis ir: " + str(self.human_number))

        self.human_number_input_label = ttk.Label(self.master, text="Sākumā izvēlieties skaitli no 25 līdz 40", style="Info.TLabel")
        self.human_number_input_label.place(relx=0.5, rely=0.2, anchor="center")

        self.human_number_label = ttk.Label(self.master, textvariable=self.human_number_display, style="Info.TLabel")
        self.human_number_label.place(relx=0.2, rely=0.3, anchor="center")

        self.human_number_input = tk.Scale(self.master, from_=25, to=40, orient=tk.HORIZONTAL, length=300)
        self.human_number_input.place(relx=0.5, rely=0.3, anchor="center")

        self.multiplier_input_label = ttk.Label(self.master, text="Izvēlieties ar ko reizināt (2, 3 vai 4)", style="Info.TLabel")
        self.multiplier_input_label.place(relx=0.5, rely=0.4, anchor="center")

        self.multiplier_input = tk.Scale(self.master, from_=2, to=4, orient=tk.HORIZONTAL, length=300)
        self.multiplier_input.place(relx=0.5, rely=0.5, anchor="center")

        self.show_turn_change_button()
    
    def show_turn_change_button(self):
        self.turn_change_button = ttk.Button(self.master, text="Mainīt gājienu", style="Main.TButton", command=self.handle_turn_change)
        self.turn_change_button.place(relx=0.85, rely=0.1, anchor="center")

    def alpha_beta_view(self):
        self.game_display_layout()

        self.gamemode_title_input_label = ttk.Label(self.master, text="Alpha beta algoritms", style="Title.TLabel")
        self.gamemode_title_input_label.place(relx=0.5, rely=0.1, anchor="center")

        self.user_submit_button = ttk.Button(self.master, text="Ievadīt", style="Main.TButton", command=self.handle_alpha_beta)
        self.user_submit_button.place(relx=0.5, rely=0.6, anchor="center")

        self.alpha_beta_text_box = tk.Text(self.master, width=90, height=10, bd=1, relief="solid")
        self.alpha_beta_text_box.insert(tk.END, "Spēles gaita")
        self.alpha_beta_text_box.place(relx=0.5, rely=0.8, anchor="center")

    def min_max_view(self):
        self.game_display_layout()

        self.gamemode_title_input_label = ttk.Label(self.master, text="Minimax algoritms", style="Title.TLabel")
        self.gamemode_title_input_label.place(relx=0.5, rely=0.1, anchor="center")

        self.user_submit_button = ttk.Button(self.master, text="Ievadīt", style="Main.TButton", command=self.handle_min_max)
        self.user_submit_button.place(relx=0.5, rely=0.6, anchor="center")

        self.min_max_text_box = tk.Text(self.master, width=90, height=10, bd=1, relief="solid")
        self.min_max_text_box.insert(tk.END, "Spēles gaita")
        self.min_max_text_box.place(relx=0.5, rely=0.8, anchor="center")

    def handle_alpha_beta(self):
        if self.current_number == 0:
            self.winner_display.set("")

        if self.alpha_beta_human_number_input_flag == False:
            self.human_number = int(self.human_number_input.get())
            self.human_number_display.set("Izvēlētais skaitlis ir: " + str(self.human_number))
            self.current_number = self.human_number
            self.alpha_beta_human_number_input_flag = True

        self.handle_game_logic("alpha_beta", self.alpha_beta_text_box)

    def handle_min_max(self):
        if self.current_number == 0:
            self.winner_display.set("")

        if self.min_max_human_number_input_flag == False:
            self.human_number = int(self.human_number_input.get())
            self.human_number_display.set("Izvēlētais skaitlis ir: " + str(self.human_number))
            self.current_number = self.human_number
            self.min_max_human_number_input_flag = True

        self.handle_game_logic("min_max", self.min_max_text_box)

    def handle_turn_change(self):
        if self.turn_order == "human":
            self.turn_order = "computer"
        else:
            self.turn_order = "human"

        self.turn_order_display.set("Gājies būs: " + ("cilvēkam" if self.turn_order == "human" else "datoram"))

    def handle_game_logic(self, gamemode, text_box):
        if self.turn_order == "human":
            self.human_turn(text_box)
            self.turn_order = "computer"
        else:
            self.computer_turn(gamemode, text_box)
            self.turn_order = "human"
        
        if self.current_number != 0:
            self.turn_change_button.place_forget()
            self.update_score_display()
            self.log_score(text_box)
        else:
            self.show_turn_change_button()

    def human_turn(self, text_box):
        text_box.insert(tk.END, "\n\nCilvēka gājiens.")

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

        if self.current_number >= 5000:
            self.end_round(text_box, False)

    def computer_turn(self, gamemode, text_box):
        text_box.insert(tk.END, "\n\nDatora gājiens.")
        
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

        if self.current_number >= 5000:
            self.end_round(text_box, True)

    def update_score_display(self):
        self.current_number_display.set("Pašreizējais skaitlis: " + str(self.current_number))
        self.human_points_display.set("Cilvēka punkti: " + str(self.human_points))
        self.computer_points_display.set("Datora punkti: " + str(self.computer_points))
        self.bank_points_display.set("Punkti bankā: " + str(self.bank_points))
        self.turn_order_display.set("Gājies būs: " + ("cilvēkam" if self.turn_order == "human" else "datoram"))

    def log_score(self, text_box):
        text_box.insert(tk.END, "\nCilvēka punkti: " + str(self.human_points))
        text_box.insert(tk.END, "\nDatora punkti: " + str(self.computer_points))
        text_box.insert(tk.END, "\nBankas punkti: " + str(self.bank_points))
        text_box.see("end")

    def end_round(self, text_box, computer_win):
        if computer_win:
            self.computer_points += self.bank_points
        else:
            self.human_points += self.bank_points

        self.update_score_display()
        text_box.insert(tk.END, "\nBeigas!")
        self.log_score(text_box)

        if self.human_points > self.computer_points:
            text_box.insert(tk.END, "\nCilvēks uzvar!")
            self.winner_display.set("Cilvēks uzvar!")
        elif self.human_points < self.computer_points:
            text_box.insert(tk.END, "\nDators uzvar!")
            self.winner_display.set("Dators uzvar!")
        else:
            text_box.insert(tk.END, "\nNeizšķirts rezultāts!")
            self.winner_display.set("Neizšķirts rezultāts!")

        text_box.insert(tk.END, "\n-----------------\n")
        text_box.see("end")

        self.cleanup_game()

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