import re
import utils


class Polynomial:
    """Reprezentacja wielomianu, głównie skupia się na parsowaniu."""
    def __init__(self, poly_string, form):
        self.poly_string = "".join(poly_string.split(" "))
        self.natural_coefficients = []
        if form == "natural":
            pre_components = re.split("(; |, |\+|\-)", self.poly_string)
            components = []
            if "" in pre_components:
                pre_components.remove("")
            if pre_components[0] == "-":
                for i in range(0, len(pre_components) - 1, 2):
                    components.append(pre_components[i] + pre_components[i + 1])
            else:
                components.append(pre_components[0])
                for i in range(1, len(pre_components) - 1, 2):
                    components.append(pre_components[i] + pre_components[i + 1])
            components[0] = (
                "+" + components[0] if components[0][0] != "-" else components[0]
            )
            self.components = components
            self.parse_natural_coefficients()
        else:
            result_x = []
            result_b = []
            saving = 0
            current = ""
            self.poly_string = utils.make_ones(self.poly_string)
            for index, char in enumerate(self.poly_string):
                if char == "(":
                    saving = 1
                if saving == 1:
                    current += char
                if (
                    char == ")"
                    and (index + 1) == len(self.poly_string)
                    or char == ")"
                    and self.poly_string[index + 1] != "("
                ):
                    saving = 0
                    current += char
                    result_x.append(current)
                    current = ""
                if saving == 0:
                    result_b.append(char)
            all_x = ""
            counter = 0
            for elem in result_x:
                current_elem = 0
                for char in elem:
                    if char == "(":
                        current_elem += 1
                if current_elem > counter:
                    counter = current_elem
                    all_x = elem

            all_x = utils.clear_list(all_x.replace("(x", "").split(")"))
            result_b = utils.create_list_of_ints(utils.clear_list(result_b))
            x = [float(elem) for elem in all_x]
            b = [float(elem) for elem in result_b]
            self.newton_coefficients = (x, b)
            self.change_to_natural_form()

    def check_degree(self):
        """Zwraca stopień wielomianu."""
        degree = 0
        for elem in self.components:
            splitted_elem = elem.split("^")
            if len(splitted_elem) > 1:
                degree = (
                    float(splitted_elem[1]) if float(splitted_elem[1]) > degree else degree
                )
            elif "x" in splitted_elem[0]:
                degree = 1 if 1 > degree else degree
        return degree

    def parse_natural_coefficients(self):
        """Parsuje współczynniki postaci naturalnej."""
        degree = self.check_degree()
        self.natural_coefficients = [0 for i in range(degree + 1)]
        for elem in self.components:
            if "x" not in elem:
                self.natural_coefficients[0] = float(elem)
            elif "x" in elem and "^" not in elem:
                char = elem.split("x")[0]
                if char == "-":
                    self.natural_coefficients[1] = -1
                elif char == "+":
                    self.natural_coefficients[1] = 1
                else:
                    self.natural_coefficients[1] = float(elem.split("x")[0])
            else:
                char = elem.split("x")[0]
                if char == "-":
                    self.natural_coefficients[float(elem.split("^")[1])] = -1
                elif char == "+":
                    self.natural_coefficients[float(elem.split("^")[1])] = 1
                else:
                    self.natural_coefficients[float(elem.split("^")[1])] = int(
                        elem.split("x")[0]
                    )

    def show_natual_form(self):
        """Zwraca formę naturaną wielomianu."""
        result_output = ""
        for degree, coefficient in enumerate(self.natural_coefficients):
            if "-" in str(coefficient):
                result_output += f"({coefficient})x^{degree} + "
            else:
                result_output += f"{coefficient}x^{degree} + "
        print(result_output[:-2])

    def change_to_natural_form(self):
        """Zmienia wielomian postaci Newtona do formy naturalnej."""
        x, b = self.newton_coefficients
        n = len(b) - 1
        a = [0 for i in range(n + 1)]
        a[n] = b[n]
        for i in range(n - 1, -1, -1):
            xi = x[i]
            a[i] = b[i]
            for k in range(i, n):
                a[k] = a[k] + (xi * a[k + 1])
        self.natural_coefficients = a

    def plot_natural_form(self, a, b):
        """Generuje wykres postaci naturalnej wielomianu."""
        utils.show_natural_polynomial(a, b, self.natural_coefficients)

    def plot_newton_form(self, a, b):
        """Generuje wykres postaci Newtona wielomianu."""
        utils.show_newton_polynomial(
            a, b, self.newton_coefficients[1], self.newton_coefficients[0]
        )
