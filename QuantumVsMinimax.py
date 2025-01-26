import random
import pickle
from collections import defaultdict
from qiskit import Aer, QuantumCircuit, transpile, assemble, execute
import os

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

def minimax(board, depth, alpha, beta, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "=":
                board[i] = "O"
                score = minimax(board, depth + 1, alpha, beta, False)
                board[i] = "="
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "=":
                board[i] = "X"
                score = minimax(board, depth + 1, alpha, beta, True)
                board[i] = "="
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

def classical_move(board):
    best_score = -float("inf")
    best_move = None
    alpha = -float("inf")
    beta = float("inf")
    for i in range(9):
        if board[i] == "=":
            board[i] = "O"
            score = minimax(board, 0, alpha, beta, False)
            board[i] = "="
            if score > best_score:
                best_score = score
                best_move = i
            alpha = max(alpha, best_score)
    return best_move

def quantum_move(board, q_table, state, epsilon):
    available_moves = [i for i, cell in enumerate(board) if cell == "="]
    if random.uniform(0, 1) < epsilon:
        move = quantum_random_move(available_moves)
    else:
        q_values = [q_table.get((state, move), 0) for move in available_moves]
        max_q = max(q_values)
        best_moves = [move for move, q in zip(available_moves, q_values) if q == max_q]
        move = random.choice(best_moves)
    return move

def quantum_random_move(available_moves):
    qc = QuantumCircuit(9, 9)
    qc.h(range(9))
    qc.measure(range(9), range(9))
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, simulator)
    qobj = assemble(compiled_circuit)
    result = execute(qc, simulator).result()
    counts = result.get_counts(qc)
    measurement = list(counts.keys())[0]
    for i, bit in enumerate(measurement):
        if bit == "1" and i in available_moves:
            return i
    return random.choice(available_moves)

def state_to_key(board):
    return "".join(board)

def update_q_table(q_table, state, action, reward, next_state, alpha=0.1, gamma=0.9):
    old_value = q_table.get((state, action), 0)
    next_max = max([q_table.get((next_state, a), 0) for a in range(9) if next_state[a] == "="], default=0)
    new_value = old_value + alpha * (reward + gamma * next_max - old_value)
    q_table[(state, action)] = new_value

def load_q_table(filename="q_table.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return {}

def save_q_table(q_table, filename="q_table.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(q_table, f)

def simulate_game(q_table, epsilon):
    board = initialize_board()
    state = state_to_key(board)
    classical_turn = True
    while True:
        if classical_turn:
            move = classical_move(board)
            board[move] = "O"
            if check_winner(board, "O"):
                reward = -1
                next_state = state_to_key(board)
                update_q_table(q_table, state, move, reward, next_state)
                return "Classical"
            if is_board_full(board):
                reward = 0
                next_state = state_to_key(board)
                update_q_table(q_table, state, move, reward, next_state)
                return "Draw"
        else:
            move = quantum_move(board, q_table, state, epsilon)
            board[move] = "X"
            if check_winner(board, "X"):
                reward = 1
                next_state = state_to_key(board)
                update_q_table(q_table, state, move, reward, next_state)
                return "Quantum"
            if is_board_full(board):
                reward = 0
                next_state = state_to_key(board)
                update_q_table(q_table, state, move, reward, next_state)
                return "Draw"
        state = state_to_key(board)
        classical_turn = not classical_turn

def main():
    q_table = load_q_table()
    epsilon = 1.0
    epsilon_decay = 0.995
    results = defaultdict(int)
    for game in range(1000):
        print(f"Simulating game {game + 1}...")
        result = simulate_game(q_table, epsilon)
        results[result] += 1
        epsilon *= epsilon_decay
    print("\nResults after 1000 games:")
    print(f"Classical AI wins: {results['Classical']}")
    print(f"Quantum AI wins: {results['Quantum']}")
    print(f"Draws: {results['Draw']}")
    save_q_table(q_table)

if __name__ == "__main__":
    main()
