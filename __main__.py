from tkinter.constants import BOTTOM, LEFT, NO, NONE
from utils import clear_list, prepare_to_show_natural_polynomial
from polynomial import Polynomial
from lagrange import Lagrange
import tkinter as tk

window = tk.Tk()
window.title("Interpolation Pulse")
window.geometry("800x500")


def clear_win() -> None:
    for widgets in window.winfo_children():
        widgets.destroy()


def main() -> None:
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


def prepare_side_values(entry: tk.Entry, poly: Polynomial) -> None:
    a, b = tuple(entry.get().split(","))
    poly.plot_basic_function_in_linear_area(float(a), float(b))


def create_polynomial(lbl: tk.Label, x: str, f: str) -> None:
    if x == "" or x == " " or f == "" or f == " ":
        lbl.config(text="Nie wprowadzono danych", fg="red")
        return
    else:
        global polynomial
        polynomial = Lagrange(x, f)
        lbl.config(text="Poprawnie wczytano dane", fg="green")


def plot_generator(poly: Polynomial) -> None:
    side_window = tk.Tk()
    side_window.title("Plot generator")
    side_window.geometry("600x400")
    lbl_instruction = tk.Label(
        side_window,
        text="Podaj zakres w postaci [a, b]: ",
        font=("Helvetica", "24"),
    )
    lbl_instruction.pack()
    etr_box_a_b = tk.Entry(side_window, width=100)
    etr_box_a_b.pack()

    btn_generate_plot = tk.Button(
        side_window,
        text="Generuj",
        font=("Helvetica", "16"),
        command=lambda: prepare_side_values(etr_box_a_b, poly),
    )
    btn_generate_plot.pack()

    side_window.mainloop()


def lagrange_interpolation() -> None:
    clear_win()
    global polynomial
    polynomial = ""
    lbl_instruction = tk.Label(
        window,
        text="Interpolacja Lagrange'a",
        font=("Helvetica", "24"),
    )
    lbl_instruction.pack()

    lbl_instr_x = tk.Label(
        window,
        text="Podaj węzły w postaci [x0, x1, ...]: ",
        font=("Helvetica", "16"),
    )
    lbl_instr_x.pack()

    etr_box_x = tk.Entry(window, width=100)
    etr_box_x.pack()

    lbl_instr_f = tk.Label(
        window,
        text="Podaj funkcję, którą chcesz interpolować: ",
        font=("Helvetica", "16"),
    )
    lbl_instr_f.pack()

    etr_box_f = tk.Entry(window, width=100)
    etr_box_f.pack()
    lbl_info = tk.Label(window, text="", font=("Helvetica", "12"), fg="green")
    lbl_info.pack()
    btn_load = tk.Button(
        window,
        text="Wczytaj dane",
        font=("Helvetica", "16"),
        command=lambda: create_polynomial(
            lbl_info, str(etr_box_x.get()), str(etr_box_f.get())
        ),
    )
    btn_load.pack()
    btn_exit = tk.Button(
        window, text="Zakończ pracę", font=("Helvetica", "16"), command=window.destroy
    )
    btn_back = tk.Button(window, text="Wróć", font=("Helvetica", "16"), command=main)
    btn_make_plot = tk.Button(
        window,
        text="Wygeneruj wykres",
        font=("Helvetica", "16"),
        command=lambda: plot_generator(polynomial),
    )
    btn_make_plot.pack(side=LEFT)
    btn_exit.pack(side=BOTTOM)
    btn_back.pack(side=BOTTOM)
    # pick = input("Wygenerować wykres? [T/N] ")
    # if pick.lower() == "t":
    #     print("1. Funkcja w określonych węzłach.")
    #     print("2. Funkcja na przedziale.")
    #     pick2 = input("Wybierz opcję: ")
    #     if pick2 == "1":
    #         polynomial.plot_basic_function_in_xi()
    #     elif pick2 == "2":
    #         a, b = tuple(input("Podaj zakres w postaci [a, b]: ").split(","))
    #         polynomial.plot_basic_function_in_linear_area(float(a), float(b))
    #     else:
    #         print("Nie wybrano żadnej opcji, powrót do menu.")
    #         main()
    # print("To wielomian interpolacyjny Lagrange'a: ", polynomial.lagrange_polynomial)
    # pick = input("Wygenerować wykres? [T/N] ")
    # if pick.lower() == "t":
    #     a, b = tuple(input("Podaj zakres w postaci [a, b]: ").split(","))
    #     polynomial.plot_lagrange_in_linear_area(float(a), float(b))


def polynomial_parse() -> None:
    clear_win()
    print("1. Postać naturalna.")
    print("2. Postać Newtona.")
    print("3. Zakończ pracę.")
    pick = input("Wybierz opcję: ")
    if pick == "1":
        poly_input = input("Podaj wielomian w postaci naturalnej: ")
        polynomial = Polynomial(poly_input, "natural")
        pick = input("Wygenerować wykres? [T/N] ")
        if pick.lower() == "t":
            a, b = tuple(input("Podaj zakres w postaci [a, b]: ").split(","))
            polynomial.plot_natural_form(float(a), float(b))
            main()
        else:
            pick = input("Czy chcesz jeszcze korzystać z programu? [T/N] ")
            if pick.lower() == "t":
                main()
            else:
                print("Kończę pracę")
                return
    elif pick == "2":
        poly_input = input("Podaj wielomian w postaci Newtona: ")
        polynomial = Polynomial(poly_input, "newton")
        pick = input("Czy pokazać postać naturalną? [T/N] ")
        if pick.lower() == "t":
            polynomial.show_natual_form()
        pick = input("Wygenerować wykres? [T/N] ")
        if pick.lower() == "t":
            a, b = tuple(input("Podaj zakres w postaci [a, b]: ").split(","))
            polynomial.plot_newton_form(float(a), float(b))
        pick = input(
            "Czy wygenerować teraz wykres na podstawie postaci naturalnej? [T/N] "
        )
        if pick.lower() == "t":
            a, b = tuple(input("Podaj zakres w postaci [a, b]: ").split(","))
            polynomial.plot_natural_form(float(a), float(b))
            main()
        else:
            pick = input("Czy chcesz jeszcze korzystać z programu? [T/N] ")
            if pick.lower() == "t":
                main()
            else:
                print("Kończę pracę")
                return
    elif pick == "3":
        print("Konczę pracę.")
        return
    else:
        print("Wybór nie został podjęty, ponownie uruchamiam program...")
        main()


if __name__ == "__main__":
    main()
