# Advanced-Programming-with-Python
Assignment for Autumn 2025
Student Name: Aparajita Singh

CONNECT FOUR-IN-A-ROW GAME using PYTHON

Overview-
This repository contains a complete implementation of Connect Four in Python, featuring:
A text-based user interface.
Optional AI opponent with three difficulty levels (easy, medium, hard).
Game data export to JSON after each match.
Basic unit tests and correctness checks.
The project was developed for a university assignment requiring demonstration of programming ability, version control via Git, and potential extension with AI or optimisation techniques.


How to Run:

Requirements-
Python 3.8 or higher
No external dependencies required


Steps-
1. Clone this repository.
  
2. Run the game in a terminal:
python connect_four.py

3. You can also specify options:
python connect_four.py --difficulty hard
python connect_four.py --ai-first
python connect_four.py --run-tests

Command-line Options
Option Description
--difficulty Set AI difficulty: easy, medium, or hard (default: medium)
--ai-first Let the AI start first
--run-tests Run built-in correctness tests and exit


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
Blocking opponent’s potential wins.


3. Game Data Export
At the end of each match, users are prompted to save game data to JSON. The export file includes:
Move sequence with player IDs.
Final board state.
Winner and timestamp.


4. Testing and Correctness
The script includes built-in assertions and basic tests for win detection and valid move logic. 
Run with: python connect_four.py --run-tests


Repository Structure
connect_four.py # Main game source code
README.md # This file
AI_Notes.md # Optional detailed explanation of AI heuristics


Credits
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

-----------------

 0 1 2 3 4 5 6

Your turn (Player 1). 
Valid columns: [0, 1, 2, 3, 4, 5, 6]
Choose column (0-6): 3

