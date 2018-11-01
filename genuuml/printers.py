"""
Printers
"""


class PlantUMLPrinter:
    """
    Printer for [PlantUML](http://plantuml.com/)
    """
    def __init__(self, class_inspector):
        self.inspector = class_inspector
        self.string_representation = None
        self.indent = 2

        self.build_string_representation()

    def build_string_representation(self):
        str_repr = "class {} as \"{}\" {{\n".format(self.inspector.absolute_class_path,
                                                self.inspector.class_name)

        for member in self.inspector.public_properties:
            str_repr += " " * self.indent
            str_repr += "+" + member
            str_repr += "\n"

        str_repr += "\n" if len(self.inspector.public_methods) > 0 else ""

        for member in self.inspector.public_methods:
            str_repr += " " * self.indent
            str_repr += "+" + member + "()"
            str_repr += "\n"

        str_repr += "}\n\n"

        for base in self.inspector.bases:
            str_repr += "{} -up-|> {}\n".format(self.inspector.absolute_class_path, base.absolute_class_path)

        str_repr += "\n" if len(self.inspector.bases) > 0 else ""

        for base in self.inspector.bases:
            str_repr += str(PlantUMLPrinter(base))

        self.string_representation = str_repr

        return self

    def __str__(self):
        return self.string_representation

