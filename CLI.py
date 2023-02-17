from rich import pretty
from rich.console import Console
from rich.prompt import Prompt
import os


class CLI:
    def __init__(self):
        self.console = Console()

    def setup(self):
        os.system('mode con: cols=80 lines=15')
        self.console.clear()
        pretty.install()

    def show_home_page(self):
        self.console.clear()
        title = "[blue bold]Chess Bot"
        self.console.print(title)


def main():
    cli = CLI()
    cli.setup()
    cli.show_home_page()
    input()


if __name__ == '__main__':
    main()
