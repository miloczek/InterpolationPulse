import tkinter as tk
from tkinter import Text
from tkinter.constants import BOTTOM, INSERT

from polynomial import Polynomial
from utils import clear_win
import main_interface


def generate_natural_form(poly: Polynomial) -> None:
    """Przedstawia na ekranie wielomian w naturalnej postaci sprowadzony z postaci Newtona."""
    side_window = tk.Tk()
    side_window.title("Generated natural form polynomial")
    side_window.geometry("600x400")
    text = Text(side_window)
    text.insert(INSERT, poly.show_natual_form())
    text.pack()


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


def polynomial_parse(window: tk.Tk) -> None:
    """Koordynuje narzędzie zmieniania postaci wielomianów."""
    clear_win(window)

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

    btn_back = tk.Button(
        window,
        text="Wróć",
        font=("Helvetica", "16"),
        command=lambda: main_interface.main(window),
    )

    lbl_instruction.pack()
    btn_nat_to_newton.pack()
    btn_newton_to_nat.pack()
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)
