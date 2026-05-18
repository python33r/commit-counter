# commit-counter

Simple program to count individual commits in a team's Git repository.

Run this in the usual way, with the path to the cloned repository as a
command line argument. You can also run it with no command line arguments.
If you do the latter, the program assumes that you are running it from
within the cloned repository.

Note: if you have [`uv`](https://docs.astral.sh/uv/) installed, you can also run it with

    uv run commits.py

A suitable version of Python will then be downloaded, if one isn't already
available on your system.
