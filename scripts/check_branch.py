"""Validate the project's codex/<type>/<description> branch convention."""

# ruff: noqa: INP001 -- Standalone repository utility, not an application package.
import argparse
import re
import sys


def is_valid_branch(branch: str) -> bool:
    return (
        re.fullmatch(
            r"codex/(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)/"
            r"[a-z0-9]+(?:-[a-z0-9]+)*",
            branch,
        )
        is not None
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("branch")
    if not is_valid_branch(parser.parse_args().branch):
        sys.exit("Expected codex/<type>/<lowercase-kebab-description>.")
