#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SofaScore 数据抓取脚本

用法：
    python fetch-sofascore.py --home "Spain" --away "Saudi Arabia" --date 2026-06-21

注意：
- SofaScore 页面结构可能变化，需要根据实际情况调整解析逻辑
- 建议使用 web_search 先找到具体比赛 URL，再用 web_extract 提取
- 本脚本提供命令行封装和示例解析逻辑
"""

import argparse
import json
import re
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
    'Accept-Language': 'en-US,en;q=0.9',
}


def search_match(home, away, date=None):
    """通过 SofaScore 搜索比赛"""
    query = f"{home} {away} sofascore"
    if date:
        query += f" {date}"

    url = f"https://www.google.com/search?q={quote_plus(query)}"
    # 实际使用时建议用 web_search 工具定位 URL
    return None


def parse_match_page(url):
    """解析 SofaScore 比赛页面"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        return {'error': f'请求失败: {e}'}

    soup = BeautifulSoup(resp.text, 'lxml')

    result = {
        'source': 'sofascore',
        'url': url,
        'home_team': None,
        'away_team': None,
        'home_score': None,
        'away_score': None,
        'possession': {'home': None, 'away': None},
        'shots': {'home': None, 'away': None},
        'shots_on_target': {'home': None, 'away': None},
        'xg': {'home': None, 'away': None},
        'lineups': {'home': [], 'away': []},
    }

    # 这些选择器基于 SofaScore 常见结构，可能需要更新
    title = soup.find('title')
    if title:
        result['page_title'] = title.get_text(strip=True)

    # 尝试从 script 标签中提取 JSON 数据
    scripts = soup.find_all('script')
    for script in scripts:
        text = script.string or ''
        if 'initialState' in text or 'window.__INITIAL_STATE__' in text:
            # 提取逻辑需要根据实际情况编写
            pass

    return result


def main():
    parser = argparse.ArgumentParser(description='抓取 SofaScore 比赛数据')
    parser.add_argument('--home', required=True, help='主队名称')
    parser.add_argument('--away', required=True, help='客队名称')
    parser.add_argument('--date', help='比赛日期 YYYY-MM-DD')
    parser.add_argument('--url', help='直接提供比赛 URL')

    args = parser.parse_args()

    if args.url:
        data = parse_match_page(args.url)
    else:
        url = search_match(args.home, args.away, args.date)
        if url:
            data = parse_match_page(url)
        else:
            data = {
                'source': 'sofascore',
                'home': args.home,
                'away': args.away,
                'date': args.date,
                'error': '未找到比赛 URL。建议先用 web_search 搜索 "SofaScore home away date" 找到具体 URL，再用 --url 参数传入。',
            }

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
