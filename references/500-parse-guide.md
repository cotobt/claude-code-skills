# 500彩票网 HTML 解析指南

基于 2026-06-19 实际抓取验证。

## 基本命令

```bash
curl -s -L "https://trade.500.com/jczq/" | iconv -f gb2312 -t utf-8//IGNORE > /tmp/500.html
```

`-L` 必须加，有302重定向。
`iconv` 加 `//IGNORE` 防止不合规字节导致中断。

## HTML结构（已验证）

### 比赛行
```html
<tr class="bet-tb-tr">
  <td>[场次编号]</td>           <!-- td[0] -->
  <td>[联赛名称]</td>           <!-- td[1] -->
  <td>[时间]</td>               <!-- td[2] -->
  <td class="td_team">          <!-- td[3] — 队名 -->
    <div class="team">
      <span class="team-l">
        <i title="排名第X">[N]</i>
        <a title="队名" class="team-l">队名</a>
      </span>
      <i class="team-vs">VS</i>
      <span class="team-r">
        <a title="队名" class="team-r">队名</a>
        <i title="排名第Y">[M]</i>
      </span>
    </div>
  </td>
  <td [让球数+单关标志]>        <!-- td[4] -->
</tr>
```

### ⚠️ 队名提取关键点

**不要从 td 纯文本提取队名** — 因为 `<i class="team-vs">VS</i>` 被解析为纯文本后，队名字符串中间会有一个 "VS"，解析困难。

**正确做法：从 title 属性提取**

```python
home_title = re.search(r'class="team-l"[^>]*title="([^"]*)"', td3_html)
away_title = re.search(r'class="team-r"[^>]*title="([^"]*)"', td3_html)
home_name = home_title.group(1) if home_title else "?"
away_name = away_title.group(1) if away_title else "?"
```

### 排名提取
排名在 `<i>` 标签的 `[N]` 中，主队在 `team-l` 范围内，客队在 `team-r` 范围内：

```python
home_rank_m = re.search(r'class="team-l"[^>]*>.*?\[(\d+)\]', td3_html)
away_rank_m = re.search(r'class="team-r"[^>]*>.*?\[(\d+)\]', td3_html)
```

### 赔率提取（已验证）

**胜平负 (nspf)：**
```python
spf = re.findall(r'data-type="nspf"[^>]*data-value="([^"]*)"[^>]*data-sp="([^"]*)"', tr_html, re.DOTALL)
# data-value: 3=主胜, 1=平, 0=客胜
```

**让球胜平负 (spf)：**
```python
rqspf = re.findall(r'data-type="spf"[^>]*data-value="([^"]*)"[^>]*data-sp="([^"]*)"', tr_html, re.DOTALL)
```

### 让球数提取
让球数在 td[4] 中，格式如 `-1`、`-1/1.5`、`+1` 等：

```python
h_match = re.search(r'([+-]?\d+(?:/\d+\.?\d*)?)\s', td4_html)
handicap = h_match.group(1) if h_match else "0"
```

### 单关标志
td[4] 中包含 `单关1` 或 `单关0`：

```python
dg = "单关" if "单关1" in td4_html else "非单关"
```

## ⚠️ 已知坑

### 1. 部分场次胜平负赔率不可投注（不是"缺失"）
2026-06-20 巴西vs海地、西班牙vs沙特等场次的 `data-type="nspf"` 为空（data-sp无值），但 `data-type="spf"`（让球盘）正常。原因：竞彩官方未开设该场次该玩法的投注。

**⛔ 绝对铁律：不可投注 = 不可补数据**
- 竞彩页面显示"暂无数据"或data-sp为空 → 该玩法该场次不可投注
- **绝对不能**从其他页面（如playid=272的页面）、其他玩法（让球盘）、其他渠道（国际博彩）扒数据来"补"缺失的赔率
- 这是竞彩官方数据完整性的红线——补了就是编数据
- 正确做法：该场次该玩法在分析中标注"不可投注"，仅分析可投注的玩法

### 2. 场次编号意义
- 周五029 = 周五第29场（周一至周日编号连续）
- 数了12场是从029到040，覆盖周五到周日
- 日期从 `06-20 03:00` 到 `06-22 09:00`

### 3. 联赛名在 td[1]
联赛名称在 `td[1]` 中，这次12场全是"世界杯"。
