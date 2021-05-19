from polynomial import Polynomial
import re


def main():
    poly_input = input("Podaj wielomian w postaci naturalnej: ")
    polynomial = Polynomial(poly_input)
    polynomial.parse_coefficients()


if __name__ == "__main__":
    main()
