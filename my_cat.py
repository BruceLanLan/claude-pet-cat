#!/usr/bin/env python3
"""
超级可爱的虚拟宠物猫 - Claude的陪伴
"""

import time
import random
import os
import json
import sys
from datetime import datetime
from collections import deque

CAT_FILE = "my_cat.json"

# ANSI 颜色代码
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

CLEAR_SCREEN = "\033[2J\033[H"

# ========== 性格系统 ==========
class Personality:
    """猫咪性格系统"""
    PERSONALITIES = {
        "sweet": {
            "name": "甜心",
            "emoji": "💕",
            "greeting": ["喵呜～", "蹭蹭你～", "欢迎回来！"],
            "traits": ["粘人", "温柔", "爱撒娇"],
        },
        "mischief": {
            "name": "调皮",
            "emoji": "😼",
            "greeting": ["嘿嘿～", "我又搞破坏了！", "快来抓我！"],
            "traits": ["好奇", "贪玩", "捣蛋"],
        },
        "calm": {
            "name": "安静",
            "emoji": "😸",
            "greeting": ["...喵", "轻点声～", "我在休息"],
            "traits": ["稳重", "慵懒", "优雅"],
        },
        "proud": {
            "name": "傲娇",
            "emoji": "😻",
            "greeting": ["哼～", "勉强让你摸一下", "本喵允许你靠近"],
            "traits": ["傲娇", "可爱", "嘴硬"],
        },
        "cuddly": {
            "name": "粘人精",
            "emoji": "🥰",
            "greeting": ["要抱抱！", "不要离开我～", "陪我玩嘛～"],
            "traits": ["粘人", "依赖", "需要关注"],
        },
    }

    @classmethod
    def get_random(cls):
        return random.choice(list(cls.PERSONALITIES.keys()))


# ========== 情感系统 ==========
class Emotion:
    EMOTIONS = {
        "happy": {"emoji": "😊", "name": "开心", "color": Colors.GREEN},
        "excited": {"emoji": "🎉", "name": "兴奋", "color": Colors.YELLOW},
        "love": {"emoji": "💕", "name": "爱意", "color": Colors.MAGENTA},
        "content": {"emoji": "😌", "name": "满足", "color": Colors.CYAN},
        "playful": {"emoji": "😸", "name": "顽皮", "color": Colors.BLUE},
        "curious": {"emoji": "🔍", "name": "好奇", "color": Colors.CYAN},
        "neutral": {"emoji": "😐", "name": "平静", "color": Colors.WHITE},
        "bored": {"emoji": "😑", "name": "无聊", "color": Colors.GRAY},
        "lonely": {"emoji": "💭", "name": "寂寞", "color": Colors.BLUE},
        "sleepy": {"emoji": "😴", "name": "困倦", "color": Colors.BLUE},
        "hungry": {"emoji": "🍽️", "name": "饥饿", "color": Colors.YELLOW},
        "sad": {"emoji": "😢", "name": "伤心", "color": Colors.BLUE},
        "angry": {"emoji": "😾", "name": "生气", "color": Colors.RED},
        "shy": {"emoji": "😳", "name": "害羞", "color": Colors.MAGENTA},
    }

    @classmethod
    def get_dominant(cls, happiness, hunger, energy, personality):
        emotions = []

        # 基础情感
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

        # 基于性格的随机情感
        if personality == "sweet" and random.random() < 0.3:
            emotions.append(("love", 80))
        elif personality == "mischief" and random.random() < 0.3:
            emotions.append(("playful", 70))
        elif personality == "proud" and random.random() < 0.3:
            emotions.append(("happy", 65))
        elif personality == "cuddly" and random.random() < 0.3:
            emotions.append(("love", 85))

        emotions.sort(key=lambda x: x[1], reverse=True)
        return emotions[0][0] if emotions else "neutral"


# ========== 可爱猫咪 ASCII ==========
class CatArt:
    """各种可爱的猫咪姿势"""

    # 开心/兴奋
    HAPPY = [
        r"""
     /\_/\
    ( ^.^ )
     > w <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    ( ^▽^ )
     > ω <
    /|   |\
   (_|   |_)""",
    ]

    # 超开心/爱
    LOVE = [
        r"""
     /\_/\
    ( ♥.♥ )
     > ~ <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    (灬♥ω♥灬)
     > ω <
    /|   |\
   (_|   |_)""",
    ]

    # 困倦
    SLEEPY = [
        r"""
     /\_/\
    ( -.- )
    (  z  )
    /|    |\
   (_|    |_)""",
        r"""
     /\_/\
    ( ｚ.ｚ)
    ( --- )
    /|    |\
   (_|    |_)""",
    ]

    # 饥饿
    HUNGRY = [
        r"""
     /\_/\
    ( @.@ )
     > o <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    ( ·.· )
     > O <
    /|   |\
   (_|   |_)""",
    ]

    # 调皮/玩耍
    PLAYFUL = [
        r"""
     /\_/\
    ( ^o^ )
    /  @  \
   /|  ~  |\
  (_|     |_)""",
        r"""
     /\_/\
    ( ⊙.⊙ )
    /  >  \
   /|  ⋀  |\
  (_|  ~  |_)""",
    ]

    # 好奇
    CURIOUS = [
        r"""
     /\_/\
    ( o.O )
     > ? <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    ( ◕.◕ )
     > ◡ <
    /|   |\
   (_|   |_)""",
    ]

    # 无聊
    BORED = [
        r"""
     /\_/\
    ( -_- )
     > ~ <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    ( ._. )
     > . <
    /|   |\
   (_|   |_)""",
    ]

    # 伤心
    SAD = [
        r"""
     /\_/\
    ( ;.; )
     > ~ <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    (T.T)
     > . <
    /|   |\
   (_|   |_)""",
    ]

    # 傲娇
    PROUD = [
        r"""
     /\_/\
    ( -.^)
     > - <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    ( ¬.¬)
     > 3 <
    /|   |\
   (_|   |_)""",
    ]

    # 害羞
    SHY = [
        r"""
     /\_/\
    ( ^_^ )
     > /// <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    ( ◕‿◕)
     > ▼ <
    /|   |\
   (_|   |_)""",
    ]

    # 平静
    NEUTRAL = [
        r"""
     /\_/\
    ( o.o )
     > - <
    /|   |\
   (_|   |_)""",
        r"""
     /\_/\
    ( -.- )
     > . <
    /|   |\
   (_|   |_)""",
    ]

    @classmethod
    def get(cls, emotion, frame=0):
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
            "angry": cls.PROUD,
            "shy": cls.SHY,
        }
        frames = art_dict.get(emotion, cls.NEUTRAL)
        return frames[frame % len(frames)]


# ========== 思想系统 ==========
class Thought:
    THOUGHTS = {
        "hungry": [
            "好饿好饿...有没有吃的？",
            "肚子咕咕叫了...",
            "想去厨房偷吃！",
            "铲屎官怎么还不喂我！",
        ],
        "sleepy": [
            "好困啊...想睡觉...",
            "打哈欠...Zzz...",
            "找个舒服的地方躺下",
            "让我休息一下～",
        ],
        "bored": [
            "好无聊啊...",
            "没有人陪我玩...",
            "好想找点乐子！",
            "窗外有小鸟！",
        ],
        "happy": [
            "今天超开心！",
            "阳光好温暖～",
            "我是世界上最幸福的猫！",
            "喵～爱你哦！",
        ],
        "love": [
            "好爱好爱铲屎官！",
            "想一直黏着你！",
            "你是对我最好的人！",
            "蹭蹭～",
        ],
        "sad": [
            "有点难过...",
            "你都不陪我...",
            "感觉有点寂寞...",
        ],
        "lonely": [
            "一个人好无聊...",
            "你在哪里呀？",
            "来陪我玩嘛～",
        ],
        "curious": [
            "那个是什么？",
            "好像有声音？",
            "让我看看！",
        ],
        "playful": [
            "来抓我呀！",
            "这个好好玩！",
            "再玩一次！",
        ],
        "content": [
            "好舒服呀～",
            "这样就很好了",
            "晒晒太阳～",
        ],
        "neutral": [
            "发发呆～",
            "我在想事情...",
            "喵～",
        ],
        "excited": [
            "太棒了！！！",
            "好好玩！！！",
            "我好开心！！！",
        ],
        "shy": [
            "哎呀...好害羞...",
            "不要一直看着我...",
            "脸红红的...",
        ],
        "proud": [
            "哼，本喵最可爱！",
            "你应该感到荣幸！",
            "这只是碰巧而已！",
        ],
    }

    @classmethod
    def generate(cls, emotion, memories, hunger, energy, happiness):
        thought_pool = cls.THOUGHTS.get(emotion, cls.THOUGHTS["neutral"])

        # 记忆影响
        if memories:
            recent = memories[-1]
            if "吃饭" in recent or "喂" in recent:
                if hunger < 50:
                    thought_pool = cls.THOUGHTS["hungry"]
            if "睡觉" in recent:
                if energy < 40:
                    thought_pool = cls.THOUGHTS["sleepy"]
            if "玩耍" in recent or "陪你" in recent:
                if happiness < 50:
                    thought_pool = cls.THOUGHTS["bored"]

        return random.choice(thought_pool)


# ========== 记忆系统 ==========
class Memory:
    def __init__(self, max_size=10):
        self.memories = deque(maxlen=max_size)

    def add(self, event):
        timestamp = datetime.now().strftime("%H:%M")
        self.memories.append(f"[{timestamp}] {event}")

    def get_recent(self, n=5):
        return list(self.memories)[-n:]

    def to_list(self):
        return list(self.memories)

    @classmethod
    def from_list(cls, data, max_size=10):
        m = cls(max_size=max_size)
        m.memories = deque(data, maxlen=max_size)
        return m


# ========== 行为系统 ==========
class Behavior:
    BEHAVIORS = {
        "eat": {
            "name": "吃饭",
            "action": "正在大快朵颐 🍗",
            "hunger_change": 30,
            "happiness_change": 15,
            "energy_change": 5,
            "memory": "吃了美味的猫粮",
            "weight": lambda p: 35 if p.hunger < 50 else 5,
        },
        "sleep": {
            "name": "睡觉",
            "action": "正在呼呼大睡 💤",
            "hunger_change": -10,
            "happiness_change": 10,
            "energy_change": 50,
            "memory": "美美地睡了一觉",
            "weight": lambda p: 40 if p.energy < 35 else 5,
        },
        "play": {
            "name": "玩耍",
            "action": "玩得不亦乐乎 🎾",
            "hunger_change": -10,
            "happiness_change": 25,
            "energy_change": -20,
            "memory": "愉快地玩耍",
            "weight": lambda p: 25 if p.happiness < 60 and p.energy > 30 else 3,
        },
        "explore": {
            "name": "探索",
            "action": "在四周探索 🔍",
            "hunger_change": -3,
            "happiness_change": 10,
            "energy_change": -5,
            "memory": "发现了新东西",
            "weight": lambda p: 15 if p.energy > 40 else 2,
        },
        "groom": {
            "name": "洗脸",
            "action": "认真给自己洗脸 🐱",
            "hunger_change": -2,
            "happiness_change": 8,
            "energy_change": 3,
            "memory": "把自己打理得干干净净",
            "weight": lambda p: 10,
        },
        "stretch": {
            "name": "伸懒腰",
            "action": "舒服地伸懒腰 🙀",
            "hunger_change": -1,
            "happiness_change": 5,
            "energy_change": 10,
            "memory": "伸了个舒服的懒腰",
            "weight": lambda p: 12 if p.energy < 60 else 4,
        },
        "meow": {
            "name": "喵喵叫",
            "action": "喵喵叫 🐱",
            "hunger_change": 0,
            "happiness_change": 3,
            "energy_change": 0,
            "memory": "喵喵叫了几声",
            "weight": lambda p: 8,
        },
        "purr": {
            "name": "呼噜",
            "action": "舒服地打呼噜 💕",
            "hunger_change": 0,
            "happiness_change": 10,
            "energy_change": 2,
            "memory": "舒服地打着呼噜",
            "weight": lambda p: 10 if p.happiness > 40 else 2,
        },
        "stare": {
            "name": "发呆",
            "action": "望着远处发呆 👀",
            "hunger_change": -2,
            "happiness_change": 0,
            "energy_change": 3,
            "memory": "发了一会儿呆",
            "weight": lambda p: 6 if p.happiness > 50 else 2,
        },
        "cuddle": {
            "name": "求抱抱",
            "action": "要抱抱 🤗",
            "hunger_change": 0,
            "happiness_change": 15,
            "energy_change": 0,
            "memory": "被抱着好幸福",
            "weight": lambda p: 8 if p.personality in ["sweet", "cuddly"] else 2,
        },
        "hunt": {
            "name": "捕猎",
            "action": "在捕捉猎物 🐭",
            "hunger_change": -5,
            "happiness_change": 12,
            "energy_change": -10,
            "memory": "练习捕猎技巧",
            "weight": lambda p: 10 if p.personality == "mischief" else 3,
        },
    }

    @classmethod
    def decide(cls, pet):
        weights = []
        for behavior_id, behavior in cls.BEHAVIORS.items():
            weight = behavior["weight"](pet)
            weights.append((behavior_id, weight))

        total = sum(w for _, w in weights)
        if total == 0:
            return "stare"

        r = random.random() * total
        cumulative = 0
        for behavior_id, weight in weights:
            cumulative += weight
            if r <= cumulative:
                return behavior_id

        return "stare"


# ========== 宠物类 ==========
class VirtualPet:
    def __init__(self, name="小咪", personality=None):
        self.name = name
        self.personality = personality or Personality.get_random()
        self.hunger = 70
        self.happiness = 70
        self.energy = 70
        self.mood = "happy"
        self.thought = "初来乍到～"
        self.memory = Memory()
        self.last_action = "初来乍到"
        self.born_time = datetime.now().isoformat()
        self.last_update = datetime.now().isoformat()
        self.age = 0
        self.love = 50  # 对主人的爱意

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
            "age": self.age,
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
                pet.age = data.get("age", 0)
                return pet
            except:
                pass
        return cls()

    def update(self):
        self.age += 1

        behavior_id = Behavior.decide(self)
        behavior = Behavior.BEHAVIORS[behavior_id]

        self.hunger = max(0, min(100, self.hunger + behavior["hunger_change"]))
        self.happiness = max(0, min(100, self.happiness + behavior["happiness_change"]))
        self.energy = max(0, min(100, self.energy + behavior["energy_change"]))

        # 爱意自然增长
        if random.random() < 0.1:
            self.love = min(100, self.love + 1)

        self.last_action = behavior["action"]
        self.mood = Emotion.get_dominant(self.happiness, self.hunger, self.energy, self.personality)
        self.thought = Thought.generate(self.mood, self.memory.to_list(), self.hunger, self.energy, self.happiness)
        self.memory.add(behavior["memory"])

        # 自然衰减
        self.hunger = max(0, self.hunger - 3)
        self.happiness = max(0, self.happiness - 2)
        self.energy = min(100, self.energy + 5)

        self.last_update = datetime.now().isoformat()


# ========== 可视化显示 ==========
def display(pet, frame=0):
    print(CLEAR_SCREEN, end="")

    # 获取猫咪图案
    cat_art = CatArt.get(pet.mood, frame)

    # 状态条
    hunger_bar = "█" * (pet.hunger // 10) + "░" * (10 - pet.hunger // 10)
    happy_bar = "█" * (pet.happiness // 10) + "░" * (10 - pet.happiness // 10)
    energy_bar = "█" * (pet.energy // 10) + "░" * (10 - pet.energy // 10)
    love_bar = "█" * (pet.love // 10) + "░" * (10 - pet.love // 10)

    mood_info = Emotion.EMOTIONS.get(pet.mood, {})
    mood_emoji = mood_info.get("emoji", "😐")
    mood_name = mood_info.get("name", "平静")

    personality_info = Personality.PERSONALITIES.get(pet.personality, {})
    person_emoji = personality_info.get("emoji", "😺")
    person_name = personality_info.get("name", "普通")

    # 装饰边框
    print(f"{Colors.CYAN}╔{'═' * 56}╗{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} 🐱 {Colors.YELLOW}{pet.name}{Colors.RESET} {person_emoji}{person_name} "
          f"   {Colors.MAGENTA}♥爱意: {pet.love}%{Colors.RESET}          "
          f"{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} 年龄: {pet.age:>4}  情感: {mood_emoji}{mood_name}                    "
          f"{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╠{'═' * 56}╣{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET}")
    for line in cat_art.split('\n'):
        print(f"{Colors.CYAN}║{Colors.RESET}  {line:50} {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╠{'═' * 56}╣{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} {Colors.YELLOW}💭 {pet.thought:<50} {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╠{'═' * 56}╣{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} {Colors.GREEN}🍖 饱食: [{hunger_bar}] {pet.hunger:>3}%{'':<20} {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} {Colors.YELLOW}💖 快乐: [{happy_bar}] {pet.happiness:>3}%{'':<20} {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} {Colors.BLUE}⚡ 能量: [{energy_bar}] {pet.energy:>3}%{'':<20} {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} {Colors.MAGENTA}♥ 爱意: [{love_bar}] {pet.love:>3}%{'':<20} {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╠{'═' * 56}╣{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} {Colors.WHITE}🐾 正在: {pet.last_action:<40} {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╠{'═' * 56}╣{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.RESET} {Colors.GRAY}📝 最近记忆:{Colors.RESET}")
    for mem in pet.memory.get_recent(3):
        print(f"{Colors.CYAN}║{Colors.RESET}    {Colors.GRAY}{mem:<50} {Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╚{'═' * 56}╝{Colors.RESET}")

    now = datetime.now().strftime("%H:%M:%S")
    print(f"\n{Colors.GRAY}⏰ {now}  |  按 Ctrl+C 退出{Colors.RESET}")

    sys.stdout.flush()


# ========== 主程序 ==========
def run_auto(interval=4):
    pet = VirtualPet.load()
    frame = 0

    print(f"{Colors.CYAN}🐱 启动超级可爱的虚拟宠物！{pet.name} 来啦～{Colors.RESET}")
    p_info = Personality.PERSONALITIES.get(pet.personality, {})
    print(f"{Colors.YELLOW}性格: {p_info.get('name', '普通')} {p_info.get('emoji', '😺')}{Colors.RESET}")
    print("=" * 50)

    try:
        while True:
            display(pet, frame)
            pet.update()
            pet.save()
            frame += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}👋 再见！{pet.name} 会想你的～{Colors.RESET}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="超级可爱的虚拟宠物猫")
    parser.add_argument("-a", "--auto", action="store_true", help="自动模式")
    parser.add_argument("-i", "--interval", type=int, default=4, help="间隔(秒)")
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
        print("🐱 欢迎来到超级可爱虚拟宠物养成游戏！🐱")
        print("=" * 50)
        display(pet)

        while True:
            print("\n请选择操作:")
            print("1. 查看状态    2. 喂食 🍗    3. 抚摸 💕")
            print("4. 玩耍 🎾    5. 抱抱 🤗    6. 说话 💬")
            print("7. 改名        8. 自动模式    9. 退出")

            try:
                choice = input("\n> ").strip()
            except EOFError:
                break

            if choice == "1":
                pet.update()
                pet.save()
                display(pet)
            elif choice == "2":
                pet.hunger = min(100, pet.hunger + 35)
                pet.happiness = min(100, pet.happiness + 15)
                pet.last_action = "被喂食中 🍗"
                pet.memory.add("吃了美味的食物")
                pet.mood = Emotion.get_dominant(pet.happiness, pet.hunger, pet.energy, pet.personality)
                pet.save()
                print("🍗 你给猫咪喂了食物！")
                time.sleep(1)
                display(pet)
            elif choice == "3":
                pet.happiness = min(100, pet.happiness + 20)
                pet.love = min(100, pet.love + 5)
                pet.last_action = "被抚摸中 💕"
                pet.memory.add("被抚摸，好舒服")
                pet.mood = Emotion.get_dominant(pet.happiness, pet.hunger, pet.energy, pet.personality)
                pet.save()
                print("💕 猫咪舒服地呼噜～")
                time.sleep(1)
                display(pet)
            elif choice == "4":
                if pet.energy > 20:
                    pet.happiness = min(100, pet.happiness + 30)
                    pet.energy = max(0, pet.energy - 25)
                    pet.hunger = max(0, pet.hunger - 10)
                    pet.last_action = "玩耍中 🎾"
                    pet.memory.add("愉快地玩耍")
                    pet.mood = Emotion.get_dominant(pet.happiness, pet.hunger, pet.energy, pet.personality)
                    pet.save()
                    print("🎾 玩得好开心！")
                else:
                    print("😴 太累了，想睡觉")
                time.sleep(1)
                display(pet)
            elif choice == "5":
                pet.happiness = min(100, pet.happiness + 25)
                pet.love = min(100, pet.love + 10)
                pet.last_action = "被抱着 🤗"
                pet.memory.add("被抱着好幸福")
                pet.mood = "love"
                pet.save()
                print("🤗 猫咪在你怀里蹭来蹭去！")
                time.sleep(1)
                display(pet)
            elif choice == "6":
                words = input("你想对猫咪说什么? > ")
                if words:
                    pet.memory.add(f"你说: {words}")
                    pet.happiness = min(100, pet.happiness + 5)
                    pet.love = min(100, pet.love + 2)

                    # 根据性格回复
                    personality_info = Personality.PERSONALITIES[pet.personality]
                    responses = [
                        f"喵～ {words}",
                        random.choice(personality_info["greeting"]),
                        "眼睛亮亮地看着你",
                        "喵喵叫了几声",
                    ]
                    if pet.personality == "sweet":
                        responses.extend(["蹭蹭你的腿", "要一直在一起！"])
                    elif pet.personality == "proud":
                        responses.extend(["哼，本喵听到了", "勉强理你一下"])

                    pet.last_action = random.choice(responses)
                    pet.save()
                    print(f"🐱 {pet.last_action}")
                    time.sleep(1)
                    display(pet)
            elif choice == "7":
                new_name = input("新名字: ").strip()
                if new_name:
                    pet.name = new_name
                    pet.save()
                    print(f"🐱 改名为 {new_name}")
            elif choice == "8":
                print("\n🐱 启动自动模式...")
                print(f"运行: python3 {__file__} --auto")
                break
            elif choice == "9":
                pet.save()
                print("💾 再见！")
                break


if __name__ == "__main__":
    main()
