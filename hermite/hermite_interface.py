import tkinter as tk
from tkinter import Text, Widget, ttk
from tkinter.constants import BOTTOM, INSERT, LEFT, NO, NONE, RIGHT, END

from utils import (
    clear_win,
    chebyshev_nodes,
    equidistant_nodes,
    random_nodes,
    check_if_nodes_and_values_are_equal,
    str_to_float_list,
    generate_vals_and_derives,
)
import main_interface
from .hermite import Hermite


def show_generated_polynomial(poly: Hermite) -> None:
    """Wypisuje na ekran wygenerowany wielomian."""
    side_window = tk.Tk()
    side_window.title("Generated polynomial")
    side_window.geometry("1200x800")
    text = Text(side_window, height=800, width=1200)
    text.insert(INSERT, poly.printable_polynomial)
    text.pack()


def generate_vals(
    xs: str,
    etr_box_y: tk.Entry,
    etr_box_y_prim: tk.Entry,
    fun_type: str,
) -> None:
    """Oblicza wartości w węzłach i wartości pochodnych dla przykładowych funkcji."""
    xs = str_to_float_list(xs)
    y, y_prim = generate_vals_and_derives(xs, fun_type)
    etr_box_y.delete(0, END)
    etr_box_y.insert(0, y)
    etr_box_y_prim.delete(0, END)
    etr_box_y_prim.insert(0, y_prim)


def show_table_of_diffs(poly: Hermite) -> None:
    """Wypisuje w okienku tablicę ilorazów różnicowych."""
    side_window = tk.Tk()
    side_window.title("Generated table of diffs")
    side_window.geometry("1200x800")
    text = Text(side_window, height=800, width=1200)
    str_of_diff_table = ""
    for line in list(poly.table_of_diffs):
        str_of_diff_table += f"{line}\n"
    text.insert(INSERT, str_of_diff_table)
    text.pack()


def create_hermite_polynomial(
    lbl_info: tk.Label, x: str, y: str, y_prim: str, precision: str
) -> None:
    """Na podstawie wczytanych węzłów i funkcji, tworzy wielomian Hermite'a."""
    global polynomial
    polynomial = Hermite(x, y, y_prim, precision)
    lbl_info.config(text="Poprawnie wczytano dane", fg="green")
    show_generated_polynomial(polynomial)
    # if x == "" or y == "" or y_prim == "":
    #     lbl_info.config(text="Nie wprowadzono danych", fg="red")
    #     return
    # elif not check_if_nodes_and_values_are_equal(x, y, y_prim):
    #     lbl_info.config(text="Niezgodna ilość węzłów i wartości", fg="red")
    #     return
    # else:
    #     try:
    #         global polynomial
    #         polynomial = Hermite(x, y, y_prim, precision)
    #         lbl_info.config(text="Poprawnie wczytano dane", fg="green")
    #         show_generated_polynomial(polynomial)
    #     except ZeroDivisionError:
    #         lbl_info.config(text="Funkcja niemożliwa do zinterpolowania", fg="red")
    #         return
    #     except Exception as e:
    #         lbl_info.config(
    #             text="Błędne dane, przy węzłach losowych może być konieczne ponowne wygenerowanie",
    #             fg="red",
    #         )
    #         print(e)
    #         return


def prepare_interval_values(
    entry: tk.Entry, info: tk.Label, poly: Hermite, mode: str
) -> None:
    """Wczytuje wartości brzegowe przedziału z pola tekstowego i
    uruchamia wizualizację funkcji"""
    try:
        a, b = tuple(entry.get().split(","))
        info.config(text="Poprawnie wygnerowano wykres", fg="green")
        if mode == "normal":
            poly.plot_basic_function_in_linear_area(float(a), float(b))
        elif mode == "hermite":
            poly.plot_hermite_in_linear_area(float(a), float(b))
        else:
            poly.plot_compare_plot_in_linear_area(float(a), float(b))
    except Exception as e:
        info.config(text="Wprowadź dobry przedział", fg="red")
        print(e)


def plot_generator(poly: Hermite, mode: str) -> None:
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
        command=lambda: prepare_interval_values(etr_box_a_b, lbl_info, poly, mode),
    )

    lbl_instruction.pack()
    etr_box_a_b.pack()
    lbl_info.pack()
    btn_generate_plot.pack()
    side_window.mainloop()


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


def hermite_interpolation(window: tk.Tk) -> None:
    """Główna funkcja przygotowująca wielomiany Hermite'a. Ustawia poprawnie
    interfejsy i uruchamia funkcje pomocnicze."""
    clear_win(window)
    global polynomial
    polynomial = ""

    lbl_instruction = tk.Label(
        window,
        text="Interpolacja Hermite'a",
        font=("Helvetica", "24"),
    )

    lbl_instr_x = tk.Label(
        window,
        text="Podaj węzły w postaci [x0, x1, ...]: ",
        font=("Helvetica", "12"),
    )

    etr_box_x = tk.Entry(window, width=100)

    lbl_instr_y = tk.Label(
        window,
        text="Podaj wartości w węzłach w postaci [y0, y1, ...]: ",
        font=("Helvetica", "12"),
    )

    etr_box_y = tk.Entry(window, width=100)

    lbl_instr_y_prim = tk.Label(
        window,
        text="Podaj wartości pochodnych w węzłach w postaci [y'0, y'1, ...]: ",
        font=("Helvetica", "12"),
    )

    etr_box_y_prim = tk.Entry(window, width=100)

    lbl_instr_prec = tk.Label(
        window,
        text="Podaj precyzję (ilość miejsc po przecinku) [pole puste, dla maksymalnej dokładności]: ",
        font=("Helvetica", "12"),
    )

    etr_box_prec = tk.Entry(window, width=3)

    lbl_info = tk.Label(window, text="", font=("Helvetica", "10"), fg="green")

    btn_load = tk.Button(
        window,
        text="Wczytaj dane i pokaż wielomian",
        font=("Helvetica", "12"),
        command=lambda: create_hermite_polynomial(
            lbl_info,
            str(etr_box_x.get()),
            str(etr_box_y.get()),
            str(etr_box_y_prim.get()),
            str(etr_box_prec.get()),
        ),
    )

    btn_diffs_table = tk.Button(
        window,
        text="Wygeneruj tablicę ilorazów różnicowych",
        font=("Helvetica", "12"),
        command=lambda: show_table_of_diffs(polynomial)
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    btn_compare_plots = tk.Button(
        window,
        text="Wygeneruj wykres porównawczy",
        font=("Helvetica", "12"),
        command=lambda: plot_generator(polynomial, "compare")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    lbl_instr_nodes_type = tk.Label(
        window,
        text="Podaj rodzaj węzłów: ",
        font=("Helvetica", "12"),
    )

    lbl_instr_fun_type = tk.Label(
        window,
        text="Wybierz przykładową funkcję, aby wygenerować wartości: ",
        font=("Helvetica", "12"),
    )

    selected_fun_type = tk.StringVar()

    cb_fun_type = ttk.Combobox(window, textvariable=selected_fun_type)
    cb_fun_type["values"] = (
        "4x^2 - 15x + 2",
        "0.78^x",
        "-7x^3 + 12x^2 - 19x + 3",
        "1/(1+25x^2)",
        "2x^3/3",
    )
    cb_fun_type["state"] = "readonly"

    btn_load_fun_vals = tk.Button(
        window,
        text="Wygeneruj wartości",
        font=("Helvetica", "12"),
        command=lambda: generate_vals(
            str(etr_box_x.get()),
            etr_box_y,
            etr_box_y_prim,
            str(cb_fun_type.get()),
        )
        if (etr_box_x.get() != "" and str(cb_fun_type.get()) != "")
        else None,
    )

    selected_type = tk.StringVar()

    cb_nodes_type = ttk.Combobox(window, textvariable=selected_type)
    cb_nodes_type["values"] = ("węzły równoodległe", "węzły losowe", "węzły Czebyszewa")
    cb_nodes_type["state"] = "readonly"

    lbl_instr_nodes_n = tk.Label(
        window,
        text="Podaj ilość węzłów: ",
        font=("Helvetica", "12"),
    )

    etr_box_nodes_n = tk.Entry(window, width=3)

    lbl_instr_nodes_interval = tk.Label(
        window,
        text="Podaj przedział węzłów [a,b]: ",
        font=("Helvetica", "12"),
    )

    etr_box_nodes_interval = tk.Entry(window, width=100)

    btn_make_nodes = tk.Button(
        window,
        text="Wygeneruj węzły",
        font=("Helvetica", "12"),
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
        window, text="Zakończ pracę", font=("Helvetica", "12"), command=window.destroy
    )

    btn_back = tk.Button(
        window,
        text="Wróć",
        font=("Helvetica", "12"),
        command=lambda: main_interface.main(window),
    )

    btn_make_function_plot = tk.Button(
        window,
        text="Wygeneruj wykres wyjściowej funkcji",
        font=("Helvetica", "12"),
        command=lambda: plot_generator(polynomial, "normal")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    btn_make_interpolation_plot = tk.Button(
        window,
        text="Wygeneruj wykres wielomianu interpolacyjnego",
        font=("Helvetica", "12"),
        command=lambda: plot_generator(polynomial, "hermite")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    var_nodes = tk.IntVar()
    ck_bx_nodes = tk.Checkbutton(
        window,
        text="Pokaż węzły interpolacji na wykresie",
        font=("Helvetica", "12"),
        variable=var_nodes,
        onvalue=1,
        offvalue=0,
    )

    lbl_instruction.pack()
    lbl_instr_x.pack()
    etr_box_x.pack()
    lbl_instr_y.pack()
    etr_box_y.pack()
    lbl_instr_y_prim.pack()
    etr_box_y_prim.pack()
    lbl_instr_prec.pack()
    etr_box_prec.pack()
    lbl_info.pack()
    btn_load.pack()
    lbl_instr_fun_type.pack()
    cb_fun_type.pack()
    btn_load_fun_vals.pack()
    lbl_instr_nodes_n.pack()
    etr_box_nodes_n.pack()
    lbl_instr_nodes_interval.pack()
    etr_box_nodes_interval.pack()
    lbl_instr_nodes_type.pack()
    cb_nodes_type.pack()
    btn_make_nodes.pack()
    ck_bx_nodes.pack()
    btn_diffs_table.pack(side=LEFT)
    btn_compare_plots.pack(side=LEFT)
    btn_make_interpolation_plot.pack(side=RIGHT)
    btn_make_function_plot.pack(side=RIGHT)
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)