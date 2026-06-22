# 场景分析：选项名消歧

## 问题

当多场比赛的"选项"列相同（如029和032都是"主胜"），场景分析表中"仅主胜错"会歧义——读者不知道说的是哪场。

## 解决方案

场景表中"命中情况"列始终使用**球队名**（或"主队名+选项"）代替纯选项名：

- ✅ `仅美国错`（唯一，一眼能识别）
- ✅ `仅土耳其错`
- ❌ `仅主胜错`（歧义，029和032都叫"主胜"）
- ✅ `美国+土耳其`（中2场）
- ❌ `主胜+主胜`（歧义）

## 实现方法（Python代码）

```python
# 为每场比赛构建唯一标识
opt_labels = {
    "029": {"label": "美国", "opt": "主胜"},  # 用球队名
    "030": {"label": "摩洛哥", "opt": "客胜"},
    "031": {"label": "巴西", "opt": "让胜"},
    "032": {"label": "土耳其", "opt": "主胜"},
}

# 中3场：仅XX错
for miss_idx in range(4):
    miss_id = ids[miss_idx]
    label = opt_labels[miss_id]["label"]
    print(f"| 仅{label}错 | ...")

# 中2场
for i in range(4):
    for j in range(i+1, 4):
        label = f"{opt_labels[ids[i]]['label']}+{opt_labels[ids[j]]['label']}"
        print(f"| {label} | ...")
```
