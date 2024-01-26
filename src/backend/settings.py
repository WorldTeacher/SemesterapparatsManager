from dataclasses import dataclass, field

import yaml


@dataclass
class Settings:
    """Settings for the app."""

    save_path: str
    database_name: str
    database_path: str
    bib_id: str
    default_apps: bool = True
    custom_applications: list[dict] = field(default_factory=list)

    def save_settings(self):
        """Save the settings to the config file."""
        with open("config.yaml", "w") as f:
            yaml.dump(self.__dict__, f)

    def load_settings(self):
        """Load the settings from the config file."""
        with open("config.yaml", "r") as f:
            data = yaml.safe_load(f)
            return data
