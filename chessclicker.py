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
        self.file_coords = [board_location.left + i * square_width + square_width / 2 for i in range(8)]
        self.rank_coords = [board_location.top + i * square_width + square_width / 2 for i in range(8)][::-1]  # Ranks start from bottom
        if not self.is_white:
            # If the clicker is black, everything is reversed
            self.file_coords = self.file_coords[::-1]
            self.rank_coords = self.rank_coords[::-1]
        print(self.file_coords)
        print(self.rank_coords)

    def detect_board(self):
        is_white = True
        for img in ["img/as_white.png", "img/as_black.png"]:
            if coords := pyautogui.locateOnScreen(img, confidence=0.8):
                print(coords)
                self.is_white = is_white  # True first time, False second
                self._calculate_coords(coords)
                return coords
            is_white = not is_white
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
    cc.make_move("e7", "e5")


if __name__ == '__main__':
    main()
