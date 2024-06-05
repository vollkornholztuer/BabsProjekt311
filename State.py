from enum import Enum

# difficulty level of the puzzle
class PuzzleDifficulty(Enum):
    NONE = 0 # no choice yet, start state
    NORMAL = 1
    HARD = 2
    IMPOSSIBLE = 3