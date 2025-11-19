import argparse
import sys

from anchorfix import __version__
from anchorfix._core import DuplicateIdError, process_html_file


def main() -> None:
    parser = argparse.ArgumentParser(description="HTMLアンカーを連番IDに変換")
    parser.add_argument("htmlfile", help="入力HTMLファイルパス")
    parser.add_argument(
        "--prefix",
        default="a",
        help="アンカーIDのプレフィックス (デフォルト: a)",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"anchorfix v{__version__}",
        help="バージョン情報を表示",
    )

    args = parser.parse_args()

    try:
        result = process_html_file(args.htmlfile, prefix=args.prefix)
        print(result, end="")
    except FileNotFoundError:
        print(f"Error: File not found: {args.htmlfile}", file=sys.stderr)
        sys.exit(1)
    except DuplicateIdError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
