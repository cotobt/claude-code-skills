#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FBref 数据抓取脚本

用法：
    python fetch-fbref.py --home "Spain" --away "Saudi Arabia" --date 2026-06-21

注意：
- FBref 页面数据丰富但结构复杂
- 建议使用球队/比赛的 FBref URL 直接提取
- 世界杯比赛 URL 格式通常为：https://fbref.com/en/matches/YYYYMMDD/HomeTeam-AwayTeam
"""

import argparse
import json
import sys
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("请先安装依赖：pip install requests beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)


HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    ),
}


def parse_match_page(url):
    """解析 FBref 比赛页面"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        return {'error': f'请求失败: {e}'}

    soup = BeautifulSoup(resp.text, 'lxml')

    result = {
        'source': 'fbref',
        'url': url,
        'home_team': None,
        'away_team': None,
        'home_score': None,
        'away_score': None,
        'possession': {'home': None, 'away': None},
        'shots': {'home': None, 'away': None},
        'shots_on_target': {'home': None, 'away': None},
        'xg': {'home': None, 'away': None},
    }

    # 尝试从比分表格提取
    scorebox = soup.find('div', class_='scorebox')
    if scorebox:
        teams = scorebox.find_all('div', class_='scorebox_bold')
        if len(teams) >= 2:
            result['home_team'] = teams[0].get_text(strip=True)
            result['away_team'] = teams[1].get_text(strip=True)

    # 提取比赛统计表格
    stats_table = soup.find('table', {'id': 'stats'})
    if stats_table:
        rows = stats_table.find_all('tr')
        for row in rows:
            th = row.find('th')
            tds = row.find_all('td')
            if th and len(tds) >= 2:
                stat_name = th.get_text(strip=True)
                if 'Possession' in stat_name:
                    result['possession'] = {'home': tds[0].get_text(strip=True),
                                            'away': tds[1].get_text(strip=True)}
                elif 'Shots' in stat_name and 'Shot on Target' not in stat_name:
                    result['shots'] = {'home': tds[0].get_text(strip=True),
                                       'away': tds[1].get_text(strip=True)}
                elif 'Shot on Target' in stat_name:
                    result['shots_on_target'] = {'home': tds[0].get_text(strip=True),
                                                 'away': tds[1].get_text(strip=True)}
                elif 'xG' in stat_name:
                    result['xg'] = {'home': tds[0].get_text(strip=True),
                                    'away': tds[1].get_text(strip=True)}

    return result


def main():
    parser = argparse.ArgumentParser(description='抓取 FBref 比赛数据')
    parser.add_argument('--home', required=True, help='主队名称')
    parser.add_argument('--away', required=True, help='客队名称')
    parser.add_argument('--date', help='比赛日期 YYYY-MM-DD')
    parser.add_argument('--url', help='直接提供比赛 URL')

    args = parser.parse_args()

    if args.url:
        data = parse_match_page(args.url)
    else:
        data = {
            'source': 'fbref',
            'home': args.home,
            'away': args.away,
            'date': args.date,
            'error': 'FBref 需要具体比赛 URL。建议先用 web_search 搜索 "FBref home away date" 找到 URL，再用 --url 参数传入。',
        }

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
