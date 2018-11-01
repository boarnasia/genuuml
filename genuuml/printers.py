"""
Printers
"""

def build_plung_uml_source(inspector, indent=2):
    source = "class {} as \"{}\" {{\n".format(inspector.absolute_class_path,
                                              inspector.class_name)

    for member in inspector.public_properties:
        source += " " * indent
        source += "+" + member
        source += "\n"

    source += "\n" if len(inspector.public_methods) > 0 else ""

    for member in inspector.public_methods:
        source += " " * indent
        source += "+" + member
        source += "\n"

    source += "}\n\n"

    for base in inspector.bases:
        source += "{} -up-|> {}\n".format(inspector.absolute_class_path, base.absolute_class_path)

    source += "\n" if len(inspector.bases) > 0 else ""

    return source

class PlantUMLPrinter:
    """
    Printer for [PlantUML](http://plantuml.com/)
    """
    def __init__(self, class_inspector):
        self.inspector = class_inspector
        self.source = ""
        self.indent = 2

        self.build_source()

    def build_source(self):
        printed_list = []
        source = ""
        def build(inspector):
            nonlocal source, printed_list
            if inspector.absolute_class_path in printed_list: return ""
            source += build_plung_uml_source(inspector, self.indent)
            printed_list.append(inspector.absolute_class_path)
            for base in inspector.bases:
                build(base)

        build(self.inspector)
        self.source = source

