# 数据源参考

## 赔率数据源

| 数据源 | URL模式 | 特点 | 采集方式 |
|--------|---------|------|----------|
| 500彩票网 | trade.500.com/jczq/ | 竞彩官方赔率，GB2312编码 | curl + iconv转码，注意302重定向 |
| 365scores | 365scores.com/en-us/football | 多家博彩商赔率汇总，无JS渲染 | web_search |
| Pinnacle | pinnacle.com | 专业博彩赔率 | web_search |
| bet365 | bet365.com/hub | 国际赔率基准 | web_search(新闻站) |

## 500彩票网采集要点

- 让球胜平负：`playid=269&g=2`
- 半全场：`playid=272&g=2`
- 比分：`playid=271&g=2`
- 日期参数 `date=2026-06-20` 可能302到首页，跟 `-L` 后从日期筛选器取 `data-num`
- 周六/周日比赛在"周六""周日"标签下，而不是"周五"
- **解析细节**：参见 `references/500-parse-guide.md` — 队名从 `title` 属性提取、排名在 `[N]` 中、让球数在td[4]中

## ⚠️ 已知解析坑

- 部分场次 `nspf`（胜平负赔率）可能缺失（推测页面部分区域JS动态渲染），此时让球盘 `spf` 仍正常，可考虑通过让球盘反推或使用国际赔率补充

## 赛程确认

- Facebook赛程帖：搜索"World Cup 2026 [日期] schedule"
- 注意时区换算：MYT(UTC+8)与北京时间一致
