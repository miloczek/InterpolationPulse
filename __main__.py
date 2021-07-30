from tkinter import Text, font
from tkinter.constants import BOTTOM, INSERT, LEFT, NO, NONE, RIGHT
from utils import clear_list, prepare_to_show_natural_polynomial
from polynomial import Polynomial
from lagrange import Lagrange
import tkinter as tk

window = tk.Tk()
window.title("Interpolation Pulse")
window.geometry("1000x800")


def clear_win() -> None:
    """Pozbywa się wszyskich elementów w oknie."""
    for widgets in window.winfo_children():
        widgets.destroy()


def main() -> None:
    """Główna funkcja, spajająca wszystkie funkcjonalności i
    porządkująca interfejsy."""
    clear_win()

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
        command=lagrange_interpolation,
    )
    btn_polynomial = tk.Button(
        window,
        text="Postacie wielomianów",
        font=("Helvetica", "16"),
        command=polynomial_parse,
    )
    btn_exit = tk.Button(
        window, text="Zakończ pracę", font=("Helvetica", "16"), command=window.destroy
    )
    btn_lagrange.pack()
    btn_polynomial.pack()
    btn_exit.pack(side=BOTTOM)
    window.mainloop()


def show_generated_polynomial(poly: Lagrange) -> None:
    side_window = tk.Tk()
    side_window.title("Generated polynomial")
    side_window.geometry("600x400")
    text = Text(side_window)
    text.insert(INSERT, poly.lagrange_polynomial)
    text.pack()


def prepare_interval_values(
    entry: tk.Entry, info: tk.Label, poly: Lagrange, mode: str
) -> None:
    """Wczytuje wartości brzegowe przedziału z pola tekstowego i
    uruchamia wizualizację funkcji"""
    try:
        a, b = tuple(entry.get().split(","))
        info.config(text="Poprawnie wygnerowano wykres", fg="green")
        if mode == "normal":
            poly.plot_basic_function_in_linear_area(float(a), float(b))
        elif mode == "lagrange":
            poly.plot_lagrange_in_linear_area(float(a), float(b))
        else:
            poly.plot_compare_plot_in_linear_area(float(a), float(b))
    except Exception as e:
        info.config(text="Wprowadź dobry przedział", fg="red")
        print(e)


def create_lagrange_polynomial(
    lbl_info: tk.Label, x: str, f: str, precision: str
) -> None:
    """Na podstawie wczytanych węzłów i funkcji, tworzy wielomian Lagrange'a."""
    if x == " " or f == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        try:
            global polynomial
            polynomial = Lagrange(x, f, precision)
            lbl_info.config(text="Poprawnie wczytano dane", fg="green")
            show_generated_polynomial(polynomial)
        except Exception as e:
            lbl_info.config(text="Błędne dane", fg="red")
            print(e)
            return


def create_natural_newton_polynomial(
    lbl_info: tk.Label, interval: str, f: str, form: str
) -> None:
    """Na podstawie wczytanego wielomianu i przedziału generujejego wykres."""
    if interval == "" or f == "":
        lbl_info.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        try:
            global polynomial
            polynomial = Polynomial(f, form)
            a, b = interval.split(",")
            lbl_info.config(text="Poprawnie wczytano dane", fg="green")
            if form == "natural":
                polynomial.plot_natural_form(float(a), float(b))
            else:
                polynomial.plot_newton_form(float(a), float(b))
        except Exception as e:
            lbl_info.config(text="Błędne dane", fg="red")
            print(e)
            return


def generate_natural_form(poly: Polynomial) -> None:
    side_window = tk.Tk()
    side_window.title("Generated natural form polynomial")
    side_window.geometry("600x400")
    text = Text(side_window)
    text.insert(INSERT, poly.show_natual_form())
    text.pack()


def natural_form() -> None:
    """Pozwala wczytać wielomian w postaci naturalnej i zobaczyć jego wykres."""
    global polynomial
    polynomial = ""
    side_window = tk.Tk()
    side_window.title("Natural form")
    side_window.geometry("600x400")
    lbl_instruction = tk.Label(
        side_window,
        text="Podaj wielomian w postaci naturalnej",
        font=("Helvetica", "24"),
    )
    etr_box_nat = tk.Entry(side_window, width=100)
    btn_load = tk.Button(
        side_window,
        text="Wczytaj wielomian i wygeneruj wykres",
        font=("Helvetica", "16"),
        command=lambda: create_natural_newton_polynomial(
            lbl_info,
            str(etr_box_a_b.get()),
            str(etr_box_nat.get()),
            "natural",
        ),
    )
    lbl_interval = tk.Label(
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

    lbl_instruction.pack()
    etr_box_nat.pack()
    lbl_interval.pack()
    etr_box_a_b.pack()
    lbl_info.pack()
    btn_load.pack()

    side_window.mainloop()


def newton_form() -> None:
    """Pozwala wczytać wielomian w postaci Newtona, zobaczyć jego wykres i
    wygenerować na jego podstawie wielomian w postaci naturalnej."""
    global polynomial
    polynomial = ""
    side_window = tk.Tk()
    side_window.title("Newton form to natural form")
    side_window.geometry("600x400")
    lbl_instruction = tk.Label(
        side_window,
        text="Podaj wielomian w postaci Newtona",
        font=("Helvetica", "24"),
    )
    etr_box_nat = tk.Entry(side_window, width=100)
    btn_load = tk.Button(
        side_window,
        text="Wczytaj wielomian i wygeneruj wykres",
        font=("Helvetica", "16"),
        command=lambda: create_natural_newton_polynomial(
            lbl_info,
            str(etr_box_a_b.get()),
            str(etr_box_nat.get()),
            "newton",
        ),
    )
    lbl_interval = tk.Label(
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

    btn_generate = tk.Button(
        side_window,
        text="Wygeneruj postać naturalną",
        font=("Helvetica", "16"),
        command=lambda: generate_natural_form(polynomial)
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    lbl_instruction.pack()
    etr_box_nat.pack()
    lbl_interval.pack()
    etr_box_a_b.pack()
    lbl_info.pack()
    btn_load.pack()
    btn_generate.pack()

    side_window.mainloop()


def plot_generator(poly: Polynomial, mode: str) -> None:
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


def lagrange_interpolation() -> None:
    """Główna funkcja przygotowująca wielomiany Lagrange'a. Ustawia poprawnie
    interfejsy i uruchamia funkcje pomocnicze."""
    clear_win()
    global polynomial
    polynomial = ""

    lbl_instruction = tk.Label(
        window,
        text="Interpolacja Lagrange'a",
        font=("Helvetica", "24"),
    )

    lbl_instr_x = tk.Label(
        window,
        text="Podaj węzły w postaci [x0, x1, ...]: ",
        font=("Helvetica", "16"),
    )

    etr_box_x = tk.Entry(window, width=100)

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
        command=lambda: create_lagrange_polynomial(
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
        command=lambda: plot_generator(polynomial, "compare")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    btn_exit = tk.Button(
        window, text="Zakończ pracę", font=("Helvetica", "16"), command=window.destroy
    )

    btn_back = tk.Button(window, text="Wróć", font=("Helvetica", "16"), command=main)

    btn_make_function_plot = tk.Button(
        window,
        text="Wygeneruj wykres wyjściowej funkcji",
        font=("Helvetica", "16"),
        command=lambda: plot_generator(polynomial, "normal")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
    )

    btn_make_interpolation_plot = tk.Button(
        window,
        text="Wygeneruj wykres wielomianu interpolacyjnego",
        font=("Helvetica", "16"),
        command=lambda: plot_generator(polynomial, "lagrange")
        if lbl_info.cget("text") == "Poprawnie wczytano dane"
        else None,
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
    btn_make_interpolation_plot.pack(side=RIGHT)
    btn_make_function_plot.pack(side=LEFT)
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)


def polynomial_parse() -> None:
    """Koordynuje narzędzie zmieniania postaci wielomianów."""
    clear_win()

    lbl_instruction = tk.Label(
        window,
        text="Postacie wielomianów",
        font=("Helvetica", "24"),
    )

    btn_nat_to_newton = tk.Button(
        window,
        text="Postać naturalna",
        font=("Helvetica", "16"),
        command=natural_form,
    )

    btn_newton_to_nat = tk.Button(
        window,
        text="Postać Newtona",
        font=("Helvetica", "16"),
        command=newton_form,
    )

    btn_exit = tk.Button(
        window, text="Zakończ pracę", font=("Helvetica", "16"), command=window.destroy
    )

    btn_back = tk.Button(window, text="Wróć", font=("Helvetica", "16"), command=main)

    lbl_instruction.pack()
    btn_nat_to_newton.pack()
    btn_newton_to_nat.pack()
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)


if __name__ == "__main__":
    main()
