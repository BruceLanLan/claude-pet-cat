#!/usr/bin/env python3
"""
🐱 Claude Pet Cat - 可爱的虚拟宠物
参考 Claude Code 启动时的吉祥物形象
"""

import time
import random
import os
import json
import sys
from datetime import datetime, timedelta
from collections import deque

CAT_FILE = "my_cat.json"

# ANSI 颜色（参考 Claude 终端风格 - 温暖色调）
CLEAR_SCREEN = "\033[2J\033[H"
MOVE_HOME = "\033[H"

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    AMBER = "\033[38;5;214m"    # 琥珀色
    ORANGE = "\033[38;5;208m"   # 橙色
    CREAM = "\033[38;5;225m"    # 奶油色
    PEACH = "\033[38;5;223m"    # 桃色
    GRAY = "\033[90m"
    LIGHT = "\033[37m"


# ========== Claude 风格的猫咪 ASCII ==========
class CatArt:
    """参考 Claude 启动吉祥物的可爱猫咪"""

    # 主要姿势 - 参考 Claude 的猫头（更圆润可爱）
    HAPPY = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ◕   ◕  │
  │    ▼    │
  │   ╰‿╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ◕   ◕  │
  │    ▼    │
  │   ╰▿╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    LOVE = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ♥   ♥  │
  │    ▼    │
  │   ╰w╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ❤   ❤  │
  │    ▼    │
  │   ╰w╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    SLEEPY = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ─   ─  │
  │    ▼    │
  │   ╰z╯   │  z
   ╲▁▁▁▁▁▁▁╱  z
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  .   .  │
  │    ▼    │    Z
  │   ╰ ╯   │  Z
   ╲▁▁▁▁▁▁▁╱  Z
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    HUNGRY = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ◔   ◔  │
  │    ▼    │
  │   ╰o╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ·   ·  │
  │    ▼    │
  │   ╰O╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    PLAYFUL = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ^   ^  │
  │    ▼    │
  │   ╰w╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ◕   ◕  │
  │    ▼    │
  │   ╰>╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    CURIOUS = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ◔   ◕  │
  │    ▼    │
  │   ╰?╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ◕   ◕  │
  │    ▼    │
  │   ╰◡╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    BORED = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ─   ─  │
  │    ▼    │
  │   ╰~╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  .   .  │
  │    ▼    │
  │   ╰.╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    SAD = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ;   ;  │
  │    ▼    │
  │   ╰~╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  T   T  │
  │    ▼    │
  │   ╰.╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    NEUTRAL = [
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ◕   ◕  │
  │    ▼    │
  │   ╰‿╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
        r"""
    ╱▔╲ ╱▔╲
   ╱  ▔▔▔  ╲
  │  ─   ─  │
  │    ▼    │
  │   ╰‿╯   │
   ╲▁▁▁▁▁▁▁╱
    │ │  │ │
    ▀▀    ▀▀""",
    ]

    @classmethod
    def get(cls, mood, frame=0):
        art_dict = {
            "happy": cls.HAPPY,
            "excited": cls.HAPPY,
            "love": cls.LOVE,
            "content": cls.NEUTRAL,
            "playful": cls.PLAYFUL,
            "curious": cls.CURIOUS,
            "neutral": cls.NEUTRAL,
            "bored": cls.BORED,
            "lonely": cls.SAD,
            "sleepy": cls.SLEEPY,
            "hungry": cls.HUNGRY,
            "sad": cls.SAD,
            "shy": cls.HAPPY,
        }
        frames = art_dict.get(mood, cls.NEUTRAL)
        return frames[frame % len(frames)]


# ========== 性格系统 ==========
class Personality:
    PERSONALITIES = {
        "sweet": {"name": "甜心", "emoji": "💕"},
        "mischief": {"name": "调皮", "emoji": "😼"},
        "calm": {"name": "安静", "emoji": "😸"},
        "proud": {"name": "傲娇", "emoji": "😻"},
        "cuddly": {"name": "粘人", "emoji": "🥰"},
    }

    @classmethod
    def get_random(cls):
        return random.choice(list(cls.PERSONALITIES.keys()))


# ========== 情感系统 ==========
class Emotion:
    EMOTIONS = {
        "happy": {"emoji": "😊", "name": "开心"},
        "excited": {"emoji": "🎉", "name": "兴奋"},
        "love": {"emoji": "💕", "name": "爱意"},
        "content": {"emoji": "😌", "name": "满足"},
        "playful": {"emoji": "😸", "name": "顽皮"},
        "curious": {"emoji": "🔍", "name": "好奇"},
        "neutral": {"emoji": "😐", "name": "平静"},
        "bored": {"emoji": "😑", "name": "无聊"},
        "lonely": {"emoji": "💭", "name": "寂寞"},
        "sleepy": {"emoji": "😴", "name": "困倦"},
        "hungry": {"emoji": "🍽️", "name": "饥饿"},
        "sad": {"emoji": "😢", "name": "伤心"},
    }

    @classmethod
    def get_dominant(cls, happiness, hunger, energy):
        emotions = []

        if hunger < 20:
            emotions.append(("hungry", 100 - hunger))
        if energy < 15:
            emotions.append(("sleepy", 100 - energy))
        if happiness > 90:
            emotions.append(("love", happiness))
        elif happiness > 75:
            emotions.append(("excited", happiness))
        elif happiness > 60:
            emotions.append(("happy", happiness))
        elif happiness > 45:
            emotions.append(("content", happiness))
        elif happiness > 30:
            emotions.append(("neutral", 50))
        elif happiness > 20:
            emotions.append(("bored", 60 - happiness))
        else:
            emotions.append(("sad", 40 - happiness))

        emotions.sort(key=lambda x: x[1], reverse=True)
        return emotions[0][0] if emotions else "neutral"


# ========== 思想系统 ==========
class Thought:
    THOUGHTS = {
        "hungry": ["好饿好饿...", "想去厨房偷吃！", "铲屎官怎么还不喂我！"],
        "sleepy": ["好困啊...", "Zzz...", "让我休息一下～"],
        "bored": ["好无聊...", "没有人陪我玩...", "窗外有小鸟！"],
        "happy": ["今天超开心！", "阳光好温暖～", "喵～爱你哦！"],
        "love": ["好爱好爱你！", "想一直黏着你！", "你是对我最好的人！"],
        "sad": ["有点难过...", "你都不陪我...", "寂寞..."],
        "lonely": ["一个人好无聊...", "你在哪里呀？", "来陪我玩嘛～"],
        "curious": ["那个是什么？", "好像有声音？", "让我看看！"],
        "playful": ["来抓我呀！", "这个好好玩！", "再玩一次！"],
        "content": ["好舒服呀～", "这样就很好了", "晒晒太阳～"],
        "neutral": ["发发呆～", "我在想事情...", "喵～"],
        "excited": ["太棒了！！！", "好好玩！！！", "好开心！！！"],
    }

    @classmethod
    def generate(cls, mood):
        return random.choice(cls.THOUGHTS.get(mood, cls.THOUGHTS["neutral"]))


# ========== 记忆系统 ==========
class Memory:
    def __init__(self, max_size=8):
        self.memories = deque(maxlen=max_size)

    def add(self, event):
        timestamp = datetime.now().strftime("%H:%M")
        self.memories.append(f"[{timestamp}] {event}")

    def get_recent(self, n=3):
        return list(self.memories)[-n:]

    def to_list(self):
        return list(self.memories)

    @classmethod
    def from_list(cls, data, max_size=8):
        m = cls(max_size=max_size)
        m.memories = deque(data, maxlen=max_size)
        return m


# ========== 行为系统 ==========
class Behavior:
    BEHAVIORS = {
        "eat": {"name": "吃饭", "action": "大快朵颐 🍗", "hunger": 25, "happiness": 10, "memory": "吃了美味的猫粮"},
        "sleep": {"name": "睡觉", "action": "呼呼大睡 💤", "hunger": -8, "happiness": 8, "memory": "美美地睡了一觉"},
        "play": {"name": "玩耍", "action": "玩得不亦乐乎 🎾", "hunger": -8, "happiness": 20, "memory": "愉快地玩耍"},
        "explore": {"name": "探索", "action": "在四周探索 🔍", "hunger": -2, "happiness": 8, "memory": "发现了新东西"},
        "groom": {"name": "洗脸", "action": "认真洗脸 🐱", "hunger": -1, "happiness": 5, "memory": "把自己打理得干干净净"},
        "stretch": {"name": "伸懒腰", "action": "伸懒腰 🙀", "hunger": 0, "happiness": 3, "memory": "伸了个舒服的懒腰"},
        "meow": {"name": "喵喵叫", "action": "喵喵叫 🐱", "hunger": 0, "happiness": 2, "memory": "喵喵叫了几声"},
        "purr": {"name": "呼噜", "action": "打呼噜 💕", "hunger": 0, "happiness": 8, "memory": "舒服地打着呼噜"},
        "stare": {"name": "发呆", "action": "发呆 👀", "hunger": -1, "happiness": 0, "memory": "发了一会儿呆"},
        "cuddle": {"name": "求抱抱", "action": "要抱抱 🤗", "hunger": 0, "happiness": 12, "memory": "被抱着好幸福"},
    }

    @classmethod
    def decide(cls, pet):
        weights = []

        # 基于状态的权重
        if pet.hunger < 40:
            weights.append(("eat", 35))
        if pet.energy < 35:
            weights.append(("sleep", 35))
        if pet.happiness < 50 and pet.energy > 30:
            weights.append(("play", 20))

        # 随机行为
        for b in ["explore", "groom", "stretch", "meow", "purr", "stare", "cuddle"]:
            weights.append((b, 8))

        total = sum(w for _, w in weights)
        if total == 0:
            return "stare"

        r = random.random() * total
        cumulative = 0
        for b, w in weights:
            cumulative += w
            if r <= cumulative:
                return b
        return "stare"


# ========== 宠物类 ==========
class VirtualPet:
    def __init__(self, name="小咪", personality=None):
        self.name = name
        self.personality = personality or Personality.get_random()
        self.hunger = 70
        self.happiness = 70
        self.energy = 70
        self.love = 50
        self.mood = "happy"
        self.thought = "初来乍到～"
        self.memory = Memory()
        self.last_action = "初来乍到"
        self.born_time = datetime.now().isoformat()
        self.last_update = datetime.now().isoformat()
        self.cycles = 0  # 活跃周期数

    def get_age(self):
        """计算真实年龄"""
        born = datetime.fromisoformat(self.born_time)
        now = datetime.now()
        delta = now - born

        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60

        if days > 0:
            return f"{days}天{days*24+hours}小时"
        elif hours > 0:
            return f"{hours}小时{minutes}分钟"
        else:
            return f"{minutes}分钟"

    def save(self):
        data = {
            "name": self.name,
            "personality": self.personality,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "love": self.love,
            "mood": self.mood,
            "thought": self.thought,
            "memory": self.memory.to_list(),
            "last_action": self.last_action,
            "born_time": self.born_time,
            "last_update": datetime.now().isoformat(),
            "cycles": self.cycles,
        }
        with open(CAT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls):
        if os.path.exists(CAT_FILE):
            try:
                with open(CAT_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                pet = cls(data.get("name", "小咪"), data.get("personality"))
                pet.hunger = data.get("hunger", 70)
                pet.happiness = data.get("happiness", 70)
                pet.energy = data.get("energy", 70)
                pet.love = data.get("love", 50)
                pet.mood = data.get("mood", "happy")
                pet.thought = data.get("thought", "...")
                pet.memory = Memory.from_list(data.get("memory", []))
                pet.last_action = data.get("last_action", "...")
                pet.born_time = data.get("born_time", datetime.now().isoformat())
                pet.cycles = data.get("cycles", 0)
                return pet
            except:
                pass
        return cls()

    def update(self):
        self.cycles += 1

        behavior_id = Behavior.decide(self)
        behavior = Behavior.BEHAVIORS[behavior_id]

        self.hunger = max(0, min(100, self.hunger + behavior["hunger"]))
        self.happiness = max(0, min(100, self.happiness + behavior["happiness"]))
        self.energy = max(0, min(100, self.energy + (20 if behavior_id == "sleep" else -5)))

        # 爱意自然增长
        if random.random() < 0.05:
            self.love = min(100, self.love + 1)

        self.last_action = behavior["action"]
        self.mood = Emotion.get_dominant(self.happiness, self.hunger, self.energy)
        self.thought = Thought.generate(self.mood)
        self.memory.add(behavior["memory"])

        # 自然衰减
        self.hunger = max(0, self.hunger - 2)
        self.happiness = max(0, self.happiness - 1)

        self.last_update = datetime.now().isoformat()


# ========== 显示系统 ==========
def display(pet, frame=0):
    """在终端顶部显示小猫"""
    print(MOVE_HOME, end="")  # 移动到顶部

    # 获取猫咪图案
    cat_art = CatArt.get(pet.mood, frame)

    # 状态条
    def bar(value):
        filled = int(value / 10)
        return "█" * filled + "░" * (10 - filled)

    mood_info = Emotion.EMOTIONS.get(pet.mood, {})
    mood_emoji = mood_info.get("emoji", "😐")
    mood_name = mood_info.get("name", "平静")

    person_info = Personality.PERSONALITIES.get(pet.personality, {})
    person_emoji = person_info.get("emoji", "😺")

    # 参考 Claude 风格的简洁可爱界面
    print(f"{Colors.AMBER}{Colors.BOLD}╭─{Colors.RESET} {Colors.AMBER}🐱 {pet.name} {person_emoji}{person_info.get('name', '')} {Colors.GRAY}─{Colors.AMBER}╮{Colors.RESET}")

    # 猫咪
    for line in cat_art.split('\n'):
        print(f"{Colors.AMBER}│{Colors.RESET}   {line:25} {Colors.AMBER}│{Colors.RESET}")

    # 想法气泡
    print(f"{Colors.AMBER}├─{Colors.RESET} {Colors.CREAM}💭 {pet.thought:<25} {Colors.AMBER}│{Colors.RESET}")

    # 状态条
    print(f"{Colors.AMBER}├{Colors.RESET} 🍖 饱食 [{bar(pet.hunger)}] {pet.hunger:>3}%  {Colors.AMBER}│{Colors.RESET}")
    print(f"{Colors.AMBER}│{Colors.RESET} 💖 快乐 [{bar(pet.happiness)}] {pet.happiness:>3}%  {Colors.AMBER}│{Colors.RESET}")
    print(f"{Colors.AMBER}│{Colors.RESET} ⚡ 能量 [{bar(pet.energy)}] {pet.energy:>3}%  {Colors.AMBER}│{Colors.RESET}")
    print(f"{Colors.AMBER}│{Colors.RESET} ♥  爱意 [{bar(pet.love)}] {pet.love:>3}%  {Colors.AMBER}│{Colors.RESET}")

    # 当前动作和年龄
    age_str = pet.get_age()
    print(f"{Colors.AMBER}├─{Colors.RESET} 🐾 {pet.last_action:<20} {Colors.GRAY}│{Colors.AMBER} {pet.get_age()}{Colors.RESET}")
    print(f"{Colors.AMBER}╰─{Colors.GRAY}──────────────────────────────────{Colors.AMBER}─╯{Colors.RESET}")

    # 记忆
    memories = pet.memory.get_recent(2)
    if memories:
        print(f"{Colors.GRAY}  最近: {memories[0][:25]}{Colors.RESET}")

    # 时间
    now = datetime.now().strftime("%H:%M")
    print(f"{Colors.GRAY}{Colors.DIM}  {now} | Ctrl+C 退出{Colors.RESET}")

    sys.stdout.flush()


# ========== 主程序 ==========
def run_auto(interval=4):
    pet = VirtualPet.load()
    frame = 0

    # 打印初始状态在顶部
    print(CLEAR_SCREEN, end="")
    print(f"\n{Colors.AMBER}🐱 启动小咪！年龄: {pet.get_age()}{Colors.RESET}\n")

    try:
        while True:
            display(pet, frame)
            pet.update()
            pet.save()
            frame += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.AMBER}👋 再见！{pet.name} 会想你的～{Colors.RESET}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Claude Pet Cat")
    parser.add_argument("-a", "--auto", action="store_true", help="自动模式")
    parser.add_argument("-i", "--interval", type=int, default=4, help="间隔秒")
    parser.add_argument("-n", "--name", type=str, help="改名")
    args = parser.parse_args()

    pet = VirtualPet.load()

    if args.name:
        pet.name = args.name
        pet.save()
        print(f"🐱 改名为 {args.name}")

    if args.auto:
        run_auto(args.interval)
    else:
        display(pet)


if __name__ == "__main__":
    main()
