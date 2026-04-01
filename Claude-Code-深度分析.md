# Claude Code 深度分析：让 AI Agent 更聪明

> 基于源码精读 + 设计指南 + Openclaw 现状，输出可落地的工程实践

---

## 目录

1. [Claude Code 的核心特点](#1-claude-code-的核心特点)
2. [让 Agent 更聪明、能连续迭代进化](#2-让-agent-更聪明能连续迭代进化)
3. [节省 Token、提高记忆长度与效率](#3-节省-token-提高记忆长度与效率)
4. [其他可抽离学习的设计](#4-其他可抽离学习的设计)

---

## 1. Claude Code 的核心特点

### 1.1 架构层面

| 特点 | 说明 | 对 Openclaw 的启发 |
|------|------|-------------------|
| **Harness 模式** | Claude Code 不是聊天机器人，而是一个 **Agent 运行时 Harness** | Openclaw 应定位为"AI 工作台"而非"聊天界面" |
| **工具优先** | 一切皆工具，原子化设计让 AI 组合使用 | 你的工具应该细粒度、可组合 |
| **五层权限架构** | 从 Session Mode 到 Path 级精细控制 | 安全是默认，不是可选 |
| **Context Engineering** | 上下文管理是核心工程挑战，不是 prompt 问题 | 需要系统化处理上下文 |
| **可观察性内置** | OpenTelemetry、成本追踪、诊断日志从一开始就有 | 观测性不能是后加的 |

### 1.2 运行时层面

```
PDAOL 循环: Perceive → Decide → Act → Observe → Loop
    ↓
Claude Code 的具体实现:
    - 多轮工具执行 (multi-turn tool execution)
    - 并行操作 (parallel operations)
    - 上下文累积 (context accumulation)
    - 自动终止 (automatic termination)
```

### 1.3 关键设计决策

1. **Trust-Gated Initialization**: 重量级操作（插件、MCP、session hooks）延迟到 trust 验证后
2. **不可变消息历史**: 消息只追加，从不修改，保证一致性
3. **Snapshot Mirror Pattern**: 用 JSON 快照记录原始接口，Python 层做干净室实现
4. **Token Budget 双维度**: 同时控制 token 数量和 USD 成本

---

## 2. 让 Agent 更聪明、能连续迭代进化

### 2.1 Openclaw 现有的好实践（需要强化）

#### ✅ 已有：MemoryVault 统一记忆引擎
```python
# 信念系统 + 置信度 + 证据追踪
beliefs: confidence, evidence_for, evidence_against, access_count

# 信念强化机制
boost_belief(belief_id, boost=0.05)  # 每次访问自动强化，上限 80%

# 矛盾检测
find_contradictions(days=3)  # 检测近 3 天相互矛盾的信念
```

#### ✅ 已有：BehaviorLoop 行为反馈闭环
```python
# 短反馈：每次任务后微调
short_feedback(task_id, task_type, actions, outcome, metrics)

# 长反馈：周期性大迭代（周/月）
long_feedback(period="weekly")

# A/B 测试
start_ab_test(test_id, task_type, variant_a, variant_b)
record_ab_result(test_id, variant, outcome)
```

#### ✅ 已有：AgentTeam + CEO 架构
```python
AgentRole: CEO, ANALYST, RESEARCHER, ENGINEER, EDITOR
智能分发: dispatch(task) → 按能力匹配 + 历史成功率排序
```

#### ✅ 已有：心跳机制（Heartbeat）
```python
# 主动检查：email, calendar, mentions, weather
# 批量合并减少 API 调用
# 状态追踪: heartbeat-state.json
```

### 2.2 需要新增的能力

#### 🔧 缺失 1：Context Compaction（上下文压缩）

Claude Code 的方案：
```
触发机制:
    - 85% token 使用率 → 警告
    - 95% token 使用率 → 强制压缩
    - API 返回 prompt_too_long → 反应式压缩

压缩算法:
    1. 在安全边界分割消息（保留最近 10 条）
    2. 用 AI 生成摘要
    3. 用简洁摘要替换详细历史

保留内容:
    ✅ 已完成的任务和结果
    ✅ 关键决策和推理
    ✅ 当前任务状态
    ✅ 重要代码变更
    ✅ 用户偏好和约束
    ❌ 细节过程被丢弃
```

**Openclaw 应该做的**：
```python
# 在 memory/vault.py 新增
def compact_conversation_history(self, keep_recent: int = 10) -> str:
    """
    压缩对话历史，返回 AI 生成的摘要。
    返回摘要字符串，调用方替换原始历史。
    """
    recent = self.query("conversations", limit=keep_recent)
    summary_prompt = f"""
    请摘要以下对话，保留关键信息：
    {json.dumps(recent, ensure_ascii=False)}

    摘要格式：
    - 关键决策：[列出]
    - 任务状态：[当前进度]
    - 用户偏好：[如有]
    """
    return ask(summary_prompt)  # 使用已有 LLM
```

#### 🔧 缺失 2：CLAUDE.md 式的项目上下文注入

Claude Code 通过 CLAUDE.md 实现：
```
多级层次:
    global → project → subdirectory → module

内容:
    - 技术栈
    - 目录结构
    - 代码规范
    - 常用命令
    - 重要约定

@ 语法引用外部文件
```

**Openclaw 应该做的**：
```python
# 在 workspace 新增 CLAUDE.md 支持
PROJECT_CONTEXT_FILE = "CLAUDE.md"

def load_project_context(project_root: Path) -> str:
    """加载项目级上下文说明文件"""
    claude_md = project_root / PROJECT_CONTEXT_FILE
    if claude_md.exists():
        return claude_md.read_text(encoding="utf-8")
    return ""

# 在每次任务执行前注入
def build_task_context(self, task: Dict) -> str:
    context_parts = []
    if self.project_context:
        context_parts.append(f"【项目上下文】\n{self.project_context}")
    if self.user_preferences:
        context_parts.append(f"【用户偏好】\n{self.user_preferences}")
    return "\n\n".join(context_parts)
```

#### 🔧 缺失 3：渐进式复杂度模型

Claude Code 的原则：
```
Level 1: 自然语言（新人用户）
Level 2: 配置项（power user）
Level 3: MCP 服务器（开发者）
Level 4: 多代理编排（团队）
```

**Openclaw 应该做的**：
```python
class ComplexityLevel(Enum):
    BASIC = 1      # 自然语言对话
    CONFIGURED = 2 # 配置驱动的行为
    EXTENDED = 3   # MCP/技能扩展
    ORCHESTRATED = 4  # 多代理团队

def get_required_complexity(task: Dict) -> ComplexityLevel:
    """分析任务需要的复杂度级别"""
    if task.get("sub_agents"):
        return ComplexityLevel.ORCHESTRATED
    if task.get("mcp_server"):
        return ComplexityLevel.EXTENDED
    if task.get("config"):
        return ComplexityLevel.CONFIGURED
    return ComplexityLevel.BASIC
```

#### 🔧 缺失 4：Coordinator 模式

Claude Code 的 Coordinator 负责任务分解和调度：
```python
# 协调者 vs 执行者
Coordinator:
    - 关注: 调度和分解
    - 工具: 主要是 AgentTool
    - 输出: 最终报告

Regular Agent:
    - 关注: 执行
    - 工具: 文件、Shell
    - 输出: 代码变更
```

**Openclaw 应该做的**：
```python
class Coordinator(Agent):
    """任务协调者：分解任务、调度子代理、整合结果"""

    def execute(self, task: Dict) -> TaskResult:
        # 1. 任务分析 + 分解
        subtasks = self.decompose(task)

        # 2. 并行调度到子代理
        results = [self.team.dispatch(st) for st in subtasks]

        # 3. 结果整合
        return self.integrate(results)
```

### 2.3 连续进化的机制设计

**Openclaw 现有的 BehaviorLoop 需要增强**：

```python
# 当前：手动触发
loop.short_feedback(...)
loop.long_feedback(period="weekly")

# 应该：自动触发 + 主动学习

class EvolutionEngine:
    """持续进化引擎"""

    def __init__(self, vault: MemoryVault):
        self.vault = vault
        self.strategy_memory = {}

    def on_task_complete(self, task: Dict, result: TaskResult):
        """任务完成时自动触发学习"""
        # 1. 提取成功模式
        if result.success:
            self._extract_success_pattern(task, result)
        else:
            self._analyze_failure(task, result)

        # 2. 更新策略建议
        self._update_strategy(task.get("type"))

        # 3. 触发 A/B 测试如果样本足够
        self._check_ab_significance(task.get("type"))

    def _extract_success_pattern(self, task, result):
        """提取成功的执行模式"""
        # 记录成功的 action 序列
        pattern = {
            "task_type": task.get("type"),
            "actions": task.get("actions", []),
            "outcome": "success",
            "confidence": result.data.get("confidence", 0.5) if result.data else 0.5
        }
        # 存储到 knowledge 表
        self.vault.add_knowledge(
            entity=f"success_pattern:{task.get('type')}",
            relation="achieved_by",
            target=str(pattern),
            weight=pattern["confidence"]
        )

    def _update_strategy(self, task_type: str):
        """基于历史反馈更新策略"""
        suggestion = self.vault.get_behavior_suggestion(task_type)
        if suggestion and suggestion.get("should_explore"):
            # 成功率低，建议探索备选方案
            self._trigger_exploration(task_type)
```

---

## 3. 节省 Token、提高记忆长度与效率

### 3.1 Claude Code 的 Token 优化策略

#### 策略 1：系统 Prompt 缓存优化

```
设计原则:
    稳定元素（核心指令、工具定义）放在开头
    → 最大化缓存命中率

动态元素（git status）放在后面
→ 每次请求变化，但占比小
```

**Openclaw 应该做的**：
```python
# 分离静态和动态上下文
STATIC_PROMPT = """[稳定不变的系统指令]"""

def build_prompt(dynamic_parts: List[str]) -> str:
    """
    动态构建 prompt，静态部分放开头以利用 LLM 的 KV cache
    """
    return STATIC_PROMPT + "\n\n" + "\n\n".join(dynamic_parts)
```

#### 策略 2：智能记忆加载

```
Claude Code:
    不是所有记忆每次都加载
    使用相关性搜索，只加载与当前任务相关的记忆

关键洞察:
    - 不要保存可推导的信息（代码结构、文件路径）
    - 要保存非显而易见的信息（团队约定、历史决策）
    - 记忆会过时，包含时间戳
    - 记忆捕获"为什么"而非"做了什么"
```

**Openclaw 应该做的**：
```python
# 当前实现：load all beliefs
def get_active_beliefs(self, category: str = ""):
    return self.query("beliefs", "status = 'active'", limit=50)

# 应该：基于任务相关性过滤
def get_relevant_beliefs(self, task_query: str, limit: int = 10) -> List[Dict]:
    """
    只加载与当前任务相关的信念

    1. 解析任务关键词
    2. 计算与信念的语义相关性
    3. 返回 top-N
    """
    all_beliefs = self.get_active_beliefs()
    task_tokens = set(task_query.lower().split())

    scored = []
    for belief in all_beliefs:
        belief_tokens = set(belief["text"].lower().split())
        overlap = task_tokens & belief_tokens
        if overlap:
            scored.append((len(overlap), belief))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [b for _, b in scored[:limit]]
```

#### 策略 3：对话历史压缩

```python
# 当前实现：TranscriptStore.compact() 简单截断
def compact(self, keep_last: int = 10):
    if len(self.entries) > keep_last:
        self.entries[:] = self.entries[-keep_last:]

# 应该：AI 生成的语义压缩
def semantic_compact(self, keep_recent: int = 5) -> str:
    """
    用 AI 生成摘要替代简单截断

    保留：关键决策、用户偏好、当前状态
    丢弃：详细过程、中间尝试
    """
    to_summarize = self.entries[:-keep_recent]
    summary = ask(
        f"请摘要以下对话，保留关键信息（决策、偏好、状态），丢弃过程细节：\n{to_summarize}",
        system="你是一个对话摘要专家，输出简洁的结构化摘要。"
    )
    return summary
```

#### 策略 4：Token 预算控制

```python
class TokenBudget:
    def __init__(self, max_tokens: int = 200000, warning_pct: float = 0.85):
        self.max_tokens = max_tokens
        self.warning_pct = warning_pct
        self.used_tokens = 0

    def estimate(self, text: str) -> int:
        """简单估算：中文按字符，英文按单词"""
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english_words = len([w for w in text.split() if w.isascii()])
        return int(chinese_chars * 1.5 + english_words)

    def check(self, new_text: str) -> str:
        """检查是否接近限额"""
        estimated = self.estimate(new_text)
        if self.used_tokens + estimated > self.max_tokens * self.warning_pct:
            return "warning"  # 触发压缩
        if self.used_tokens + estimated > self.max_tokens:
            return "stop"  # 停止追加
        return "ok"
```

### 3.2 记忆效率的具体数值参考

```
Claude Code 建议:
    CLAUDE.md: < 2000 characters
    git status: 截断至 2000 characters
    系统 prompt: ~10% token 预算
    用户上下文: ~20% token 预算
    对话历史: ~60% token 预算
    输出预算: ~10% token 预算
```

### 3.3 Openclaw 当前记忆的优化空间

```python
# 当前: query_conversation_history 简单关键词匹配
# 应该: 语义搜索

# 当前: beliefs 无优先级
# 应该: 访问频率加权 + 时间衰减

# 当前: 52K+ 行代码，结构清晰
# 但缺少: 主动压缩、相关性加载、Token 预算控制
```

---

## 4. 其他可抽离学习的设计

### 4.1 消息流式架构（Streaming）

```python
# Claude Code 的 SSE 流式设计
yield {'type': 'message_start', ...}
yield {'type': 'command_match', ...}
yield {'type': 'tool_match', ...}
yield {'type': 'permission_denial', ...}
yield {'type': 'message_delta', 'text': ...}
yield {'type': 'message_stop', ...}

# 优势:
# - 用户实时看到输出
# - 工具执行有进度反馈
# - 错误不会导致整次请求失败
```

**Openclaw 应该做的**：
```python
# 在 LLM 调用层支持流式
def stream_ask(prompt: str, system: str = "") -> Generator[str, None, None]:
    """流式返回 LLM 输出"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 工具执行也流式化
def stream_tool_execution(self, tool_calls: List[Dict]) -> Generator[Dict, None, None]:
    for tc in tool_calls:
        yield {'type': 'tool_start', 'tool': tc['name']}
        result = self.execute_tool(tc)
        yield {'type': 'tool_result', 'tool': tc['name'], 'result': result}
```

### 4.2 状态机模式（任务系统）

```python
# Claude Code 的任务状态机
pending → running → completed / failed / killed
                         ↑
                      终态（不可逆）

# Task ID 设计
前缀 (b=bash, a=agent, r=remote) + 8位 base-36 随机
→ 防枚举攻击
```

**Openclaw 应该做的**：
```python
class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"  # 终态

class Task:
    def __init__(self, task_id: str, task_type: str):
        self.task_id = task_id
        self.task_type = task_type
        self.state = TaskState.PENDING
        self.output_file: Optional[Path] = None
        self.created_at = datetime.now()

    def transition(self, new_state: TaskState):
        """状态转换，带终态保护"""
        if self.state in (TaskState.COMPLETED, TaskState.FAILED, TaskState.KILLED):
            raise InvalidStateTransition(f"终态不可转换: {self.state}")
        self.state = new_state

    def generate_id(prefix: str) -> str:
        """生成防枚举的 Task ID"""
        random_part = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=8))
        return f"{prefix}{random_part}"
```

### 4.3 可观察性内置

```python
# Claude Code: OpenTelemetry 集成
# Openclaw 已有: metrics 记录，但缺少:

# 1. 追踪（Trace）—— 请求级别的调用链
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("handle_task")
def handle_task(self, task: Dict):
    with span:
        result = self.execute(task)
        span.set_attribute("task.type", task.get("type"))
        span.set_attribute("task.success", result.success)
        return result

# 2. 结构化日志
import structlog
logger = structlog.get_logger()
logger.info("task_completed",
    task_id=task_id,
    duration_ms=duration,
    agent=agent_id
)

# 3. 成本追踪
self.vault.record_metric(
    "llm.cost_usd",
    cost,
    {"model": model, "task_type": task_type}
)
```

### 4.4 多代理通信模式

```python
# Claude Code: SendMessageTool 实现代理间直接通信
# Openclaw 已有: AgentTeam.dispatch()

# 应该增强：代理间消息传递
class AgentMessage:
    def __init__(self, from_agent: str, to_agent: str,
                 content: str, msg_type: str = "direct"):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.msg_type = msg_type
        self.timestamp = datetime.now()

    def send(self):
        """发送消息给目标代理"""
        self.team.deliver_message(self)

class AgentTeam:
    def deliver_message(self, msg: AgentMessage):
        """消息传递，异步非阻塞"""
        target = self.agents.get(msg.to_agent)
        if target:
            target.receive(msg)

    def broadcast(self, from_agent: str, content: str):
        """广播消息给所有代理"""
        for agent_id, agent in self.agents.items():
            if agent_id != from_agent:
                self.deliver_message(AgentMessage(from_agent, agent_id, content, "broadcast"))
```

### 4.5 渐进式信任模型

```python
# Claude Code: Trust-Gated Initialization
# Openclaw 可以借鉴：

class TrustLevel(Enum):
    UNTRUSTED = 0  # 仅读操作
    BASIC = 1      # 普通任务
    TRUSTED = 2    # 敏感操作（发邮件、删除）
    FULL = 3       # 系统级操作

    @classmethod
    def from_flags(cls, flags: Dict) -> 'TrustLevel':
        if flags.get("bypass_permissions"):
            return cls.FULL
        if flags.get("trusted"):
            return cls.TRUSTED
        if flags.get("basic"):
            return cls.BASIC
        return cls.UNTRUSTED

def requires_trust(operation: str, required: TrustLevel) -> bool:
    """检查操作需要的信任级别"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if self.trust_level.value < required.value:
                raise PermissionDenied(f"{operation} 需要 {required.name} 权限")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

@requires_trust("发送邮件", TrustLevel.TRUSTED)
def send_email(self, to: str, content: str):
    ...
```

### 4.6 为失败设计

```python
# Claude Code 的多层错误恢复
# Openclaw 应该增强：

class RetryStrategy:
    def __init__(self, max_retries: int = 3, backoff: str = "exponential"):
        self.max_retries = max_retries
        self.backoff = backoff  # exponential, linear, fixed

    def execute(self, func: Callable, *args, **kwargs):
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except RetryableError as e:
                last_error = e
                sleep_time = self._calc_sleep(attempt)
                time.sleep(sleep_time)
            except FatalError:
                raise  # 不重试

        raise MaxRetriesExceeded(last_error)

    def _calc_sleep(self, attempt: int) -> float:
        if self.backoff == "exponential":
            return min(2 ** attempt, 30)  # 最多 30 秒
        elif self.backoff == "linear":
            return attempt * 5
        return 10

# 错误分类
class RetryableError(Exception):
    """可重试错误：网络超时、API 限流、临时故障"""
    pass

class FatalError(Exception):
    """致命错误：权限不足、参数错误、逻辑错误"""
    pass

class DegradeableError(Exception):
    """可降级错误：非核心功能失败，降级处理"""
    pass
```

---

## 5. 落地建议：Openclaw 改进优先级

### 第一阶段（高价值、低复杂度）

```
1. ✅ 增强 MemoryVault.get_relevant_beliefs()  — 相关性加载
2. ✅ 实现 TokenBudget 类 — Token 预算控制
3. ✅ 增强 BehaviorLoop — 主动触发 + 自动学习
4. ✅ 添加项目上下文注入 (CLAUDE.md) — Context Engineering
```

### 第二阶段（高价值、中等复杂度）

```
5. 🔧 Context Compaction — AI 生成的语义压缩
6. 🔧 流式输出支持 — Streaming 架构
7. 🔧 任务状态机 + Task ID 防枚举
8. 🔧 Coordinator 模式 — 多代理协调
```

### 第三阶段（长期价值）

```
9. 🏗️ OpenTelemetry 集成 — 可观察性
10. 🏗️ 多代理消息传递机制
11. 🏗️ 渐进式信任模型
12. 🏗️ 结构化错误恢复策略
```

---

## 6. 关键设计哲学总结

| Claude Code 设计原则 | Openclaw 实践 |
|---------------------|---------------|
| **透明性优于便利** | 所有操作记录到 vault，错误不静默 |
| **安全是默认** | 需要 trust 标志才执行敏感操作 |
| **单一职责** | Agent 角色分离，工具原子化 |
| **显式优于隐式** | Context Engineering 系统化 |
| **为失败设计** | RetryStrategy + 错误分类 |
| **可观察性一等公民** | metrics + 结构化日志 |
| **渐进复杂性** | TrustLevel 渐进信任 |
| **智能遗忘** | Context Compaction 选择性丢弃 |

---

## 参考

- **源码精读**: [BruceLanLan/claw-code](https://github.com/BruceLanLan/claw-code)
- **设计指南**: [6551Team/claude-code-design-guide](https://github.com/6551Team/claude-code-design-guide)
- **Openclaw**: `/Users/bruce/openclaw-optimized/`
