import os
import requests
import io
import zipfile
from concurrent.futures import ThreadPoolExecutor
from utils import load_config


def is_target_file(target_folder, file_name):
    return (
        os.path.isfile(os.path.join(target_folder, file_name)) 
        and not file_name.startswith('.')
    )

def get_target_files(folder):
    return [
        os.path.join(folder, file_name)
        for file_name in os.listdir(folder)
        if is_target_file(folder, file_name)
    ]

def create_zip(files):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files:
            zipf.write(file_path, os.path.basename(file_path))
    zip_buffer.seek(0) 
    return zip_buffer


def upload_zip(zip_buffer, upload_url, link_storage_url):
    with requests.Session() as session:
        response = session.post(upload_url, files={"file": zip_buffer})
        response.raise_for_status()
        
        file_url = response.json().get("link")
        response = session.post(link_storage_url, json={"url": file_url})
        response.raise_for_status()
    
def delete_files(files):
    with ThreadPoolExecutor() as executor:
        executor.map(os.remove, files)


def upload_files_and_clear():
    config = load_config()
    target_files = get_target_files(config["target_folder"])
    if len(target_files) == 0: return
    zip_buffer = create_zip(target_files)
    upload_zip(
        zip_buffer,
        config["upload_url"],
        config["link_storage_url"]
    )
    delete_files(target_files)


if __name__ == "__main__":
    import time
    t = time.time()
    upload_files_and_clear()
    print(time.time() - t)