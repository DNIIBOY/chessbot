from typing import overload

import chess
import chess.engine


class ChessBot:
    def __init__(self, engine_path: str, is_white: bool, time_limit=1):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.is_white = is_white
        self.board = chess.Board()
        self.time_limit = time_limit

    def receive_move(self, move: chess.Move):
        white_to_move = self.board.turn  # True if the next move should be made by white
        if white_to_move is self.is_white:
            # Raise error if bot receives a move, when it is its turn to move
            raise ValueError("It is the bots turn to move, run make_move()")
        self.board.push(move)

    def make_move(self) -> chess.Move:
        white_to_move = self.board.turn  # True if the next move should be made by white
        if white_to_move is not self.is_white:
            raise ValueError("It is your turn to move, run receive_move()")
        result = self.engine.play(self.board, chess.engine.Limit(time=self.time_limit))
        self.board.push(result.move)
        return result.move


def main():
    engine_path = "engine\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
    bot = ChessBot(engine_path, is_white=False)
    while not bot.board.is_game_over():
        rec = input("Move: ")
        bot.receive_move(rec)
        res = bot.make_move()
        print(res)
        print(chess.square_name(res.from_square))
        print(chess.square_name(res.to_square))


if __name__ == '__main__':
    main()
