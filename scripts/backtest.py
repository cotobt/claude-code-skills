#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动回测脚本

用法：
    python backtest.py --results results.json --output backtest-report.md

results.json 格式：
{
  "matches": [
    {
      "date": "2026-06-12",
      "home": "墨西哥",
      "away": "南非",
      "score": "2-0",
      "home_odds": 1.3,
      "draw_odds": 4.5,
      "away_odds": 9.0,
      "notes": "东道主"
    }
  ]
}

如果没有赔率数据，可以省略 odds 字段，脚本会做定性回测。

输出：标准化的 markdown 回测报告
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def parse_score(score):
    """解析比分，返回 (home_goals, away_goals)"""
    try:
        home, away = score.split('-')
        return int(home.strip()), int(away.strip())
    except Exception:
        return None, None


def get_implied_favorite(home_odds, draw_odds, away_odds):
    """根据赔率判断热门方"""
    if not all([home_odds, draw_odds, away_odds]):
        return None

    odds = {'home': home_odds, 'draw': draw_odds, 'away': away_odds}
    favorite = min(odds, key=odds.get)
    return favorite


def get_actual_result(home_goals, away_goals):
    """根据比分判断实际结果"""
    if home_goals is None or away_goals is None:
        return None
    if home_goals > away_goals:
        return 'home'
    elif home_goals < away_goals:
        return 'away'
    else:
        return 'draw'


def is_favorite_correct(favorite, actual):
    """判断热门方是否打出"""
    if favorite is None or actual is None:
        return None
    return favorite == actual


def generate_report(matches):
    """生成回测报告"""
    total = len(matches)
    with_odds = sum(1 for m in matches if m.get('home_odds'))
    without_odds = total - with_odds

    correct_count = 0
    upset_count = 0
    unknown_count = 0

    lines = []
    lines.append('# 回测报告')
    lines.append('')
    lines.append('## 一、回测概览')
    lines.append('')
    lines.append('| 项目 | 数值 |')
    lines.append('|:---|:---|')
    lines.append(f'| 总场次 | {total} |')
    lines.append(f'| 有赔率场次 | {with_odds} |')
    lines.append(f'| 无赔率场次 | {without_odds} |')
    lines.append(f'| 生成时间 | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |')
    lines.append('')

    # 场次清单表
    lines.append('## 二、场次清单与规则触发表')
    lines.append('')
    lines.append('| 日期 | 比赛 | 比分 | 热门方 | 实际结果 | 热门方命中 | 触发规则 | 备注 |')
    lines.append('|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|')

    for m in matches:
        home = m.get('home', '')
        away = m.get('away', '')
        score = m.get('score', '')
        home_goals, away_goals = parse_score(score)
        actual = get_actual_result(home_goals, away_goals)

        favorite = get_implied_favorite(
            m.get('home_odds'),
            m.get('draw_odds'),
            m.get('away_odds')
        )

        favorite_str = {
            'home': home,
            'draw': '平局',
            'away': away,
            None: '无数据'
        }.get(favorite, '无数据')

        actual_str = {
            'home': f'{home}胜',
            'draw': '平局',
            'away': f'{away}胜',
            None: '未知'
        }.get(actual, '未知')

        correct = is_favorite_correct(favorite, actual)
        if correct is True:
            correct_str = '✅'
            correct_count += 1
        elif correct is False:
            correct_str = '❌'
            upset_count += 1
        else:
            correct_str = '—'
            unknown_count += 1

        rules = m.get('rules', '待填充')
        notes = m.get('notes', '')

        lines.append(f"| {m.get('date', '')} | {home} vs {away} | {score} | {favorite_str} | {actual_str} | {correct_str} | {rules} | {notes} |")

    lines.append('')

    # 命中率统计
    lines.append('## 三、方向判断命中率')
    lines.append('')
    lines.append('| 类型 | 场次 | 占比 |')
    lines.append('|:---|:---:|:---|')
    lines.append(f'| 热门方命中 | {correct_count} | {correct_count/total*100:.1f}%' if total else '| 热门方命中 | 0 | — |')
    lines.append(f'| 冷门/下盘打出 | {upset_count} | {upset_count/total*100:.1f}%' if total else '| 冷门/下盘打出 | 0 | — |')
    lines.append(f'| 无法判断 | {unknown_count} | {unknown_count/total*100:.1f}%' if total else '| 无法判断 | 0 | — |')
    lines.append('')

    # 规则触发统计（占位）
    lines.append('## 四、规则触发统计表')
    lines.append('')
    lines.append('| 规则 | 触发次数 | 命中次数 | 命中率 |')
    lines.append('|:---|:---:|:---:|:---|')
    lines.append('| 🚌冷门检测 | 待填充 | 待填充 | 待填充 |')
    lines.append('| 🎈伪传控陷阱 | 待填充 | 待填充 | 待填充 |')
    lines.append('| 📉对手质量折扣 | 待填充 | 待填充 | 待填充 |')
    lines.append('| 🏠东道主加成 | 待填充 | 待填充 | 待填充 |')
    lines.append('| 🐴黑马球队 | 待填充 | 待填充 | 待填充 |')
    lines.append('')

    # 关键案例和经验教训
    lines.append('## 五、关键案例分析')
    lines.append('')
    lines.append('（根据场次清单中标记为冷门或规则触发的比赛，选择2-4场深入分析）')
    lines.append('')
    lines.append('### 案例1：')
    lines.append('- **赛前背景**：')
    lines.append('- **触发规则**：')
    lines.append('- **判断**：')
    lines.append('- **实际结果**：')
    lines.append('- **结论**：')
    lines.append('')

    lines.append('## 六、经验教训')
    lines.append('')
    lines.append('| 序号 | 发现 | 对应规则 | 后续优化 |')
    lines.append('|:---:|:---|:---|:---|')
    lines.append('| 1 | 待填充 | 待填充 | 待填充 |')
    lines.append('')

    lines.append('## 七、局限性说明')
    lines.append('')
    lines.append('- 缺少精确赛前赔率时，热门方判断基于赔率推断或球队实力')
    lines.append('- 部分规则触发需要控球率、射门、xG 等数据，本表可能未完全覆盖')
    lines.append('- 样本量和规则触发次数有限时，命中率可能受偶然性影响')
    lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='自动生成世界杯投注方案回测报告')
    parser.add_argument('--results', required=True, help='赛果 JSON 文件路径')
    parser.add_argument('--output', '-o', default='backtest-report.md', help='输出 markdown 文件路径')

    args = parser.parse_args()

    results_path = Path(args.results)
    if not results_path.exists():
        print(f"错误：文件不存在 {results_path}", file=sys.stderr)
        sys.exit(1)

    with open(results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    matches = data.get('matches', [])
    if not matches:
        print("错误：没有比赛数据", file=sys.stderr)
        sys.exit(1)

    report = generate_report(matches)

    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"回测报告已生成：{output_path}")
    print(f"总场次：{len(matches)}")


if __name__ == '__main__':
    main()
