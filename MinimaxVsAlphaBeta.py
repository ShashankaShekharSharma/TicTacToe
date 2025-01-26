import random
from collections import defaultdict

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

def simulate_game():
    board = initialize_board()
    minimax_turn = True

    while True:
        if minimax_turn:
            move = minimax_move(board)
            board[move] = "O"
            if check_winner(board, "O"):
                return "Minimax"
            if is_board_full(board):
                return "Draw"
        else:
            move = alphabeta_move(board)
            board[move] = "X"
            if check_winner(board, "X"):
                return "AlphaBeta"
            if is_board_full(board):
                return "Draw"

        minimax_turn = not minimax_turn

def main():
    results = defaultdict(int)

    for game in range(1000):
        result = simulate_game()
        results[result] += 1
        print(f"Game {game + 1}: {result} wins")

    print("\nResults after 1000 games:")
    print(f"Minimax wins: {results['Minimax']}")
    print(f"AlphaBeta wins: {results['AlphaBeta']}")
    print(f"Draws: {results['Draw']}")

if __name__ == "__main__":
    main()
