from os.path import join, dirname
from argparse import ArgumentParser

from .inspectors import ClassInspector
from .printers import PlantUMLPrinter
from . import __version__


def _parse_args() -> object:
    """
    Parse arguments, return parser.
    """
    parser = ArgumentParser()
    parser.add_argument("target_class",
                        help="Class name in python package. ex: scrapy.spiders.CrawlSpider")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(__version__))
    args = parser.parse_args()

    return args


def generate_class_hierarchy(target_class_path: str) -> ClassInspector:
    inspector = ClassInspector(class_path=target_class_path)

    return inspector


def main():
    parser = _parse_args()
    class_hierarchy = generate_class_hierarchy(parser.target_class)
    printer = PlantUMLPrinter(class_hierarchy)
    print(printer.source)


if __name__=='__main__':
    main()
