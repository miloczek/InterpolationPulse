from numpy.lib.polynomial import polyint
from .nifs3 import Nifs3
import tkinter as tk
from tkinter import IntVar, ttk
from tkinter import Text
from tkinter.constants import BOTTOM, INSERT, LEFT, RIGHT, END

from utils import clear_win, chebyshev_nodes, equidistant_nodes, random_nodes
import main_interface
from typing import List


def prepare_interval_values(
    entry: tk.Entry, info: tk.Label, poly: Nifs3, var_nodes: IntVar, linspace: str
) -> None:
    """Wczytuje wartości brzegowe przedziału z pola tekstowego i
    uruchamia wizualizację funkcji"""
    try:
        a, b = tuple(entry.get().split(","))
        info.config(text="Poprawnie wygnerowano wykres", fg="green")
        poly.plot_basic_function_in_linear_area(float(a), float(b), var_nodes, linspace)
    except Exception as e:
        info.config(text="Wprowadź dobry przedział", fg="red")
        print(e)


def plot_generator(poly: Nifs3, var_nodes: IntVar) -> None:
    """Funkcja wczytująca zakres i generująca wykres."""
    side_window = tk.Tk()
    side_window.title("Plot generator")
    side_window.geometry("700x600")
    lbl_instruction = tk.Label(
        side_window,
        text="Podaj zakres w postaci: a, b ",
        font=("Helvetica", "24"),
    )
    etr_box_a_b = tk.Entry(side_window, width=100)
    lbl_linspace = tk.Label(
        side_window,
        text="Podaj liczbę punktów w przestrzeni liniowej wykresu (pole puste = 1000)",
        font=("Helvetica", "15"),
    )
    etr_box_linspace = tk.Entry(side_window, width=20)
    lbl_info = tk.Label(
        side_window,
        text="",
        font=("Helvetica", "16"),
    )
    btn_generate_plot = tk.Button(
        side_window,
        text="Generuj",
        font=("Helvetica", "16"),
        command=lambda: prepare_interval_values(
            etr_box_a_b,
            lbl_info,
            poly,
            var_nodes,
            str(etr_box_linspace.get()),
        ),
    )

    lbl_instruction.pack()
    etr_box_a_b.pack()
    lbl_linspace.pack()
    etr_box_linspace.pack()
    lbl_info.pack()
    btn_generate_plot.pack()
    side_window.mainloop()


def show_generated_polynomials(poly: Nifs3) -> None:
    """Wypisuje na ekran wygenerowane wielomiany."""
    side_window = tk.Tk()
    side_window.title("Generated polynomials")
    side_window.geometry("1200x800")
    text = Text(side_window, height=800, width=1200)
    text.insert(INSERT, poly.poly_str)
    text.pack()


def create_nifs3_interpolation(
    lbl_info: tk.Label, x: str, f: str, precision: str
) -> None:
    """Na podstawie wczytanych węzłów i funkcji, tworzy NIFS3."""
    if x == "" or f == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        try:
            global polynomial
            polynomial = Nifs3(x, f, precision)
            lbl_info.config(text="Poprawnie wczytano dane", fg="green")
            show_generated_polynomials(polynomial)
        except Exception as e:
            lbl_info.config(
                text="Błędne dane, przy węzłach losowych może być konieczne ponowne wygenerowanie.",
                fg="red",
            )
            print(e)
            return


def generate_nodes(
    lbl_info: tk.Label, etr_box_x: tk.Entry, n: str, a_b_str: str, type: str
) -> None:
    """Generuje węzły interpolacji na podstawie podanej ilości."""
    try:
        n = int(n)
        a, b = tuple(a_b_str.split(","))
        nodes_str = ""
        lbl_info.config(text="", fg="green")
        if type == "węzły równoodległe":
            nodes_tab = equidistant_nodes(n, float(a), float(b))
        elif type == "węzły losowe":
            nodes_tab = random_nodes(n, float(a), float(b))
        elif type == "węzły Czebyszewa":
            nodes_tab = chebyshev_nodes(n, float(a), float(b))
        for node in nodes_tab:
            nodes_str += f"{node}, "
        etr_box_x.delete(0, END)
        etr_box_x.insert(0, nodes_str)
    except Exception as e:
        lbl_info.config(text="Ilość musi być wyrażona liczbą", fg="red")
        print(e)
        return


def nifs3_interpolation(window: tk.Tk) -> None:
    """Koordynuje narzędzie interpolacji NIFS 3."""
    clear_win(window)
    global polynomial
    polynomial = ""

    lbl_instruction = tk.Label(
        window,
        text="Interpolacja NIFS3",
        font=("Helvetica", "24"),
    )
    lbl_instr_x = tk.Label(
        window,
        text="Podaj węzły w postaci: x0, x1, ... ",
        font=("Helvetica", "16"),
    )

    etr_box_x = tk.Entry(window, width=100)

    lbl_instr_f = tk.Label(
        window,
        text="Podaj funkcję, którą chcesz interpolować: ",
        font=("Helvetica", "16"),
    )

    etr_box_f = tk.Entry(window, width=100)

    lbl_instr_f = tk.Label(
        window,
        text="Podaj funkcję, którą chcesz interpolować: ",
        font=("Helvetica", "16"),
    )

    etr_box_f = tk.Entry(window, width=100)

    lbl_instr_prec = tk.Label(
        window,
        text="Podaj precyzję (liczba miejsc po przecinku) [pole puste, dla maksymalnej dokładności]: ",
        font=("Helvetica", "16"),
    )

    etr_box_prec = tk.Entry(window, width=3)

    lbl_info = tk.Label(window, text="", font=("Helvetica", "12"), fg="green")

    btn_load = tk.Button(
        window,
        text="Wczytaj dane i pokaż wielomian",
        font=("Helvetica", "16"),
        command=lambda: create_nifs3_interpolation(
            lbl_info,
            str(etr_box_x.get()),
            str(etr_box_f.get()),
            str(etr_box_prec.get()),
        ),
    )

    btn_compare_plots = tk.Button(
        window,
        text="Wygeneruj wykres porównawczy",
        font=("Helvetica", "16"),
        command=lambda: polynomial.plot_compare_plot_in_linear_area(var_nodes)
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    lbl_instr_nodes_type = tk.Label(
        window,
        text="Podaj rodzaj węzłów: ",
        font=("Helvetica", "16"),
    )

    selected_type = tk.StringVar()

    cb_nodes_type = ttk.Combobox(window, textvariable=selected_type)
    cb_nodes_type["values"] = ("węzły równoodległe", "węzły losowe", "węzły Czebyszewa")
    cb_nodes_type["state"] = "readonly"

    lbl_instr_nodes_n = tk.Label(
        window,
        text="Podaj liczbę węzłów: ",
        font=("Helvetica", "16"),
    )

    etr_box_nodes_n = tk.Entry(window, width=3)

    lbl_instr_nodes_interval = tk.Label(
        window,
        text="Podaj przedział węzłów: a, b ",
        font=("Helvetica", "16"),
    )

    etr_box_nodes_interval = tk.Entry(window, width=100)

    btn_make_chebyshev_nodes = tk.Button(
        window,
        text="Wygeneruj węzły",
        font=("Helvetica", "16"),
        command=lambda: generate_nodes(
            lbl_info,
            etr_box_x,
            str(etr_box_nodes_n.get()),
            str(etr_box_nodes_interval.get()),
            str(cb_nodes_type.get()),
        )
        if (
            etr_box_nodes_n.get() != ""
            and etr_box_nodes_interval.get() != ""
            and cb_nodes_type.get() != ""
        )
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
        command=lambda: plot_generator(polynomial, var_nodes)
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    btn_make_interpolation_plot = tk.Button(
        window,
        text="Wygeneruj wykres wielomianu interpolacyjnego",
        font=("Helvetica", "16"),
        command=lambda: polynomial.plot_nifs3_in_linear_area(var_nodes)
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    var_nodes = tk.IntVar()
    ck_bx_nodes = tk.Checkbutton(
        window,
        text="Pokaż węzły interpolacji na wykresie",
        font=("Helvetica", "16"),
        variable=var_nodes,
        onvalue=1,
        offvalue=0,
    )

    lbl_instruction.pack()
    lbl_instr_x.pack()
    etr_box_x.pack()
    lbl_instr_f.pack()
    etr_box_f.pack()
    lbl_instr_prec.pack()
    etr_box_prec.pack()
    lbl_info.pack()
    btn_load.pack()
    btn_compare_plots.pack()
    lbl_instr_nodes_n.pack()
    etr_box_nodes_n.pack()
    lbl_instr_nodes_interval.pack()
    etr_box_nodes_interval.pack()
    lbl_instr_nodes_type.pack()
    cb_nodes_type.pack()
    btn_make_chebyshev_nodes.pack()
    ck_bx_nodes.pack()
    btn_make_interpolation_plot.pack(side=RIGHT)
    btn_make_function_plot.pack(side=LEFT)
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)
