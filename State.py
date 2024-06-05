from enum import Enum

# difficulty level of the puzzle
class PuzzleDifficulty(Enum):
    NONE = 0 # no choice yet, start state
    EASY = 1
    NORMAL = 2
    HARD = 3