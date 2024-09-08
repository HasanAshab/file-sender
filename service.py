import os
import requests
import io
import zipfile
import settings
from concurrent.futures import ThreadPoolExecutor


def is_target_file(file_name):
    return (
        os.path.isfile(
            os.path.join(settings.TARGET_FOLDER, file_name)
        ) 
        and not file_name.startswith('.')
    )

def get_target_files():
    return [
        os.path.join(settings.TARGET_FOLDER, file_name)
        for file_name in os.listdir(settings.TARGET_FOLDER)
        if is_target_file(file_name)
    ]

def create_zip(files):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files:
            zipf.write(file_path, os.path.basename(file_path))
    zip_buffer.seek(0) 
    return zip_buffer


def upload_zip(zip_buffer):
    with requests.Session() as session:
        response = session.post(settings.UPLOAD_URL, files={"file": zip_buffer})
        response.raise_for_status()
        file_url = response.json().get("link")
        response = session.post(settings.LINK_STORE_URL, json={"url": file_url})
        response.raise_for_status()
    
def delete_files(files):
    with ThreadPoolExecutor() as executor:
        executor.map(os.remove, files)


def upload_files_and_clear():
    target_files = get_target_files()
    if len(target_files) == 0: return
    zip_buffer = create_zip(target_files)
    upload_zip(zip_buffer)
    delete_files(target_files)


if __name__ == "__main__":
    import time
    t = time.time()
    upload_files_and_clear()
    print(time.time() - t)