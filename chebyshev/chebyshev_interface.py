from tkinter.constants import BOTTOM

from numpy.lib import utils
import main_interface
import tkinter as tk
from utils import clear_win, chebyshev_plot


def generate_chebyshev_plots(lbl_info: tk.Label, a_b: tk.Entry, n: tk.Entry) -> None:
    """Przygotowuje przedziały, zajmuje się przechwytywaniem błędów i wywołuje funkcję generującą wykresy."""
    if a_b.get() == "" or n.get() == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        try:
            a, b = tuple(a_b.get().split(","))
            n1, n2 = tuple(n.get().split(","))
            chebyshev_plot(float(a), float(b), int(n1), int(n2))
            lbl_info.config(text="Poprawnie wygnerowano wykres", fg="green")
        except Exception as e:
            lbl_info.config(text="Błędne dane, przy węzłach losowych może być konieczne ponowne wygenerowanie", fg="red")
            print(e)
            return


def chebyshev_polynomials(window: tk.Tk) -> None:
    """Główna funkcja koordynująca dane potrzebne do wygnerowania wielomianów
    Czebyszewa"""
    clear_win(window)

    lbl_instruction = tk.Label(
        window,
        text="Wielomiany Czebyszewa",
        font=("Helvetica", "24"),
    )

    lbl_instr_n = tk.Label(
        window,
        text="Podaj przedział stopni wielomianów w postaci [a, b]: ",
        font=("Helvetica", "16"),
    )

    etr_box_n = tk.Entry(window, width=100)

    lbl_instr_a_b = tk.Label(
        window,
        text="Podaj zakres w postaci [a, b]: ",
        font=("Helvetica", "16"),
    )

    etr_box_a_b = tk.Entry(window, width=100)

    lbl_info = tk.Label(window, text="", font=("Helvetica", "12"), fg="green")

    btn_load = tk.Button(
        window,
        text="Wczytaj dane i pokaż wielomiany",
        font=("Helvetica", "16"),
        command=lambda: generate_chebyshev_plots(lbl_info, etr_box_a_b, etr_box_n),
    )

    btn_exit = tk.Button(
        window, text="Zakończ pracę", font=("Helvetica", "16"), command=window.destroy
    )

    btn_back = tk.Button(
        window,
        text="Wróć",
        font=("Helvetica", "16"),
        command=lambda: main_interface.main(window),
    )

    lbl_instruction.pack()
    lbl_instr_n.pack()
    etr_box_n.pack()
    lbl_instr_a_b.pack()
    etr_box_a_b.pack()
    lbl_info.pack()
    btn_load.pack()
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)