import re


class Polynomial:
    def __init__(self, poly_string, form):
        if form == "natural":
            self.poly_string = "".join(poly_string.split(" "))
            pre_components = re.split('(; |, |\+|\-)', self.poly_string)
            components = []
            if "" in pre_components:
                pre_components.remove("")
            if pre_components[0] == "-":
                for i in range(0, len(pre_components) - 1, 2):
                    components.append(pre_components[i] + pre_components[i+1])
            else:
                components.append(pre_components[0])
                for i in range(1, len(pre_components) - 1, 2):
                    components.append(pre_components[i] + pre_components[i+1])
            components[0] = "+" + \
                components[0] if components[0][0] != "-" else components[0]
            self.components = components
            self.parse_natural_coefficients()
        else:
            

    def check_degree(self):
        degree = 0
        for elem in self.components:
            splitted_elem = elem.split("^")
            if len(splitted_elem) > 1:
                degree = int(splitted_elem[1]) if int(
                    splitted_elem[1]) > degree else degree
            elif "x" in splitted_elem[0]:
                degree = 1 if 1 > degree else degree
        return degree

    def parse_natural_coefficients(self):
        degree = self.check_degree()
        self.natural_coefficients = [0 for i in range(degree + 1)]
        for elem in self.components:
            if "x" not in elem:
                self.natural_coefficients[0] = int(elem)
            elif "x" in elem and "^" not in elem:
                char = elem.split("x")[0]
                if char == "-":
                    self.natural_coefficients[1] = -1
                elif char == "+":
                    self.natural_coefficients[1] = 1
                else:
                    self.natural_coefficients[1] = int(elem.split("x")[0])
            else:
                char = elem.split("x")[0]
                if char == "-":
                    self.natural_coefficients[int(elem.split("^")[1])] = -1
                elif char == "+":
                    self.natural_coefficients[int(elem.split("^")[1])] = 1
                else:
                    self.natural_coefficients[int(elem.split("^")[1])] = int(
                        elem.split("x")[0])

    def show_natual_form(self):
        result_output = ""
        for degree, coefficient in enumerate(self.natural_coefficients):
            if "-" in str(coefficient):
                result_output += f"({coefficient})x^{degree} + "
            else:
                result_output += f"{coefficient}x^{degree} + "
        print(result_output[:-2])
