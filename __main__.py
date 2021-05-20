from polynomial import Polynomial
import re


def main():
    print("1. Postać naturalna")
    print("2. Postać Newtona")
    poly_input = input("Podaj wielomian w postaci naturalnej: ")
    polynomial = Polynomial(poly_input, "")
    polynomial.show_natual_form()


if __name__ == "__main__":
    main()
