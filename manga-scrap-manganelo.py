from bs4 import BeautifulSoup
import requests
import os
import re

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'referer': 'https://manganelo.com/'
}
manga_title = 'AoT'
pattern = re.compile(r'https:.*jpg')
for i in range(136, 137):
    img_url_data = []
    url = f"https://manganelo.com/chapter/kxqh9261558062112/chapter_{i}"
    req = requests.get(url)
    if req.status_code == 200:
        page_content = BeautifulSoup(req.content, 'html.parser')
        for img_url in page_content.select('.container-chapter-reader > img'):
            dummy_txt = str(img_url).split('>')
            for txt in dummy_txt:
                matches = pattern.search(txt)
                if matches:
                    img_url_data.append(matches.group(0))

    for idx, img_url in enumerate(img_url_data):
        resp = requests.get(img_url, headers=headers)
        if resp.status_code == 200:
            filename = f"./{manga_title}/{manga_title}{i}/{manga_title}-{i}-{idx+1}.jpg"
            print(filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                f.write(resp.content)
            del resp
        else:
            print(f' status {resp.status_code}: {idx} -> {img_url}')
