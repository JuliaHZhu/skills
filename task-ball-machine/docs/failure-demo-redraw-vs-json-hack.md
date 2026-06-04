# Failure Demo: 手改 JSON 是不是贩毒？

## 场景

今天早上机器抽到了：

```
即么 morning     💼  回复邮件                           ✅完成了
```

你实际做的是：休息了。

你想把 morning 的任务修改为 "上午休息了"，同时把 💼 Work 球换成 🧘 Rest 球。

---

## ❌ 错误做法：直接改 JSON

你打开 `state.json`，伸手进去调：

```json
// 服了你，第一次手改 JSON
{
  "morning": {
    "box": "Rest",          // 刚才还是 Work，变成 Rest！
    "content": "上午休息了",
    "ball_id": "BALL-RES-001"  // 定向爬进了一颗 Rest 球
  }
}
```

然后再入侵 `boxes` 部分，人工调整 used 和 stack：

```json
"Work": {
  "stack": ["BALL-WORK-001", "BALL-WORK-002"],  // 把它扔回去
  "used": ["BALL-WORK-003"]                       // 从 used 里弹出来
},
"Rest": {
  "stack": ["BALL-RES-002", "BALL-RES-003"],     // 取出一颗
  "used": ["BALL-RES-001"]                        // 塞进去
}
```

### 结果：统计是对的，但过程是假的

| 问题 | 说明 |
|------|------|
| 统计数据 | Work 2/3，Rest 1/3，看上去对 |
| 退弹机制 | ❌ 被跳过了，没有把球推回箱子里 |
| 随机性 | ❌ 你直接抱走了 BALL-RES-001，而不是摇到的 |
| 可见性 | ❌ `redraw` 的记录在日志里为空，因为你完全绕过了它 |
| 可重复性 | ❌ 其他人读你的操作，看不出发生了什么 |

**的确，手改 JSON 给你一个"正确的结果"，但你得到的结果是被偷出来的。**

这就像有人在吃赚饭库里直接进数据库更新"已打卡"一样——后台显示对，但你并没有真的拿起手机打卡。

---

## ✅ 正确做法：用 CLI 走退弹流程

```bash
# 1. 退弹：把 💼 Work 球扔回箱子，重新摇
ball-machine redraw morning
# 打印：重新抽到 📚 Study
# 不对。再来。

ball-machine redraw morning
# 重新抽到 📚 Study
# 不对。再来。

ball-machine redraw morning
# 重新抽到 🏃 Health
# 不对。再来。

ball-machine redraw morning
# 重新抽到 🧘 Rest  ← 好了！
```

```bash
# 2. 修改内容：给球贴上正确的标签
ball-machine edit morning "上午休息了"
```

```bash
# 3. 完成
ball-machine complete morning
```

### 结果：统计对，过程也对

| 属性 | 手改 JSON | CLI 流程 |
|------|-----------|-----------|
| 统计数据 | ✅ 对 | ✅ 对 |
| 退弹录影 | ❌ 没有 | ✅ 4 次 |
| 随机录影 | ❌ 直接抱走 | ✅ 随机抽取 |
| 可查询 | ❌ 无操作记录 | ✅ state 保留次序 |
| 可重复 | ❌ 不可重现 | ✅ 每次打开都能看到 |

---

## 观念性比较

```
错误流程：
  morning——Work球——(edit JSON 换成 Rest)——完成
         ↑
    跳过了退弹机制和随机摇箱

正确流程：
  morning——Work球——redraw(Study)——redraw(Study)——redraw(Health)——redraw(Rest)——edit——complete
         ↑↓                                      ↓
       归还                                   随机摇到
```

---

## 必要性

**这不是冒险主义，是统计安全。**

不同箱子的完成率会影响：
- 你下一次调整周期长度的决策
- 哪个盒子需要加球
- 你的"实际产出"跟"计划产出"是不是一致

手改 JSON = 在记账上假装做了结果正确的事，但实际的"曲率"是被篡改的。

---

## 唯一可以改 JSON 的情况

1. **系统崩溃恢复**——state.json 损坏，由管理员从备份恢复
2. **开发调试**——在开发环境下测试，不用于生产数据
3. **迁移**——把数据从一个环境导入另一个，且需要保证一致性

**日常使用不应该手动编辑 state.json。**
