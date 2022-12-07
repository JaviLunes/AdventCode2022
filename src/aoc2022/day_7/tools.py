# coding=utf-8
"""Tools used for solving the Day 7: No Space Left On Device puzzle."""

# Standard library imports:
from collections.abc import Iterable
from typing import Union


class File:
    """Node of a FileSystem tree representing an individual file."""
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def __repr__(self) -> str:
        return f"{self.name} (file, size={self.size})"


class Dir:
    """Node of a FileSystem tree representing a directory (with child nodes)."""
    def __init__(self, name: str):
        self.name = name
        self._children = {}

    def __repr__(self) -> str:
        return f"{self.name} (dir)"

    def add_child(self, child: Union[File, "Dir"]) -> None:
        """Register a new File or Dir object as a child of this Dir."""
        self._children.update({child.name: child})

    def get_child(self, target_dir: str) -> Union[File, "Dir"]:
        """Retrieve a child Dir from within this Dir, registering it first if new."""
        try:
            return self._children[target_dir]
        except KeyError:
            child = Dir(name=target_dir)
            self.add_child(child=child)
            return child

    @property
    def children(self) -> list[Union[File, "Dir"]]:
        """Provide all child Dir and File objects within this Dir."""
        return list(self._children.values())

    @property
    def size(self) -> int:
        """Provide the sum of sizes of all children within this Dir."""
        return sum(child.size for child in self._children.values())


class FileSystem:
    """Tree representation of Dir and File nodes nested within a root Dir."""
    def __init__(self):
        self.root = Dir(name="/")
        self.current = self.root
        self.parents = []

    @classmethod
    def from_terminal_output(cls, output: list[str]):
        """Build a FileSystem object from the terminal output of different commands."""
        file_system = FileSystem()
        for cmd, cmd_in, cmd_out in cls._parse_commands(output=output):
            if cmd == "cd":
                file_system.cd_make(target=cmd_in)
            elif cmd == "ls":
                file_system.ls_make(ls_output=cmd_out)
            else:
                raise ValueError(f"Unknown '{cmd}' command.")
        return file_system

    @staticmethod
    def _parse_commands(output: list[str]) -> Iterable[tuple[str, str, list[str]]]:
        """Parse lines of a terminal output into commands and their inputs/outputs."""
        command_groups = "|".join(["|"] + output).split("|$ ")[1:]
        for group in command_groups:
            if group.startswith("ls"):
                cmd = group.split("|")[0]
                cmd_in = ""
                cmd_out = group.split("|")[1:]
            else:
                cmd, cmd_in = group.split(" ")
                cmd_out = [""]
            yield cmd, cmd_in, cmd_out

    def cd_make(self, target: str) -> None:
        """Change the current directory to a target, creating it if required."""
        if target == "/":
            self.current = self.root
            self.parents = []
        elif target == "..":
            self.current = self.parents.pop(-1)
        else:
            self.parents.append(self.current)
            self.current = self.current.get_child(target_dir=target)

    def ls_make(self, ls_output: list[str]) -> None:
        """Add Dir and File objects to the current Dir."""
        for line in ls_output:
            size_or_dir, name = line.split(" ")
            if size_or_dir == "dir":
                child = Dir(name=name)
            else:
                child = File(name=name, size=int(size_or_dir))
            self.current.add_child(child=child)

    @property
    def children(self) -> list[Dir | File]:
        """Provide all Dir and File objects stored within this FileSystem."""
        return [self.root] + list(self._explode_children(parent=self.root))

    def _explode_children(self, parent: Dir) -> Iterable[Dir | File]:
        """Yield all child  within the provided parent Dir object."""
        for child in parent.children:
            yield child
            if isinstance(child, Dir):
                yield from self._explode_children(parent=child)

    @property
    def available_space(self) -> int:
        """Provide the total disk space of this FileSystem minus its used space."""
        return 70000000 - self.root.size

    def find_light_dirs(self, max_size: int) -> list[Dir]:
        """Return Dir children with at most a max size, sorted by decreasing size."""
        directories = list(filter(lambda i: isinstance(i, Dir), self.children))
        light_directories = list(filter(lambda d: d.size <= max_size, directories))
        return sorted(light_directories, key=lambda d: d.size, reverse=True)

    def find_heavy_dirs(self, min_size: int) -> list[Dir]:
        """Return Dir children with at least a min size, sorted by decreasing size."""
        directories = list(filter(lambda i: isinstance(i, Dir), self.children))
        heavy_directories = list(filter(lambda d: d.size >= min_size, directories))
        return sorted(heavy_directories, key=lambda d: d.size, reverse=True)

    def find_directory_to_delete(self, required_space: int) -> Dir:
        """Find the smallest Dir child that would free enough disk space."""
        space_to_delete = required_space - self.available_space
        heavy_dirs = self.find_heavy_dirs(min_size=space_to_delete)
        heavy_dirs = sorted(heavy_dirs, key=lambda d: d.size)
        return heavy_dirs[0]
