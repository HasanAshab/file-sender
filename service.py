import os
import requests

def upload_files_and_clear():
    target_dir = '/storage/emulated/0/Documents/CubeCallRecorder/All'
    try:
        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    response = requests.post('https://example.com/upload', files={'file': f})
                    response.raise_for_status()  # Check for errors in the response

                os.remove(file_path)

    except Exception as e:
        pass

if __name__ == "__main__":
    upload_files_and_clear()
