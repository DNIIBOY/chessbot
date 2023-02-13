import chess
import chess.engine


class ChessBot:
    def __init__(self, engine_path: str, is_white: bool):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.is_white = is_white
        self.board = chess.Board()

    def receive_move(self, san_move: str):
        white_to_move = self.board.turn  # True if the next move should be made by white
        if white_to_move is self.is_white:
            # Raise error if bot receives a move, when it is its turn to move
            raise ValueError("It is the bots turn to move, run make_move()")
        self.board.push_san(san_move)

    def make_move(self) -> str:
        white_to_move = self.board.turn  # True if the next move should be made by white
        if white_to_move is not self.is_white:
            raise ValueError("It is your turn to move, run receive_move()")
        result = self.engine.play(self.board, chess.engine.Limit(time=1))
        self.board.push(result.move)
        return result.move
