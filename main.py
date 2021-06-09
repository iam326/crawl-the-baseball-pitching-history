import json
import re
from time import sleep

import requests
from bs4 import BeautifulSoup

WAIT = 5
# 2021/03/26
START = 95
# 2021/06/09
END = 472

teams_data = {
  '巨人': {},
  'ヤクルト': {},
  'DeNA': {},
  '中日': {},
  '阪神': {},
  '広島': {},
  '西武': {},
  '日本ハム': {},
  'ロッテ': {},
  'オリックス': {},
  'ソフトバンク': {},
  '楽天': {},
}

for i in range(START, END - 1):
    sleep(WAIT)

    response = requests.get('https://baseball.yahoo.co.jp/npb/game/2021000{}/top'.format(str(i).zfill(3)))
    soup = BeautifulSoup(response.text, 'html.parser')

    # 日付を取得する
    title = soup.find('title').get_text()
    if title.startswith('エラーページ'):
        continue
    date = re.findall(r'\d+', title.split()[0])
    game_date = '{}{}{}'.format(date[0], date[1].zfill(2), date[2].zfill(2))

    # チーム名を取得する
    vs = soup.select_one('.bb-head01__title').get_text()
    teams = vs.split('vs.')
    home_team = teams[0].strip()
    visitor_team = teams[1].strip()

    # 両チームのバッテリーを取得する
    batteries = soup.select('#battery > table > tbody > tr > td')
    if len(batteries) == 0:
        continue

    # ビジターチームの登板投手名を取得する
    visitor_pitchers = [p.strip() for p in batteries[0].get_text().split('-')[0].split('、')]
    teams_data[visitor_team][game_date] = visitor_pitchers

    # ホームチームの登板投手名を取得する
    home_pitchers = [p.strip() for p in batteries[1].get_text().split('-')[0].split('、')]
    teams_data[home_team][game_date] = home_pitchers

    print('{} : {} : {} : {}'.format(
        game_date, home_team, len(home_pitchers), home_pitchers))
    print('{} : {} : {} : {}'.format(
        game_date, visitor_team, len(visitor_pitchers), visitor_pitchers))

# JSON ファイルとして出力する
with open('teams-data.json', 'w') as f:
    json.dump(teams_data, f, indent=4, ensure_ascii=False)
