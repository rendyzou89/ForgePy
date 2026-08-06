"""
==================================================
ForgePy
Version : v0.7.2
Module  : Application Entry Point
==================================================
"""

from cli.dispatcher import Dispatcher
from cli.parser import Parser


def main() -> None:
    parser = Parser()
    args = parser.parse()

    Dispatcher().dispatch(args)


if __name__ == "__main__":
    main()