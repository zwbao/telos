# Telos 社会学实验框架

## 假设（松散陈述）

"把人生方向外部化成一段声明，并强制在决策点引用它，会改变人对主观意义的感知吗？"

不预设方向。可能是正向（主观意义↑）、负向（感觉像被算法囚禁）、或无显著变化。

## 数据

### 观察日志 `~/.claude/telos/observations.jsonl`

每行一个 JSON 事件。字段：

| 字段 | 类型 | 含义 |
|---|---|---|
| `ts` | ISO 8601 UTC | 事件时间戳 |
| `mode` | string | 事件类型（见下表）|
| 其他 | - | 随事件类型变化的元数据 |

事件类型 `mode`：
- `hook_session_start` — CC session 开始
- `hook_prompt_submit` — 用户提交 prompt（含 `matched`, `is_decision`, `prompt_len`）
- `hook_stop` — CC session 结束（含 `message_count`, `summary_chars`）
- `hook_error` — hook 自身出错（含 `hook`, `error`）
- （V1 扩展更多 skill 调用事件）

### 周度分数 `~/.claude/telos/weekly.md`

一行一周：`YYYY-MM-DD | score/10 | one-sentence reason`

### 决策库 `~/.claude/telos/decisions/`

每个重大决策一个 markdown 文件，含：问题、北极星引用、选项枚举、推荐、理由、（事后）outcome。

### 日志 `~/.claude/telos/journal/*.md`

自由文本，对外永不聚合。

## 匿名化协议（V2+ 如果对外聚合）

上报时只保留：
- `observations.jsonl`（无 PII — 本身就没有 prompt 内容）
- `weekly.md` 的分数列（去掉 reason 句子）
- 决策的**结构**（选项数量、alignment 分布），不含具体内容

永不上报：profile.md、journal、decisions 正文。

## 知情同意

V0：只有创建者自己用，无需同意。
V1：如果分发给朋友，`docs/CONSENT.md` 写明数据策略。
V2：若扩到 ≥ 10 用户，IRB 或等效审查。

## 明确不测

- 个性变化（MBTI 漂移）
- 生产力（完成任务数）
- 收入变化
- 关系变化
- 临床心理指标（PHQ-9, GAD-7 等）—— 这需要真正的临床设置

## Claimed vs Observed

主观意义分（用户自评）和行为模式（observations + decisions alignment）是两个独立信号。不做因果推断。两个信号的相关性本身就是有价值的观察。
