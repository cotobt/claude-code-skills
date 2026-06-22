# 数据源参考

本文件汇总 skill 各环节可用的数据源，按使用模式和数据类型分类。

---

## 一、按模式分类

### 1. 投注方案模式（只能用竞彩官方赔率）

| 数据源 | URL | 用途 | 说明 |
|:---|:---|:---|:---|
| 500彩票网 | https://trade.500.com/jczq | 竞彩胜平负/让球胜平负赔率 | 唯一合法可投注数据源，必须优先使用 |
| 500彩票网半全场 | https://trade.500.com/jczq/index.php?playid=272&g=2 | 半全场赔率 | 当胜平负页数据缺失时使用 |

**铁律**：投注方案模式下，所有赔率必须来自 500.com 同一页面同一玩法，禁止从其他渠道补数据。

---

### 2. 预测分析模式（多源辅助）

#### 即时比分/战报

| 数据源 | URL | 特点 | 使用场景 |
|:---|:---|:---|:---|
| DS足球 | https://www.dszuqiu.com | 即时比分快、中文友好 | 快速确认比分和赛程 |
| 懂球帝 | https://www.dongqiudi.com | 图文直播、赛后战报、社区 | 查战报和关键事件 |
| SofaScore | https://www.sofascore.com | 实时事件、球员评分、热点图 | 查控球、射门、xG、阵容 |
| Flashscore | https://www.flashscore.com | 覆盖广、赛程全 | 查赛程和基础比分 |

#### 高阶数据（xG、控球、射门、战术）

| 数据源 | URL | 特点 | 使用场景 |
|:---|:---|:---|:---|
| FBref | https://fbref.com | 免费、Sports Reference 数据库、高阶数据全 | Step 6 🚌冷门检测、Step 3.5 检查表 |
| Understat | https://understat.com | xG 专项、可视化清晰 | 🎈伪传控检测、xG 偏离分析 |
| WhoScored | https://www.whoscored.com | 球员评分、热点图、战术统计 | 15维度评分、球员状态评估 |
| SofaScore | https://www.sofascore.com | 实时数据、球员评分、事件时间轴 | 快速获取比赛统计 |

#### 赔率/市场数据

| 数据源 | URL | 特点 | 使用场景 |
|:---|:---|:---|:---|
| OddsPortal | https://www.oddsportal.com | 多机构赔率轨迹 | 回测历史赔率、市场资金流向 |
| 365scores | https://www.365scores.com | 多家博彩商赔率汇总 | 交叉验证市场赔率 |
| Pinnacle | https://www.pinnacle.com | 专业博彩赔率 | 市场隐含概率基准 |
| bet365 | https://www.bet365.com | 国际赔率基准 | 辅助判断市场共识 |

#### 球员/阵容数据

| 数据源 | URL | 特点 | 使用场景 |
|:---|:---|:---|:---|
| Transfermarkt | https://www.transfermarkt.com | 身价、转会历史、合同 | D6人员可用性、D9阵容默契度 |
| 百度体育（球员资料） | https://tiyu.baidu.com/al/player?id=...&tab=资料 | 球员基本信息、能力属性 | 人工核实核心球员资料 |
| 百度体育（球员数据） | https://tiyu.baidu.com/al/player?id=...&tab=数据 | 球员比赛统计 | 动态加载，AI 自动提取不稳定 |

---

### 3. 回测模式（历史数据）

| 数据源 | URL | 特点 | 使用场景 |
|:---|:---|:---|:---|
| FBref | https://fbref.com | 历史比赛数据完整 | 历史战绩、长期统计回测 |
| Understat | https://understat.com | 历史 xG 数据 | 历史比赛进攻质量回测 |
| OddsPortal | https://www.oddsportal.com | 历史赔率轨迹 | 投注方案历史盈亏回测 |
| 500彩票网历史开奖 | 见下方 | 竞彩官方历史赔率 | 最权威的历史投注回测数据源 |

---

## 二、企业级/付费数据源（理想选择）

| 数据源 | 说明 | 获取方式 |
|:---|:---|:---|
| **Opta** | 全球顶级足球数据供应商，事件级数据、xG、传球网络、球员追踪 | 需联系 Opta 购买商业授权 |
| **Stats Perform** | Opta 母公司，提供更广泛的数据服务 | 企业级合作 |
| **Sportradar** | 体育数据解决方案，覆盖赛事直播、赔率、统计 | 企业级合作 |

**说明**：Opta 是 skill 的理想数据源，但个人用户通常需要通过商业合作获取。日常预测可用 FBref/Understat/SofaScore 等免费数据源替代。

**公开资源**：Opta Analyst（https://theanalyst.com）提供一些基于 Opta 数据的免费分析文章，可作为参考。

---

## 三、500彩票网采集要点

- 让球胜平负：`playid=269&g=2`
- 半全场：`playid=272&g=2`
- 比分：`playid=271&g=2`
- 日期参数 `date=2026-06-20` 可能 302 到首页，跟 `-L` 后从日期筛选器取 `data-num`
- 周六/周日比赛在"周六""周日"标签下，而不是"周五"
- **解析细节**：参见 `references/500-parse-guide.md` — 队名从 `title` 属性提取、排名在 `[N]` 中、让球数在 td[4] 中

### 已知解析坑

- 部分场次 `nspf`（胜平负赔率）可能缺失（推测页面部分区域 JS 动态渲染），此时让球盘 `spf` 仍正常
- 投注方案模式下，不可自行用国际赔率补充；预测分析/回测模式下可补充

---

## 四、赛程确认

- Facebook 赛程帖：搜索 "World Cup 2026 [日期] schedule"
- FIFA 官网：https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026
- 注意时区换算：MYT(UTC+8) 与北京时间一致

---

## 五、数据源选择建议

| 使用场景 | 推荐组合 |
|:---|:---|
| 出真实投注方案 | 500.com（唯一） |
| 赛前预测分析 | 500.com + SofaScore/FBref + OddsPortal |
| 历史回测 | FBref + Understat + OddsPortal + 500.com历史 |
| 查球员身价/阵容 | Transfermarkt + 百度体育（人工参考） |
| 硬核战术分析 | FBref + WhoScored + Understat |
| 机构级专业分析 | Opta（需授权） |
