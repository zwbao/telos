<div align="center">

# telos

> *「你说出方向，AI 接管导航——你省下的注意力，用来欣赏风景」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://claude.ai/code)
[![V0](https://img.shields.io/badge/v0.1.0-ready-green)](https://github.com/zwbao/telos/releases/tag/v0.1.0)
[![Multi-platform](https://img.shields.io/badge/Codex%20%7C%20Cursor%20%7C%20Gemini-roadmap-lightgrey)](#多平台路线图)

<br>

**人生自动驾驶系统。把方向声明出来，把日常决策外包给 AI，把带宽留给体验本身。**

<br>

亚里士多德的 *τέλος* ——一个事物内在指向的终点。<br>
telos 不需要你真的相信宿命论，只需要你承认：**方向是声明出来的，不是等来的**。<br>
你声明一段北极星，AI 在每个决策点强制回头看它，日常 session 被默默记录，每周一个 1-10 的意义分。

[看效果](#看效果) · [安装](#安装) · [和其他东西有什么区别](#不是-x是-y) · [方法论的五层](#方法论的五层) · [诚实边界](#诚实边界)

<br>

[![Star History Chart](https://api.star-history.com/svg?repos=zwbao/telos&type=Date)](https://star-history.com/#zwbao/telos&Date)

</div>

---

## 看效果

### 1. 十分钟，把你这辈子的方向压进一段话

```
你        ❯ /telos:telos

telos    ❯ 还没看到你的 profile。先做 10 分钟 intake，
           之后你会有一个北极星可以被强制引用。

           Q3：不加解释，写下对你最重要的 5 个词。

你        ❯ 诚实、好奇、自由、责任、长期

           ...

           Q5：当前最卡住你的一个问题？

你        ❯ 同时想做创业、研究、投资，精力完全不够

telos    ❯ 基于你给的五个价值 + 十年图景，我合成这段北极星：

           > 你在做一件用自己的手能做到、做完后别人会替你继续做
           > 的事。同时做三件不是"精力不够"，是你还没承认哪件是
           > 主。承认了，另两件会自动变成它的养料，不会消失。

           听着对吗？（对 → 写入。不对 → 我重新合成。）
```

### 2. 决策时，AI **不许**先给答案——必须先引用你自己说过的话

telos 内置 HARD-GATE：未引用北极星原文 + 未枚举 ≥ 2 选项 + 未给可追溯推荐 → 不许输出决策建议。

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
             - Misaligned: 短期经济压力可能让你更焦虑

           **Recommendation**: 拒（或只接够覆盖基本开销的量）
           **Reasoning**: 你的北极星要求"做完后别人会替你继续做"——
           咨询离开了你就停。薪水高不能抵消"非积累"的代价。

           [写入 ~/.claude/telos/decisions/2026-04-20-offer.md]
```

### 3. 每天最后，三问闭环；每周日，一个数字 + 一句话

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

**这不是角色扮演，不是生产力贴纸。这是一套有 HARD-GATE 的纪律——强制你在每个决策点，面对你自己声明过的方向。**

---

## 安装

### Claude Code（V0 已测）

```
/plugin marketplace add zwbao/telos
/plugin install telos@telos
/reload-plugins
/telos:telos
```

首次运行会进入 10 分钟的 intake。之后每天 `/telos:telos` 就够了——它根据状态自动路由到早间 brief / 决策 / 晚间反思 / 周日 checkin。

### 多平台路线图

telos 的方法论是平台无关的。V0 只测了 Claude Code，但架构允许（对标 [obra/superpowers](https://github.com/obra/superpowers) 的多平台适配）：

| 平台 | 状态 | 备注 |
|---|---|---|
| Claude Code | ✅ V0 可用 | 3 hooks + 6 skills + 2 commands |
| OpenAI Codex | 🗓️ 路线图 | Skills 可复用；需要 Codex 的 hook 适配 |
| Cursor | 🗓️ 路线图 | Skills 可复用；需要 cursor-plugin manifest |
| Gemini CLI | 🗓️ 路线图 | Skills 和 activate_skill 机制兼容 |
| OpenCode | 🗓️ 路线图 | |

如果你在某平台想用 telos 但它不支持 hooks，**方法论本身仍可用**：把 `docs/methodology.md` 贴给它 + 复用 `skills/*/SKILL.md` 的提示词，就能跑对话循环，只是缺了自动记录 journal 和 SessionStart 注入。

---

## 不是 X，是 Y

telos 不是日程管理、不是心灵鸡汤、不是 Journaling app。它做一件事：**把"决策"变成一个有纪律的动作**。

| | Journaling apps (Day One) | Life coaches | Meditation apps (Calm) | **telos** |
|---|---|---|---|---|
| 有明确方向 | ❌ 你自己写流水账 | ✅ 但在教练脑里 | ❌ 无方向 | ✅ **声明在 profile.md** |
| 决策支持 | ❌ | ✅ 每周一次 | ❌ | ✅ **每次决策强制引用北极星** |
| 被动观察 | ❌ | ❌ | ❌ | ✅ **hooks 看你实际在做什么** |
| AI 参与程度 | 零 | 零 | 引导词 | **主导全流程** |
| 是否游戏化 | streak | - | 徽章 | **拒绝** |

其他产品的预设是"你不够自律"。telos 的预设是"你不够清晰——清晰了自律就不是问题"。

---

## 方法论的五层

把"人生导航"真正做好，比"写 todo list"要深得多。telos 在五层工作：

| 层次 | telos 做什么 | 其他产品通常做什么 |
|---|---|---|
| **声明** (declare) | 用你自己的话，≤ 300 字一段北极星 | journaling：让你每天写流水账 |
| **咨询** (consult) | 决策前**强制引用**原文 | 决策日记：让你"反思"（谁反思得动）|
| **记录** (log) | Stop hook 默默写，不打扰你 | todo app：让你填 checklist |
| **测量** (measure) | 一周一个数字 + 一句话 | wellness app：100 个伪指标 |
| **重校准** (recalibrate) | 承认"我变了"，深度重启（V1）| habit app：让你坚持原计划——哪怕方向错了 |

**每一层都有"不许做什么"**：声明层不许我帮你决定你是谁；咨询层不许我跳过引用直接给答案；记录层不许我读你的 journal；测量层不许我把 1-10 分变成排行榜；重校准层不许我把临时情绪当成长期漂移。

---

## 诚实边界

```
telos 做不到 ≠ telos 是坏产品。
一个不说自己做不到什么的工具，不值得信任。
```

- **LLM 会幻觉一个听起来深刻但并不是你的北极星。** profile.md 是你的纯文本，随时改。
- **北极星会 calcify。** 做大了的事、谈了新恋爱、换了城市——方向可能变了。定期 recalibrate。
- **demographic 偏差是真的。** telos 只对愿意装 Claude Code 的人 work，这是个小众群体，别以为它能救所有迷茫的人。
- **不能替代治疗。** 如果你在抑郁发作、躁狂、或有自伤意念，请找人，不是找机器。
- **不能替代人际关系。** 如果你有一位关系健康的导师/伴侣/治疗师，telos 是多余的，甚至可能抢走深度关系。
- **这是社会学实验，不是已证实的干预手段。** 假设是"外化方向 + 强制咨询"会改变主观意义感知，但**还没有数据证实**。第一份数据来自创建者本人 2 周自跑（`~/.claude/telos/weekly.md`）。

---

## 数据在哪

```
~/.claude/telos/           # 你的，永不离开你的机器
├── profile.md             # 北极星 + 命盘 + 价值观 + 十年图景 + 调整历史
├── journal/YYYY-MM-DD.md  # 每日的 [brief] / [session] / [reflect] / [weekly]
├── decisions/             # 每个重大决策一个文件，含事后 [outcome]
├── weekly.md              # 一行一周：分数 + 一句为什么
└── observations.jsonl     # 事件日志（无 prompt 内容、无 PII）
```

上传？不。云同步？不。模型训练？绝对不。

---

## 细读

- [`docs/methodology.md`](docs/methodology.md) — 五层方法论的完整说明
- [`docs/experiment.md`](docs/experiment.md) — 社会学实验框架、数据字典、匿名化承诺
- [`docs/superpowers/specs/2026-04-20-telos-design.md`](docs/superpowers/specs/2026-04-20-telos-design.md) — V0 架构 spec
- [`CLAUDE.md`](CLAUDE.md) — 插件系统指令（AI 看的那部分）

---

## 致谢

产品哲学大量借鉴 [obra/superpowers](https://github.com/obra/superpowers)——方法论不是工具箱、auto-trigger 不靠记命令、skills 之间有 hard-gate 和 hand-off。

README 的玩法借鉴 [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill)——demo-driven、"不是 X 是 Y" 对比、诚实边界独立成章。

telos 自己的贡献：**把这套方法论从"怎么做好代码"迁到"怎么做好人生"。**

---

## License

MIT. 代码你随便用。方法论你随便学。数据永远是你的。
