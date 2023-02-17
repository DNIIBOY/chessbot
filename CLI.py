import chess
from chessbot import ChessBot
from chessclicker import ChessClicker
from confighandler import ConfigHandler
from rich import pretty
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt, Confirm
import sys
from time import sleep

TITLE_ART = """[green]
 ██████╗██╗  ██╗███████╗███████╗███████╗    ██████╗  ██████╗ ████████╗
██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██║     ███████║█████╗  ███████╗███████╗    ██████╔╝██║   ██║   ██║   
██║     ██╔══██║██╔══╝  ╚════██║╚════██║    ██╔══██╗██║   ██║   ██║   
╚██████╗██║  ██║███████╗███████║███████║    ██████╔╝╚██████╔╝   ██║   
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
                                                                      """


class CLI:
    def __init__(self):
        self.console = Console()
        self.config = ConfigHandler("config.json")
        self.title_art = TITLE_ART
        self.clicker: ChessClicker = None
        self.bot: ChessBot = None

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
        self.console.clear()
        self.console.rule()
        self.console.print(self.title_art)
        self.console.rule(f"[green]Playing as {'[italic white]white' if self.clicker.is_white else '[italic]black'}")
        input()

    def show_configs(self):
        options = f"""
        1. Time limit per move: {self.config.time_limit}
        2. Draw ponder arrows: {self.config.draw_ponder_arrows}
        3. Auto restart: {self.config.auto_restart}
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
