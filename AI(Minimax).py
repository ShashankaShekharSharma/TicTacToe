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

def computer_move(board):
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

def play_game():
    board = initialize_board()
    display_board(board)

    while True:
        human_pos = human_move(board)
        board[human_pos] = "X"
        display_board(board)

        if check_winner(board, "X"):
            print("You win!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break

        print("Computer is making a move...")
        computer_pos = computer_move(board)
        board[computer_pos] = "O"
        display_board(board)

        if check_winner(board, "O"):
            print("Computer wins!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()
