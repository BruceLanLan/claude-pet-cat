# Agent Harness 开发速查卡

> 六维框架 · 核心要点 · 关键数值 · 一页掌握

---

## 六维检查清单

### 1️⃣ Runtime（运行时）

| 检查项 | 状态 |
|--------|------|
| PDAOL 循环（Perceive → Decide → Act → Observe → Loop） | ☐ |
| 不可变消息历史（只追加，不修改） | ☐ |
| Token 预算双维度（数量 + USD 成本） | ☐ |
| 优雅退出（85%警告 / 95%压缩 / 100%停止） | ☐ |
| 流式事件架构（Generator yield） | ☐ |
| 二元反馈自愈（两次执行比对） | ☐ |

### 2️⃣ Tools（工具系统）

| 检查项 | 状态 |
|--------|------|
| 原子化接口（name/description/input_schema/execute） | ☐ |
| 单一职责（不造大而全的工具） | ☐ |
| 延迟加载（defer_loading + Tool Search Tool） | ☐ |
| Token 路由打分（name/description/source_hint 匹配） | ☐ |
| 工具执行结果标准化 | ☐ |

### 3️⃣ Context（上下文）

| 检查项 | 状态 |
|--------|------|
| 缓存友好结构（稳定区开头） | ☐ |
| CLAUDE.md 支持（< 2000 chars） | ☐ |
| git status 注入（截断 2000 chars） | ☐ |
| 注入优先级（user-append > custom > project > default） | ☐ |
| 三层压缩（Micro/Auto/Full） | ☐ |

### 4️⃣ Memory（记忆）

| 检查项 | 状态 |
|--------|------|
| L0: MEMORY.md 索引（< 200行/25KB） | ☐ |
| L1: 短期记忆（会话/日记） | ☐ |
| L2: 长期记忆（信念+置信度+矛盾检测） | ☐ |
| L3: 归档记忆（ZIP 快照热插拔） | ☐ |
| 相关性加载（非全量） | ☐ |
| AutoDream 整理（Orient→Gather→Consolidate→Prune） | ☐ |
| 记忆写入原则（why 而非 what，带时间戳） | ☐ |

### 5️⃣ Safety（安全）

| 检查项 | 状态 |
|--------|------|
| 五层权限（Session Mode → Path 级） | ☐ |
| 信任门控（重量级操作延迟到 trust 确认） | ☐ |
| 高危操作确认（rm -rf 类强制确认） | ☐ |
| YOLO 自适应权限（ML 分类器跳过审批） | ☐ |

### 6️⃣ Evolution（进化）

| 检查项 | 状态 |
|--------|------|
| 短反馈（每次任务后微调，保留 100 条） | ☐ |
| 长反馈（周/月大迭代，保留 12 期） | ☐ |
| A/B 测试框架（最少 10 样本） | ☐ |
| 心跳机制（主动检查，批量合并） | ☐ |
| 渐进复杂度（Level 1-4） | ☐ |

---

## 关键数值

| 参数 | 值 |
|------|-----|
| CLAUDE.md | < 2000 chars |
| git status | < 2000 chars |
| MEMORY.md | < 200 行 / 25KB |
| Token 警告 | 85% |
| Token 压缩 | 95% |
| 对话历史保留 | 10 条（压缩边界） |
| 信念置信度上限 | 80% |
| 信念强化增量 | +5% / 访问 |
| 短反馈保留 | 100 条 |
| 长反馈保留 | 12 期 |
| A/B 测试最小样本 | 10 |
| 记忆强化上限 | 80% |
| MicroCompact | 零 API 成本 |
| AutoCompact | 92% 阈值触发 |

---

## 快速参考

### 记忆分层

```
L0: MEMORY.md（索引，指针）
L1: 会话/日记（短期）
L2: 信念/决策/知识图谱（长期）
L3: ZIP 快照（归档，可热插拔）
```

### 权限五层

```
1. Session Mode（全局基调）
2. Tool Whitelist/Blacklist
3. Tool-Level（读放行/写确认）
4. Operation-Level（rm -rf vs git status）
5. Path/Command-Level（精确控制）
```

### 三层压缩

```
MicroCompact → 正则本地清理（零成本）
AutoCompact → LLM 92% 阈值（API 成本）
Full Compact → 摘要 + 重新注入（高成本）
```

### AutoDream 四阶段

```
Orient（定向）→ Gather（收集）→ Consolidate（合并纠错）→ Prune（裁剪）
触发：≥24h 离线空闲 + ≥5 会话
```

### 渐进复杂度

```
Level 1: 自然语言（新人）
Level 2: 配置驱动（power user）
Level 3: MCP/Skills（开发者）
Level 4: 多代理编排（团队）
```

---

## 核心公式

```
Agent 壁垒 =
  Harness(工程化约束)
  + Context(上下文管理)
  + Memory(记忆工程)
  + Safety(安全默认)
  + Evolution(持续进化)

不是模型越大越强，而是 Harness 越完善越强。
```

---

*基于 Claude Code 源码 + 设计指南 + 综合分析提炼 | 2026-04-01*
