from tkinter import Text, font
from tkinter.constants import BOTTOM, INSERT, LEFT, NO, NONE, RIGHT
from utils import clear_list, prepare_to_show_natural_polynomial, clear_win
from polynomial import Polynomial
from lagrange import Lagrange
from lagrange_inteface import lagrange_interpolation
from polynomial_interface import polynomial_parse
import tkinter as tk

window = tk.Tk()
window.title("Interpolation Pulse")
window.geometry("1000x800")


def main() -> None:
    """Główna funkcja, spajająca wszystkie funkcjonalności i
    porządkująca interfejsy."""
    clear_win(window)

    lbl_instruction = tk.Label(
        window,
        text="Proszę o wybranie jednej z dostępnych opcji:",
        font=("Helvetica", "24"),
    )
    lbl_instruction.pack()
    btn_lagrange = tk.Button(
        window,
        text="Interpolacja Lagrange'a",
        font=("Helvetica", "16"),
        command=lambda: lagrange_interpolation(window),
    )
    btn_polynomial = tk.Button(
        window,
        text="Postacie wielomianów",
        font=("Helvetica", "16"),
        command=lambda: polynomial_parse(window),
    )
    btn_exit = tk.Button(
        window, text="Zakończ pracę", font=("Helvetica", "16"), command=window.destroy
    )
    btn_lagrange.pack()
    btn_polynomial.pack()
    btn_exit.pack(side=BOTTOM)
    window.mainloop()


if __name__ == "__main__":
    main()
