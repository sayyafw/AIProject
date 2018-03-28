import Board

if __name__ == "__main__":

    board = Board.Board()
    board.populate_board()
    board.read_board()
    if board.mode == "Moves":
        board.move()

    print(board.closest_piece(board.black_pieces[0]))

