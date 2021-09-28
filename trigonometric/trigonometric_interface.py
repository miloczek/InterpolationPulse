import tkinter as tk
from tkinter import Text
from tkinter.constants import BOTTOM, END, INSERT, LEFT, NO, RIGHT
from typing_extensions import IntVar
from numpy.core.fromnumeric import var

from utils import check_if_nodes_and_values_are_equal, clear_win, generate_pi_nodes
import main_interface
from .trigonometric import Trigonometric


def generate_nodes(lbl_info: tk.Label, n: str, etr_box_x: tk.Entry) -> None:
    """Generuje zestaw równoodległych węzłów postaci t - 2kπ/n"""
    try:
        lbl_info.config(text=""),
        etr_box_x.delete(0, END)
        etr_box_x.insert(0, generate_pi_nodes(int(n)))
    except Exception as e:
        lbl_info.config(text="n musi być wyrażone liczbą", fg="red")
        print(e)
        return


def prepare_interval_values(
    entry: tk.Entry,
    info: tk.Label,
    poly: Trigonometric,
    var_nodes: IntVar,
    linspace: str,
) -> None:
    """Wczytuje wartości brzegowe przedziału z pola tekstowego i
    uruchamia wizualizację funkcji"""
    try:
        a, b = tuple(entry.get().split(","))
        info.config(text="Poprawnie wygenerowano wykres", fg="green")
        poly.interpolation_plot(float(a), float(b), var_nodes, linspace)

    except Exception as e:
        info.config(text="Wprowadź dobry przedział", fg="red")
        print(e)


def plot_generator(poly: Trigonometric, var_nodes: IntVar) -> None:
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


def show_generated_polynomial(poly: Trigonometric) -> None:
    """Wypisuje na ekran wygenerowany wielomian."""
    side_window = tk.Tk()
    side_window.title("Generated polynomial")
    side_window.geometry("600x400")
    text = Text(side_window)
    text.insert(INSERT, poly.trigonometric_polynomial)
    text.pack()


def create_trigonometric_interpolation(
    lbl_info: tk.Label,
    x: str,
    y: str,
) -> None:
    """Na podstawie wczytanych danych, tworzy interpolacyjny wielomian trygonometryczny."""
    if x == "" or y == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    elif not check_if_nodes_and_values_are_equal([x, y]):
        lbl_info.config(text="Niezgodna liczba węzłów i wartości", fg="red")
        return
    else:
        try:
            global polynomial
            polynomial = Trigonometric(x, y)
            lbl_info.config(text="Poprawnie wczytano dane", fg="green")
            show_generated_polynomial(polynomial)
        except Exception as e:
            lbl_info.config(
                text="Błędne dane",
                fg="red",
            )
            print(e)
    return


def trigonometric_interpolation(window: tk.Tk) -> None:
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
        text="Podaj węzły",
        font=("Helvetica", "16"),
    )

    etr_box_x = tk.Entry(window, width=100)

    lbl_instr_y = tk.Label(
        window,
        text="Podaj wartości w węzłach",
        font=("Helvetica", "16"),
    )

    etr_box_y = tk.Entry(window, width=100)

    lbl_info = tk.Label(window, text="", font=("Helvetica", "12"), fg="green")

    btn_load = tk.Button(
        window,
        text="Wczytaj dane i pokaż wielomian",
        font=("Helvetica", "16"),
        command=lambda: create_trigonometric_interpolation(
            lbl_info,
            str(etr_box_x.get()),
            str(etr_box_y.get()),
        )
        if str(etr_box_x.get()) != "" and str(etr_box_y.get())
        else None,
    )

    btn_compare_plots = tk.Button(
        window,
        text="Wygeneruj wykres wielomianu interpolacyjnego",
        font=("Helvetica", "16"),
        command=lambda: plot_generator(polynomial, var_nodes)
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

    lbl_instr_nodes = tk.Label(
        window,
        text="Generowanie równoodległych węzłów postaci x_k = 2kπ/n",
        font=("Helvetica", "16"),
    )

    lbl_instr_n = tk.Label(
        window,
        text="Podaj nieparzyste n",
        font=("Helvetica", "16"),
    )

    etr_box_n = tk.Entry(window, width=5)

    btn_generate_nodes = tk.Button(
        window,
        text="Wygeneruj węzły",
        font=("Helvetica", "16"),
        command=lambda: generate_nodes(lbl_info, str(etr_box_n.get()), etr_box_x)
        if str(etr_box_n.get()) != "" and int(etr_box_n.get()) % 2 != 0
        else lbl_info.config(
            text="Brak danych albo parzysta liczba węzłów",
            fg="red",
        ),
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
    lbl_info.pack()
    btn_load.pack()
    btn_compare_plots.pack()
    lbl_instr_nodes.pack()
    lbl_instr_n.pack()
    etr_box_n.pack()
    btn_generate_nodes.pack()
    ck_bx_nodes.pack()
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)
