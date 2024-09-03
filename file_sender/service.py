import os
import requests
from utils import load_config


def upload_files_and_clear():
    config = load_config()
    target_folder = config["target_folder"]
    
    try:
        for file_name in os.listdir(target_folder):
            file_path = os.path.join(target_folder, file_name)

            if os.path.isfile(file_path) and not file_name.startswith("."):
                with open(file_path, "rb") as f:
                    response = requests.post(config["upload_url"], files={"file": f})
                    response.raise_for_status()

                file_url = response.json().get("link")
                response = requests.post(config["link_storage_url"], data={"url":file_url})
                response.raise_for_status()
                
                os.remove(file_path)

    except Exception as e:
        pass

if __name__ == "__main__":
    upload_files_and_clear()
