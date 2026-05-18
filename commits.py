# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///

# Program to gather stats on team member commits & per-week totals.
# (Useful when GitHub is being flaky!)

# You can supply the path to a cloned repository on the command line.
# If you don't supply any command line arguments, it is assumed that you
# are running the program from within a cloned repository.

import os
import sys
from collections import Counter
from datetime import date, timedelta
from subprocess import run


type Details = tuple(list[str], list[date])

DATE_FORMAT = "%a %b %d %H:%M:%S %Y %z"

SEVEN_DAYS = timedelta(days=7)


def get_commit_details() -> Details:
    """
    Extract committer names and commit dates from git log output.
    """
    result = run(["git", "log"], capture_output=True)
    lines = result.stdout.decode().split("\n")
    names = [line[8:].strip() for line in lines if line.startswith("Author: ")]
    dates = [
        date.strptime(line[6:].strip(), DATE_FORMAT)
        for line in lines
        if line.startswith("Date: ")
    ]
    return names, dates


def display_individual_counts(names: list[str]):
    """
    Display individual commit counts, ranked highest to lowest,
    and a total count across all committers.
    """
    counts = Counter(names)
    for item in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{item[1]:3} {item[0]}")
    print("---")
    print(f"{counts.total():3}")


def shift_to_monday(d: date) -> date:
    year, week, _ = d.isocalendar()
    return date.fromisocalendar(year, week, 1)


def display_weekly_totals(dates: list[date]):
    """
    Display total commits per week for the time period spanned by commits.
    """
    totals = Counter(shift_to_monday(d) for d in dates)

    print("\n+------------+---------+")
    print("| Week       | Commits |")
    print("+------------+---------+")

    week_start = shift_to_monday(min(dates))
    while week_start <= shift_to_monday(max(dates)):
        weekly_total = totals.get(week_start, 0)
        print(f"| {week_start} |   {weekly_total:3}   |")
        week_start += SEVEN_DAYS

    print("+----------------------+")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])

    names, dates = get_commit_details()
    display_individual_counts(names)
    display_weekly_totals(dates)
