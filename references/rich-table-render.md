# 终端表格渲染问题

## 症状

在Windows PowerShell终端中，render_table()输出的Unicode画线字符（┌ ┐ │ └ ┘ ├ ┤ ┼）可能不可见或渲染为乱码，导致表格内容一片空白。

## 原因

Windows PowerShell / Windows Terminal对Unicode框线字符的渲染与Linux终端行为不同。Hermes CLI的rich库默认使用box.SIMPLE（仅有横线无竖线），且execute_code输出的特殊字符可能被过滤。

## 修复方案

### 方案一（已实施）：patch rich库

修改Hermes依赖的rich库markdown.py中的box设置：
- 文件：`/home/bryan_pan/.local/lib/python3.12/site-packages/rich/markdown.py`
- 第251行：`box=box.SIMPLE` → `box=box.HEAVY`
- 效果：markdown表格在Hermes CLI终端中显示完整边框（┏ ┳ ┓ ┃）

### 方案二（备用）：纯Markdown表格

如果render_table()的Unicode字符仍然不可见，退回到纯Markdown格式：
```python
def md_table(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |']
    lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    for row in rows:
        lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')
    return '\n'.join(lines)
```
这种格式在所有终端中都能渲染。

## 表宽控制

终端宽度通常为80列。超过6列的表格会被截断或不可见。
- 10列赔率表 → 拆成胜平负（6列）和让球盘（6列）两张
- 投注明细表通常6列以内
- 场景分析表通常4列以内
