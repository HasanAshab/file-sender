import os
import requests
import zipfile
import tempfile
from utils import load_config

def create_zip_from_files(target_folder):
    """Creates a ZIP file containing all the files in the target folder."""
    temp_dir = tempfile.gettempdir()
    zip_path = os.path.join(temp_dir, f"file-sender-{}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_name in os.listdir(target_folder):
            file_path = os.path.join(target_folder, file_name)
            if os.path.isfile(file_path) and not file_name.startswith("."):
                zipf.write(file_path, os.path.basename(file_path))
    return zip_path

def upload_zip(zip_path, config):
    """Uploads the ZIP file to the specified API and deletes it after upload."""
    with open(zip_path, "rb") as f:
        response = requests.post(config["upload_url"], files={"file": f})
        response.raise_for_status()

    file_url = response.json().get("link")
    response = requests.post(config["link_storage_url"], data={"url": file_url})
    response.raise_for_status()


def delete_files_in_folder(target_folder):
    """Deletes all files in the target folder."""
    for file_name in os.listdir(target_folder):
        file_path = os.path.join(target_folder, file_name)
        if os.path.isfile(file_path) and not file_name.startswith("."):
            os.remove(file_path)

def upload_files_and_clear():
    config = load_config()
    target_folder = config["target_folder"]

    zip_path = create_zip_from_files(target_folder)
    if zip_path:
        upload_zip(zip_path, config)
        
        os.remove(zip_path)

        delete_files_in_folder(target_folder)


if __name__ == "__main__":
    import time
    t = time.time()
    upload_files_and_clear()
    print(time.time() - t)