def print_board(board):
    print("\n")
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("--+---+--")
    print("\n")


def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_draw(board):
    return all(cell != " " for row in board for cell in row)


def get_move(board, player):
    while True:
        try:
            pos = int(input(f"Player {player}, enter position (1-9): ")) - 1

            if pos < 0 or pos > 8:
                print("Invalid position. Choose 1-9.")
                continue

            row, col = divmod(pos, 3)

            if board[row][col] != " ":
                print("Position already taken. Try again.")
                continue

            return row, col

        except ValueError:
            print("Please enter a valid number.")


def main():
    board = [[" " for _ in range(3)] for _ in range(3)]

    first_player_symbol = ""
    while first_player_symbol not in ["X", "O"]:
        first_player_symbol = input("First player choose X or O: ").upper()

    player1 = first_player_symbol
    player2 = "O" if player1 == "X" else "X"

    current_player = player1

    print_board(board)

    while True:
        row, col = get_move(board, current_player)
        board[row][col] = current_player

        print_board(board)

        if check_winner(board, current_player):
            print(f" Player {current_player} wins!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        current_player = player2 if current_player == player1 else player1


if __name__ == "__main__":
    main()