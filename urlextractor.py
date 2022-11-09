from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import re
import json
from tqdm import tqdm
import argparse
from urllib.parse import urlparse

wbmpattern1 = re.compile(r"https?:\/\/web\.archive\.org/web/\d{8,}\/")
wbmpattern2 = re.compile(r"^\/web\/\d{8,}.*?\/")

# pattern for ORF stories
# r'https?:\/\/\w*\.orf.at/.*/\d{3,}'

def extract_urls(html_path, pattern):
    with open(html_path, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')
    anchors = soup.find_all(href=pattern)
    links = [a['href'] for a in anchors]
    links = [re.sub(wbmpattern1, "", l) for l in links]
    links = [re.sub(wbmpattern2, "", l) for l in links]
    return list(set(links))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script to extract all URLs according to a regex pattern. \
                                                    Usage: "python urlextractor.py http://example.com" ')

    parser.add_argument('url', type=str, help='The website to parse. e.g. "http://example.com."')
    parser.add_argument('--regex', dest='regex', type=str, help="A custom regular expression. Enclose regex in double quotation marks")
    parser.add_argument('--debug', dest='debug', default=False, action="store_true", help="Debug flag. Only parse first 10 files")

    args = parser.parse_args()
    assert args.url, 'Please specify a URL'
    base_url = args.url

    if base_url.startswith('http'):
            base_domain = urlparse(base_url).netloc
    else: 
        base_domain = urlparse(base_url).path

    p = Path.cwd() / 'output' / base_domain

    assert p.exists(), f'Nothing downloaded for {base_domain}! Aborting'

    if args.regex:
        url_pattern = re.compile(args.regex)
    else:
        url_pattern = r'https?:\/\/' + base_domain.replace('.', '\.')
        url_pattern = re.compile(url_pattern)


    html_files = list(p.rglob('*.htm*'))

    # debugging: limit to only 10 files
    if args.debug:
        html_files = html_files[:10]

    urls = []
    errors = []

    with tqdm(total=len(html_files), unit='files') as pbar:
        for html in html_files:
            try:
                urls += extract_urls(html, url_pattern)
                urls = list(set(urls))
            except Exception as e:
                errors.append({f'{html}': f'{e}'})
            finally:
                pbar.update(1)

    print(f'Extracted {len(urls)} URLs!')
    print(f'Got {len(errors)} errors')

    timestamp = datetime.now().strftime('%Y_%m_%d_%H%m%s')

    output_file = base_domain + '_urls_' + timestamp + '.json'
    output_file = Path.cwd() / output_file

    with open(output_file, 'w') as f:
        json.dump(urls, f)

    print(f'saved to {output_file}')

    if len(errors) > 0:
        error_file = base_domain + '_urls_' + timestamp + '_errors.json'
        error_file = Path.cwd() / error_file
        with open(error_file, 'w') as f:
            json.dump(errors, f)

    print('Done!')
