import chess
from chessbot import ChessBot
from chessclicker import ChessClicker
from confighandler import ConfigHandler
from time import sleep


def setup():
    global clicker
    global bot
    global config
    config.load()
    engine_path = "engine\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
    clicker.detect_board()
    bot = ChessBot(engine_path, is_white=clicker.is_white, time_limit=config.time_limit)


def get_move():
    global clicker
    global bot
    move = clicker.wait_for_move()
    if move == chess.Move.null():
        return True
    print("Receiving: ", move)
    bot.receive_move(move)


def make_move():
    global clicker
    global bot
    result = bot.make_move()
    print("Making: ", result.move)
    clicker.make_move(result.move)


def main():
    setup()
    if not clicker.is_white:
        get_move()

    while not bot.board.is_game_over():
        make_move()
        if bot.board.is_game_over():
            break
        sleep(0.1)
        if get_move():
            return
    print(bot.stop())


if __name__ == '__main__':
    clicker = ChessClicker()
    bot: ChessBot = None
    config = ConfigHandler("config.json")
    main()
    print("ggez")
