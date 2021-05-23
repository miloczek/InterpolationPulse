from polynomial import Polynomial
import re


def main():
    print("1. Postać naturalna")
    print("2. Postać Newtona")
    pick = input("Wybierz opcję: ")
    if pick == "1":
        poly_input = input("Podaj wielomian w postaci naturalnej: ")
        polynomial = Polynomial(poly_input, "natural")
        polynomial.show_natual_form()
    else:
        poly_input = input("Podaj wielomian w postaci Newtona: ")
        polynomial = Polynomial(poly_input, "newton")



if __name__ == "__main__":
    main()
