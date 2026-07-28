#!/usr/bin/env python3
"""Create a no-overwrite PEP 723 Python script skeleton."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--requires-python", required=True)
    parser.add_argument("--dependency", action="append", default=[])
    args = parser.parse_args()

    output: Path = args.output
    if output.exists():
        parser.error(f"refusing to overwrite existing path: {output}")
    if not output.parent.exists():
        parser.error(f"parent directory does not exist: {output.parent}")

    dependency_lines = "\n".join(
        f'#   "{dependency}",' for dependency in args.dependency
    )
    dependencies = "# dependencies = []"
    if dependency_lines:
        dependencies = f"# dependencies = [\n{dependency_lines}\n# ]"

    content = f'''#!/usr/bin/env python3
# /// script
# requires-python = "{args.requires_python}"
{dependencies}
# ///


def main() -> None:
    pass


if __name__ == "__main__":
    main()
'''
    output.write_text(content, encoding="utf-8")
    output.chmod(0o755)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
