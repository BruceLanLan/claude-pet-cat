#!/usr/bin/env python3
"""
🐱 虚拟宠物宇宙 - Pixel Pet Universe
参考 Digimon/Tamagotchi 设计的像素风格虚拟宠物养成游戏
"""

import time
import random
import os
import json
import sys
from datetime import datetime, timedelta
from collections import deque

DATA_FILE = "pet_data.json"

# ========== 像素艺术字符 ==========
PIXELS = {
    "dark": "█",
    "medium": "▓",
    "light": "░",
    "empty": " ",
}

# ========== 宠物DNA数据 ==========
PETS_DATA = {
    "mimi": {
        "name_cn": "小咪",
        "name_en": "Mimi",
        "element": "normal",
        "personality": "calm",
        "pixel": [
            "  ██████  ",
            " ██░░░░██ ",
            "█░░█░█░░░█",
            "█░░░░░░░░█",
            "█░░█░█░░░█",
            " ██▓▓▓██ ",
            "  ██░░██  ",
            "   ███    ",
        ],
        "dna": {"hp": 80, "attack": 45, "defense": 50, "speed": 60, "luck": 70}
    },
    "spark": {
        "name_cn": "火花",
        "name_en": "Spark",
        "element": "fire",
        "personality": "energetic",
        "pixel": [
            "  ▓▓▓▓▓▓  ",
            " ▓▓░░░░▓▓ ",
            "▓▓░▓░▓░░▓▓",
            "▓▓░░░░░░░▓▓",
            "▓▓░▓░▓░░▓▓",
            " ▓▓▓▓▓▓▓▓ ",
            "  ▓▓░░▓▓  ",
            "   ▓▓▓▓   ",
        ],
        "dna": {"hp": 75, "attack": 65, "defense": 40, "speed": 70, "luck": 55}
    },
    "bubble": {
        "name_cn": "水球",
        "name_en": "Bubble",
        "element": "water",
        "personality": "playful",
        "pixel": [
            "  ░░▓▓▓░░  ",
            " ░░░▓▓▓░░░ ",
            "░░▒▒▓▓▒▒▒░",
            "░░▒░░░░░░▒░",
            "░░▒▒▓▓▒▒▒░",
            " ░░░▓▓▓░░░ ",
            "  ░░░░░░░  ",
            "   ░░▓▓░░  ",
        ],
        "dna": {"hp": 85, "attack": 50, "defense": 55, "speed": 65, "luck": 60}
    },
    "leaf": {
        "name_cn": "叶子",
        "name_en": "Leaf",
        "element": "grass",
        "personality": "calm",
        "pixel": [
            "   ░░░░░   ",
            "  ░▓▓▓▓▓░  ",
            " ░▓░░░░░▓░ ",
            "░▓░▓░░▓░▓░",
            "░▓░░░░░░▓░",
            " ░▓░░░░▓░ ",
            "  ░▓▓▓▓▓░  ",
            "   ░░░░░░  ",
        ],
        "dna": {"hp": 80, "attack": 50, "defense": 60, "speed": 55, "luck": 65}
    },
    "zap": {
        "name_cn": "闪电",
        "name_en": "Zap",
        "element": "electric",
        "personality": "curious",
        "pixel": [
            "   ░▓░░░   ",
            "  ░▓▓░░░░  ",
            "  ░░░▓░░░░ ",
            " ░░▓▓▓░░░░ ",
            "░░░░░▓░░░░░",
            "░░░░░▓░░░░░",
            " ░░░░▓░░░░ ",
            "  ░░░░░░░░  ",
        ],
        "dna": {"hp": 70, "attack": 70, "defense": 40, "speed": 85, "luck": 50}
    },
    "shadow": {
        "name_cn": "暗影",
        "name_en": "Shadow",
        "element": "dark",
        "personality": "shy",
        "pixel": [
            "  ░░░░░░░  ",
            " ░░░░░░░░░ ",
            "░░█░░░░█░░░",
            "░░█░█░█░█░░",
            "░░░░░░░░░░░",
            "░░░░░░░░░░░",
            " ░░░░░░░░░ ",
            "  ░░░░░░░░  ",
        ],
        "dna": {"hp": 75, "attack": 60, "defense": 45, "speed": 75, "luck": 40}
    },
    "star": {
        "name_cn": "星光",
        "name_en": "Star",
        "element": "light",
        "personality": "gentle",
        "pixel": [
            "   ░░░░░   ",
            "  ░░▓▓▓░░  ",
            " ░░▓▓▓▓▓░░░",
            "░░▓▓░▓░▓▓░░",
            "░░░▓▓▓▓▓░░░",
            " ░░░▓▓▓░░░ ",
            "  ░░░░░░░░  ",
            "   ░░░░░░░   ",
        ],
        "dna": {"hp": 85, "attack": 45, "defense": 55, "speed": 60, "luck": 80}
    },
    "coal": {
        "name_cn": "煤炭",
        "name_en": "Coal",
        "element": "dark",
        "personality": "lazy",
        "pixel": [
            "  ░░░░░░░  ",
            " ░░░░░░░░░ ",
            "░░░░░░░░░░░",
            "░░██░░░██░░",
            "░░░░░░░░░░░",
            "░░░░░░░░░░░",
            " ░░░░░░░░░ ",
            "  ░░░░░░░░  ",
        ],
        "dna": {"hp": 90, "attack": 40, "defense": 70, "speed": 30, "luck": 50}
    },
    "snow": {
        "name_cn": "雪花",
        "name_en": "Snow",
        "element": "water",
        "personality": "gentle",
        "pixel": [
            "  ░░░░░░░  ",
            " ░░░▓▓░░░░ ",
            "░░░▓▓▓▓░░░░",
            "░░░░▓▓▓░░░░",
            "░░░░▓▓▓░░░░",
            "░░░░░▓░░░░░",
            " ░░░░░░░░░░ ",
            "  ░░░░░░░░  ",
        ],
        "dna": {"hp": 80, "attack": 45, "defense": 60, "speed": 55, "luck": 75}
    },
    "blaze": {
        "name_cn": "火焰",
        "name_en": "Blaze",
        "element": "fire",
        "personality": "proud",
        "pixel": [
            "   ░░░░░   ",
            "  ░▓▓▓▓▓░  ",
            " ░▓░░░░░▓░ ",
            "░▓░░░░░░▓░",
            "░░▓░░░▓░░░",
            " ░░▓░░▓░░░ ",
            "  ░░▓▓▓░░░  ",
            "   ░░░░░░░   ",
        ],
        "dna": {"hp": 80, "attack": 75, "defense": 45, "speed": 65, "luck": 55}
    },
    "mint": {
        "name_cn": "薄荷",
        "name_en": "Mint",
        "element": "grass",
        "personality": "curious",
        "pixel": [
            "   ░░░░░   ",
            "  ░▒▒▒▒▒░  ",
            " ░▒░░░░░▒░ ",
            "░▒░░▒░░░▒░",
            "░▒░░▒░░░▒░",
            " ░▒░░░░▒░░ ",
            "  ░▒▒▒▒▒░░  ",
            "   ░░░░░░░   ",
        ],
        "dna": {"hp": 78, "attack": 52, "defense": 58, "speed": 68, "luck": 62}
    },
    "amber": {
        "name_cn": "琥珀",
        "name_en": "Amber",
        "element": "earth",
        "personality": "calm",
        "pixel": [
            "  ░▒▒▒▒▒░  ",
            " ▒▒░░░░░░▒▒",
            "▒░░▒░░▒░░▒░",
            "▒░░░░░░░░░▒",
            "▒░░▒░░▒░░▒░",
            " ▒▒░░░░░▒▒ ",
            "  ░▒▒▒▒▒░  ",
            "   ░░░░░░░   ",
        ],
        "dna": {"hp": 85, "attack": 55, "defense": 65, "speed": 45, "luck": 60}
    },
    "thunder": {
        "name_cn": "雷霆",
        "name_en": "Thunder",
        "element": "electric",
        "personality": "energetic",
        "pixel": [
            "   ░▓░░░   ",
            "  ░▓▓░░░░  ",
            "  ░░░▓░░░░ ",
            " ░░▓▓▓░░░░░",
            "░░░░░▓░░░░░",
            "░░░░░▓░░░░░",
            " ░░░░▓░░░░░",
            "  ░░░░░░░░░  ",
        ],
        "dna": {"hp": 72, "attack": 72, "defense": 42, "speed": 88, "luck": 48}
    },
    "moon": {
        "name_cn": "月光",
        "name_en": "Moon",
        "element": "light",
        "personality": "mysterious",
        "pixel": [
            "  ░░░░░░░░  ",
            " ░░░░▓▓░░░░ ",
            "░░░░▓▓▓▓░░░░",
            "░░░░░▓▓░░░░░",
            "░░░░▓▓▓▓░░░░",
            "░░░░░▓░░░░░░",
            " ░░░░░░░░░░ ",
            "  ░░░░░░░░░  ",
        ],
        "dna": {"hp": 82, "attack": 50, "defense": 58, "speed": 62, "luck": 70}
    },
    "sakura": {
        "name_cn": "樱花",
        "name_en": "Sakura",
        "element": "flower",
        "personality": "gentle",
        "pixel": [
            "   ░▒▒▒░   ",
            "  ░▒░░░▒░  ",
            " ░▒░░░░░▒░░",
            "░▒░░▓░▓░░▒░",
            "░▒░░░░░░░▒░",
            " ░▒░░░░▒░░ ",
            "  ░▒▒▒▒▒░░  ",
            "   ░░░░░░░   ",
        ],
        "dna": {"hp": 78, "attack": 48, "defense": 55, "speed": 58, "luck": 78}
    },
    "dawn": {
        "name_cn": "晨曦",
        "name_en": "Dawn",
        "element": "light",
        "personality": "optimistic",
        "pixel": [
            "   ░░░░░░░   ",
            "  ░▓░░░▓░░  ",
            " ░░▓▓▓▓▓▓░░░",
            "░░░░▓▓▓▓░░░░",
            "░░░░░▓▓░░░░░",
            " ░░░░░▓░░░░░ ",
            "  ░░░░░░░░░░░  ",
            "   ░░░░░░░░░   ",
        ],
        "dna": {"hp": 82, "attack": 58, "defense": 52, "speed": 70, "luck": 72}
    },
    "chaos": {
        "name_cn": "混沌",
        "name_en": "Chaos",
        "element": "dark",
        "personality": "mysterious",
        "pixel": [
            "  ░░░░░░░░  ",
            " ░░▒▓░░▓▒░░ ",
            "░░░▓█░█▓░░░░",
            "░░░░░█░░░░░░",
            "░░░▓█░█▓░░░░",
            " ░░▒▓░░▓▒░░ ",
            "  ░░░░░░░░░░  ",
            "   ░░░░░░░░░   ",
        ],
        "dna": {"hp": 88, "attack": 80, "defense": 50, "speed": 75, "luck": 35}
    },
    "coral": {
        "name_cn": "珊瑚",
        "name_en": "Coral",
        "element": "water",
        "personality": "friendly",
        "pixel": [
            "  ░░░░░░░░  ",
            " ░▓░░░░░░▓░ ",
            "░░░░░░░░░░░░",
            "░▓▓░░░░░▓▓░",
            "░░░░░░░░░░░░",
            "░░░░░░░░░░░░",
            " ░░░░░░░░░░░ ",
            "  ░░░░░░░░░░░  ",
        ],
        "dna": {"hp": 85, "attack": 52, "defense": 60, "speed": 60, "luck": 68}
    },
    "charcoal": {
        "name_cn": "炭仔",
        "name_en": "Charcoal",
        "element": "dark",
        "personality": "independent",
        "pixel": [
            "  ░░░░░░░░  ",
            " ░░░░░░░░░░ ",
            "░░░░░░░░░░░░",
            "░░██░░░██░░",
            "░░░░░░░░░░░",
            "░░░░░░░░░░░",
            " ░░░░░░░░░░░ ",
            "  ░░░░░░░░░░░  ",
        ],
        "dna": {"hp": 88, "attack": 55, "defense": 68, "speed": 38, "luck": 52}
    },
}

# ========== 道具数据 ==========
ITEMS_DATA = {
    # 食物类
    "cat_food": {"name": "猫粮", "type": "food", "effect": {"hunger": 20}, "desc": "普通的猫粮"},
    "premium_food": {"name": "高级猫罐", "type": "food", "effect": {"hunger": 40}, "desc": "美味的高级罐头"},
    "snack": {"name": "零食小鱼", "type": "food", "effect": {"hunger": 10}, "desc": "可口的小零食"},
    "nutrition_paste": {"name": "营养膏", "type": "food", "effect": {"hunger": 30}, "desc": "营养丰富的膏状食品"},
    "catnip": {"name": "猫薄荷", "type": "food", "effect": {"hunger": 15, "happiness": 10}, "desc": "猫咪最喜欢的草"},

    # 玩具类
    "yarn_ball": {"name": "毛线球", "type": "toy", "effect": {"happiness": 15}, "desc": "可以滚来滚去的毛线球"},
    "feather_wand": {"name": "逗猫棒", "type": "toy", "effect": {"happiness": 20}, "desc": "羽毛做的逗猫棒"},
    "laser_pointer": {"name": "激光笔", "type": "toy", "effect": {"happiness": 25}, "desc": "猫咪追着跑的小红点"},
    "cat_tree": {"name": "猫爬架", "type": "toy", "effect": {"happiness": 30}, "desc": "大型玩具设施"},

    # 装饰类
    "red_bow": {"name": "红色蝴蝶结", "type": "clothes", "slot": "neck", "effect": {"charm": 10}, "desc": "漂亮的红色蝴蝶结"},
    "blue_collar": {"name": "蓝色项圈", "type": "clothes", "slot": "neck", "effect": {"charm": 15}, "desc": "时尚的蓝色项圈"},
    "star_hairpin": {"name": "星星发卡", "type": "clothes", "slot": "head", "effect": {"charm": 20}, "desc": "闪亮的星星发卡"},
    "gentleman_hat": {"name": "绅士礼帽", "type": "clothes", "slot": "head", "effect": {"charm": 25}, "desc": "帅气的礼帽"},
    "princess_dress": {"name": "公主裙", "type": "clothes", "slot": "body", "effect": {"charm": 30}, "desc": "可爱的公主裙"},
    "hero_cape": {"name": "英雄披风", "type": "clothes", "slot": "back", "effect": {"charm": 35}, "desc": "帅气的披风"},

    # 药品类
    "basic_medicine": {"name": "基础药品", "type": "medicine", "effect": {"health": 30}, "desc": "基础的药品"},
    "premium_medicine": {"name": "高级药品", "type": "medicine", "effect": {"health": 60}, "desc": "效果更好的药品"},
    "first_aid": {"name": "急救包", "type": "medicine", "effect": {"health": 100}, "desc": "可以完全恢复健康"},

    # 特殊类
    "wish_star": {"name": "许愿星", "type": "special", "effect": {"luck": 10}, "desc": "可以提升幸运值"},
    "exp_potion": {"name": "经验药水", "type": "special", "effect": {"experience": 50}, "desc": "获得额外经验"},
    "dna_reshaper": {"name": "DNA重组器", "type": "special", "effect": {"reset_dna": True}, "desc": "重置宠物DNA"},
}

# ========== 成就数据 ==========
ACHIEVEMENTS_DATA = {
    # 成长类
    "newborn": {"name": "新生儿", "desc": "获得第一只宠物", "type": "growth", "condition": {"has_pet": True}},
    "one_week": {"name": "一天天长大", "desc": "年龄达到1周", "type": "growth", "condition": {"age_days": 7}},
    "one_month": {"name": "一周岁啦", "desc": "年龄达到1个月", "type": "growth", "condition": {"age_days": 30}},
    "veteran": {"name": "资深铲屎官", "desc": "养了100天", "type": "growth", "condition": {"age_days": 100}},

    # 互动类
    "first_pet": {"name": "第一次触碰", "desc": "首次抚摸", "type": "interaction", "condition": {"pet_count": 1}},
    "first_feed": {"name": "喂食开始", "desc": "首次喂食", "type": "interaction", "condition": {"feed_count": 1}},
    "play_master": {"name": "玩耍达人", "desc": "玩耍100次", "type": "interaction", "condition": {"play_count": 100}},
    "talk_master": {"name": "对话大师", "desc": "对话500次", "type": "interaction", "condition": {"talk_count": 500}},
    "daily_user": {"name": "从不缺席", "desc": "连续7天互动", "type": "interaction", "condition": {"streak": 7}},

    # 收集类
    "collector_10": {"name": "初级收藏家", "desc": "收集10个道具", "type": "collection", "condition": {"item_count": 10}},
    "collector_50": {"name": "道具大亨", "desc": "收集50个道具", "type": "collection", "condition": {"item_count": 50}},
    "pet_5": {"name": "宠物图鉴1", "desc": "解锁5只宠物", "type": "collection", "condition": {"pet_variety": 5}},
    "pet_master": {"name": "宠物大师", "desc": "解锁所有20只宠物", "type": "collection", "condition": {"pet_variety": 20}},

    # 事件类
    "night_fright": {"name": "深夜惊醒", "desc": "触发夜惊事件", "type": "event", "condition": {"night_event": True}},
    "sick_recovery": {"name": "生病痊愈", "desc": "首次照顾生病", "type": "event", "condition": {"sick_recovery": True}},

    # 隐藏类
    "lucky_star": {"name": "天选之人", "desc": "幸运达到100", "type": "hidden", "condition": {"luck": 100}},
    "true_love": {"name": "真爱", "desc": "爱意100%保持7天", "type": "hidden", "condition": {"love_streak": 7}},
}

# ========== 随机互动事件 ==========
RANDOM_EVENTS = [
    # 正面事件
    {"type": "hug", "msg": "喵喵～要抱抱！", "chance": 0.05},
    {"type": "snack", "msg": "喵～给我点零食嘛！", "chance": 0.05},
    {"type": "discover", "msg": "喵！快看这个！", "chance": 0.08},
    {"type": "cute", "msg": "喵呜～(卖萌)", "chance": 0.10},
    {"type": "playful", "msg": "来抓我呀～", "chance": 0.08},

    # 负面事件
    {"type": "mischief", "msg": "哼！就不理你！(调皮)", "chance": 0.05},
    {"type": "sick", "msg": "喵...不舒服...", "chance": 0.02},

    # 中性事件
    {"type": "dream", "msg": "喵...Zzz...", "chance": 0.03},
    {"type": "stretch", "msg": "啊～伸个懒腰～", "chance": 0.05},
]

# ========== 进化系统 ==========
EVOLUTIONS = {
    "mimi": {"next": "mimi_prime", "level": 10, "name": "小咪公主"},
    "spark": {"next": "blaze", "level": 10, "name": "火焰"},
    "bubble": {"next": "coral", "level": 10, "name": "珊瑚"},
    "leaf": {"next": "sakura", "level": 10, "name": "樱花"},
    "zap": {"next": "thunder", "level": 10, "name": "雷霆"},
    "shadow": {"next": "chaos", "level": 10, "name": "混沌"},
    "star": {"next": "dawn", "level": 10, "name": "晨曦"},
    "coal": {"next": "charcoal", "level": 10, "name": "炭仔"},
    "snow": {"next": "frost", "level": 10, "name": "霜霜"},
}

# 进化形态数据
EVOLUTION_FORMS = {
    "mimi_prime": {
        "name_cn": "小咪公主",
        "name_en": "Princess Mimi",
        "element": "light",
        "pixel": [
            "  ░░░░░░  ",
            " ░░▓▓▓▓░░ ",
            "░░▓░░░▓░░░",
            "░░░░▓░░░░░",
            "░░▓░░░▓░░░",
            " ░░▓▓▓▓░░ ",
            "  ░░▓▓░░  ",
            "   ░▓▓    ",
        ],
        "dna": {"hp": 120, "attack": 65, "defense": 80, "speed": 80, "luck": 95}
    },
    "blaze": {
        "name_cn": "火焰",
        "name_en": "Blaze",
        "element": "fire",
        "pixel": [
            "  ▓▓▓▓▓▓  ",
            " ▓▓░░░░▓▓ ",
            "▓▓░▓▓▓░░▓▓",
            "▓▓░░░░░░░▓▓",
            "▓▓░▓▓▓░░▓▓",
            " ▓▓▓▓▓▓▓▓ ",
            "  ▓▓░░▓▓  ",
            "   ▓▓▓▓   ",
        ],
        "dna": {"hp": 110, "attack": 95, "defense": 60, "speed": 90, "luck": 70}
    },
}


class Pet:
    """宠物类"""

    def __init__(self, species="mimi", name=None):
        self.id = f"pet_{int(time.time() * 1000)}"
        self.species = species
        data = PETS_DATA.get(species, PETS_DATA["mimi"])
        self.name = name or data["name_cn"]

        # DNA
        base_dna = data["dna"].copy()
        # 随机变异 ±10%
        self.dna = {
            k: max(1, int(v * random.uniform(0.9, 1.1)))
            for k, v in base_dna.items()
        }

        # 基础属性
        self.level = 1
        self.experience = 0
        self.exp_to_level = 100

        # 状态
        self.hunger = 80
        self.happiness = 80
        self.energy = 80
        self.health = 100
        self.love = 50

        # 衣着
        self.clothes = {"head": None, "neck": None, "body": None, "back": None}

        # 记忆
        self.memory = deque(maxlen=20)
        self.last_interaction = None

        # 时间
        self.born_time = datetime.now().isoformat()
        self.last_update = datetime.now().isoformat()
        self.age_days = 0

        # 互动统计
        self.stats = {
            "feed_count": 0,
            "play_count": 0,
            "pet_count": 0,
            "talk_count": 0,
            "total_interactions": 0,
        }

        # 心情
        self.mood = "happy"
        self.thought = "..."

        self.add_memory("出生了！")

    def add_memory(self, event):
        timestamp = datetime.now().strftime("%H:%M")
        self.memory.append(f"[{timestamp}] {event}")

    def get_age_str(self):
        born = datetime.fromisoformat(self.born_time)
        delta = datetime.now() - born
        days = delta.days
        hours = delta.seconds // 3600
        if days > 0:
            return f"{days}天{hours}小时"
        elif hours > 0:
            return f"{hours}小时"
        else:
            return "新出生"

    def get_mood(self):
        if self.health < 30:
            return "sick"
        elif self.energy < 20:
            return "tired"
        elif self.hunger < 20:
            return "hungry"
        elif self.happiness > 80:
            return "happy"
        elif self.happiness > 50:
            return "content"
        elif self.happiness < 30:
            return "sad"
        else:
            return "neutral"

    def update(self):
        """更新宠物状态"""
        # 自然衰减
        self.hunger = max(0, self.hunger - 3)
        self.happiness = max(0, self.happiness - 2)
        self.energy = min(100, self.energy + 5)

        # 检查生病
        if random.random() < 0.01 and self.health > 50:
            self.health = max(10, self.health - 20)
            self.add_memory("好像生病了...")

        # 自然恢复
        if self.health < 100 and random.random() < 0.1:
            self.health = min(100, self.health + 5)

        self.mood = self.get_mood()
        # 更新想法
        mood_thoughts = self.THOUGHTS.get(self.mood, self.THOUGHTS["neutral"])
        if random.random() < 0.3:
            self.thought = random.choice(mood_thoughts)
        self.last_update = datetime.now().isoformat()

        # 更新年龄
        born = datetime.fromisoformat(self.born_time)
        self.age_days = (datetime.now() - born).days

    def add_exp(self, amount):
        """增加经验"""
        self.experience += amount
        while self.experience >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        """升级"""
        old_level = self.level
        self.level += 1
        self.experience -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)

        # 属性提升
        self.dna["hp"] += random.randint(2, 5)
        self.dna["attack"] += random.randint(1, 3)
        self.dna["defense"] += random.randint(1, 3)
        self.dna["speed"] += random.randint(1, 3)
        self.dna["luck"] += random.randint(0, 2)

        self.add_memory(f"升级到 {self.level} 级了！")

        # 检查进化
        if self.level == 10:
            evo_msg = self.check_evolution()
            if evo_msg:
                print(f"\n{'='*40}")
                print(evo_msg)
                print(f"{'='*40}\n")

    # ========== 互动方法 ==========
    THOUGHTS = {
        "happy": ["今天超开心！", "阳光好温暖～", "喵～"],
        "love": ["好爱好爱你！", "想一直黏着你！", "你是最好的人！"],
        "hungry": ["好饿好饿...", "想去厨房偷吃！", "铲屎官在哪！"],
        "sad": ["有点难过...", "你都不陪我...", "寂寞..."],
        "excited": ["太棒了！！！", "好好玩！！！", "好开心！！！"],
        "neutral": ["发发呆～", "我在想事情...", "喵～"],
    }

    def feed(self, food_power=20):
        """喂食"""
        self.hunger = min(100, self.hunger + food_power)
        self.happiness = min(100, self.happiness + 5)
        self.stats["feed_count"] += 1
        self.stats["total_interactions"] += 1
        self.add_memory("吃了美味的食物")
        self.thought = random.choice(self.THOUGHTS.get("happy", self.THOUGHTS["neutral"]))
        return f"🍗 喂食成功！饱食度 +{food_power}"

    def play(self, fun=20):
        """玩耍"""
        if self.energy < 10:
            return "⚡ 宠物太累了，需要休息"
        self.happiness = min(100, self.happiness + fun)
        self.energy = max(0, self.energy - 10)
        self.hunger = max(0, self.hunger - 5)
        self.stats["play_count"] += 1
        self.stats["total_interactions"] += 1
        self.add_exp(10)
        self.add_memory("愉快地玩耍")
        self.thought = random.choice(self.THOUGHTS.get("excited", self.THOUGHTS["neutral"]))
        return f"🎾 玩耍成功！快乐度 +{fun}, 经验 +10"

    def pet_touch(self):
        """抚摸"""
        self.love = min(100, self.love + 5)
        self.happiness = min(100, self.happiness + 8)
        self.stats["pet_count"] += 1
        self.stats["total_interactions"] += 1
        self.add_memory("被抚摸好舒服")
        self.thought = random.choice(self.THOUGHTS.get("love", self.THOUGHTS["neutral"]))
        return f"💕 抚摸成功！爱意 +5, 快乐 +8"

    def talk(self, words="喵～"):
        """对话"""
        self.happiness = min(100, self.happiness + 3)
        self.love = min(100, self.love + 2)
        self.stats["talk_count"] += 1
        self.stats["total_interactions"] += 1
        responses = ["喵～", "咪咪", "呼噜～", "主人好！", "爱你哦！"]
        self.thought = random.choice(responses)
        self.add_memory(f"听到: {words}")
        return f"💬 对话: {self.thought}"

    def heal(self, amount=30):
        """治疗"""
        self.health = min(100, self.health + amount)
        self.add_memory("接受了治疗")
        return f"❤️ 治疗成功！健康 +{amount}"

    def check_evolution(self):
        """检查是否可以进化"""
        if self.species in EVOLUTIONS:
            evo = EVOLUTIONS[self.species]
            if self.level >= evo["level"]:
                # 可以进化
                evo_data = EVOLUTION_FORMS.get(evo["next"])
                if evo_data:
                    self.species = evo["next"]
                    self.name = evo_data["name_cn"]
                    # 更新DNA
                    for k, v in evo_data["dna"].items():
                        self.dna[k] = v
                    self.add_memory(f"进化成了 {self.name}！")
                    return f"✨ 恭喜！{self.name} 进化了！"
        return None


class GameData:
    """游戏数据管理"""

    def __init__(self):
        self.pets = []
        self.inventory = {}  # {item_id: count}
        self.coins = 1000
        self.achievements = []
        self.stats = {
            "total_play_time": 0,
            "current_streak": 0,
            "last_play_date": None,
        }
        self.unlocked_pets = ["mimi"]
        self.current_pet_index = 0

    def save(self):
        # 转换宠物数据为JSON可序列化格式
        def pet_to_dict(pet):
            d = pet.__dict__.copy()
            # deque转list
            if "memory" in d:
                d["memory"] = list(d["memory"])
            return d

        data = {
            "pets": [pet_to_dict(p) for p in self.pets],
            "inventory": self.inventory,
            "coins": self.coins,
            "achievements": self.achievements,
            "stats": self.stats,
            "unlocked_pets": self.unlocked_pets,
            "current_pet_index": self.current_pet_index,
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)

                game = cls()
                game.inventory = data.get("inventory", {})
                game.coins = data.get("coins", 1000)
                game.achievements = data.get("achievements", [])
                game.stats = data.get("stats", game.stats)
                game.unlocked_pets = data.get("unlocked_pets", ["mimi"])
                game.current_pet_index = data.get("current_pet_index", 0)

                # 恢复宠物
                for pet_data in data.get("pets", []):
                    pet = Pet()
                    pet.__dict__.update(pet_data)
                    # list转deque
                    if "memory" in pet.__dict__ and isinstance(pet.__dict__["memory"], list):
                        pet.__dict__["memory"] = deque(pet.__dict__["memory"], maxlen=20)
                    game.pets.append(pet)

                return game
            except:
                pass
        return cls()

    def add_pet(self, species):
        """添加宠物"""
        if species in PETS_DATA:
            pet = Pet(species)
            self.pets.append(pet)
            if species not in self.unlocked_pets:
                self.unlocked_pets.append(species)
            return pet
        return None

    def get_current_pet(self):
        if self.pets and 0 <= self.current_pet_index < len(self.pets):
            return self.pets[self.current_pet_index]
        return self.pets[0] if self.pets else None

    def add_item(self, item_id, count=1):
        if item_id in self.inventory:
            self.inventory[item_id] += count
        else:
            self.inventory[item_id] = count

    def use_item(self, item_id):
        if self.inventory.get(item_id, 0) > 0:
            self.inventory[item_id] -= 1
            if self.inventory[item_id] <= 0:
                del self.inventory[item_id]
            return True
        return False

    def add_achievement(self, achievement_id):
        if achievement_id not in self.achievements:
            self.achievements.append(achievement_id)
            return True
        return False


def display_pet(pet, frame=0):
    """显示宠物像素界面"""
    # 获取像素图案
    pet_data = PETS_DATA.get(pet.species, PETS_DATA["mimi"])
    pixel_art = pet_data["pixel"]

    # 清理屏幕
    print("\033[2J\033[H", end="")

    # 获取心情
    mood_emoji = {"happy": "😊", "content": "😐", "sad": "😢", "hungry": "😫", "tired": "😴", "sick": "🤒"}
    mood_str = mood_emoji.get(pet.mood, "😐")

    # 显示界面
    print("╔══════════════════════════════════════════════════╗")
    print(f"║ 🏠 宠物之家    💰 1000    📅 {pet.get_age_str():>10}    ║".format(pet.get_age_str()))
    print("╠══════════════════════════════════════════════════╣")
    print("║                                                  ║")

    # 显示像素宠物
    for line in pixel_art:
        print(f"║     {line:30}        ║")

    print("║                                                  ║")
    print(f"║   💭 \"{pet.thought}\"                           ║")
    print("╠══════════════════════════════════════════════════╣")

    # 状态条
    def bar(value):
        return "█" * (value // 10) + "░" * (10 - value // 10)

    print(f"║ 🍖 饱食: [{bar(pet.hunger)}] {pet.hunger:3}%              ║")
    print(f"║ 💖 快乐: [{bar(pet.happiness)}] {pet.happiness:3}%              ║")
    print(f"║ ⚡ 能量: [{bar(pet.energy)}] {pet.energy:3}%              ║")
    print(f"║ ❤️ 健康: [{bar(pet.health)}] {pet.health:3}%              ║")
    print(f"║ 💕 爱意: [{bar(pet.love)}] {pet.love:3}%              ║")

    print("╠══════════════════════════════════════════════════╣")
    print(f"║ Lv.{pet.level} {pet.name} | DNA: HP:{pet.dna['hp']} ATK:{pet.dna['attack']} DEF:{pet.dna['defense']} SPD:{pet.dna['speed']} LCK:{pet.dna['luck']}  ║")
    print("╚══════════════════════════════════════════════════╝")

    sys.stdout.flush()


def run_auto(game, interval=4):
    """自动运行模式"""
    pet = game.get_current_pet()
    if not pet:
        print("没有宠物！请先添加宠物")
        return

    frame = 0
    print("🐱 启动宠物宇宙！\n")

    try:
        while True:
            display_pet(pet, frame)
            pet.update()
            game.save()

            # 随机事件
            if random.random() < 0.1:
                event = random.choice(RANDOM_EVENTS)
                if random.random() < event["chance"]:
                    pet.thought = event["msg"]
                    pet.add_memory(event["msg"])

            frame += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        game.save()
        print("\n👋 再见！")


def interactive_menu(game):
    """交互菜单"""
    pet = game.get_current_pet()
    if not pet:
        print("没有宠物！")
        return

    while True:
        print("\n" + "="*40)
        print("🐱 宠物宇宙 - 交互菜单")
        print("="*40)
        print(f"当前宠物: {pet.name} (Lv.{pet.level})")
        print(f"饱食: {pet.hunger}% | 快乐: {pet.happiness}% | 能量: {pet.energy}%")
        print(f"健康: {pet.health}% | 爱意: {pet.love}%")
        print("-" * 40)
        print("1. 🍗 喂食")
        print("2. 🎾 玩耍")
        print("3. 💕 抚摸")
        print("4. 💬 对话")
        print("5. ❤️ 治疗")
        print("6. 🎨 换装")
        print("7. 🎁 背包")
        print("8. 🏆 成就")
        print("9. ➕ 添加新宠物")
        print("0. 🚪 退出")
        print("-" * 40)

        choice = input("选择: ").strip()

        if choice == "1":
            result = pet.feed(25)
            print(result)
        elif choice == "2":
            result = pet.play(20)
            print(result)
        elif choice == "3":
            result = pet.pet_touch()
            print(result)
        elif choice == "4":
            words = input("想说什么: ").strip() or "喵～"
            result = pet.talk(words)
            print(result)
        elif choice == "5":
            result = pet.heal(30)
            print(result)
        elif choice == "6":
            # 换装菜单
            print("\n🎨 服装系统 (暂未开放)")
        elif choice == "7":
            # 背包
            print(f"\n🎁 背包: 金币 {game.coins}")
            if game.inventory:
                for item_id, count in game.inventory.items():
                    item = ITEMS_DATA.get(item_id, {})
                    print(f"  - {item.get('name', item_id)} x{count}")
            else:
                print("  背包是空的")
        elif choice == "8":
            # 成就
            print(f"\n🏆 已获成就: {len(game.achievements)}")
            for a in game.achievements:
                ach = ACHIEVEMENTS_DATA.get(a, {})
                print(f"  ✓ {ach.get('name', a)}")
        elif choice == "9":
            print("\n可选宠物:")
            for i, (sid, data) in enumerate(PETS_DATA.items()):
                lock = "🔒" if sid not in game.unlocked_pets else "✓"
                print(f"  {i+1}. {data['name_cn']} ({data['name_en']}) {lock}")
            try:
                idx = int(input("选择号码: ")) - 1
                species = list(PETS_DATA.keys())[idx]
                game.add_pet(species)
                print(f"添加了 {PETS_DATA[species]['name_cn']}！")
            except:
                pass
        elif choice == "0":
            game.save()
            print("再见！")
            break

        game.save()
        display_pet(pet)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="虚拟宠物宇宙")
    parser.add_argument("-a", "--auto", action="store_true", help="自动模式")
    parser.add_argument("-i", "--interval", type=int, default=4, help="间隔秒")
    parser.add_argument("--add-pet", type=str, help="添加宠物")
    parser.add_argument("-m", "--menu", action="store_true", help="交互菜单模式")
    args = parser.parse_args()

    game = GameData.load()

    # 如果没有宠物，默认添加小咪
    if not game.pets:
        game.add_pet("mimi")

    if args.add_pet:
        game.add_pet(args.add_pet)
        print(f"添加了 {PETS_DATA[args.add_pet]['name_cn']}！")

    if args.auto:
        run_auto(game, args.interval)
    elif args.menu:
        interactive_menu(game)
    else:
        pet = game.get_current_pet()
        display_pet(pet)


if __name__ == "__main__":
    main()
