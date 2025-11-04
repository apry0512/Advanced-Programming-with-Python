"""Connect four- Text based game with AI, game export and tests."""

from __future__ import annotations
import math
import random
import json
import time
from datetime import datetime
from typing import List, Tuple, Optional
import argparse

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4  #number of tokens needed in a line to win

class Board:
  def __init__(self):
    #Create a 6X7 grid initialised with empty cells(0)
    self.grid = [[EMPTY for _ in
range(COLUMN_COUNT)] for _ in
range(ROW_COUNT)]

def copy(self) -> 'Board':
  #for AI simulation
        b = Board()
        b.grid = [row[:] for row in self.grid]
        return b

def drop_piece(self, row: int, col: int, piece: int) -> None:
  #To place a players piece in specified row, column
        assert 0 <= row < ROW_COUNT and 0 <= col < COLUMN_COUNT, "drop_piece: row/col out of range"
        assert self.grid[row][col] == EMPTY, "drop_piece: cell not empty"
        self.grid[row][col] = piece
