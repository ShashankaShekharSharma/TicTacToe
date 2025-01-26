import random
import pickle
from collections import defaultdict
from qiskit import Aer, QuantumCircuit, transpile, assemble, execute
import math


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


def minimax(board, depth, is_maximizing):
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
                score = minimax(board, depth + 1, False)
                board[i] = "="
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "=":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = "="
                best_score = min(score, best_score)
        return best_score


def minimax_move(board):
    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == "=":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = "="
            if score > best_score:
                best_score = score
                best_move = i
    return best_move


def alphabeta(board, depth, alpha, beta, is_maximizing):
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
                score = alphabeta(board, depth + 1, alpha, beta, False)
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
                score = alphabeta(board, depth + 1, alpha, beta, True)
                board[i] = "="
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  
        return best_score


def alphabeta_move(board):
    best_score = -float("inf")
    best_move = None
    alpha = -float("inf")
    beta = float("inf")
    for i in range(9):
        if board[i] == "=":
            board[i] = "O"
            score = alphabeta(board, 0, alpha, beta, False)
            board[i] = "="
            if score > best_score:
                best_score = score
                best_move = i
            alpha = max(alpha, best_score)
    return best_move


class MCTSNode:
    def __init__(self, board, parent=None):
        self.board = board.copy()
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = [i for i, cell in enumerate(board) if cell == "="]

    def select_child(self):
        return max(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))

    def expand(self):

        move = random.choice(self.untried_moves)
        self.untried_moves.remove(move)
        new_board = self.board.copy()
        new_board[move] = "X" if self.parent and self.parent.board.count("O") > self.board.count("O") else "O"
        child = MCTSNode(new_board, self)
        self.children.append(child)
        return child

    def update(self, result):

        self.visits += 1
        self.wins += result

    def simulate(self):

        board = self.board.copy()
        current_player = "X" if self.parent and self.parent.board.count("O") > self.board.count("O") else "O"
        while True:
            if check_winner(board, "O"):
                return 1
            if check_winner(board, "X"):
                return -1
            if is_board_full(board):
                return 0
            move = random.choice([i for i, cell in enumerate(board) if cell == "="])
            board[move] = current_player
            current_player = "X" if current_player == "O" else "O"


def mcts(board, iterations=1000):
    root = MCTSNode(board)

    for _ in range(iterations):
        node = root

        while node.untried_moves == [] and node.children != []:
            node = node.select_child()

        if node.untried_moves != []:
            node = node.expand()

        result = node.simulate()

        while node is not None:
            node.update(result)
            node = node.parent


    return max(root.children, key=lambda c: c.visits).board


def mcts_move(board):
    new_board = mcts(board)
    for i in range(9):
        if board[i] != new_board[i]:
            return i


def state_to_key(board):
    return "".join(board)


def load_q_table(filename="q_table.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return {}  


def save_q_table(q_table, filename="q_table.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(q_table, f)


def reinforcement_move(board, q_table, state, epsilon):
    available_moves = [i for i, cell in enumerate(board) if cell == "="]
    

    if random.uniform(0, 1) < epsilon:

        return random.choice(available_moves)
    else:

        q_values = [q_table.get((state, move), 0) for move in available_moves]
        max_q = max(q_values)
        best_moves = [move for move, q in zip(available_moves, q_values) if q == max_q]
        return random.choice(best_moves)


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


def update_q_table(q_table, state, action, reward, next_state, alpha=0.1, gamma=0.9):
    old_value = q_table.get((state, action), 0)
    next_max = max([q_table.get((next_state, a), 0) for a in range(9) if next_state[a] == "="], default=0)
    new_value = old_value + alpha * (reward + gamma * next_max - old_value)
    q_table[(state, action)] = new_value


def simulate_game(player1, player2, q_table=None, epsilon=0.1):
    board = initialize_board()
    state = state_to_key(board)
    player1_turn = True  

    while True:
        if player1_turn:

            if player1 == "Human":
                move = human_move(board)
            elif player1 == "Minimax":
                move = minimax_move(board)
            elif player1 == "AlphaBeta":
                move = alphabeta_move(board)
            elif player1 == "MCTS":
                move = mcts_move(board)
            elif player1 == "Reinforcement":
                move = reinforcement_move(board, q_table, state, epsilon)
            elif player1 == "Quantum":
                move = quantum_move(board, q_table, state, epsilon)
            board[move] = "X"
            if check_winner(board, "X"):
                display_board(board)
                print("Player 1 wins!")
                return "Player 1"
            if is_board_full(board):
                display_board(board)
                print("It's a draw!")
                return "Draw"
        else:

            if player2 == "Human":
                move = human_move(board)
            elif player2 == "Minimax":
                move = minimax_move(board)
            elif player2 == "AlphaBeta":
                move = alphabeta_move(board)
            elif player2 == "MCTS":
                move = mcts_move(board)
            elif player2 == "Reinforcement":
                move = reinforcement_move(board, q_table, state, epsilon)
            elif player2 == "Quantum":
                move = quantum_move(board, q_table, state, epsilon)
            board[move] = "O"
            if check_winner(board, "O"):
                display_board(board)
                print("Player 2 wins!")
                return "Player 2"
            if is_board_full(board):
                display_board(board)
                print("It's a draw!")
                return "Draw"


        state = state_to_key(board)
        player1_turn = not player1_turn
        display_board(board)


def main():

    players = ["Human", "Minimax", "AlphaBeta", "MCTS", "Reinforcement", "Quantum"]


    print("Choose Player 1:")
    for i, player in enumerate(players):
        print(f"{i + 1}. {player}")
    player1 = players[int(input("Enter your choice (1-6): ")) - 1]


    print("Choose Player 2:")
    for i, player in enumerate(players):
        print(f"{i + 1}. {player}")
    player2 = players[int(input("Enter your choice (1-6): ")) - 1]


    q_table = {}
    if player1 in ["Reinforcement", "Quantum"] or player2 in ["Reinforcement", "Quantum"]:
        q_table = load_q_table()


    print("\nStarting the game...")
    result = simulate_game(player1, player2, q_table)


    if player1 in ["Reinforcement", "Quantum"] or player2 in ["Reinforcement", "Quantum"]:
        save_q_table(q_table)


if __name__ == "__main__":
    main()