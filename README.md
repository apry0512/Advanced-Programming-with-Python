# Advanced-Programming-with-Python
Assignment for Autumn 2025
Student Name: Aparajita Singh

Overview-
Explore this amazing Connect Four repository! It offers a full Python implementation complete with a fun text-based interface, an optional AI opponent with three exciting difficulty levels, and the ability to export your game data to JSON after every match.

Requirements-
Python 3.8 or higher
No external dependencies required


Steps-
1. Clone this repository.
2. Run the game in a terminal:
python connect_four.py


Command-line Options
Difficulty Set AI difficulty: easy, medium, or hard (default: medium)
Let the AI start first
Run built-in correctness tests and exit


Features-
1. Text-Based Game Loop
Fully interactive CLI version.
Human vs Human or Human vs AI modes.
Handles invalid inputs gracefully.

2. AI Opponent
Easy: Random valid move.
Medium: Minimax search to depth 3 with alpha-beta pruning.
Hard: Minimax search to depth 5 with alpha-beta pruning.
Evaluation heuristic prioritises:
Central column control.
Open 3-in-a-row or 4-in-a-row sequences.
Blocking the opponent’s potential wins.


3. Game Data Export
At the end of each match, users are prompted to save game data to a JSON file. The export file includes:
Move sequence with player IDs.
Final board state.
Winner and timestamp.

4. Testing and Correctness
The script includes built-in assertions and basic tests for win detection and valid move logic. 
Run with: python connect_four.py --run-tests


Credits-
Developed by: Aparajita Singh
Course: Advanced Programming with Python (ITNPAC1)
Institution: University of Stirling
Date: November 2025


Example Game Session
Starting Connect Four

|0 0 0 0 0 0 0|

|0 0 0 0 0 0 0|

|0 0 0 0 0 0 0|

|0 0 0 0 0 0 0|

|0 0 0 0 0 0 0|

|0 0 0 0 0 0 0|
----------------
 0 1 2 3 4 5 6

Your turn (Player 1). 
Valid columns: [0, 1, 2, 3, 4, 5, 6]
Choose column (0-6): 3
