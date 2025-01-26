import numpy as np
from qiskit import Aer, QuantumCircuit, transpile, assemble, execute
import random
import pickle

def initialize_board():
    return ["=" for _ in range(9)]

def display_board(board):
    print(f"{board[0]} {board[1]} {board[2]}")
    print(f"{board[3]} {board[4]} {board[5]}")
    print(f"{board[6]} {board[7]} {board[8]}")
    print()

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_board_full(board):
    return "=" not in board

def quantum_move(board, q_table, state, epsilon):
    available_moves = [i for i, cell in enumerate(board) if cell == "="]
    if random.uniform(0, 1) < epsilon:
        return random.choice(available_moves)
    else:
        q_values = [q_table.get((state, move), 0) for move in available_moves]
        max_q = max(q_values)
        best_moves = [move for move, q in zip(available_moves, q_values) if q == max_q]
        return random.choice(best_moves)

def human_move(board):
    while True:
        try:
            move = int(input("Enter your move (0-8): "))
            if move < 0 or move > 8:
                print("Invalid move. Please enter a number between 0 and 8.")
            elif board[move] != "=":
                print("Cell already occupied. Try again.")
            else:
                return move
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 8.")

def state_to_key(board):
    return "".join(board)

def update_q_table(q_table, state, action, reward, next_state, alpha=0.1, gamma=0.9):
    old_value = q_table.get((state, action), 0)
    next_max = max([q_table.get((next_state, a), 0) for a in range(9) if next_state[a] == "="], default=0)
    new_value = old_value + alpha * (reward + gamma * next_max - old_value)
    q_table[(state, action)] = new_value

def save_q_table(q_table, filename="q_table.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(q_table, f)

def load_q_table(filename="q_table.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def play_game(q_table, epsilon):
    board = initialize_board()
    display_board(board)
    state = state_to_key(board)

    while True:
        human_pos = human_move(board)
        board[human_pos] = "X"
        display_board(board)

        if check_winner(board, "X"):
            print("You win!")
            reward = -1
            next_state = state_to_key(board)
            update_q_table(q_table, state, human_pos, reward, next_state)
            save_q_table(q_table)
            break
        if is_board_full(board):
            print("It's a draw!")
            reward = 0
            next_state = state_to_key(board)
            update_q_table(q_table, state, human_pos, reward, next_state)
            save_q_table(q_table)
            break

        print("Quantum player is making a move...")
        quantum_pos = quantum_move(board, q_table, state, epsilon)
        board[quantum_pos] = "O"
        display_board(board)

        if check_winner(board, "O"):
            print("Quantum player wins!")
            reward = 1
            next_state = state_to_key(board)
            update_q_table(q_table, state, quantum_pos, reward, next_state)
            save_q_table(q_table)
            break
        if is_board_full(board):
            print("It's a draw!")
            reward = 0
            next_state = state_to_key(board)
            update_q_table(q_table, state, quantum_pos, reward, next_state)
            save_q_table(q_table)
            break

        state = state_to_key(board)

if __name__ == "__main__":
    q_table = load_q_table()
    epsilon = 0.1
    while True:
        play_game(q_table, epsilon)
        play_again = input("Play again? (y/n): ").lower()
        if play_again != "y":
            break
