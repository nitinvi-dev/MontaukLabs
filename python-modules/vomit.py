import os
import requests
import re
from dotenv import load_dotenv

load_dotenv("../.env")


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    file_path = os.path.join(dest_folder, url.split('/')[-1].replace(" ", "_"))

    r = requests.get(url, stream=True)
    if r.ok:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


def vomit_data_files():
    # url for getting download urls : calling by page
    url = 'https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/'

    # preparing data in list of dictionary to getting actual download link
    response = requests.get(url)
    response_data = response.json()
    blobs_data = response_data['blobs']

    # defining a list of urls for download
    download_list = []

    # preparing download list of urls for download files ending with index.json
    i = 0
    for data in blobs_data:
        for key, value in data.items():
            if key == 'downloadUrl' and re.search('index.json$', value):
                download_list.append(value)
                if i == 20: break;
                i += 1

    # downloading latest files into a given folder
    for i in download_list[:-11:-1]:
        download(i, "data")


if __name__ == '__main__':
    vomit_data_files()