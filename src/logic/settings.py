import yaml
from dataclasses import dataclass, field

@dataclass
class Settings:
    """Settings for the app."""
    save_path: str
    database_name: str
    database_path: str
    default_apps:bool = True
    custom_applications: list[dict] = field(default_factory=list)
    def save_settings(self):
        """Save the settings to the config file."""
        with open("config.yaml", "w") as f:
            yaml.dump(self.__dict__, f)
    
#open the config file and load the settings
with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

