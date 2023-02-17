import os.path
import json


class ConfigHandler:
    def __init__(self, file_name: str):
        self.time_limit: float = 1.0
        self.draw_ponder_arrows: bool = False
        self.auto_restart: bool = False
        self.file_name = file_name

    def load(self) -> dict:
        if not os.path.exists(self.file_name):
            self.save()
            return self.get()

        with open("config.json", "r") as f:
            config = json.load(f)

        self.time_limit = config.get("time_limit", self.time_limit)
        self.draw_ponder_arrows = config.get("draw_ponder_arrows", self.draw_ponder_arrows)
        self.auto_restart = config.get("auto_restart", self.auto_restart)
        return self.get()

    def save(self) -> bool:
        with open(self.file_name, "w") as f:
            f.write(json.dumps(self.get(), indent=4))
        return True

    def get(self) -> dict:
        return {
            "time_limit": self.time_limit,
            "draw_ponder_arrows": self.draw_ponder_arrows,
            "auto_restart": self.auto_restart
        }


def main():
    config = ConfigHandler("config.json")
    print(config.load())
    config.auto_restart = False
    config.save()


if __name__ == '__main__':
    main()
