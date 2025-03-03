from dataclasses import dataclass

@dataclass(frozen=True)
class Difficulty:
    squares: int
    mines: int