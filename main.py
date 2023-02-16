from chessbot import ChessBot
from chessclicker import ChessClicker
from time import sleep
import sys


def setup():
    if len(sys.argv) > 1:
        limit = float(sys.argv[1])
    else:
        limit = 1
    global clicker
    global bot
    engine_path = "engine\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
    clicker.detect_board()
    bot = ChessBot(engine_path, is_white=clicker.is_white, time_limit=limit)


def get_move():
    global clicker
    global bot
    move = clicker.wait_for_move()
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
        if bot.board.is_game_over():
            break
        sleep(0.1)
        get_move()
    print(bot.stop())


if __name__ == '__main__':
    clicker = ChessClicker()
    bot: ChessBot = None
    main()
    print("ggez")
