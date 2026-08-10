"""
==================================================
ForgePy
Module  : Application Entry Point
==================================================
"""

from cli.dispatcher import Dispatcher
from cli.parser import Parser


def main() -> int:
    parser = Parser()
    args = parser.parse()

    return Dispatcher().dispatch(args)


if __name__ == "__main__":
    raise SystemExit(main())
