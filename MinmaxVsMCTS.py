import random
from collections import defaultdict
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

def simulate_game():
    board = initialize_board()
    alphabeta_turn = True
    while True:
        if alphabeta_turn:
            move = alphabeta_move(board)
            board[move] = "O"
            if check_winner(board, "O"):
                return "AlphaBeta"
            if is_board_full(board):
                return "Draw"
        else:
            move = mcts_move(board)
            board[move] = "X"
            if check_winner(board, "X"):
                return "MCTS"
            if is_board_full(board):
                return "Draw"
        alphabeta_turn = not alphabeta_turn

def main():
    results = defaultdict(int)
    for game in range(1000):
        result = simulate_game()
        results[result] += 1
        print(f"Game {game + 1}: {result} wins")
    print("\nResults after 1000 games:")
    print(f"AlphaBeta wins: {results['AlphaBeta']}")
    print(f"MCTS wins: {results['MCTS']}")
    print(f"Draws: {results['Draw']}")

if __name__ == "__main__":
    main()
