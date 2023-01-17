# coding=utf-8
"""Hardcoded dictionaries mapping pairs of areas' borders for example and input cubes."""

# Set constants:
EXAMPLE_EDGES = {
    ((0, 2), "↑"): dict(area_out=(1, 0), facing_out="↓", inv_out=True),
    ((0, 2), "↓"): dict(area_out=(1, 2), facing_out="↓", inv_out=False),
    ((0, 2), "→"): dict(area_out=(2, 3), facing_out="←", inv_out=True),
    ((0, 2), "←"): dict(area_out=(1, 1), facing_out="↓", inv_out=False),
    ((1, 2), "↓"): dict(area_out=(2, 2), facing_out="↓", inv_out=False),
    ((1, 2), "→"): dict(area_out=(2, 3), facing_out="↓", inv_out=True),
    ((1, 2), "←"): dict(area_out=(1, 1), facing_out="←", inv_out=False),
    ((2, 2), "↓"): dict(area_out=(1, 0), facing_out="↑", inv_out=True),
    ((2, 2), "→"): dict(area_out=(2, 3), facing_out="→", inv_out=False),
    ((2, 2), "←"): dict(area_out=(1, 1), facing_out="↑", inv_out=True),
    ((1, 0), "→"): dict(area_out=(1, 1), facing_out="→", inv_out=False),
    ((1, 0), "←"): dict(area_out=(2, 3), facing_out="↑", inv_out=True)}
INPUT_EDGES = {
    ((0, 1), "↑"): dict(area_out=(3, 0), facing_out="→", inv_out=False),
    ((0, 1), "↓"): dict(area_out=(1, 1), facing_out="↓", inv_out=False),
    ((0, 1), "→"): dict(area_out=(0, 2), facing_out="→", inv_out=False),
    ((0, 1), "←"): dict(area_out=(2, 0), facing_out="→", inv_out=True),
    ((0, 2), "↑"): dict(area_out=(3, 0), facing_out="↑", inv_out=False),
    ((0, 2), "↓"): dict(area_out=(1, 1), facing_out="←", inv_out=False),
    ((0, 2), "→"): dict(area_out=(2, 1), facing_out="←", inv_out=True),
    ((1, 1), "↓"): dict(area_out=(2, 1), facing_out="↓", inv_out=False),
    ((1, 1), "←"): dict(area_out=(2, 0), facing_out="↓", inv_out=False),
    ((2, 0), "→"): dict(area_out=(2, 1), facing_out="→", inv_out=False),
    ((2, 0), "↓"): dict(area_out=(3, 0), facing_out="↓", inv_out=False),
    ((3, 0), "→"): dict(area_out=(2, 1), facing_out="↑", inv_out=False)}
