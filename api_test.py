import requests
import json
import os
import pandas as pd
from urllib.parse import urlparse
from urllib.parse import urljoin


request_url =  "https://web.archive.org/cdx/search/xd"

base_url = "https://mainichi.jp/english"
ts_from = 20140101
ts_to = 20150101
filter_mime_type = 'mimetype:text/html'

if not base_url.endswith('/'):
    base_url += '/'

base_url_parsed = urlparse(base_url)


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

print(r.status_code)

json_response = json.loads(r.content)
df = pd.DataFrame(columns=json_response[0],data=json_response[1:])

# with open('dump.json', 'w') as f:
#     f.write(json.dumps(json_response))

for index, row in df.iterrows():
    print(f'Index : {index}')
    file_timestamp = row['timestamp']
    file_url = row['original']
    print(file_timestamp, file_url, row['length'])
    
    # check if already downloaded

    file_url_parsed = urlparse(file_url)

    file_path, file_name = os.path.split(file_url_parsed.path)
    file_path = os.path.join(base_url_parsed.netloc, file_timestamp, *file_path.split('/'))

    if file_name == '':
        file_name = 'index.html'

    if os.path.exists(os.path.join(file_path, file_name)):
        print('File already exists! Skipping...')
        continue

    download_url = f'https://web.archive.org/web/{file_timestamp}/{file_url}'

    r = requests.get(download_url)

    print('Status code: ')
    print(r.status_code)

    if r.status_code != 200:
        print('No response! Skipping...')
        continue

    os.makedirs(file_path, exist_ok=True)

    with open(os.path.join(file_path, file_name), 'wb') as f:
        f.write(r.content)
