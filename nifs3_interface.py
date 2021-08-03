from nifs3 import Nifs3
import tkinter as tk
from tkinter import Text
from tkinter.constants import BOTTOM, INSERT, LEFT, NO

from numpy.lib.polynomial import poly
from utils import clear_win
import main_interface
from typing import List


def create_three_nodes_interpolation(
    lbl_info: tk.Label, x1: str, x2: str, x3: str, f: str
) -> None:
    """Na podstawie wczytanych węzłów i funkcji, tworzy NIFS3."""
    if x1 == "" or x2 == "" or x3 == "" or f == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        global polynomial
        polynomial = Nifs3([x1, x2, x3], f, "three")
        print(polynomial.polys)


def three_nodes_interpolation(window: tk.Tk) -> None:
    """Interpolacja NIFS3 za pomocą trzech węzłów."""
    clear_win(window)
    global polynomial
    polynomial = ""

    lbl_instruction = tk.Label(
        window,
        text="Interpolacja NIFS3 trzema węzłami",
        font=("Helvetica", "24"),
    )

    lbl_instr_x = tk.Label(
        window,
        text="Podaj węzły interpolacji",
        font=("Helvetica", "16"),
    )

    etr_box_x1 = tk.Entry(window, width=10)
    etr_box_x2 = tk.Entry(window, width=10)
    etr_box_x3 = tk.Entry(window, width=10)

    lbl_instr_f = tk.Label(
        window,
        text="Podaj funkcję, którą chcesz interpolować: ",
        font=("Helvetica", "16"),
    )

    etr_box_f = tk.Entry(window, width=100)

    lbl_info = tk.Label(window, text="", font=("Helvetica", "12"), fg="green")

    btn_load = tk.Button(
        window,
        text="Wczytaj dane i pokaż wielomian",
        font=("Helvetica", "16"),
        command=lambda: create_three_nodes_interpolation(
            lbl_info,
            str(etr_box_x1.get()),
            str(etr_box_x2.get()),
            str(etr_box_x3.get()),
            str(etr_box_f.get()),
        ),
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
    lbl_instr_x.pack()
    etr_box_x1.pack()
    etr_box_x2.pack()
    etr_box_x3.pack()
    lbl_instr_f.pack()
    etr_box_f.pack()
    lbl_info.pack()
    btn_load.pack()
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)


def four_nodes_interpolation(window: tk.Tk) -> None:
    """Interpolacja NIFS3 za pomocą czterech węzłów."""
    clear_win(window)
    global polynomial
    polynomial = ""

    lbl_instruction = tk.Label(
        window,
        text="Interpolacja NIFS3 trzema węzłami",
        font=("Helvetica", "24"),
    )

    lbl_instr_x = tk.Label(
        window,
        text="Podaj węzły interpolacji",
        font=("Helvetica", "16"),
    )

    etr_box_x1 = tk.Entry(window, width=10)
    etr_box_x2 = tk.Entry(window, width=10)
    etr_box_x3 = tk.Entry(window, width=10)
    etr_box_x4 = tk.Entry(window, width=10)

    lbl_instr_f = tk.Label(
        window,
        text="Podaj funkcję, którą chcesz interpolować: ",
        font=("Helvetica", "16"),
    )

    etr_box_f = tk.Entry(window, width=100)

    lbl_info = tk.Label(window, text="", font=("Helvetica", "12"), fg="green")

    # btn_load = tk.Button(
    #     window,
    #     text="Wczytaj dane i pokaż wielomian",
    #     font=("Helvetica", "16"),
    #     command=lambda: create_three_nodes_interpolation(
    #         lbl_info,
    #         str(etr_box_x.get()),
    #         str(etr_box_f.get()),
    #         str(etr_box_prec.get()),
    #     ),
    # )

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
    lbl_instr_x.pack()
    etr_box_x1.pack()
    etr_box_x2.pack()
    etr_box_x3.pack()
    etr_box_x4.pack()
    lbl_instr_f.pack()
    etr_box_f.pack()
    lbl_info.pack()
    # btn_load.pack()
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)


def nifs3_interpolation(window: tk.Tk) -> None:
    """Koordynuje narzędzie interpolacji NIFS 3."""
    clear_win(window)

    lbl_instruction = tk.Label(
        window,
        text="Interpolacja NIFS3",
        font=("Helvetica", "24"),
    )

    btn_three_nodes = tk.Button(
        window,
        text="Trzy węzły",
        font=("Helvetica", "16"),
        command=lambda: three_nodes_interpolation(window),
    )

    btn_four_nodes = tk.Button(
        window,
        text="Cztery węzły",
        font=("Helvetica", "16"),
        command=lambda: four_nodes_interpolation(window),
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
    btn_three_nodes.pack()
    btn_four_nodes.pack()
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)