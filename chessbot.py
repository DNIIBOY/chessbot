import chess
import chess.engine


class ChessBot:
    def __init__(self, engine_path: str, is_white: bool, time_limit=1):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.is_white = is_white
        self.board = chess.Board()
        self.time_limit = time_limit

    def receive_move(self, move: chess.Move) -> None:
        """
        Receive a move
        :param move: The move played by the opponent
        :return: None
        """
        white_to_move = self.board.turn  # True if the next move should be made by white
        if white_to_move is self.is_white:
            # Raise error if bot receives a move, when it is its turn to move
            raise ValueError("It is the bots turn to move, run make_move()")
        self.board.push(move)

    def make_move(self) -> chess.engine.PlayResult:
        """
        The bot will make a move.
        :return: The result, containing the move made by the engine
        """
        white_to_move = self.board.turn  # True if the next move should be made by white
        if white_to_move is not self.is_white:
            raise ValueError("It is your turn to move, run receive_move()")
        result = self.engine.play(self.board, chess.engine.Limit(time=self.time_limit))
        self.board.push(result.move)
        return result

    def stop(self) -> str:
        """
        Stop the bot.
        :return: The final state of the board
        """
        self.engine.quit()
        return str(self.board)
