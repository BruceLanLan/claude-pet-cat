# Agent Harness 开发速查卡

> 六维框架 · 核心要点 · 关键数值 · 一页掌握

---

## 六维检查清单

### 1️⃣ Runtime（运行时）

| # | 检查项 | 备注 |
|---|--------|------|
| ☐ | PDAOL 循环（Perceive → Decide → Act → Observe → Loop） | 控制循环非问答 |
| ☐ | 不可变消息历史（只追加，不修改） | 压缩时生成摘要替换 |
| ☐ | Token 预算双维度（数量 + USD 成本） | 同时控成本和溢出 |
| ☐ | 优雅退出（85%警告 / 95%压缩 / 100%停止） | 分级触发 |
| ☐ | 流式事件架构（Generator yield） | 事件类型化 |
| ☐ | **二元反馈自愈**（两次执行比对，不一致则介入） | 新机制 |
| ☐ | 状态机模式（pending→running→completed/failed/killed） | 终态不可逆 |

### 2️⃣ Tools（工具系统）

| # | 检查项 | 备注 |
|---|--------|------|
| ☐ | 原子化接口（name/description/input_schema/execute） | 单一职责 |
| ☐ | 单一职责（不造大而全的工具） | AI 组合使用 |
| ☐ | **延迟加载**（defer_loading + Tool Search Tool） | 初始开销锐减 85% |
| ☐ | Token 路由打分（name/description/source_hint 匹配） | 精准命中 |
| ☐ | 工具执行结果标准化 | 统一格式 |
| ☐ | 编程化工具调用（模型写脚本→沙盒执行） | 防上下文溢出 |

### 3️⃣ Context（上下文）

| # | 检查项 | 备注 |
|---|--------|------|
| ☐ | 缓存友好结构（稳定区开头，最大化 KV cache） | 系统指令/工具定义在前 |
| ☐ | CLAUDE.md 支持（< 2000 chars） | 项目规范 |
| ☐ | git status 注入（截断 2000 chars） | 动态元素放后 |
| ☐ | 注入优先级（user-append > custom > project > default） | 明确层级 |
| ☐ | **MicroCompact**（正则本地清理，零 API 消耗） | 高容量输出清理 |
| ☐ | **AutoCompact**（LLM 92% 阈值触发，3 次断路器） | 摘要替换 |
| ☐ | **Full Compact**（摘要 + 重新注入活跃状态） | 极长对话 |

### 4️⃣ Memory（记忆）

| # | 检查项 | 备注 |
|---|--------|------|
| ☐ | L0: MEMORY.md 索引（< 200行 / 25KB） | 指向文件的指针 |
| ☐ | L1: 短期记忆（会话 / 日记） | memory/YYYY-MM-DD.md |
| ☐ | L2: 长期记忆（信念+置信度+矛盾检测） | SQLite |
| ☐ | L3: 归档记忆（ZIP 快照热插拔） | 跨环境迁移 |
| ☐ | 相关性加载（非全量，按任务匹配） | 节省 token |
| ☐ | **AutoDream 整理**（Orient→Gather→Consolidate→Prune） | 条件触发 |
| ☐ | 记忆写入原则（why 而非 what，带时间戳） | 不存可推导信息 |
| ☐ | 信念强化（访问后 +5%，上限 80%） | 频繁访问自动加强 |
| ☐ | 矛盾检测（涨/跌、买入/卖出 等对立词） | 近 N 天检测 |

### 5️⃣ Safety（安全）

| # | 检查项 | 备注 |
|---|--------|------|
| ☐ | Session Mode（default / acceptEdits / bypassPermissions / plan） | 全局基调 |
| ☐ | Tool Whitelist/Blacklist（settings.json / CLAUDE.md） | 配置驱动 |
| ☐ | Tool-Level（读工具自动 / 写工具确认） | 粒度分级 |
| ☐ | Operation-Level（rm -rf vs git status） | 同工具不同风险 |
| ☐ | Path/Command-Level（精确到目录/文件/命令） | 最细粒度 |
| ☐ | 信任门控（重量级操作延迟到 trust 确认后） | 插件/MCP/hooks |
| ☐ | **YOLO 自适应权限**（ML 分类器分析上下文连贯性） | 自动跳过审批 |

### 6️⃣ Evolution（进化）

| # | 检查项 | 备注 |
|---|--------|------|
| ☐ | 短反馈（每次任务后微调，保留 100 条） | 成功强化/失败记录 |
| ☐ | 长反馈（周/月大迭代，保留 12 期） | 战略性调整 |
| ☐ | A/B 测试框架（最少 10 样本，10% 差距判定） | 持续验证 |
| ☐ | 心跳机制（主动检查，批量合并减少 API） | email/日历/天气 |
| ☐ | 渐进复杂度（Level 1-4） | 自然语言→配置→MCP→多代理 |

---

## 关键数值

| 参数 | 值 | 说明 |
|------|-----|------|
| CLAUDE.md | < 2000 chars | 单文件限制 |
| git status | < 2000 chars | 截断限制 |
| MEMORY.md | < 200 行 / 25KB | 索引文件限制 |
| Token 警告 | 85% | 触发警告 |
| Token AutoCompact | 92% | LLM 压缩触发 |
| Token Full Compact | 95%+ | 极长对话 |
| 对话历史保留 | 10 条 | 压缩边界 |
| 信念置信度上限 | 80% | 防止过度自信 |
| 信念强化增量 | +5% | 每次访问 |
| 短反馈保留 | 100 条 | 最近 |
| 长反馈保留 | 12 期 | 最近 |
| A/B 测试最小样本 | 10 | 显著结论 |
| MicroCompact | 零 API 成本 | 正则清理 |
| Tool 延迟加载 | -85% 初始开销 | 3-5 个按需拉取 |
| AutoDream 触发 | ≥24h 离线 + ≥5 会话 | 后台自动整理 |

---

## 快速参考

### 记忆分层

```
L0: MEMORY.md —— 轻量索引（<200行/25KB），指向文件的指针，常驻内存
L1: 会话/日记 —— memory/YYYY-MM-DD.md，短期上下文
L2: 信念/决策/知识图谱 —— SQLite，置信度+证据追踪+矛盾检测
L3: ZIP 快照 —— 归档，可跨环境热插拔
```

### 上下文压缩三层

```
MicroCompact → 正则清理大文件输出（stdout/stderr 截断）
             → 零 API 消耗，本地完成

AutoCompact → 92% Token 阈值触发
            → LLM 生成摘要（保留决策/状态/偏好）
            → 3 次失败断路器

Full Compact → 极长对话触发
             → 摘要 + 重新注入活跃文件状态 + Plan
```

### AutoDream 四阶段

```
条件触发：离线空闲 + ≥24h + ≥5 会话

Orient（定向）→ 确定当前项目状态
Gather（收集）→ 收集相关记忆片段
Consolidate（合并）→ 纠错消重，消除矛盾
Prune（裁剪）→ 删除过时/低价值信息

输出：相对日期→绝对日期，矛盾→解决，长篇→摘要
```

### 权限五层

```
1. Session Mode —— 全局基调
   default / acceptEdits / bypassPermissions(⚠️) / plan

2. Tool Whitelist/Blacklist —— 配置级
   settings.json 或 CLAUDE.md

3. Tool-Level —— 工具级
   读 → 自动放行
   写/执行 → 需确认

4. Operation-Level —— 操作级
   同工具不同风险：rm -rf (高危) vs git status (低危)

5. Path/Command-Level —— 最细粒度
   特定目录/文件/命令的精确控制
```

### YOLO 自适应权限

```
原理：ML 分类器分析会话上下文连贯性

规则简化版：
  读操作 → 上下文连贯则自动放行
  写操作 → 首次确认，后续学习
  Shell 高危（rm -rf）→ 物理隔离 / 强制确认

实现：置信度阈值 + 历史行为学习
```

### Tool Search Tool 延迟加载

```
问题：50 个工具定义 = 77K tokens

解法：
  1. 大部分工具标记 defer_loading
  2. 只保留一个轻量 Tool Search Tool
  3. 需要时动态拉取 3-5 个最相关工具
  4. 初始开销锐减 85%

适用：MCP 服务器 / 插件系统
```

### 渐进复杂度 Level

```
Level 1: 自然语言 —— 新人，简单对话
Level 2: 配置驱动 —— power user，CLAUDE.md/settings.json
Level 3: MCP/Skills —— 开发者，扩展集成
Level 4: 多代理编排 —— 团队，Coordinator 模式
```

### 二元反馈自愈

```
同一请求执行两次 → 比对结果
  结果一致 → 置信度高，继续
  结果不一致 → 触发介入（反思/重试）

适用：代码执行、工具调用、外部 API
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
  + Tool(工具系统)

不是模型越大越强，
而是 Harness 越完善越强。
```

---

## 实现优先级

```
Phase 1（高价值·低复杂度）
  ☐ 相关性记忆加载
  ☐ Token 预算控制
  ☐ CLAUDE.md 支持
  ☐ 短反馈 + 长反馈

Phase 2（高价值·中复杂度）
  ☐ MicroCompact 正则压缩
  ☐ AutoCompact LLM 压缩
  ☐ Tool Search Tool 延迟加载
  ☐ Coordinator 多代理模式

Phase 3（高价值·高复杂度）
  ☐ AutoDream 后台整理
  ☐ YOLO 自适应权限
  ☐ Full Compact
  ☐ 二元反馈自愈
```

---

*基于 Claude Code 源码 + 设计指南 + 多方综合分析提炼 | 2026-04-01*
