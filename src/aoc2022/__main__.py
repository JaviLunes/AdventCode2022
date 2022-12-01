# coding=utf-8
"""Main access point for command-line execution of core functions."""

# Standard library imports:
import sys

# Local application imports:
from aoc2022.common import AdventBuilder, AdventCalendar, AdventSolver


def main():
    """Main function managing execution requests of core functions from command line."""
    try:
        _, flag, *args = sys.argv
        assert flag in [
            "-h", "--help", "-b", "--build", "-s", "--solve", "-r", "--register"]
        day = -1 if not args else int(args[0])
    except (ValueError, AssertionError):
        print("Value Error: Provided command line arguments are not valid.")
        _print_help()
        sys.exit(2)
    else:
        if flag in ("-h", "--help"):
            _print_help()
            sys.exit(0)
        elif flag in ("-b", "--build"):
            builder = AdventBuilder()
            if day == -1:
                builder.build_all_templates()
            else:
                builder.build_templates(day=day)
        elif flag in ("-s", "--solve"):
            solver = AdventSolver()
            if day == -1:
                solver.print_all_days()
            else:
                solver.print_day(day=day)
        elif flag in ("-r", "--register"):
            calendar = AdventCalendar()
            if day == -1:
                calendar.register_all_days()
            else:
                calendar.register_day(day=day)
        else:
            print(f"Value Error: Unrecognised '{flag}' flag.")
            _print_help()
            sys.exit(2)


def _print_help():
    """Print usage information about the main function and its parameters."""
    usage = f"""\nUsage:
        -m aoc2022 [OPTION] [day]
    Arguments:
        -h, --help:
            Display this usage message and exit.
        -b, --build:
            Generate template files for solving and testing the provided day.
        -s, --solve:
            Compute and print the solutions to the puzzle of the provided day.
        - r, --register:
            Compute the solutions to the puzzle of the provided day and write 
            them to the table calendar in the README.md file.
        day:
            Puzzle number to build/solve. If -1 or not provided and building, 
            all not yet built puzzles will be built. If -1 or not provided 
            and solving or registering, all built puzzles will be solved or 
            registered.
    """.replace("\n    ", "\n")
    print(usage)


# Execute main code:
if __name__ == "__main__":
    main()
