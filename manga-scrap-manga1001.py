import urllib.request
from bs4 import BeautifulSoup
import requests
import os
import errno
import re

# ==============================
manganame_jp = 'アオアシ'
manganame_en = 'ao-ashi'
chapter_start = 225
chapter_end = 230
# ==============================

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
           'referer': 'https://manga1001.com/%E3%80%90%E7%AC%AC1%E8%A9%B1%E3%80%91%E3%82%A2%E3%82%AA%E3%82%A2%E3%82%B7-raw/'}

for i in range(chapter_start, chapter_end + 1):
    img_url_data = []
    url = f"https://manga1001.com/【第{i}話】{manganame_jp}-raw"
    req = requests.get(url)
    if req.status_code == 200:
        page_content = BeautifulSoup(req.content, 'html.parser')
        for img_url in page_content.select('figure.wp-block-image > img'):
            img_url_data.append(re.search('https://.*-\.jpg', str(img_url)).group())

    for idx, img_url in enumerate(img_url_data):
        resp = requests.get(img_url, headers=headers)
        if resp.status_code == 200:
            filename = f"./{manganame_en}-raw/{manganame_en}-{i}/{manganame_en}-{i}-raw-{idx+1}.jpg"
            print(filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                f.write(resp.content)
            del resp
        else:
            print(f' status {resp.status_code}: {idx} -> {img_url}')

