from nifs3 import Nifs3
import tkinter as tk
from tkinter import Text
from tkinter.constants import BOTTOM, INSERT, LEFT, RIGHT

from utils import clear_win
import main_interface
from typing import List


def prepare_interval_values3(
    entry: tk.Entry, info: tk.Label, poly: Nifs3, mode: str
) -> None:
    """Wczytuje wartości brzegowe przedziału z pola tekstowego i
    uruchamia wizualizację funkcji"""
    try:
        a, b = tuple(entry.get().split(","))
        info.config(text="Poprawnie wygnerowano wykres", fg="green")
        if mode == "normal":
            poly.plot_basic_function_in_linear_area(float(a), float(b))
        elif mode == "nifs3":
            poly.plot_nifs3_in_linear_area3(float(a), float(b))
        else:
            poly.plot_compare_plot_in_linear_area3(float(a), float(b))
    except Exception as e:
        info.config(text="Wprowadź dobry przedział", fg="red")
        print(e)


def prepare_interval_values4(
    entry: tk.Entry, info: tk.Label, poly: Nifs3, mode: str
) -> None:
    """Wczytuje wartości brzegowe przedziału z pola tekstowego i
    uruchamia wizualizację funkcji"""
    try:
        a, b = tuple(entry.get().split(","))
        info.config(text="Poprawnie wygnerowano wykres", fg="green")
        if mode == "normal":
            poly.plot_basic_function_in_linear_area(float(a), float(b))
        elif mode == "nifs3":
            poly.plot_nifs3_in_linear_area4(float(a), float(b))
        else:
            poly.plot_compare_plot_in_linear_area4(float(a), float(b))
    except Exception as e:
        info.config(text="Wprowadź dobry przedział", fg="red")
        print(e)


def plot_generator3(poly: Nifs3, mode: str) -> None:
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
        command=lambda: prepare_interval_values3(etr_box_a_b, lbl_info, poly, mode),
    )

    lbl_instruction.pack()
    etr_box_a_b.pack()
    lbl_info.pack()
    btn_generate_plot.pack()
    side_window.mainloop()


def plot_generator4(poly: Nifs3, mode: str) -> None:
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
        command=lambda: prepare_interval_values4(etr_box_a_b, lbl_info, poly, mode),
    )

    lbl_instruction.pack()
    etr_box_a_b.pack()
    lbl_info.pack()
    btn_generate_plot.pack()
    side_window.mainloop()


def show_generated_polynomials(poly: Nifs3, mode: str) -> None:
    """Wypisuje na ekran wygenerowane wielomiany."""
    side_window = tk.Tk()
    side_window.title("Generated polynomials")
    side_window.geometry("600x400")
    text = Text(side_window)
    if mode == "three":
        text.insert(
            INSERT,
            f"{poly.polys[0]}, x ∈ [{poly.x[0]}, {poly.x[1]}] \n {poly.polys[1]}, x ∈ [{poly.x[1]}, {poly.x[2]}] ",
        )
    elif mode == "four":
        text.insert(
            INSERT,
            f"{poly.polys[0]}, x ∈ [{poly.x[0]}, {poly.x[1]}] \n {poly.polys[1]}, x ∈ [{poly.x[1]}, {poly.x[2]}] \n {poly.polys[2]}, x ∈ [{poly.x[2]}, {poly.x[3]}] ",
        )
    text.pack()


def create_three_nodes_interpolation(
    lbl_info: tk.Label, x1: str, x2: str, x3: str, f: str, precision: str
) -> None:
    """Na podstawie wczytanych węzłów i funkcji, tworzy NIFS3."""
    if x1 == "" or x2 == "" or x3 == "" or f == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        try:
            global polynomial
            polynomial = Nifs3([x1, x2, x3], f, "three", precision)
            lbl_info.config(text="Poprawnie wczytano dane", fg="green")
            show_generated_polynomials(polynomial, "three")
        except Exception as e:
            lbl_info.config(text="Błędne dane", fg="red")
            print(e)
            return


def create_four_nodes_interpolation(
    lbl_info: tk.Label, x1: str, x2: str, x3: str, x4: str, f: str, precision: str
) -> None:
    """Na podstawie wczytanych węzłów i funkcji, tworzy NIFS3."""
    if x1 == "" or x2 == "" or x3 == "" or x4 == "" or f == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        try:
            global polynomial
            polynomial = Nifs3([x1, x2, x3, x4], f, "four", precision)
            lbl_info.config(text="Poprawnie wczytano dane", fg="green")
            show_generated_polynomials(polynomial, "four")
        except Exception as e:
            lbl_info.config(text="Błędne dane", fg="red")
            print(e)
            return


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

    lbl_instr_prec = tk.Label(
        window,
        text="Podaj precyzję (ilość miejsc po przecinku) [pole puste, dla maksymalnej dokładności]: ",
        font=("Helvetica", "16"),
    )

    etr_box_prec = tk.Entry(window, width=3)

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
            str(etr_box_prec.get()),
        ),
    )

    btn_compare_plots = tk.Button(
        window,
        text="Wygeneruj wykres porównawczy",
        font=("Helvetica", "16"),
        command=lambda: plot_generator3(polynomial, "compare")
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

    btn_make_function_plot = tk.Button(
        window,
        text="Wygeneruj wykres wyjściowej funkcji",
        font=("Helvetica", "16"),
        command=lambda: plot_generator3(polynomial, "normal")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    btn_make_interpolation_plot = tk.Button(
        window,
        text="Wygeneruj wykres wielomianu interpolacyjnego",
        font=("Helvetica", "16"),
        command=lambda: plot_generator3(polynomial, "nifs3")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    lbl_instruction.pack()
    lbl_instr_x.pack()
    etr_box_x1.pack()
    etr_box_x2.pack()
    etr_box_x3.pack()
    lbl_instr_f.pack()
    etr_box_f.pack()
    lbl_instr_prec.pack()
    etr_box_prec.pack()
    lbl_info.pack()
    btn_load.pack()
    btn_compare_plots.pack()
    btn_make_interpolation_plot.pack(side=RIGHT)
    btn_make_function_plot.pack(side=LEFT)
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)


def four_nodes_interpolation(window: tk.Tk) -> None:
    """Interpolacja NIFS3 za pomocą czterech węzłów."""
    clear_win(window)
    global polynomial
    polynomial = ""

    lbl_instruction = tk.Label(
        window,
        text="Interpolacja NIFS3 czterema węzłami",
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

    lbl_instr_prec = tk.Label(
        window,
        text="Podaj precyzję (ilość miejsc po przecinku) [pole puste, dla maksymalnej dokładności]: ",
        font=("Helvetica", "16"),
    )

    etr_box_prec = tk.Entry(window, width=3)

    lbl_info = tk.Label(window, text="", font=("Helvetica", "12"), fg="green")

    btn_load = tk.Button(
        window,
        text="Wczytaj dane i pokaż wielomian",
        font=("Helvetica", "16"),
        command=lambda: create_four_nodes_interpolation(
            lbl_info,
            str(etr_box_x1.get()),
            str(etr_box_x2.get()),
            str(etr_box_x3.get()),
            str(etr_box_x4.get()),
            str(etr_box_f.get()),
            str(etr_box_prec.get()),
        ),
    )

    btn_compare_plots = tk.Button(
        window,
        text="Wygeneruj wykres porównawczy",
        font=("Helvetica", "16"),
        command=lambda: plot_generator3(polynomial, "compare")
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

    btn_make_function_plot = tk.Button(
        window,
        text="Wygeneruj wykres wyjściowej funkcji",
        font=("Helvetica", "16"),
        command=lambda: plot_generator3(polynomial, "normal")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    btn_make_interpolation_plot = tk.Button(
        window,
        text="Wygeneruj wykres wielomianu interpolacyjnego",
        font=("Helvetica", "16"),
        command=lambda: plot_generator3(polynomial, "nifs3")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    lbl_instruction.pack()
    lbl_instr_x.pack()
    etr_box_x1.pack()
    etr_box_x2.pack()
    etr_box_x3.pack()
    etr_box_x4.pack()
    lbl_instr_f.pack()
    etr_box_f.pack()
    lbl_instr_prec.pack()
    etr_box_prec.pack()
    lbl_info.pack()
    btn_load.pack()
    btn_compare_plots.pack()
    btn_make_interpolation_plot.pack(side=RIGHT)
    btn_make_function_plot.pack(side=LEFT)
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