from anchorfix import __version__
from anchorfix._core import format_python_info, anchorfix


def main() -> None:
    print(f"anchorfix v{__version__}\n")
    print(format_python_info(anchorfix()))


if __name__ == "__main__":
    main()
