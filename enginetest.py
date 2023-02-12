import chess
import chess.engine

ENGINE_PATH = "engine\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"

def main():
    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
    board = chess.Board()
    while not board.is_game_over():
            result = engine.play(board, chess.engine.Limit(time=0.5))
            board.push(result.move)
            print("-------------")
            print(board)
    engine.quit()


if __name__ == "__main__":
    main()
