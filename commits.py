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
import datetime as dt
from collections import Counter
from datetime import date
from subprocess import run


DATE_FORMAT = "%a %b %d %H:%M:%S %Y %z"

type Details = tuple(list[str], list[date])


def get_commit_details() -> Details:
    """
    Extract names from 'Author:' lines in git log output.
    """
    result = run(["git", "log"], capture_output=True)
    lines = result.stdout.decode().split("\n")
    names = [line[8:].strip() for line in lines if line.startswith("Author: ")]
    dates = [
        dt.date.strptime(line[6:].strip(), DATE_FORMAT)
        for line in lines
        if line.startswith("Date: ")
    ]
    return names, dates


def display_individual_totals(names: list[str]):
    """
    Display individual commit counts, ranked highest to lowest,
    and a total count across all committers.
    """
    counts = Counter(names)
    for item in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{item[1]:3} {item[0]}")
    print("---")
    print(f"{counts.total():3}")


def display_weekly_totals(dates: list[date]):
    """
    Display total commits per week for the time period spanned by commits.

    Note: it is assumed that the time period is within a single year.
    """
    dates.sort()
    year = dates[0].year
    week_counts = Counter(d.isocalendar()[1] for d in dates)
    first_week = min(week_counts.keys())
    last_week = max(week_counts.keys())

    print("\n+------------+---------+")
    print("| Week       | Commits |")
    print("+------------+---------+")
    for week in range(first_week, last_week + 1):
        start_of_week = date.fromisocalendar(year, week, 1)
        count = week_counts.get(week, 0)
        print(f"| {start_of_week} |   {count:3}   |")
    print("+----------------------+")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])

    names, dates = get_commit_details()
    display_individual_totals(names)
    display_weekly_totals(dates)
