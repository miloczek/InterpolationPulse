import tkinter as tk
from tkinter import Text
from tkinter.constants import BOTTOM, INSERT, LEFT, RIGHT

from numpy.lib.twodim_base import tri
from utils import clear_win
import main_interface
from .trygonometric import Trygonometric


def prepare_interval_values(
    entry: tk.Entry, info: tk.Label, poly: Trygonometric
) -> None:
    """Wczytuje wartości brzegowe przedziału z pola tekstowego i
    uruchamia wizualizację funkcji"""
    try:
        a, b = tuple(entry.get().split(","))
        info.config(text="Poprawnie wygnerowano wykres", fg="green")
        poly.interpolation_plot(float(a), float(b))

    except Exception as e:
        info.config(text="Wprowadź dobry przedział", fg="red")
        print(e)


def plot_generator(poly: Trygonometric) -> None:
    """Funkcja wczytująca zakres i generująca wykres."""
    side_window = tk.Tk()
    side_window.title("Plot generator")
    side_window.geometry("600x400")
    lbl_instruction = tk.Label(
        side_window,
        text="Podaj zakres w postaci [a, b]: ",
        font=("Helvetica", "24"),
    )
    etr_box_a_b = tk.Entry(side_window, width=100)
    lbl_info = tk.Label(
        side_window,
        text="",
        font=("Helvetica", "16"),
    )
    btn_generate_plot = tk.Button(
        side_window,
        text="Generuj",
        font=("Helvetica", "16"),
        command=lambda: prepare_interval_values(etr_box_a_b, lbl_info, poly),
    )

    lbl_instruction.pack()
    etr_box_a_b.pack()
    lbl_info.pack()
    btn_generate_plot.pack()
    side_window.mainloop()


def show_generated_polynomial(poly: Trygonometric) -> None:
    """Wypisuje na ekran wygenerowany wielomian."""
    side_window = tk.Tk()
    side_window.title("Generated polynomial")
    side_window.geometry("600x400")
    text = Text(side_window)
    text.insert(INSERT, poly.trygonometric_polynomial)
    text.pack()


def create_trygonometric_interpolation(
    lbl_info: tk.Label,
    f: str,
    n: str,
) -> None:
    """Na podstawie wczytanych danych, tworzy interpolacyjny wielomian trygonometryczny."""
    if f == "" or n == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        try:
            global polynomial
            polynomial = Trygonometric(f, n)
            lbl_info.config(text="Poprawnie wczytano dane", fg="green")
            show_generated_polynomial(polynomial)
        except Exception as e:
            lbl_info.config(text="Błędne dane", fg="red")
            print(e)
    return


def trygonometric_interpolation(window: tk.Tk) -> None:
    """Interpolacja trygonometryczna funkcji."""
    clear_win(window)
    global polynomial
    polynomial = ""

    lbl_instruction = tk.Label(
        window,
        text="Interpolacja trygonometryczna funkcji",
        font=("Helvetica", "24"),
    )

    lbl_instr_x = tk.Label(
        window,
        text="Podaj funkcję generującą punkty i ich ilość, na podstawie której chcemy otrzymać interpolacyjną funkcję okresową.",
        font=("Helvetica", "16"),
    )

    etr_box_f = tk.Entry(window, width=100)
    etr_box_n = tk.Entry(window, width=10)

    lbl_info = tk.Label(window, text="", font=("Helvetica", "12"), fg="green")

    btn_load = tk.Button(
        window,
        text="Wczytaj dane i pokaż wielomian",
        font=("Helvetica", "16"),
        command=lambda: create_trygonometric_interpolation(
            lbl_info,
            str(etr_box_f.get()),
            str(etr_box_n.get()),
        ),
    )

    btn_compare_plots = tk.Button(
        window,
        text="Wygeneruj wykres porównawczy",
        font=("Helvetica", "16"),
        command=lambda: plot_generator(polynomial)
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
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
    etr_box_f.pack()
    etr_box_n.pack()
    lbl_info.pack()
    btn_load.pack()
    btn_compare_plots.pack()
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)