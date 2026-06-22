#!/usr/bin/env python3
"""表格渲染工具 — 自动计算中文字符宽度，生成对齐的终端表格

用法：
    exec(open('...render-table.py').read())
    print(render_table(headers, rows))          # Unicode画线边框
    print(md_table(headers, rows))              # 纯Markdown（终端渲染用）

表宽控制：每张表不超过6列。超过6列拆成两张窄表。
"""

def render_table(headers, rows):
    """自动计算中文字符宽度的表格渲染器
    
    headers: 列表，表头
    rows: 列表的列表，每行数据
    返回：带Unicode边框的表格字符串
    """
    def w(s):
        return sum(2 if ord(c) > 127 else 1 for c in str(s))
    
    col_widths = []
    for i, h in enumerate(headers):
        cw = w(h)
        for row in rows:
            cw = max(cw, w(row[i]) if i < len(row) else 0)
        col_widths.append(cw + 2)
    
    sep = '├' + '┼'.join('─' * cw for cw in col_widths) + '┤'
    top = '┌' + '┬'.join('─' * cw for cw in col_widths) + '┐'
    bot = '└' + '┴'.join('─' * cw for cw in col_widths) + '┘'
    
    lines = [top]
    
    # 表头行
    hdr = '│'
    for i, h in enumerate(headers):
        pad = col_widths[i] - w(h)
        left = 1
        right = pad - left
        hdr += ' ' * left + str(h) + ' ' * right + '│'
    lines.append(hdr)
    lines.append(sep)
    
    # 数据行（每行之间加横线分隔）
    for i, row in enumerate(rows):
        line = '│'
        for j, cell in enumerate(row):
            cell_s = str(cell)
            pad = col_widths[j] - w(cell_s)
            left = 1
            right = pad - left
            line += ' ' + cell_s + ' ' * right + '│'
        lines.append(line)
        if i < len(rows) - 1:
            lines.append(sep)
    
    lines.append(bot)
    return '\n'.join(lines)


def md_table(headers, rows):
    """纯Markdown表格（无Unicode边框字符）
    
    当render_table的Unicode字符在终端中不可见时使用此函数。
    在任何终端中都能正确渲染。
    """
    lines = ['| ' + ' | '.join(headers) + ' |']
    lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    for row in rows:
        lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')
    return '\n'.join(lines)


if __name__ == '__main__':
    # 自测
    headers = ['票号', '串法', '组合', '倍数', '金额']
    rows = [
        ['1', '2串1', '巴西让负 + 土耳其主胜', '3', '¥6'],
        ['2', '2串1', '巴西让负 + 美国主胜', '3', '¥6'],
        ['3', '2串1', '土耳其主胜 + 苏格兰平', '1', '¥2'],
    ]
    print("=== Unicode边框 ===")
    print(render_table(headers, rows))
    print()
    print("=== 纯Markdown ===")
    print(md_table(headers, rows))
