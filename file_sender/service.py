import os
import time
import requests
import zipfile
import tempfile
from utils import load_config


def create_zip(files):
    temp_dir = tempfile.gettempdir()
    zip_path = os.path.join(temp_dir, f"file-sender-{time.time()}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files:
            zipf.write(file_path, os.path.basename(file_path))
    return zip_path


def upload_zip(zip_path, upload_url, link_storage_url):
    with open(zip_path, "rb") as f:
        response = requests.post(upload_url, files={"file": f})
        response.raise_for_status()

    file_url = response.json().get("link")
    response = requests.post(link_storage_url, data={"url": file_url})
    response.raise_for_status()


def delete_files(files):
    for file_path in files:
        os.remove(file_path)


def upload_files_and_clear():
    config = load_config()
    target_folder = config["target_folder"]
    target_files = [ 
        os.path.join(target_folder, file_name)
        for file_name in os.listdir(target_folder)
        if not file_name.startswith('.')
    ]

    zip_path = create_zip(target_files)
    if zip_path:
        upload_zip(
            zip_path,
            config["upload_url"],
            config["link_storage_url"]
        )
        os.remove(zip_path)
        delete_files(target_files)


if __name__ == "__main__":
    t = time.time()
    upload_files_and_clear()
    print(time.time() - t)