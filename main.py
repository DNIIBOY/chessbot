from chessbot import ChessBot
from chessclicker import ChessClicker
from time import sleep


def main():
    engine_path = "engine\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
    clicker = ChessClicker()
    clicker.detect_board()
    bot = ChessBot(engine_path, is_white=clicker.is_white)
    if not clicker.is_white:
        move = clicker.wait_for_move()
        bot.receive_move(move)

    while not bot.board.is_game_over():
        move = bot.make_move()
        print("Making: ", move)
        clicker.make_move(move)
        sleep(0.7)
        move = clicker.wait_for_move()
        print("Receiving: ", move)
        bot.receive_move(move)


if __name__ == '__main__':
    main()
