#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一数据获取入口
根据数据源参数调用不同的抓取脚本

用法：
    python fetch-match-data.py --source sofascore --home "Spain" --away "Saudi Arabia"
    python fetch-match-data.py --source fbref --date 2026-06-15
    python fetch-match-data.py --source oddsportal --home "Turkey" --away "Paraguay"

注意：
- 这些脚本依赖 requests 和 beautifulsoup4
- 安装：pip install requests beautifulsoup4 lxml
- 部分网站有反爬机制，可能需要设置 User-Agent 或使用代理
- 如果抓取失败，会回退到提示用户使用 web_search/web_extract
"""

import argparse
import json
import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser(description='足球比赛数据统一获取工具')
    parser.add_argument('--source', required=True,
                        choices=['sofascore', 'fbref', 'oddsportal', '500'],
                        help='数据源')
    parser.add_argument('--home', help='主队名称')
    parser.add_argument('--away', help='客队名称')
    parser.add_argument('--date', help='日期，格式 YYYY-MM-DD')
    parser.add_argument('--output', '-o', default='-',
                        help='输出文件，默认输出到 stdout')

    args = parser.parse_args()

    source_map = {
        'sofascore': 'fetch-sofascore.py',
        'fbref': 'fetch-fbref.py',
        'oddsportal': 'fetch-oddsportal.py',
        '500': 'fetch-500.py',
    }

    script_path = SCRIPT_DIR / source_map[args.source]

    if not script_path.exists():
        print(f"错误：脚本不存在 {script_path}", file=sys.stderr)
        sys.exit(1)

    cmd = ['python3', str(script_path)]
    if args.home:
        cmd.extend(['--home', args.home])
    if args.away:
        cmd.extend(['--away', args.away])
    if args.date:
        cmd.extend(['--date', args.date])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"抓取失败：{e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("返回数据不是有效 JSON", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        sys.exit(1)

    output_json = json.dumps(data, ensure_ascii=False, indent=2)

    if args.output == '-':
        print(output_json)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"数据已保存到 {args.output}")


if __name__ == '__main__':
    main()
