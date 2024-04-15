from sys import stdout

import requests


def print_inline(string):
    print(string, end="")
    stdout.flush()


def download_file(url, file_path):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to download file. Response status code: {response.status_code}")
        return False
    
    with open(file_path, "wb") as f:
        f.write(response.content)
    
    return True
