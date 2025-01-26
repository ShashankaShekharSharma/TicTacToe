import random
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
        new_board[move] = "O" if self.parent and self.parent.board.count("X") > self.board.count("X") else "X"
        child = MCTSNode(new_board, self)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

    def simulate(self):
        board = self.board.copy()
        current_player = "O" if self.parent and self.parent.board.count("X") > self.board.count("X") else "X"
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

def computer_move(board):
    print("Computer is thinking...")
    new_board = mcts(board)
    for i in range(9):
        if board[i] != new_board[i]:
            return i

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
