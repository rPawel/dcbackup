import yaml
import glob


def load(app_composer_path):
    stream = open(app_composer_path, "r")
    return yaml.load_all(stream)


def find_configs(input_dir):
    return glob.glob(input_dir + "/*/docker-compose.yml")
