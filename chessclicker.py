import chess
import pyautogui
import PIL
import cv2
from time import sleep

import pyscreeze


class ChessClicker:
    def __init__(self):
        self.file_coords = []  # Coordinates of center of each file, len=8
        self.rank_coords = []  # Coordinates of center of each rank, len=8
        self.is_white = None  # Is the clicker playing for white?

    def _calculate_coords(self, board_location: pyscreeze.Box):
        square_width = board_location.width / 8
        print(square_width)
        self.file_coords = [board_location.left + i * square_width + square_width/2 for i in range(8)]
        self.rank_coords = [board_location.top + i * square_width + square_width/2 for i in range(8)][::-1]  # Ranks start from bottom
        # self.file_coords = [i+square_width/2 for i in self.file_coords]  # Center of each file
        # self.rank_coords = [i+square_width/2 for i in self.rank_coords]  # Center of each rank
        print(self.file_coords)
        print(self.rank_coords)

    def detect_board(self):
        for i, img in enumerate(["img/as_white.png", "img/as_black.png"]):
            if coords := pyautogui.locateOnScreen(img, confidence=0.8):
                print(coords)
                self.is_white = i % 2  # True first time, False second
                self._calculate_coords(coords)
                return coords
        return []

    def make_move(self, from_square: str, to_square: str):
        if not (self.file_coords and self.rank_coords):
            return
        from_square = chess.parse_square(from_square)
        to_square = chess.parse_square(to_square)
        for square in [from_square, to_square]:
            file_coord = self.file_coords[chess.square_file(square)]
            rank_coord = self.rank_coords[chess.square_rank(square)]
            pyautogui.click(file_coord, rank_coord)
            sleep(0.1)


def main():
    cc = ChessClicker()
    sleep(1)
    cc.detect_board()
    cc.make_move("e2", "e4")


if __name__ == '__main__':
    main()
