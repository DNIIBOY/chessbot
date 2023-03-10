import os.path
import json


class ConfigHandler:
    def __init__(self, file_name: str):
        self.time_limit: float = 1.0
        self.depth_limit: int = 5
        self.use_depth_limit: bool = False
        self.draw_ponder_arrows: bool = False
        self.calculate_score: bool = False
        self.file_name = file_name
        self.config_names = ("time_limit", "depth_limit", "use_depth_limit", "draw_ponder_arrows", "calculate_score")
        self.config_types = (float, int, bool, bool, bool)

    def __repr__(self):
        return f"ConfigHandler({self.get()})"

    def load(self) -> dict:
        if not os.path.exists(self.file_name):
            self.save()
            return self.get()

        with open("config.json", "r") as f:
            config = json.load(f)

        self.time_limit = config.get("time_limit", self.time_limit)
        self.depth_limit = config.get("depth_limit", self.depth_limit)
        self.use_depth_limit = config.get("use_depth_limit", self.use_depth_limit)
        self.draw_ponder_arrows = config.get("draw_ponder_arrows", self.draw_ponder_arrows)
        self.calculate_score = config.get("calculate_score", self.calculate_score)
        return self.get()

    def save(self) -> bool:
        with open(self.file_name, "w") as f:
            f.write(json.dumps(self.get(), indent=4))
        return True

    def get(self) -> dict:
        return {
            "time_limit": self.time_limit,
            "depth_limit": self.depth_limit,
            "use_depth_limit": self.use_depth_limit,
            "draw_ponder_arrows": self.draw_ponder_arrows,
            "calculate_score": self.calculate_score
        }

    def change_config(self, config_name: str, value: float | bool):
        match config_name:
            case "time_limit":
                self.time_limit = float(value)
            case "depth_limit":
                self.depth_limit = int(value)
            case "use_depth_limit":
                self.use_depth_limit = bool(value)
            case "draw_ponder_arrows":
                self.draw_ponder_arrows = bool(value)
            case "calculate_score":
                self.calculate_score = bool(value)
            case _:
                raise ValueError(f"Config named {config_name} does not exist")


def main():
    config = ConfigHandler("config.json")
    config.load()
    print(config)


if __name__ == '__main__':
    main()
