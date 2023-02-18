import chess
import chess.engine
from chessbot import ChessBot
from chessclicker import ChessClicker
from confighandler import ConfigHandler
from rich import pretty
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt, Confirm
import sys
import threading
from time import sleep

TITLE_ART = """[green]
 ██████╗██╗  ██╗███████╗███████╗███████╗    ██████╗  ██████╗ ████████╗
██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██║     ███████║█████╗  ███████╗███████╗    ██████╔╝██║   ██║   ██║   
██║     ██╔══██║██╔══╝  ╚════██║╚════██║    ██╔══██╗██║   ██║   ██║   
╚██████╗██║  ██║███████╗███████║███████║    ██████╔╝╚██████╔╝   ██║   
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
                                                                      """

ENGINE_PATH = "engine\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"


class CLI:
    def __init__(self):
        self.console = Console()
        self.config = ConfigHandler("config.json")
        self.title_art = TITLE_ART
        self.clicker: ChessClicker | None = None
        self.bot: ChessBot | None = None
        self.game_info: chess.engine.InfoDict | None = None

    def setup(self):
        # os.system('mode con: cols=80 lines=15')
        self.console.clear()
        self.config.load()
        pretty.install()
        self.clicker = ChessClicker()

    def show_home_page(self):
        options = """[green]
        [R]un the bot
        [D]etect the board
        [C]hange config
        [Q]uit the program
        """
        self.console.clear()
        self.console.rule()
        self.console.print(self.title_art)
        self.console.rule()
        self.console.print(f"[green]Board found: [/green]{self.clicker.has_found_board()}")
        self.console.print(options)
        choice = Prompt.ask("[green]What would you like to do?", choices=["r", "d", "c", "q"])
        if choice == "r" and not self.clicker.has_found_board():
            self.show_home_page()
        choices = {
            "r": self.run,
            "d": self.clicker.detect_board,
            "c": self.change_config,
            "q": self.quit
        }
        choices[choice]()
        self.show_home_page()

    def run(self):
        self.bot = ChessBot(ENGINE_PATH, self.clicker.is_white, self.config.time_limit)
        # self.analysis_thread = threading.Thread(target=self.bot.analyse_loop)
        # self.analysis_thread.start()
        sleep(self.config.time_limit)
        try:
            if self.config.calculate_score:
                self.game_info = self.bot.analyse()
            self.show_play_page()
            if not self.bot.is_white:
                # Receive a move first if playing as black
                self.bot.receive_move(self.clicker.wait_for_move())
                if self.config.calculate_score:
                    self.game_info = self.bot.analyse()
            self.play_chess()
        except KeyboardInterrupt:
            self.bot.stop()
            self.show_home_page()

    def show_play_page(self):
        self.console.clear()
        self.console.rule()
        self.console.print(self.title_art)
        self.console.rule(f"[green]Playing as {'[italic white]white' if self.clicker.is_white else '[italic]black'}")
        # Flipped board when playing as black
        board = self.bot.board if self.bot.is_white else self.bot.board.transform(chess.flip_vertical)
        if self.config.calculate_score:
            self.console.print("[green]" + str(board)[:31], end="")
            score = self.game_info["score"].white() if self.bot.is_white else self.game_info["score"].black()
            self.console.print(" " * 10 + f"[green]score: {score}")
            self.console.print("[green]" + str(board)[32:])
        else:
            self.console.print("[green]" + str(board))

    def play_chess(self):
        self.show_play_page()
        result = self.bot.make_move()
        self.clicker.make_move(result.move)
        if self.bot.board.is_game_over():
            self.bot.stop()
            self.show_home_page()
        if self.config.draw_ponder_arrows:
            self.clicker.draw_move_arrow(result.ponder)
        if self.config.calculate_score:
            self.game_info = self.bot.analyse()
        self.show_play_page()
        move = self.clicker.wait_for_move()
        if move == chess.Move.null() or self.bot.board.is_game_over():
            # If they resign or the game ended
            self.bot.stop()
            self.show_home_page()
        self.bot.receive_move(move)
        self.game_info = self.bot.analyse()
        self.play_chess()

    def show_configs(self):
        options = f"""
        1. Time limit per move: {self.config.time_limit}
        2. Draw ponder arrows: {self.config.draw_ponder_arrows}
        3. Calculate game score: {self.config.calculate_score}
        """
        self.console.clear()
        self.console.rule()
        self.console.print(self.title_art)
        self.console.rule("[green] Options")
        self.console.print(options)

    def change_config(self):
        self.show_configs()
        choice = Prompt.ask("[green]Which option do you wish to change", choices=["1", "2", "3", "q"])
        if choice == "q":
            self.config.save()
            self.show_home_page()
        choice = int(choice) - 1
        self.change_single_config(self.config.config_names[choice], self.config.config_types[choice])

    def change_single_config(self, config_name: str, config_type: type):
        self.show_configs()
        if config_type == float:
            new_val = FloatPrompt.ask(f"[green]What should the new value of {config_name} be?", default=1)
        elif config_type == bool:
            new_val = Confirm.ask(f"[green]Do you want {config_name} to be on?", default=False)
        else:
            raise ValueError(f"Unsupported type '{config_type}'")
        self.config.change_config(config_name, new_val)
        self.change_config()

    def quit(self):
        self.console.clear()
        sys.exit(0)


def main():
    cli = CLI()
    cli.setup()
    cli.show_home_page()


if __name__ == '__main__':
    main()
