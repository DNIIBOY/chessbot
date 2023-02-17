from rich import pretty
from rich.console import Console
from rich.prompt import Prompt
import sys


class CLI:
    def __init__(self):
        self.console = Console()
        self.title_art = """[green]
 ██████╗██╗  ██╗███████╗███████╗███████╗    ██████╗  ██████╗ ████████╗
██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██║     ███████║█████╗  ███████╗███████╗    ██████╔╝██║   ██║   ██║   
██║     ██╔══██║██╔══╝  ╚════██║╚════██║    ██╔══██╗██║   ██║   ██║   
╚██████╗██║  ██║███████╗███████║███████║    ██████╔╝╚██████╔╝   ██║   
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
                                                                      """

    def setup(self):
        # os.system('mode con: cols=80 lines=15')
        self.console.clear()
        pretty.install()

    def show_home_page(self):
        options = """[green]
        [R]un the bot
        [C]hange config
        [Q]uit the program
        """
        self.console.clear()
        self.console.rule()
        self.console.print(self.title_art)
        self.console.rule()
        self.console.print(options)
        choice = Prompt.ask("[green]What would you like to do?", choices=["r", "c", "q"], default="r")
        choices = {
            "r": print("ok"),
            "c": self.show_config_page(),
            "q": self.quit()
        }
        return choices[choice]

    def show_config_page(self):
        options = """
        1. Time limit per move: {}
        2. Draw ponder arrows : {}
        3. Auto restart: {}
        """.format(1, True, False)
        self.console.clear()
        self.console.rule()
        self.console.print(self.title_art)
        self.console.rule("[green] Options")
        self.console.print(options)
        choice = Prompt.ask("[green]Which option do you wish to change", choices=["1", "2", "3", "q"], default="q")

    def quit(self):
        self.console.clear()
        sys.exit(0)


def main():
    cli = CLI()
    cli.setup()
    cli.show_home_page()


if __name__ == '__main__':
    main()
