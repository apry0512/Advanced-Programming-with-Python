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
WINDOW_LENGTH = 4


class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

    def copy(self) -> 'Board':
        b = Board()
        b.grid = [row[:] for row in self.grid]
        return b

    def drop_piece(self, row: int, col: int, piece: int) -> None:
        assert 0 <= row < ROW_COUNT and 0 <= col < COLUMN_COUNT, "drop_piece: row/col out of range"
        assert self.grid[row][col] == EMPTY, "drop_piece: cell not empty"
        self.grid[row][col] = piece

    def is_valid_location(self, col: int) -> bool:
        return self.grid[0][col] == EMPTY

    def get_next_open_row(self, col: int) -> Optional[int]:
        for r in range(ROW_COUNT - 1, -1, -1):
            if self.grid[r][col] == EMPTY:
                return r
        return None

    def print_board(self) -> None:
        # Print top row first
        symbol = {EMPTY: '.', PLAYER_PIECE: 'X', AI_PIECE: 'O'}
        for row in self.grid:
            print('|' + ' '.join(symbol[x] for x in row) + '|')
        print('-' * (2 * COLUMN_COUNT + 1))
        print(' ' + ' '.join(str(i) for i in range(COLUMN_COUNT)))

    def winning_move(self, piece: int) -> bool:

        # Check horizontal win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if all(self.grid[r][c + i] == piece for i in range(4)):
                    return True

        # Check vertical win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if all(self.grid[r + i][c] == piece for i in range(4)):
                    return True

        # Check positive slope diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if all(self.grid[r + i][c + i] == piece for i in range(4)):
                    return True

        # Check negative slope diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if all(self.grid[r - i][c + i] == piece for i in range(4)):
                    return True

        return False

    def get_valid_locations(self) -> List[int]:
        return [c for c in range(COLUMN_COUNT) if self.is_valid_location(c)]

    def is_terminal_node(self) -> bool:
        return self.winning_move(PLAYER_PIECE) or self.winning_move(AI_PIECE) or len(self.get_valid_locations()) == 0


def evaluate_window(window: List[int], piece: int) -> int:
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score


def score_position(board: Board, piece: int) -> int:
    score = 0
    center_array = [board.grid[r][COLUMN_COUNT // 2] for r in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal
    for r in range(ROW_COUNT):
        row_array = board.grid[r]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLUMN_COUNT):
        col_array = [board.grid[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positive slope diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board.grid[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Negative slope diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board.grid[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def minimax(board: Board, depth: int, alpha: int, beta: int, maximizingPlayer: bool, piece: int) -> Tuple[int, Optional[int]]:
    valid_locations = board.get_valid_locations()
    is_terminal = board.is_terminal_node()
    if depth == 0 or is_terminal:
        if is_terminal:
            if board.winning_move(AI_PIECE):
                return (math.inf, None)
            elif board.winning_move(PLAYER_PIECE):
                return (-math.inf, None)
            else: # Game over
                return (0, None)
        else:
            return (score_position(board, piece), None)

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            assert row is not None
            b_copy = board.copy()
            b_copy.drop_piece(row, col, AI_PIECE)
            new_score, _ = minimax(b_copy, depth - 1, alpha, beta, False, piece)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_col

    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = board.get_next_open_row(col)
            assert row is not None
            b_copy = board.copy()
            b_copy.drop_piece(row, col, PLAYER_PIECE)
            new_score, _ = minimax(b_copy, depth - 1, alpha, beta, True, piece)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_col


def pick_best_move(board: Board, piece: int, difficulty: str = 'medium') -> int:
    valid_locations = board.get_valid_locations()
    if not valid_locations:
        raise ValueError("No valid moves available")

    if difficulty == 'easy':
        return random.choice(valid_locations)
    elif difficulty == 'medium':
        depth = 3
    elif difficulty == 'hard':
        depth = 5
    else:
        depth = 3 
        # Default to medium in case of invalid difficulty 

    _, col = minimax(board, depth, -math.inf, math.inf, True, piece)
    if col is None:
        return random.choice(valid_locations)
    return col

def export_game(moves: List[Tuple[int, int]], board: Board, winner: Optional[int]) -> str:
    data = {
        'moves': [{'player': m[0], 'col': m[1]} for m in moves],
        'final_board': board.grid,
        'winner': int(winner) if winner is not None else None,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    filename = f"connect_four_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return filename


def play_game(human_first: bool = True, ai_difficulty: str = 'medium') -> None:
    board = Board()
    game_over = False
    turn = 0 if human_first else 1
    moves: List[Tuple[int, int]] = []

    print("Starting Connect Four")
    board.print_board()

    while not game_over:
        if turn == 0:

            # Human's turn
            valid_cols = board.get_valid_locations()
            print(f"Your turn (Player {PLAYER_PIECE}). Valid columns: {valid_cols}")
            while True:
                try:
                    col = int(input("Choose column (0-6): "))
                    if col not in valid_cols:
                        print("Column full or invalid, choose again.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Enter a number 0-6.")

            row = board.get_next_open_row(col)
            assert row is not None
            board.drop_piece(row, col, PLAYER_PIECE)
            moves.append((PLAYER_PIECE, col))

            if board.winning_move(PLAYER_PIECE):
                board.print_board()
                print("You win!")
                game_over = True
                winner = PLAYER_PIECE

        else:
            # AI's turn
            print("AI is thinking...")
            col = pick_best_move(board, AI_PIECE, ai_difficulty)
            row = board.get_next_open_row(col)
            assert row is not None
            board.drop_piece(row, col, AI_PIECE)
            moves.append((AI_PIECE, col))

            if board.winning_move(AI_PIECE):
                board.print_board()
                print("AI wins!")
                game_over = True
                winner = AI_PIECE

        board.print_board()

        if len(board.get_valid_locations()) == 0 and not game_over:
            print("Game is a draw.")
            game_over = True
            winner = None

        turn ^= 1

    # to export
    save = input("Save this game to JSON? (y/n): ").strip().lower()
    if save == 'y':
        fname = export_game(moves, board, winner)
        print(f"Saved game to {fname}")

def run_basic_tests():
    print("Running basic tests...")
    b = Board()

    assert b.get_next_open_row(0) == ROW_COUNT - 1
    r = b.get_next_open_row(0)
    b.drop_piece(r, 0, PLAYER_PIECE)
    assert b.grid[ROW_COUNT - 1][0] == PLAYER_PIECE
    assert b.is_valid_location(0)

    for i in range(ROW_COUNT - 1):
        rr = b.get_next_open_row(0)
        if rr is None:
            break
        b.drop_piece(rr, 0, AI_PIECE)
    assert not b.is_valid_location(0)

    # for horizontal win
    b2 = Board()
    for c in range(4):
        r = b2.get_next_open_row(c)
        assert r is not None
        b2.drop_piece(r, c, PLAYER_PIECE)
    assert b2.winning_move(PLAYER_PIECE)

    # for vertical win
    b3 = Board()
    c = 0
    for _ in range(4):
        r = b3.get_next_open_row(c)
        assert r is not None
        b3.drop_piece(r, c, AI_PIECE)
    assert b3.winning_move(AI_PIECE)

    # for diagonal win
    b4 = Board()
    moves = [(PLAYER_PIECE, 0), (AI_PIECE, 1), (PLAYER_PIECE, 1), (AI_PIECE, 2), (AI_PIECE, 2), (PLAYER_PIECE, 2),
             (AI_PIECE, 3), (AI_PIECE, 3), (AI_PIECE, 3), (PLAYER_PIECE, 3)]
    for p, col in moves:
        r = b4.get_next_open_row(col)
        assert r is not None
        b4.drop_piece(r, col, p)
    assert b4.winning_move(PLAYER_PIECE)

    print("All basic tests passed.")


def main():
    parser = argparse.ArgumentParser(description='Connect Four game')
    parser.add_argument('--run-tests', action='store_true', help='Run basic tests and exit')
    parser.add_argument('--ai-first', action='store_true', help='Let AI play first')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'], help='AI difficulty')
    args = parser.parse_args([]) 
    if args.run_tests:
        run_basic_tests()
        return

    human_first = not args.ai_first
    
    ai_difficulty = args.difficulty
    if ai_difficulty is None:
        while True:
            difficulty_input = input("Choose AI difficulty (easy, medium, hard): ").strip().lower()
            if difficulty_input in ['easy', 'medium', 'hard']:
                ai_difficulty = difficulty_input
                break
            else:
                print("Invalid difficulty. Please choose 'easy', 'medium', or 'hard'.")

    play_game(human_first=human_first, ai_difficulty=ai_difficulty)


if __name__ == '__main__':
    main()
