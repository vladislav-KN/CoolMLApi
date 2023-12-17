import json
import os

from app.base_classes.base_predict_models import Config


class ConfigFileLoader(Config):
    @classmethod
    def load_from_file(cls, file_name: str = "appconfig.json") -> 'Config':
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                config_data = json.load(file)
                return cls(**config_data)
        else:
            best = {'criterion': 'friedman_mse', 'learning_rate': 0.01, 'max_depth': 10, 'min_samples_leaf': 1, 'min_samples_split': 10, 'n_estimators': 90, 'subsample': 0.01}
            # Создание файла с стандартными значениями, если файла нет
            default_config = cls(api_url="http://localhost:38080/api/trainings", file_path="app\\model_files\\base.pkl",best_setup = best)
            default_config.save_to_file(file_name)
            return default_config

    def save_to_file(self, file_name: str = "appconfig.json") -> None:
        with open(file_name, "w") as file:
            json.dump(self.model_dump(), file, indent=2)

