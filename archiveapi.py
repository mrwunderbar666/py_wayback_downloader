import requests
import json
import os
import pandas as pd
from urllib.parse import urlparse
import concurrent.futures

import argparse


def download_archive(input_list):
    _, file_timestamp, file_url, file_type, _, _, file_length = input_list
    print(file_timestamp, file_url, file_length)
    
    # check if already downloaded

    file_url_parsed = urlparse(file_url)

    file_path, file_name = os.path.split(file_url_parsed.path)
    file_path = os.path.join("output", base_url_parsed.netloc, file_timestamp, *file_path.split('/'))

    if file_name == '':
        file_name = 'index.html'

    if os.path.exists(os.path.join(file_path, file_name)):
        print('File already exists! Skipping...')
        return None

    # construct download url
    download_url = f'https://web.archive.org/web/{file_timestamp}/{file_url}'

    # download file
    r = requests.get(download_url)

    print('Status code: ')
    print(r.status_code)

    if r.status_code != 200:
        print('No response! Skipping...')
        return None

    # create directory structure

    os.makedirs(file_path, exist_ok=True)

    # save file
    with open(os.path.join(file_path, file_name), 'wb') as f:
        f.write(r.content)
    return True

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Usage: archiveapi http://example.com \nDownload an entire website from the Wayback Machine.')

    parser.add_argument('base_url', type=str, nargs=1, help='The website or path to download. e.g. "http://example.com"')
    parser.add_argument('--from', type=int, nargs=1, help="Starting date to download. Timestamp in format YYYYMMDD, e.g. 20120808")
    parser.add_argument('--to', type=int, nargs=1, help="End date to download. Timestamp in format YYYYMMDD, e.g. 20120808")
    parser.add_argument('--threads', type=int, nargs=1, help="Number of concurrent downloads. Recommended 4 - 16")
    
    args = parser.parse_args()
    print(args)

    request_url =  "https://web.archive.org/cdx/search/xd"
    n_threads = 16

    base_url = "https://mainichi.jp/english"
    ts_from = 20140101
    ts_to = 20150101
    filter_mime_type = 'mimetype:text/html'

    if not base_url.endswith('/'):
        base_url += '/'

    base_url_parsed = urlparse(base_url)

    # add maximum possible daterange as default

    payload = {'url': f'{base_url}*',
                # 'fl': 'timestamp,original',
                'collapse': 'digest',
                'gzip': "false",
                'output': 'json',
                'filter': ['statuscode:200', filter_mime_type],
                'from': ts_from,
                'to': ts_to,
                }

    print('Requesting Index...')

    r = requests.get(request_url, params=payload)

    if r.status_code != 200:
        print('Bad response!')
        print('Status code:')
        print(r.status_code)
        print('Headers')
        print(r.headers)
        pass

    print('Good Response')
    print(r.status_code)

    json_response = json.loads(r.content)

    download_list = json_response[1:]
    print(f'Got {len(download_list)} to download...')

    # with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
    #     executor.map(download_archive, download_list)
