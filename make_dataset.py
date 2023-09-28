import urllib.request
import json
import urllib.parse
from urllib.parse import urlsplit, quote
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

# url = 'https://pokemon.fandom.com/ko/wiki/흥나숭_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/나몰빼미_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/도치마론_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/비크티니_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/모부기_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/나무지기_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/치코리타_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/토게틱_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/포푸니_(포켓몬)'
url = 'https://pokemon.fandom.com/ko/wiki/이상해씨_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/레트라_(포켓몬)'
# url = 'https://pokemon.fandom.com/ko/wiki/신비록_(포켓몬)'

url_info = urlsplit(url)
encoded_url = f'{url_info.scheme}://{url_info.netloc}{quote(url_info.path)}'

info = []
erros = []
target_number = 1017
cnt = 0
for _ in tqdm(range(target_number+2)):
    cnt += 1
    req = Request(encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req)
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find("div", {"class": "name-ko"}).text.strip()
    number = soup.find("div", {"class": "index"}).text.strip()
    try:
        img_url = soup.find("div", {"class":"image rounded"}).find("img")['data-src']
        filepath = f"images/{number.replace('.', '_')}_{name}.png"
        urllib.request.urlretrieve(img_url, filepath)
    except:
        filepath = None
    doc_text = '\n'.join([p.text.replace('\n', '').strip() for p in soup.find_all("p")])
    types = [poke_type['title'].split(' ')[0].strip() for poke_type in soup.select('tbody > tr > td > div')[0].select('span > a')]

    info.append(dict(
        name=name,
        number=number,
        types=types,
        doc_text=doc_text,
        image_path=filepath,
        url=encoded_url
    ))
    next_monster = soup.find("table").findAll("a")[-1]['href']
    encoded_url = "https://pokemon.fandom.com" + next_monster
    if number == f"No.{target_number:04d}":
        break

    if cnt >= target_number:
        break

pd.DataFrame(info).to_csv('pokemon.csv', index=False)
with open('pokemon.json', 'w') as f:
    json.dump(info, f, ensure_ascii=False, indent=4)