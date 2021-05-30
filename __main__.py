from polynomial import Polynomial
from lagrange import Lagrange


def main() -> None:
    print("1. Interpolacja Lagrange'a.")
    print("2. Postacie wielomianów.")
    print("3. Zakończ pracę.")
    pick = input("Wybierz opcję: ")
    if pick == "1":
        lagrange_interpolation()
    elif pick == "2":
        polynomial_parse()
    elif pick == "3":
        print("Konczę pracę.")
        return
    else:
        print("Wybór nie został podjęty, ponownie uruchamiam program...")
        main()


def lagrange_interpolation() -> None:
    x = input("Podaj węzły w postaci [x0, x1, ...]: ")
    f = input("Podaj funkcję, którą chcesz interpolować: ")
    polynomial = Lagrange(x, f)
    pick = input("Wygenerować wykres? [T/N] ")
    if pick.lower() == "t":
        print("1. Funkcja w określonych węzłach.")
        print("2. Funkcja na przedziale.")
        pick2 = input("Wybierz opcję: ")
        if pick2 == "1":
            polynomial.plot_basic_function_in_xi()
        elif pick2 == "2":
            a, b = tuple(input("Podaj zakres w postaci [a, b]: ").split(","))
            polynomial.plot_basic_function_in_linear_area(int(a), int(b))
        else:
            print("Nie wybrano żadnej opcji, powrót do menu.")
            main()
    print("To wielomian interpolacyjny Lagrange'a: ", polynomial.lagrange_polynomial)
    pick = input("Wygenerować wykres? [T/N] ")
    if pick.lower() == "t":
        a, b = tuple(input("Podaj zakres w postaci [a, b]: ").split(","))
        polynomial.plot_lagrange_in_linear_area(int(a), int(b))


def polynomial_parse() -> None:
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
            polynomial.plot_natural_form(int(a), int(b))
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
            polynomial.plot_newton_form(int(a), int(b))
        pick = input(
            "Czy wygenerować teraz wykres na podstawie postaci naturalnej? [T/N] "
        )
        if pick.lower() == "t":
            a, b = tuple(input("Podaj zakres w postaci [a, b]: ").split(","))
            polynomial.plot_natural_form(int(a), int(b))
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
