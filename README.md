<div align="center">

# telos

> *「乘物以游心」* — 《庄子 · 人间世》

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://claude.ai/code)
[![V0](https://img.shields.io/badge/v0.1.0-ready-green)](https://github.com/zwbao/telos/releases/tag/v0.1.0)
[![Self-trial](https://img.shields.io/badge/creator--self--trial-day%202%2F14-orange)](#边界)

<br>

### 用 AI 越多，决策越快，方向越糊。
### 速度遮蔽了方向的缺席——这是为此而设的一道纪律。

<br>

telos 不是日程管理，不是 Journaling，不是心灵鸡汤。<br>
它只做一件事：**让"决策"成为一个有纪律的动作。**

你把北极星留在 `profile.md` 里。<br>
AI 每次想给你建议时，先被强制回头看它一眼；<br>
日常 session 被默默记录，每周交出一个 1–10 的意义分。<br>
数据永远在你本地——不上传、不训练、不同步。

<br>

<sub>*亚里士多德的* τέλος *——一个事物内在指向的终点。
你不必信宿命论，只须承认：方向是声明出来的，不是等来的。*</sub>

<br>

**适合：** 重度 AI 用户 · 同时在推进几件方向不相容的事 · 觉得"每天都在做，却说不清在为什么做"

**不适合：** 已有稳定可信的师友/伴侣/治疗师（别抢深度关系）· 正在抑郁发作（请找人，不是找机器）

<br>

> **当前状态** · V0.1.0 shipped 2026-04-20 · 创建者本人 14 天自跑实验进行中 · 首批数据来自 `~/.claude/telos/weekly.md`，不取自你

<br>

[看效果](#看效果) · [安装](#安装) · [对比](#对比) · [方法论](#方法论) · [边界](#边界)

<br>

[![Star History Chart](https://api.star-history.com/svg?repos=zwbao/telos&type=Date)](https://star-history.com/#zwbao/telos&Date)

</div>

---

## 看效果

### 1. 十分钟，把这辈子的方向压进一段话

```
你        ❯ /telos:telos

telos    ❯ 还没看到你的 profile。先做 10 分钟 intake，
           之后你会有一段北极星，可以被强制引用。

           Q3：不加解释，写下对你最重要的 5 个词。

你        ❯ 诚实、好奇、自由、责任、长期

           ...

           Q5：当前最卡住你的一个问题？

你        ❯ 同时想做的事太多，精力配不上

telos    ❯ 基于你给的五个价值 + 十年图景，我合成这段北极星：

           > 你在做一件用自己的手能做到、做完后别人会替你继续
           > 做的事。同时做三件不是"精力不够"，是你还没承认
           > 哪件是主。承认了，另两件会自动变成它的养料。

           听着对吗？（对 → 写入。不对 → 我重新合成。）
```

### 2. 决策时，AI 不许先给答案——必须先引用你自己说过的话

telos 内置 HARD-GATE：未引用北极星原文 + 未枚举 ≥ 2 选项 + 未给可追溯推荐 → **不许**输出决策建议。

```
你        ❯ /telos:telos 我应不应该接这个咨询 offer？薪水是主业的 1.5 倍

telos    ❯ 🤔 deciding-with-telos

           **Polestar**:
           > 你在做一件用自己的手能做到、做完后别人会替你继续做的事。

           **Decision restated**: 接一个经济回报高、但不可积累的兼职。

           **Options**:
           - A: 接
             - Aligned: 现金流能让你主业少妥协
             - Misaligned: 咨询的产出不变成"你的"
           - B: 拒
             - Aligned: 每分钟都花在你能积累的事上
             - Misaligned: 短期经济压力可能更焦虑

           **Recommendation**: 拒（或只接够覆盖基本开销的量）
           **Reasoning**: 你的北极星要求"做完后别人会替你继续做"——
           咨询离开了你就停。薪水高不能抵消"非积累"的代价。

           [写入 ~/.claude/telos/decisions/2026-04-20-offer.md]
```

### 3. 每天最后，三问收束；每周日，一个数字加一句话

```
你        ❯ /telos:telos

telos    ❯ 今天 brief 已有。开始 reflection：
           1. 今天什么对齐了？

你        ❯ 推进了研究代码，没被消息群拉走

telos    ❯ 2. 今天什么没对齐？

你        ❯ 晚上 2 小时刷短视频

telos    ❯ 3. 明天想带走一件什么事？

你        ❯ 设一个"手机放书房"的硬规则

telos    ❯ 已追加到 journal。明天 brief 时会把"手机放书房"
           作为今日避免项之一。

           ---

           顺手：这是本周第 7 天，做个 weekly checkin 吗？
           1-10，这周感觉多有意义？

你        ❯ 6。推进了三件事，但 Q4 焦虑仍在。

telos    ❯ 记了。三个月内连续低于 4 我会提醒你做 recalibrate。
```

这不是角色扮演，不是生产力贴纸。这是一道 HARD-GATE——**逼你在每个决策点，面对你自己声明过的那段话**。

---

## 安装

### Claude Code（V0 已测）

```
/plugin marketplace add zwbao/telos
/plugin install telos@telos
/reload-plugins
/telos:telos
```

首跑进入 10 分钟 intake。之后每天一句 `/telos:telos` 就够——它按当前状态自动分流到早间 brief / 决策 / 晚间反思 / 周日 checkin。

### 多平台路线图

方法论与平台无关。V0 只在 Claude Code 验证过，架构允许多平台适配：

| 平台 | 状态 | 备注 |
|---|---|---|
| Claude Code | ✅ V0 可用 | 3 hooks + 6 skills + 2 commands |
| OpenAI Codex | 🗓️ 路线图 | Skills 可复用；需 Codex hook 适配 |
| Cursor | 🗓️ 路线图 | Skills 可复用；需 cursor-plugin manifest |
| Gemini CLI | 🗓️ 路线图 | Skills 与 activate_skill 机制兼容 |
| OpenCode | 🗓️ 路线图 | |

即便所在平台不支持 hooks，**方法论本身仍可用**：把 `docs/methodology.md` 贴进去 + 复用 `skills/*/SKILL.md` 的提示词，就能跑对话循环——只是少了 journal 自动记录与 SessionStart 注入。

---

## 对比

telos 和日程、教练、冥想工具做的不是同一件事。它只做一件：**让"决策"成为一个有纪律的动作**。

| | Journaling (Day One) | Life coach | Meditation (Calm) | **telos** |
|---|---|---|---|---|
| 有明确方向 | ❌ 自己写流水账 | ✅ 在教练脑里 | ❌ 无方向 | ✅ **声明在 profile.md** |
| 决策支持 | ❌ | ✅ 每周一次 | ❌ | ✅ **每次决策强制引用北极星** |
| 被动观察 | ❌ | ❌ | ❌ | ✅ **hooks 看你实际在做什么** |
| AI 参与度 | 零 | 零 | 引导词 | **主导全流程** |
| 是否游戏化 | streak | - | 徽章 | **拒绝** |

其他工具预设你"不够自律"。telos 预设你"还没清晰"——清晰了，自律就不成其为问题。

---

## 方法论

把"人生导航"真正做好，远比写 todo 深。telos 在五层上工作：

| 层 | telos 的做法 | 其他工具通常做法 |
|---|---|---|
| **声明** (declare) | 用你自己的话，≤ 300 字一段北极星 | journaling：让你每天写流水账 |
| **咨询** (consult) | 决策前**强制引用**原文 | 决策日记：让你"反思"（谁反思得动） |
| **记录** (log) | Stop hook 默默写，不打扰你 | todo app：让你填 checklist |
| **测量** (measure) | 一周一个数字 + 一句话 | wellness app：一百个伪指标 |
| **重校准** (recalibrate) | 承认"我变了"，深度重启（V1） | habit app：让你坚持原计划——哪怕方向已错 |

每一层都写明了**不做之事**——

- **声明层**：不许我替你决定你是谁
- **咨询层**：不许跳过引用直接给答案
- **记录层**：不许读你的 journal
- **测量层**：不许把 1–10 分做成排行榜
- **重校准层**：不许把临时情绪认作长期漂移

---

## 边界

```
做不到 ≠ 坏产品。
一个不说自己做不到什么的工具，不值得信。
```

- **LLM 会幻觉一段听上去深刻、却并非你的北极星。** profile.md 是你的纯文本，随时改。
- **北极星会 calcify。** 事业做起来了，谈了新恋爱，换了城市——方向可能已变。记得定期 recalibrate。
- **人群偏差真实存在。** telos 只服务于愿意装 Claude Code 的人，这是小众群体，别以为它能救所有迷茫的人。
- **不能替代治疗。** 抑郁发作、躁狂、自伤意念，请找人，不是找机器。
- **不能替代关系。** 你若已有关系健康的导师/伴侣/治疗师，telos 是多余的——甚至会抢走本属于深度关系的位置。
- **这是社会学实验，不是已证实的干预。** 假设是"外化方向 + 强制咨询"会改变主观意义感知，**尚无数据证实**。首批数据来自创建者本人的 14 天自跑（`~/.claude/telos/weekly.md`）。

---

## 数据

```
~/.claude/telos/           # 你的，永不离你的机器
├── profile.md             # 北极星 · 命盘 · 价值观 · 十年图景 · 调整史
├── journal/YYYY-MM-DD.md  # 每日 [brief] / [session] / [reflect] / [weekly]
├── decisions/             # 一次决策一份文件，含事后 [outcome]
├── weekly.md              # 一行一周：分数 + 一句为什么
└── observations.jsonl     # 事件日志（无 prompt 内容，无 PII）
```

上传？不。云同步？不。模型训练？绝不。

---

## 细读

- [`docs/methodology.md`](docs/methodology.md) — 五层方法论的完整说明
- [`docs/experiment.md`](docs/experiment.md) — 社会学实验框架、数据字典、匿名化承诺
- [`docs/superpowers/specs/2026-04-20-telos-design.md`](docs/superpowers/specs/2026-04-20-telos-design.md) — V0 架构 spec
- [`CLAUDE.md`](CLAUDE.md) — 插件系统指令（AI 看的那部分）

---

## License

MIT。代码任用。方法论任学。数据永远是你的。
