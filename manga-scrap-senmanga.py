import urllib.request
from bs4 import BeautifulSoup
import requests
import os
import errno
import re


def get_pages(str1):
    nums_str = re.findall("\d+", str1)
    nums = [int(x) for x in nums_str]
    return sorted(set(nums))


# ==============================
url_name = 'Detective_Conan'
manganame_en = 'detective-conan'
chapter_start = 1054
chapter_end = 1072
# ==============================

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'referer': 'https://raw.senmanga.com/'
}

for chapter in range(chapter_start, chapter_end + 1):
    pages = []
    url = f"https://raw.senmanga.com/{url_name}/{chapter}"
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        page_content = BeautifulSoup(req.content, 'html.parser')
        pages = get_pages(
            str(page_content.select('select[name=page] > option')))

    for page in pages:
        img_url = f"https://raw.senmanga.com/viewer/{url_name}/{chapter}/{page}"
        resp = requests.get(img_url, headers=headers)
        if resp.status_code == 200:
            filename = f"./{manganame_en}-raw/{manganame_en}-{chapter}/{manganame_en}-{chapter}-raw-{page}.jpg"
            print(filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                f.write(resp.content)
            del resp
        else:
            print(f' status {resp.status_code}: {page} -> {img_url}')
