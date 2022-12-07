# coding=utf-8
"""Main access point for command-line execution of core functions."""

# Standard library imports:
import sys

# Third party imports:
from aoc_tools.puzzle_solving import AdventCalendar, AdventSolver
from aoc_tools.puzzle_building import AdventBuilder

# Local application imports:
from aoc2022.info import BASE_PATH_PUZZLES, BASE_PATH_TESTS, FILE_PATH_README
from aoc2022.info import PUZZLE_NAMES, YEAR


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
        builder = AdventBuilder(
            year=YEAR, puzzles_base_path=BASE_PATH_PUZZLES,
            puzzle_names=PUZZLE_NAMES, tests_base_path=BASE_PATH_TESTS)
        solver = AdventSolver(year=YEAR, puzzle_names=PUZZLE_NAMES)
        calendar = AdventCalendar(readme_file=FILE_PATH_README, solver=solver)
        if flag in ("-h", "--help"):
            _print_help()
            sys.exit(0)
        elif flag in ("-b", "--build"):
            if day == -1:
                builder.build_all_templates()
            else:
                builder.build_templates(day=day)
        elif flag in ("-s", "--solve"):
            if day == -1:
                solver.print_all_days()
            else:
                solver.print_day(day=day)
        elif flag in ("-r", "--register"):
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
        -m aoc{YEAR} [OPTION] [day]
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
