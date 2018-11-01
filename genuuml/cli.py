from argparse import ArgumentParser

from .inspectors import ClassInspector
from .printers import PlantUMLPrinter


def _parse_args() -> object:
    """
    Parse arguments, return parser.
    """
    parser = ArgumentParser()
    parser.add_argument("target_class",
                        help="Class name in python package. ex: scrapy.spiders.CrawlSpider")
    args = parser.parse_args()

    return args

def generate_class_hierarchy(target_class_path: str) -> ClassInspector:
    inspector = ClassInspector(class_path=target_class_path)

    return inspector

def main():
    parser = _parse_args()
    class_hierarchy = generate_class_hierarchy(parser.target_class)
    print(PlantUMLPrinter(class_hierarchy))


if __name__=='__main__':
    main()
