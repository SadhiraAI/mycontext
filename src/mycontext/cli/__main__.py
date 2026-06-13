"""Enable `python -m mycontext.cli`."""

from . import main

if __name__ == "__main__":
    raise SystemExit(main())
