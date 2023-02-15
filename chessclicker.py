import chess
import pyautogui
from time import sleep

import pyscreeze


class ChessClicker:
    def __init__(self):
        self.file_coords = []  # Coordinates of center of each file, len=8
        self.rank_coords = []  # Coordinates of center of each rank, len=8
        self.offset_size = 0  # Distance in x and y direction from top left corner of square to store coordinate
        self.is_white = None  # Is the clicker playing for white?
        self.active_colors = [(0, 0, 0), (0, 0, 0)]  # RGB values of the color of an active square on both dark and light squares
        self.last_move = [0, 0]  # From and to square, of the last move made

    def _calculate_coords(self, board_location: pyscreeze.Box) -> None:
        """
        Calculate coordinates of each file and rank
        :param board_location: Location of the board
        :return: None
        """
        square_width = board_location.width / 8
        self.offset_size = square_width / 2
        self.file_coords = [board_location.left + i * square_width + self.offset_size for i in range(8)]
        self.rank_coords = [board_location.top + i * square_width + self.offset_size for i in range(8)][::-1]  # Ranks start from bottom
        self.offset_size -= 5  # Subtract 1, to ensure reversing this stays within the right square
        if not self.is_white:
            # If the clicker is black, everything is reversed
            self.file_coords = self.file_coords[::-1]
            self.rank_coords = self.rank_coords[::-1]

    def _detect_active_colors(self) -> list[tuple[int, int, int]]:
        """
        Detect the background color of an active square,
        by clicking squares and reading values
        :return: List of colors of dark and light squares while active
        """
        for square in [0, 1]:
            file_coord = self.file_coords[chess.square_file(square)]
            rank_coord = self.rank_coords[chess.square_rank(square)]
            pyautogui.click(file_coord, rank_coord)  # Click the square, to give it active background
            image = pyautogui.screenshot()
            # Check top left corner of each square, to get only the background color
            color = image.getpixel((file_coord - self.offset_size, rank_coord - self.offset_size))
            self.active_colors[square] = color
            sleep(0.1)
        pyautogui.click(file_coord, rank_coord)  # Click the last square again, to deselect
        return self.active_colors

    def detect_board(self) -> pyscreeze.Box | False:
        """
        Detect location and size of the chess board
        :return: A box with the board, or False if not found
        """
        is_white = True
        for img in ["img/as_white.png", "img/as_black.png"]:
            if coords := pyautogui.locateOnScreen(img, confidence=0.8):
                print(coords)
                self.is_white = is_white  # True first time, False second
                self._calculate_coords(coords)
                self._detect_active_colors()
                return coords
            is_white = not is_white
        return False

    def find_latest_move(self) -> [chess.Square]:
        """
        Find the latest move made on the board (may include own move)
        :return: List of squares the move was made from and to
        """
        from_square = -1
        to_square = -1
        for f, file in enumerate(self.file_coords):
            for r, rank in enumerate(self.rank_coords):
                image = pyautogui.screenshot()
                corner_color = image.getpixel((file - self.offset_size, rank - self.offset_size))
                if corner_color not in self.active_colors:
                    continue
                center_color = image.getpixel((file, rank))
                if center_color == corner_color:
                    from_square = chess.parse_square(chess.FILE_NAMES[f] + chess.RANK_NAMES[r])
                else:
                    to_square = chess.parse_square(chess.FILE_NAMES[f] + chess.RANK_NAMES[r])
                if from_square != -1 and to_square != -1:
                    return [from_square, to_square]

    def wait_for_move(self) -> [chess.Square]:
        """
        Wait until there is made a move, which was not made by the clicker
        :return: The new move
        """
        while True:
            latest = self.find_latest_move()
            if latest != self.last_move:
                return latest

    def make_move(self, from_square: str, to_square: str) -> None:
        """
        Make a move from one square to another
        :param from_square: Name of the square to move from, eg: "e2"
        :param to_square: Name of the square to move to, eg: "e4"
        :return: None
        """
        if not (self.file_coords and self.rank_coords):
            return
        from_square = chess.parse_square(from_square)
        to_square = chess.parse_square(to_square)
        for square in [from_square, to_square]:
            file_coord = self.file_coords[chess.square_file(square)]
            rank_coord = self.rank_coords[chess.square_rank(square)]
            pyautogui.click(file_coord, rank_coord)
            sleep(0.1)
        self.last_move = [from_square, to_square]


def main():
    cc = ChessClicker()
    sleep(1)
    cc.detect_board()
    cc.make_move("e7", "e5")
    mvfrom, mvto = cc.wait_for_move()
    print(chess.square_name(mvfrom), chess.square_name(mvto))


if __name__ == '__main__':
    main()
