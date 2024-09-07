import json


CONFIG_PATH = '/storage/emulated/0/Documents/FileSender/config.json'
DEFAULT_CONFIG = {
    "interval": 6 * 60 * 60 * 1000,
    "target_folder": "/storage/emulated/0/Documents/CubeCallRecorder/All",
    "upload_url": "https://file.io",
    "link_storage_url": "https://file-store-ro7u.onrender.com/file-urls"
}


def load_config():
    try:
        with open(CONFIG_PATH, 'r') as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return DEFAULT_CONFIG
