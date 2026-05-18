# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

# Program to gather stats on individual team member commits.
# (Useful when GitHub is being flaky!)

# You can supply the path to a cloned repository on the command line.
# If you don't supply any command line arguments, it is assumed that you
# are running the program from within a cloned repository.

import os
import sys
from collections import Counter
from subprocess import run


def get_committer_names() -> list[str]:
    """
    Extract names from 'Author:' lines in git log output.
    """
    result = run(["git", "log"], capture_output=True)
    lines = result.stdout.decode().split("\n")
    return [line[8:] for line in lines if line.startswith("Author: ")]


def display_commit_counts(counts: Counter):
    """
    Display commit counts, ranked highest to lowest, and a total.
    """
    items = counts.items()
    for name, count in sorted(items, key=lambda x: x[1], reverse=True):
        print(f"{count:3} {name}")
    print("---")
    print(f"{counts.total():3}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])

    names = get_committer_names()
    commits = Counter(names)
    display_commit_counts(commits)
