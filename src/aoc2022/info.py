# coding=utf-8
"""Constants defining metadata for this project."""""

# Standard library imports:
from pathlib import Path

# Set constants:
BASE_PATH_PUZZLES = Path(__file__).parent
BASE_PATH_TESTS = Path(__file__).parents[2] / "tests"
FILE_PATH_README = Path(__file__).parents[2] / "README.md"
PUZZLE_NAMES = tuple([
    "Day 1: Calorie Counting", "Day 2: Rock Paper Scissors",
    "Day 3: Rucksack Reorganization", "Day 4: Camp Cleanup", "Day 5: Supply Stacks",
    "Day 6: Tuning Trouble", "Day 7: No Space Left On Device",
    "Day 8: Treetop Tree House", "Day 9: Rope Bridge", "Day 10: Cathode-Ray Tube",
    "Day 11: Monkey in the Middle", "Day 12: Hill Climbing Algorithm",
    "Day 13: Distress Signal", "Day 14: Regolith Reservoir",
    "Day 15: Beacon Exclusion Zone", "Day 16: Proboscidea Volcanium",
    "Day 17: Pyroclastic Flow", "-",
    "-", "Day 20: Grove Positioning System", "-",
    "-", "-", "-",
    "-"])
YEAR = 2022
