import chess.engine

from chessbot import ChessBot
from chessclicker import ChessClicker
from time import sleep


def setup():
    global clicker
    global bot
    engine_path = "engine\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
    clicker.detect_board()
    bot = ChessBot(engine_path, is_white=clicker.is_white)


def get_move():
    global clicker
    global bot
    clicker.wait_for_move()
    sleep(1)
    move = clicker.find_latest_move()
    print("Receiving: ", move)
    bot.receive_move(move)


def make_move():
    global clicker
    global bot
    move = bot.make_move()
    print("Making: ", move)
    clicker.make_move(move)


def main():
    setup()
    if not clicker.is_white:
        get_move()

    while not bot.board.is_game_over():
        make_move()
        get_move()


if __name__ == '__main__':
    clicker = ChessClicker()
    bot: ChessBot = None
    main()
