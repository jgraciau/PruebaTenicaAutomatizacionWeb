import argparse
import logging
from pathlib import Path
from typing import Sequence

from agents.architect.architect_agent import ArchitectAgent


PLATFORM_ROOT = Path(__file__).resolve().parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the SKP Architect Agent against existing knowledge maps."
    )
    parser.add_argument(
        "--knowledge-dir",
        type=Path,
        default=PLATFORM_ROOT / "knowledge",
        help="Directory containing the five required knowledge maps.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PLATFORM_ROOT / "outputs",
        help="Directory where Architect Agent reports are written.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args(argv)
    ArchitectAgent(
        knowledge_directory=args.knowledge_dir,
        output_directory=args.output_dir,
    ).execute()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
