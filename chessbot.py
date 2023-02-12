import chess
import chess.engine


class ChessBot:
    def __init__(self, engine_path: str, is_white: bool):
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.is_white = is_white
        self.board = chess.Board()

    def receive_move(self, sen_move: str):
        pass

    def make_move(self) -> str:
        pass
