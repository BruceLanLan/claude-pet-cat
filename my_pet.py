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

# ========== 性格系统 ==========
PERSONALITIES = {
    "gentle": {
        "name": "温柔",
        "emoji": "💕",
        "feed_msg": ["好吃～谢谢主人！", "好美味呀～", "主人最好了！"],
        "play_msg": ["一起玩吧～", "好开心！", "最喜欢主人了！"],
        "pet_msg": ["舒服～", "再摸摸我嘛～", "喵～"],
        "talk_msg": ["主人好～", "今天也很开心！", "爱你哦～"],
        "mood_thoughts": {
            "happy": ["今天好幸福！", "有主人真好～", "阳光好温暖～"],
            "love": ["好爱好爱你！", "想一直黏着你！", "你是最好的主人！"],
            "hungry": ["有点饿了...", "想吃东西～", "主人什么时候喂我？"],
            "sad": ["有点难过...", "你都不陪我...", "寂寞..."],
            "excited": ["太棒了！！！", "好好玩！！！", "好开心！！！"],
            "neutral": ["发发呆～", "我在想事情...", "喵～"],
        }
    },
    "energetic": {
        "name": "活泼",
        "emoji": "⚡",
        "feed_msg": ["太好吃了！再来点！", "美味！", "我还能吃更多！"],
        "play_msg": ["来抓我呀！", "太好玩了！", "再来一次！"],
        "pet_msg": ["舒服！", "我最喜欢你了！", "嘿嘿！"],
        "talk_msg": ["主人！主人！", "今天干什么？", "好无聊啊！"],
        "mood_thoughts": {
            "happy": ["今天超开心！", "精力旺盛！", "去冒险吧！"],
            "love": ["我好喜欢你！", "你是最好的伙伴！", "永远在一起！"],
            "hungry": ["饿死了！！！", "我要吃东西！！！", "快喂我！！！"],
            "sad": ["不开心...", "好无聊...", "没精神..."],
            "excited": ["太棒了！！！", "冲啊！！！", "好玩！！！"],
            "neutral": ["好无聊...", "找点事做...", "出发！"],
        }
    },
    "cheerful": {
        "name": "开朗",
        "emoji": "😊",
        "feed_msg": ["好好吃！", "谢谢主人！", "幸福！"],
        "play_msg": ["太好玩了！", "再来！", "我好开心！"],
        "pet_msg": ["舒服！", "我好幸福！", "喵！"],
        "talk_msg": ["主人好！", "今天也很棒！", "笑一个！"],
        "mood_thoughts": {
            "happy": ["今天超开心！", "阳光好温暖！", "世界真美好！"],
            "love": ["好爱好爱你！", "你是最棒的主人！", "幸福！"],
            "hungry": ["有点饿了...", "想吃点东西～", "什么时候吃饭？"],
            "sad": ["有点难过...", "安慰我嘛...", "呜呜..."],
            "excited": ["太棒了！！！", "好开心！！！", "哈哈哈！！！"],
            "neutral": ["今天干什么呢？", "晒晒太阳～", "发发呆～"],
        }
    },
    "shy": {
        "name": "害羞",
        "emoji": "🌸",
        "feed_msg": ["谢、谢谢...", "好吃...", "主人给的..."],
        "play_msg": ["这、这样吗...", "我玩不来...", "害怕..."],
        "pet_msg": ["呀！", "不要这样...", "好痒..."],
        "talk_msg": ["主、主人好...", "那、那个...", "嗯..."],
        "mood_thoughts": {
            "happy": ["今天不错...", "有点开心...", "阳光..."],
            "love": ["喜欢...主人...", "心跳好快...", "不敢看..."],
            "hungry": ["那个...我饿了...", "想说...", "不敢..."],
            "sad": ["难过...", "一个人...", "害怕..."],
            "excited": ["呀！不要！", "吓一跳！", "太、太快了！"],
            "neutral": ["那个...", "我在想...", "嗯..."],
        }
    },
    "brave": {
        "name": "勇敢",
        "emoji": "⚔️",
        "feed_msg": ["很好！", "有力量了！", "吃饱了战斗！"],
        "play_msg": ["这就是战斗！", "我不怕！", "来啊！"],
        "pet_msg": ["嗯！", "我是最强的！", "不错！"],
        "talk_msg": ["主人！我们去战斗！", "我会保护你！", "出发！"],
        "mood_thoughts": {
            "happy": ["战斗！战斗！", "充满力量！", "准备好了！"],
            "love": ["我会保护你！", "你是我的伙伴！", "永远战斗！"],
            "hungry": ["快去吃饭！", "没力气了！", "战斗需要能量！"],
            "sad": ["我不会放弃！", "站起来！", "这只是挫折！"],
            "excited": ["冲锋！！！", "战斗！！！", "杀啊！！！"],
            "neutral": ["准备战斗！", "等待时机...", "观察敌人..."],
        }
    },
    "calm": {
        "name": "冷静",
        "emoji": "🧘",
        "feed_msg": ["谢谢", "不错", "可以"],
        "play_msg": ["嗯", "可以", "还行"],
        "pet_msg": ["嗯", "还行", "可以"],
        "talk_msg": ["什么事", "嗯", "好的"],
        "mood_thoughts": {
            "happy": ["不错", "可以", "还好"],
            "love": ["知道了", "嗯", "一直都在"],
            "hungry": ["饿了", "想吃饭", "知道了"],
            "sad": ["知道了", "嗯", "会好的"],
            "excited": ["淡定", "不要激动", "冷静"],
            "neutral": ["思考中...", "等待...", "观察..."],
        }
    },
    "playful": {
        "name": "调皮",
        "emoji": "😜",
        "feed_msg": ["嘿嘿！", "好吃！", "再来！"],
        "play_msg": ["来抓我呀！", "嘿嘿！", "躲开了！"],
        "pet_msg": ["嘿嘿！", "痒！", "好玩！"],
        "talk_msg": ["主人！", "嘿嘿！", "猜猜我在哪？"],
        "mood_thoughts": {
            "happy": ["嘿嘿！", "太好玩了！", "整蛊开始！"],
            "love": ["最喜欢主人了！", "嘿嘿！", "给你看个好玩的！"],
            "hungry": ["饿死了！", "要吃东西！", "嘿嘿去偷吃的！"],
            "sad": ["没心情玩了...", "无聊...", "不开心..."],
            "excited": ["太好玩了！！！", "整蛊时间到！", "嘿嘿嘿嘿！"],
            "neutral": ["找点乐子...", "嘿嘿...", "捣蛋..."],
        }
    },
    "kind": {
        "name": "善良",
        "emoji": "🌟",
        "feed_msg": ["谢谢你！", "好好吃！", "幸福！"],
        "play_msg": ["一起玩吧！", "好开心！", "你真好！"],
        "pet_msg": ["好舒服！", "谢谢！", "喜欢你！"],
        "talk_msg": ["主人好！", "今天也要开心！", "爱你哦！"],
        "mood_thoughts": {
            "happy": ["今天好幸福！", "帮助别人真开心！", "世界真美好！"],
            "love": ["好爱好爱你！", "你是世界上最好的人！", "幸福！"],
            "hungry": ["有点饿了...", "但还可以忍...", "谢谢你照顾我..."],
            "sad": ["有点难过...", "想哭...", "抱抱..."],
            "excited": ["太棒了！", "好开心！", "爱你！"],
            "neutral": ["今天干什么呢？", "发发呆～", "晒太阳～"],
        }
    },
    "proud": {
        "name": "骄傲",
        "emoji": "👑",
        "feed_msg": ["勉强及格", "不错", "符合我的身份"],
        "play_msg": ["本大爷天下无敌！", "让你们看看！", "太简单了！"],
        "pet_msg": ["嗯，舒服", "这还差不多", "可以"],
        "talk_msg": ["见到本大爷是你的荣幸！", "我是最棒的！", "臣服于本大爷吧！"],
        "mood_thoughts": {
            "happy": ["本大爷心情好！", "天下无双！", "膜拜本大爷吧！"],
            "love": ["算你走运！", "本大爷允许你喜欢我！", "这是你的荣幸！"],
            "hungry": ["还不快去准备食物！", "敢让本大爷饿着！", "快喂本大爷！"],
            "sad": ["哼！本大爷只是暂时...！", "这不重要！", "本大爷不需要！"],
            "excited": ["本大爷天下无敌！", "最强的就是我！", "颤抖吧凡人！"],
            "neutral": ["本大爷在想什么呢...", "无聊...太无敌了...", "寻找对手..."],
        }
    },
    "mysterious": {
        "name": "神秘",
        "emoji": "🔮",
        "feed_msg": ["...", "嗯", "可以"],
        "play_msg": ["...", "随便", "你开心就好"],
        "pet_msg": ["...", "嗯", "随意"],
        "talk_msg": ["...嗯", "...?", "...过来"],
        "mood_thoughts": {
            "happy": ["...", "嗯...不错", "...笑容"],
            "love": ["...命运...", "...连接...", "...永恒..."],
            "hungry": ["...饥饿...", "...需要...", "...能量..."],
            "sad": ["...孤独...", "...命运...", "...黑暗..."],
            "excited": ["...命运...！", "...觉醒...！", "...力量...！"],
            "neutral": ["...思考...", "...命运...", "...未来..."],
        }
    },
    "curious": {
        "name": "好奇",
        "emoji": "❓",
        "feed_msg": ["这是什么？好吃！", "嗯？新的食物！", "研究一下！"],
        "play_msg": ["这是什么？好好玩！", "那个是什么？", "让我看看！"],
        "pet_msg": ["嗯？舒服！", "这是什么？", "新感觉！"],
        "talk_msg": ["主人！那是什么？", "为什么？", "那个是什么？"],
        "mood_thoughts": {
            "happy": ["那个是什么？", "好有趣！", "去看看！"],
            "love": ["主人是什么？", "喜欢...为什么？", "想知道更多！"],
            "hungry": ["那个能吃吗？", "研究食物...", "饿了！"],
            "sad": ["为什么难过？", "研究一下...", "不懂..."],
            "excited": ["那个！！！", "好有趣！！！", "去看看去看！"],
            "neutral": ["那个是什么？", "思考...", "研究..."],
        }
    },
    "lazy": {
        "name": "懒惰",
        "emoji": "💤",
        "feed_msg": ["嗯...放那里吧", "好...麻烦", "吃...就吃"],
        "play_msg": ["不想动...", "好累...", "睡觉..."],
        "pet_msg": ["嗯...", "随便...", "别吵..."],
        "talk_msg": ["嗯...", "好困...", "不想动..."],
        "mood_thoughts": {
            "happy": ["睡觉...", "好吃...", "舒服..."],
            "love": ["嗯...喜欢...", "别吵...", "睡觉..."],
            "hungry": ["不想动...", "好麻烦...", "一会再吃..."],
            "sad": ["别理我...", "想睡觉...", "无聊..."],
            "excited": ["不想动...", "睡觉...", "别吵..."],
            "neutral": ["睡觉...", "好累...", "不想动..."],
        }
    },
    "independent": {
        "name": "独立",
        "emoji": "🏔️",
        "feed_msg": ["我自己来", "谢谢", "可以"],
        "play_msg": ["我自己玩", "不用管我", "我自己"],
        "pet_msg": ["嗯", "还行", "可以"],
        "talk_msg": ["嗯", "知道", "我自己可以"],
        "mood_thoughts": {
            "happy": ["自由！", "不错", "一个人也很好"],
            "love": ["嗯...谢谢", "知道了", "我会珍惜"],
            "hungry": ["自己找吃的", "独立...", "没问题"],
            "sad": ["没关系", "一个人也可以", "坚强..."],
            "excited": ["自由飞翔！", "一个人！", "去冒险！"],
            "neutral": ["思考...", "计划...", "独立..."],
        }
    },
}

# ========== 宠物DNA数据 ==========
# 重新设计的宠物 - 每种属性有独特的生物原型
# 12x12 像素画布，每种宠物有独特的可爱设计
PETS_DATA = {
    # ===== Normal 属性 =====
    "mimi": {
        "name_cn": "奶糖",
        "name_en": "Mimi",
        "element": "normal",
        "personality": "gentle",
        "desc": "一只温柔可爱的小猫咪",
        "pixel": [
            "    ░░░░    ",
            "  ░░▓▓▓▓░░  ",
            " ░░▓░░░▓▓░░ ",
            "░░▓░░░░░▓▓░░",
            "░░▓▓▓▓▓▓▓▓░░",
            "░░░░▓▓▓░░░░░",
            "░░░░▓▓▓░░░░░",
            " ░░▓▓▓▓▓░░ ",
            " ░░░░░░░░░░ ",
            "  ░░░░░░░░  ",
            "   ░░░░░░   ",
            "    ░░░░    ",
        ],
        "dna": {"hp": 80, "attack": 45, "defense": 50, "speed": 60, "luck": 70}
    },
    "cookie": {
        "name_cn": "饼干",
        "name_en": "Cookie",
        "element": "normal",
        "personality": "playful",
        "desc": "活泼好动的小花猫",
        "pixel": [
            "    ░░░░    ",
            "  ░░▓▓▓▓░░  ",
            " ░░▓░░░▓▓░░ ",
            "░░▓░░░░░▓▓░░",
            "░░▓▓▓▓▓▓▓▓░░",
            "░░░░▓▓▓░░░░░",
            "░░░░░▓▓░░░░░",
            " ░░░░▓▓░░░░ ",
            "  ░░░▓▓░░░░ ",
            "   ░░░░░░   ",
            "    ░░░░    ",
            "            ",
        ],
        "dna": {"hp": 78, "attack": 48, "defense": 48, "speed": 65, "luck": 68}
    },

    # ===== Fire 属性 =====
    "ember": {
        "name_cn": "小火",
        "name_en": "Ember",
        "element": "fire",
        "personality": "energetic",
        "desc": "尾巴尖燃烧着火焰的小狐狸",
        "pixel": [
            "    ░░░░░   ",
            "   ░░░░░░░  ",
            "  ░░░▓▓▓░░░ ",
            "  ░░▓▓▓▓▓░░ ",
            " ░░▓░░▓▓░░▓░",
            "░░▓░░░░░░▓▓░░",
            "░░░░░░░░░░░░░",
            " ░░░░░░░░░░ ",
            "  ░░░░░░░░  ",
            "   ░░░░░░   ",
            "    ░░░░    ",
            "            ",
        ],
        "dna": {"hp": 75, "attack": 65, "defense": 40, "speed": 70, "luck": 55}
    },
    "flame": {
        "name_cn": "焰尾",
        "name_en": "Flame",
        "element": "fire",
        "personality": "brave",
        "desc": "全身环绕着火焰的烈焰狐狸",
        "pixel": [
            "  ░░░░░░░░░  ",
            " ░░░░░░░░░░░ ",
            "░░░░▓▓▓▓▓░░░░",
            "░░░▓▓▓▓▓▓▓░░░",
            "░░▓░░▓▓▓▓░░▓░",
            "░░▓░░░░░░░▓▓░░",
            "░░░░▓▓░░▓░░░░",
            " ░░░▓▓▓▓░░░░ ",
            "  ░░░░░░░░░  ",
            "   ░░░░░░░   ",
            "    ░░░░    ",
            "            ",
        ],
        "dna": {"hp": 85, "attack": 80, "defense": 50, "speed": 75, "luck": 50}
    },

    # ===== Water 属性 =====
    "droplet": {
        "name_cn": "水滴",
        "name_en": "Droplet",
        "element": "water",
        "personality": "gentle",
        "desc": "用水做的蓝色小水獭",
        "pixel": [
            "    ░░░░░   ",
            "   ░░░░░░░  ",
            "  ░░░░░░░░░ ",
            "  ░░▓▓▓▓░░░ ",
            " ░░▓▓▓▓▓▓░░░",
            "░░▓░░░░░░▓▓░░",
            "░░░░░░░░░░░░░",
            " ░░░░░░░░░░░ ",
            " ░░░░░░░░░░░ ",
            "  ░░░░░░░░░  ",
            "   ░░░░░░   ",
            "            ",
        ],
        "dna": {"hp": 85, "attack": 50, "defense": 55, "speed": 65, "luck": 60}
    },
    "splash": {
        "name_cn": "水花",
        "name_en": "Splash",
        "element": "water",
        "personality": "cheerful",
        "desc": "喜欢玩水的活泼水獭",
        "pixel": [
            "   ░░░░░░░░  ",
            "  ░░░░░░░░░░ ",
            "  ░░▓▓▓▓▓░░░ ",
            " ░░▓▓▓▓▓▓▓░░░",
            "░░▓░░░░░░▓▓░░░",
            "░░░░░░░░░░░░░░",
            " ░░░▓▓▓░░░░░░",
            "  ░░░▓▓░░░░░ ",
            "  ░░░░░░░░░░░ ",
            "   ░░░░░░░░   ",
            "    ░░░░░░    ",
            "            ",
        ],
        "dna": {"hp": 90, "attack": 55, "defense": 60, "speed": 70, "luck": 65}
    },

    # ===== Grass 属性 =====
    "sprout": {
        "name_cn": "嫩芽",
        "name_en": "Sprout",
        "element": "grass",
        "personality": "calm",
        "desc": "头顶嫩叶的绿色小精灵",
        "pixel": [
            "     ░░░░    ",
            "    ░░░░░░   ",
            "   ░░░▓░░░░  ",
            "  ░░░▓▓░░░░░ ",
            "  ░░░▓░░░░░░░",
            " ░░░░░░░░░░░░",
            "░░░▓▓▓▓▓▓▓▓░░",
            "░░▓▓▓▓▓▓▓▓▓░░",
            " ░░░░░░░░░░░░",
            "  ░░░░░░░░░░░",
            "   ░░░░░░░░   ",
            "            ",
        ],
        "dna": {"hp": 80, "attack": 50, "defense": 60, "speed": 55, "luck": 65}
    },
    "bloossom": {
        "name_cn": "花开了",
        "name_en": "Bloossom",
        "element": "grass",
        "personality": "kind",
        "desc": "身体开满鲜花的精灵",
        "pixel": [
            "   ░░░░░░░░░  ",
            "  ░░░▓▓░░░░░░ ",
            "  ░░▓▓▓▓░░░░░░",
            "  ░░▓▓░░░░░░░░",
            " ░░░░░░░░░░░░░",
            "░░▓▓▓▓▓▓▓▓▓▓░░",
            "░░▓▓▓▓▓▓▓▓▓▓░░",
            " ░░░░░░░░░░░░░",
            "  ░░░░░░░░░░░ ",
            "   ░░░░░░░░   ",
            "    ░░░░░░    ",
            "            ",
        ],
        "dna": {"hp": 95, "attack": 60, "defense": 75, "speed": 60, "luck": 80}
    },

    # ===== Electric 属性 =====
    "sparky": {
        "name_cn": "小电",
        "name_en": "Sparky",
        "element": "electric",
        "personality": "cheerful",
        "desc": "全身充满电的小老鼠",
        "pixel": [
            "     ░░░░    ",
            "    ░░░░░░   ",
            "   ░░░░░░░░░  ",
            "  ░░░░▓▓░░░░░ ",
            " ░░░░▓▓▓░░░░░░",
            "░░░░░░░░░░░░░░░",
            "░░░░▓▓▓▓▓▓░░░░",
            "░░░░▓▓▓▓▓▓░░░░",
            " ░░░░░░░░░░░░░",
            "  ░░░░░░░░░░░░",
            "   ░░░░░░░░   ",
            "            ",
        ],
        "dna": {"hp": 70, "attack": 70, "defense": 40, "speed": 85, "luck": 50}
    },
    "volt": {
        "name_cn": "伏特",
        "name_en": "Volt",
        "element": "electric",
        "personality": "energetic",
        "desc": "闪电环绕的电力鼠王",
        "pixel": [
            "  ░░░░░░░░░░░  ",
            " ░░░░░░░░░░░░░ ",
            "░░░░░▓▓▓▓░░░░░░",
            "░░░░░▓▓▓▓░░░░░░",
            "░░░░░░░░░░░░░░░░",
            "░░░░▓▓▓▓▓▓▓░░░░",
            "░░░░▓▓▓▓▓▓▓░░░░",
            "░░░░░░░░░░░░░░░░",
            " ░░░░░░░░░░░░░ ",
            "  ░░░░░░░░░░░░  ",
            "   ░░░░░░░░░░   ",
            "            ",
        ],
        "dna": {"hp": 80, "attack": 85, "defense": 50, "speed": 95, "luck": 55}
    },

    # ===== Ice 属性 =====
    "frost": {
        "name_cn": "小冰",
        "name_en": "Frost",
        "element": "ice",
        "personality": "shy",
        "desc": "全身冰蓝色的小企鹅",
        "pixel": [
            "    ░░░░░    ",
            "   ░░░░░░░   ",
            "  ░░░▓▓▓░░░░  ",
            "  ░░▓▓▓▓▓░░░░ ",
            " ░░░░░▓▓░░░░░░ ",
            "░░░░░░░░░░░░░░░",
            "░░▓▓▓▓▓▓▓▓▓▓░░",
            "░░▓▓▓▓▓▓▓▓▓▓░░",
            "░░░░░░░░░░░░░░░",
            " ░░░░░░░░░░░░░",
            "  ░░░░░░░░░░░░",
            "   ░░░░░░░░   ",
        ],
        "dna": {"hp": 80, "attack": 45, "defense": 60, "speed": 55, "luck": 75}
    },
    "blizzard": {
        "name_cn": "寒霜",
        "name_en": "Blizzard",
        "element": "ice",
        "personality": "proud",
        "desc": "冰雪环绕的冰霜企鹅",
        "pixel": [
            "  ░░░░░░░░░░░  ",
            " ░░░░░░░░░░░░░ ",
            "░░░░░▓▓▓▓░░░░░░",
            "░░░░▓▓▓▓▓▓░░░░░",
            "░░░░░░▓▓░░░░░░░",
            "░░░░░░░░░░░░░░░░",
            "░░░▓▓▓▓▓▓▓▓▓░░░",
            "░░░▓▓▓▓▓▓▓▓▓░░░",
            "░░░░░░░░░░░░░░░░",
            " ░░░░░░░░░░░░░ ",
            "  ░░░░░░░░░░░░  ",
            "   ░░░░░░░░░   ",
        ],
        "dna": {"hp": 95, "attack": 55, "defense": 80, "speed": 65, "luck": 80}
    },

    # ===== Dark 属性 =====
    "shadow": {
        "name_cn": "暗影",
        "name_en": "Shadow",
        "element": "dark",
        "personality": "shy",
        "desc": "全身漆黑的幽灵猫",
        "pixel": [
            "            ",
            "   ░░░░░░░   ",
            "  ░░░░░░░░░░  ",
            " ░░░░▓▓▓░░░░░ ",
            "░░░░▓▓▓▓▓░░░░░",
            "░░░░░░░░░░░░░░░",
            "░░▓░░░░░░▓▓░░░",
            "░░▓▓░░░░▓▓▓░░░",
            "░░░░░░░░░░░░░░░",
            " ░░░░░░░░░░░░░",
            "  ░░░░░░░░░░░░",
            "            ",
        ],
        "dna": {"hp": 75, "attack": 60, "defense": 45, "speed": 75, "luck": 40}
    },
    "nightmare": {
        "name_cn": "梦魇",
        "name_en": "Nightmare",
        "element": "dark",
        "personality": "mysterious",
        "desc": "掌控噩梦的暗影王者",
        "pixel": [
            "  ░░░░░░░░░░░  ",
            " ░░░░░░░░░░░░░ ",
            "░░░░░▓▓▓▓░░░░░░",
            "░░░░▓▓▓▓▓▓░░░░░",
            "░░░░░░░░░░░░░░░░",
            "░░░░▓▓░░▓▓░░░░░",
            "░░░░▓▓▓▓▓▓░░░░░",
            "░░░░░░░░░░░░░░░░",
            " ░░░░░░░░░░░░░ ",
            "  ░░░░░░░░░░░░  ",
            "   ░░░░░░░░░   ",
            "            ",
        ],
        "dna": {"hp": 90, "attack": 85, "defense": 60, "speed": 80, "luck": 45}
    },

    # ===== Light 属性 =====
    "star": {
        "name_cn": "星光",
        "name_en": "Star",
        "element": "light",
        "personality": "gentle",
        "desc": "全身散发着柔和光芒的小天使",
        "pixel": [
            "     ░░░░    ",
            "   ░░░░░░░   ",
            "  ░░░░░░░░░  ",
            "  ░░▓▓▓▓░░░  ",
            " ░░░▓▓▓▓░░░░░",
            "░░░░░░░░░░░░░░",
            "░░░░░░░░░░░░░░",
            "░░░░░░░░░░░░░░",
            " ░░░░░░░░░░░░ ",
            "  ░░░░░░░░░░░ ",
            "   ░░░░░░░░   ",
            "            ",
        ],
        "dna": {"hp": 85, "attack": 45, "defense": 55, "speed": 60, "luck": 80}
    },
    "lumina": {
        "name_cn": "光辉",
        "name_en": "Lumina",
        "element": "light",
        "personality": "kind",
        "desc": "拥有神圣光芒的光之天使",
        "pixel": [
            "  ░░░░░░░░░░░  ",
            " ░░░░░░░░░░░░░ ",
            "░░░░░░▓▓░░░░░░░",
            "░░░░░▓▓▓▓░░░░░░",
            "░░░░░░░░░░░░░░░░",
            "░░░░░░░░░░░░░░░░",
            "░░░░░░░░░░░░░░░░",
            "░░░░░░░░░░░░░░░░",
            " ░░░░░░░░░░░░░ ",
            "  ░░░░░░░░░░░░  ",
            "   ░░░░░░░░░   ",
            "            ",
        ],
        "dna": {"hp": 100, "attack": 55, "defense": 70, "speed": 70, "luck": 95}
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

# ========== 属性相克系统 ==========
TYPE_CHART = {
    "fire": {"weak": ["water", "earth"], "strong": ["grass", "ice"]},
    "water": {"weak": ["electric", "grass"], "strong": ["fire", "earth"]},
    "grass": {"weak": ["fire", "ice"], "strong": ["water", "earth"]},
    "electric": {"weak": ["dark"], "strong": ["water", "flying"]},
    "dark": {"weak": ["light", "fairy"], "strong": ["psychic", "ghost"]},
    "light": {"weak": ["dark", "shadow"], "strong": ["dark", "shadow"]},
    "normal": {"weak": [], "strong": []},
    "flying": {"weak": ["electric", "ice"], "strong": ["grass", "fighting"]},
    "ice": {"weak": ["fire", "fighting", "rock"], "strong": ["grass", "flying", "dragon"]},
    "fighting": {"weak": ["flying", "psychic", "fairy"], "strong": ["normal", "dark", "ice"]},
    "psychic": {"weak": ["dark", "ghost", "shadow"], "strong": ["fighting", "poison"]},
    "ghost": {"weak": ["light", "ghost"], "strong": ["psychic", "ghost"]},
    "earth": {"weak": ["water", "grass", "ice"], "strong": ["fire", "electric", "poison", "rock"]},
    "poison": {"weak": ["psychic", "ground"], "strong": ["grass", "fairy"]},
    "rock": {"weak": ["water", "grass", "fighting", "ground", "steel"], "strong": ["fire", "ice", "flying", "bug"]},
    "steel": {"weak": ["fire", "fighting", "ground"], "strong": ["ice", "rock", "fairy"]},
    "dragon": {"weak": ["ice", "dragon", "fairy"], "strong": ["fire", "water", "electric", "grass"]},
    "fairy": {"weak": ["poison", "steel"], "strong": ["fighting", "dark", "dragon"]},
    "flower": {"weak": ["fire", "ice", "poison", "shadow"], "strong": ["water", "earth"]},
    "shadow": {"weak": ["light", "fire"], "strong": ["psychic", "ghost"]},
}

def get_type_effectiveness(attack_type, defense_type):
    """获取属性相克效果"""
    if defense_type not in TYPE_CHART:
        return 1.0
    defense_chart = TYPE_CHART[defense_type]
    if attack_type in defense_chart.get("strong", []):
        return 2.0
    if attack_type in defense_chart.get("weak", []):
        return 0.5
    return 1.0

# ========== 技能数据 ==========
SKILLS_DATA = {
    # 普通技能
    "scratch": {"name": "抓挠", "type": "attack", "power": 20, "element": "normal", "pp": 35, "desc": "普通的物理攻击"},
    "tackle": {"name": "撞击", "type": "attack", "power": 25, "element": "normal", "pp": 30, "desc": "冲撞对手"},
    "quick_attack": {"name": "电光一闪", "type": "attack", "power": 25, "element": "normal", "pp": 30, "desc": "快速攻击"},
    "bite": {"name": "咬住", "type": "attack", "power": 30, "element": "normal", "pp": 25, "desc": "用牙齿咬住"},

    # 火系技能
    "ember": {"name": "火花", "type": "attack", "power": 30, "element": "fire", "pp": 25, "desc": "喷出小型火焰"},
    "fireball": {"name": "火球", "type": "attack", "power": 40, "element": "fire", "pp": 20, "desc": "发射火球"},
    "flame_thrower": {"name": "烈焰喷射", "type": "attack", "power": 50, "element": "fire", "pp": 15, "desc": "喷射剧烈火焰"},
    "inferno": {"name": "燃烧殆尽", "type": "attack", "power": 65, "element": "fire", "pp": 10, "desc": "让对手陷入燃烧"},

    # 水系技能
    "water_gun": {"name": "水枪", "type": "attack", "power": 30, "element": "water", "pp": 25, "desc": "喷出水枪"},
    "bubble_beam": {"name": "泡沫光线", "type": "attack", "power": 40, "element": "water", "pp": 20, "desc": "发射泡沫"},
    "hydro_pump": {"name": "水炮", "type": "attack", "power": 55, "element": "water", "pp": 10, "desc": "强力水系攻击"},
    "surf": {"name": "冲浪", "type": "attack", "power": 45, "element": "water", "pp": 15, "desc": "利用波浪攻击"},

    # 草系技能
    "vine_whip": {"name": "藤鞭", "type": "attack", "power": 30, "element": "grass", "pp": 25, "desc": "伸长藤鞭攻击"},
    "razor_leaf": {"name": "飞叶快刀", "type": "attack", "power": 40, "element": "grass", "pp": 20, "desc": "发射锋利叶片"},
    "solar_beam": {"name": "日光束", "type": "attack", "power": 60, "element": "grass", "pp": 10, "desc": "收集阳光发射"},
    "leaf_storm": {"name": "叶风暴", "type": "attack", "power": 55, "element": "grass", "pp": 10, "desc": "叶片龙卷风"},

    # 电系技能
    "thunder_shock": {"name": "电击", "type": "attack", "power": 30, "element": "electric", "pp": 30, "desc": "轻微电击"},
    "thunderbolt": {"name": "十万伏特", "type": "attack", "power": 45, "element": "electric", "pp": 15, "desc": "强力电击"},
    "thunder": {"name": "雷电", "type": "attack", "power": 60, "element": "electric", "pp": 10, "desc": "召唤雷电"},
    "volttackle": {"name": "电光一闪", "type": "attack", "power": 70, "element": "electric", "pp": 5, "desc": "闪电冲击"},

    # 冰系技能
    "ice_shard": {"name": "冰砾", "type": "attack", "power": 25, "element": "ice", "pp": 30, "desc": "发射冰碎片"},
    "ice_beam": {"name": "冰冻光束", "type": "attack", "power": 45, "element": "ice", "pp": 15, "desc": "冰冻光线"},
    "blizzard": {"name": "暴风雪", "type": "attack", "power": 60, "element": "ice", "pp": 10, "desc": "猛烈寒风"},
    "aurora_beam": {"name": "极光光束", "type": "attack", "power": 45, "element": "ice", "pp": 15, "desc": "美丽的极光攻击"},

    # 飞行系技能
    "wing_attack": {"name": "翅膀攻击", "type": "attack", "power": 35, "element": "flying", "pp": 25, "desc": "用翅膀拍打"},
    "aerial_ace": {"name": "燕返", "type": "attack", "power": 40, "element": "flying", "pp": 20, "desc": "敏捷的空中攻击"},
    "sky_attack": {"name": "天空攻击", "type": "attack", "power": 55, "element": "flying", "pp": 10, "desc": "从天空俯冲"},

    # 地面系技能
    "earthquake": {"name": "地震", "type": "attack", "power": 60, "element": "earth", "pp": 10, "desc": "强烈地震"},
    "rock_tomb": {"name": "岩石封闭", "type": "attack", "power": 40, "element": "rock", "pp": 15, "desc": "投掷岩石"},
    "mud_slap": {"name": "泥巴炸弹", "type": "attack", "power": 30, "element": "earth", "pp": 25, "desc": "投掷泥巴"},

    # 格斗系技能
    "karate_chop": {"name": "空手劈", "type": "attack", "power": 35, "element": "fighting", "pp": 25, "desc": "手刀攻击"},
    "double_kick": {"name": "二段踢", "type": "attack", "power": 45, "element": "fighting", "pp": 20, "desc": "连续踢击"},
    "mega_punch": {"name": "百万吨拳击", "type": "attack", "power": 55, "element": "fighting", "pp": 10, "desc": "强力拳击"},

    # 超能力系技能
    "psybeam": {"name": "幻象光线", "type": "attack", "power": 40, "element": "psychic", "pp": 20, "desc": "奇异光线"},
    "psychic": {"name": "精神强念", "type": "attack", "power": 55, "element": "psychic", "pp": 10, "desc": "超能力攻击"},
    "rest": {"name": "睡觉", "type": "heal", "power": 0, "element": "psychic", "pp": 10, "desc": "恢复体力"},

    # 幽灵系技能
    "shadow_ball": {"name": "暗影球", "type": "attack", "power": 50, "element": "dark", "pp": 15, "desc": "暗影能量球"},
    "night_shade": {"name": "噩梦", "type": "attack", "power": 45, "element": "shadow", "pp": 15, "desc": "噩梦攻击"},

    # 光系技能
    "flash": {"name": "闪光", "type": "attack", "power": 30, "element": "light", "pp": 25, "desc": "刺眼光芒"},
    "sunbeam": {"name": "阳光烈焰", "type": "attack", "power": 50, "element": "light", "pp": 10, "desc": "聚集阳光"},

    # 龙系技能
    "dragon_rage": {"name": "龙之怒", "type": "attack", "power": 50, "element": "dragon", "pp": 10, "desc": "愤怒的龙息"},
    "dragon_claw": {"name": "龙爪", "type": "attack", "power": 50, "element": "dragon", "pp": 15, "desc": "锋利的龙爪"},

    # 毒系技能
    "poison_sting": {"name": "毒针", "type": "attack", "power": 25, "element": "poison", "pp": 30, "desc": "注射毒液"},
    "sludge_bomb": {"name": "污泥炸弹", "type": "attack", "power": 50, "element": "poison", "pp": 15, "desc": "投掷毒泥"},

    # 防御技能
    "defense_curl": {"name": "缩壳", "type": "defense", "power": 0, "element": "normal", "pp": 40, "desc": "提高防御"},
    "shield": {"name": "护盾", "type": "defense", "power": 0, "element": "normal", "pp": 20, "desc": "使用护盾"},
    "dodge": {"name": "闪避", "type": "defense", "power": 0, "element": "normal", "pp": 25, "desc": "回避攻击"},
    "light_screen": {"name": "光墙", "type": "defense", "power": 0, "element": "light", "pp": 15, "desc": "反射特殊攻击"},

    # 恢复技能
    "heal": {"name": "治愈", "type": "heal", "power": 0, "element": "normal", "pp": 20, "desc": "恢复体力"},
    "recover": {"name": "自我再生", "type": "heal", "power": 0, "element": "normal", "pp": 10, "desc": "大量恢复"},
    "drain": {"name": "吸取", "type": "heal", "power": 20, "element": "grass", "pp": 15, "desc": "吸取体力"},
    "drain_life": {"name": "生命吸取", "type": "heal", "power": 30, "element": "dark", "pp": 10, "desc": "吸取对手生命"},

    # 增益技能
    "growl": {"name": "叫声", "type": "debuff", "power": 0, "element": "normal", "pp": 40, "desc": "降低对手攻击"},
    "tail_whip": {"name": "摇尾巴", "type": "debuff", "power": 0, "element": "normal", "pp": 30, "desc": "降低对手防御"},
    "screech": {"name": "刺耳声", "type": "debuff", "power": 0, "element": "normal", "pp": 40, "desc": "大幅降低防御"},
    "charm": {"name": "撒骄", "type": "buff", "power": 0, "element": "fairy", "pp": 20, "desc": "降低对手攻击"},
    "swords_dance": {"name": "剑舞", "type": "buff", "power": 0, "element": "normal", "pp": 20, "desc": "大幅提升攻击"},
}

# ========== 宠物初始技能 (根据属性和阶段) ==========
PET_STARTING_SKILLS = {
    # Normal
    "mimi": ["scratch", "tackle", "defense_curl", "heal"],
    "cookie": ["scratch", "quick_attack", "bite", "defense_curl"],
    # Fire
    "ember": ["scratch", "ember", "growl", "defense_curl"],
    "flame": ["scratch", "fireball", "flame_thrower", "growl"],
    # Water
    "droplet": ["scratch", "water_gun", "defense_curl", "heal"],
    "splash": ["scratch", "bubble_beam", "surf", "hydro_pump"],
    # Grass
    "sprout": ["scratch", "vine_whip", "growl", "heal"],
    "bloossom": ["scratch", "razor_leaf", "leaf_storm", "drain"],
    # Electric
    "sparky": ["scratch", "thunder_shock", "quick_attack", "defense_curl"],
    "volt": ["scratch", "thunderbolt", "thunder", "volttackle"],
    # Ice
    "frost": ["scratch", "ice_shard", "defense_curl", "heal"],
    "blizzard": ["scratch", "ice_beam", "blizzard", "aurora_beam"],
    # Dark
    "shadow": ["scratch", "bite", "shadow_ball", "dodge"],
    "nightmare": ["scratch", "shadow_ball", "night_shade", "dragon_rage"],
    # Light
    "star": ["scratch", "flash", "heal", "recover"],
    "lumina": ["scratch", "sunbeam", "solar_beam", "recover"],
}

# ========== 进化形态技能 ==========
EVOLUTION_SKILLS = {
    # Normal 进化
    "mimi": ["scratch", "quick_attack", "swords_dance", "recover"],
    "cookie": ["scratch", "bite", "slash", "dragon_claw"],
    # Fire 进化
    "ember": ["scratch", "flame_thrower", "inferno", "dragon_claw"],
    "flame": ["scratch", "flame_thrower", "inferno", "earthquake"],
    # Water 进化
    "droplet": ["scratch", "hydro_pump", "surf", "bubble_beam"],
    "splash": ["scratch", "hydro_pump", "surf", "blizzard"],
    # Grass 进化
    "sprout": ["scratch", "leaf_storm", "solar_beam", "drain"],
    "bloossom": ["scratch", "leaf_storm", "solar_beam", "recover"],
    # Electric 进化
    "sparky": ["scratch", "thunderbolt", "thunder", "volttackle"],
    "volt": ["scratch", "thunderbolt", "thunder", "dragon_claw"],
    # Ice 进化
    "frost": ["scratch", "ice_beam", "blizzard", "aurora_beam"],
    "blizzard": ["scratch", "blizzard", "ice_beam", "solar_beam"],
    # Dark 进化
    "shadow": ["scratch", "shadow_ball", "night_shade", "dragon_claw"],
    "nightmare": ["scratch", "shadow_ball", "night_shade", "psychic"],
    # Light 进化
    "star": ["scratch", "sunbeam", "solar_beam", "recover"],
    "lumina": ["scratch", "sunbeam", "solar_beam", "psychic"],
}

# ========== 进化系统 (简化版，兼容旧代码) ==========
EVOLUTIONS = {
    "mimi": {"next": "cookie", "level": 10, "name": "奶球"},
    "cookie": {"next": "mimi", "level": 20, "name": "花纹猫"},
    "ember": {"next": "flame", "level": 10, "name": "焰尾"},
    "droplet": {"next": "splash", "level": 10, "name": "水花"},
    "sprout": {"next": "bloossom", "level": 10, "name": "花开了"},
    "sparky": {"next": "volt", "level": 10, "name": "伏特"},
    "frost": {"next": "blizzard", "level": 10, "name": "寒霜"},
    "shadow": {"next": "nightmare", "level": 10, "name": "梦魇"},
    "star": {"next": "lumina", "level": 10, "name": "光辉"},
}

# ========== 多阶段进化链 (Digimon风格) ==========
# Baby → Child → Adult → Perfect → Ultimate
EVOLUTION_CHAINS = {
    # 奶糖系 (Normal)
    "mimi": {
        "baby": {"name": "奶糖", "level": 1, "dna_mult": 0.8},
        "child": {"name": "奶球", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "奶油猫", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "绒毛王子", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "云绒狮王", "level": 50, "dna_mult": 2.0},
    },
    "cookie": {
        "baby": {"name": "饼干", "level": 1, "dna_mult": 0.8},
        "child": {"name": "曲奇", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "花纹猫", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "斑点虎", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "猎影豹", "level": 50, "dna_mult": 2.0},
    },
    # 小火系 (Fire)
    "ember": {
        "baby": {"name": "小火", "level": 1, "dna_mult": 0.8},
        "child": {"name": "焰尾", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "烈焰狐", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "炎狱魔狐", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "九尾炎帝", "level": 50, "dna_mult": 2.0},
    },
    "flame": {
        "baby": {"name": "焰尾", "level": 1, "dna_mult": 0.8},
        "child": {"name": "烈焰", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "火焰雄狮", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "炎狱雄狮", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "烈焰麒麟", "level": 50, "dna_mult": 2.0},
    },
    # 水滴系 (Water)
    "droplet": {
        "baby": {"name": "水滴", "level": 1, "dna_mult": 0.8},
        "child": {"name": "水花", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "水獭王", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "海浪巨兽", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "深海龙王", "level": 50, "dna_mult": 2.0},
    },
    "splash": {
        "baby": {"name": "水花", "level": 1, "dna_mult": 0.8},
        "child": {"name": "浪潮", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "海豚精灵", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "风暴海豚", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "海神波塞冬", "level": 50, "dna_mult": 2.0},
    },
    # 嫩芽系 (Grass)
    "sprout": {
        "baby": {"name": "嫩芽", "level": 1, "dna_mult": 0.8},
        "child": {"name": "小绿", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "花精灵", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "森林守护者", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "自然之神", "level": 50, "dna_mult": 2.0},
    },
    "bloossom": {
        "baby": {"name": "花开了", "level": 1, "dna_mult": 0.8},
        "child": {"name": "花簇", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "花园仙子", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "花语精灵", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "花之女王", "level": 50, "dna_mult": 2.0},
    },
    # 小电系 (Electric)
    "sparky": {
        "baby": {"name": "小电", "level": 1, "dna_mult": 0.8},
        "child": {"name": "电光", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "雷鼠", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "闪电战鼠", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "雷电王", "level": 50, "dna_mult": 2.0},
    },
    "volt": {
        "baby": {"name": "伏特", "level": 1, "dna_mult": 0.8},
        "child": {"name": "特斯拉", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "电光龙", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "雷鸣兽", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "雷霆巨兽", "level": 50, "dna_mult": 2.0},
    },
    # 小冰系 (Ice)
    "frost": {
        "baby": {"name": "小冰", "level": 1, "dna_mult": 0.8},
        "child": {"name": "冰晶", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "冰企鹅", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "寒霜使者", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "冰雪女王", "level": 50, "dna_mult": 2.0},
    },
    "blizzard": {
        "baby": {"name": "寒霜", "level": 1, "dna_mult": 0.8},
        "child": {"name": "暴雪", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "极地巨兽", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "冰原之王", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "冰雪巨龙", "level": 50, "dna_mult": 2.0},
    },
    # 暗影系 (Dark)
    "shadow": {
        "baby": {"name": "暗影", "level": 1, "dna_mult": 0.8},
        "child": {"name": "幽灵", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "梦魇兽", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "暗夜魔君", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "毁灭之神", "level": 50, "dna_mult": 2.0},
    },
    "nightmare": {
        "baby": {"name": "梦魇", "level": 1, "dna_mult": 0.8},
        "child": {"name": "噩梦", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "恐惧恶魔", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "阴影主宰", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "暗黑帝王", "level": 50, "dna_mult": 2.0},
    },
    # 星光系 (Light)
    "star": {
        "baby": {"name": "星光", "level": 1, "dna_mult": 0.8},
        "child": {"name": "流星", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "光之天使", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "光明使者", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "太阳神", "level": 50, "dna_mult": 2.0},
    },
    "lumina": {
        "baby": {"name": "光辉", "level": 1, "dna_mult": 0.8},
        "child": {"name": "光束", "level": 5, "dna_mult": 1.0},
        "adult": {"name": "独角兽", "level": 15, "dna_mult": 1.3},
        "perfect": {"name": "神圣独角兽", "level": 30, "dna_mult": 1.6},
        "ultimate": {"name": "神圣之光", "level": 50, "dna_mult": 2.0},
    },
}

# 进化条件检查
def check_evolution_conditions(pet):
    """检查进化条件"""
    chain = EVOLUTION_CHAINS.get(pet.species)
    if not chain:
        return None

    # 根据当前阶段检查下一阶段
    stage_order = ["baby", "child", "adult", "perfect", "ultimate"]
    current_idx = stage_order.index(pet.evolution_stage) if pet.evolution_stage in stage_order else 0

    if current_idx >= len(stage_order) - 1:
        return None  # 已达到最高阶段

    next_stage = stage_order[current_idx + 1]
    next_info = chain.get(next_stage)

    # 检查等级
    if pet.level < next_info["level"]:
        return None

    # 检查亲密度 (需要50以上)
    if pet.love < 50 and next_stage in ["adult", "perfect"]:
        return None

    return next_stage, next_info


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
    "coral": {
        "name_cn": "珊瑚",
        "name_en": "Coral",
        "element": "water",
        "pixel": [
            "  ░░▓▓░░  ",
            " ░░▓▓▓▓░░ ",
            "░░▓▓░░▓▓░░",
            "░░▓▓▓▓▓▓░░",
            "░░░░▓▓░░░░",
            " ░░░░▓▓░░ ",
            "  ░░░░░░  ",
            "   ░░░░   ",
        ],
        "dna": {"hp": 115, "attack": 70, "defense": 80, "speed": 75, "luck": 80}
    },
    "sakura": {
        "name_cn": "樱花",
        "name_en": "Sakura",
        "element": "flower",
        "pixel": [
            "  ░░▓░░░  ",
            " ░▓▓▓▓▓░░ ",
            "░▓░░░░░▓░░",
            "░░▓▓▓▓▓░░░",
            "░░░░▓▓░░░░",
            " ░░░░▓▓░░ ",
            "  ░░░░░░  ",
            "   ░░░░   ",
        ],
        "dna": {"hp": 105, "attack": 65, "defense": 75, "speed": 70, "luck": 90}
    },
    "thunder": {
        "name_cn": "雷霆",
        "name_en": "Thunder",
        "element": "electric",
        "pixel": [
            "  ░░░░░░  ",
            " ░░▓▓▓▓░░ ",
            "░░▓░░░▓░░░",
            "░░▓▓▓▓▓░░░",
            "░░░░▓▓░░░░",
            " ░░░▓▓░░░ ",
            "  ░░░░░░░ ",
            "   ░█░█   ",
        ],
        "dna": {"hp": 100, "attack": 95, "defense": 55, "speed": 110, "luck": 65}
    },
    "chaos": {
        "name_cn": "混沌",
        "name_en": "Chaos",
        "element": "dark",
        "pixel": [
            "  ░░░░░░░ ",
            " ░░▓▓▓▓░░ ",
            "░░▓▓░░▓▓░░",
            "░░░░▓▓░░░░",
            "░░▓▓░░▓▓░░",
            " ░░▓▓▓▓░░ ",
            "  ░░░░░░  ",
            "   ░░░░   ",
        ],
        "dna": {"hp": 115, "attack": 100, "defense": 65, "speed": 95, "luck": 50}
    },
    "dawn": {
        "name_cn": "晨曦",
        "name_en": "Dawn",
        "element": "light",
        "pixel": [
            "  ░░░░░░  ",
            " ░▓▓▓▓▓░░ ",
            "░▓░░░░░▓░░",
            "░░▓▓▓▓▓░░░",
            "░░░░░░░░░░░",
            " ░░░░░░░░ ",
            "  ░░░░░░  ",
            "   ░░░░   ",
        ],
        "dna": {"hp": 110, "attack": 75, "defense": 70, "speed": 85, "luck": 95}
    },
    "charcoal": {
        "name_cn": "炭仔",
        "name_en": "Charcoal",
        "element": "dark",
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
        "dna": {"hp": 120, "attack": 80, "defense": 90, "speed": 50, "luck": 70}
    },
    "frost": {
        "name_cn": "霜霜",
        "name_en": "Frost",
        "element": "ice",
        "pixel": [
            "  ░░░░░░  ",
            " ░░▓▓▓▓░░ ",
            "░░▓░░░▓░░░",
            "░░░░▓▓░░░░",
            "░░▓░░░▓░░░",
            " ░░▓▓▓▓░░ ",
            "  ░░░░░░  ",
            "   ░░░░   ",
        ],
        "dna": {"hp": 110, "attack": 60, "defense": 80, "speed": 70, "luck": 85}
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

        # 性格
        self.personality_type = data.get("personality", "gentle")
        self.personality = PERSONALITIES.get(self.personality_type, PERSONALITIES["gentle"])

        # 技能
        self.skills = self.get_starting_skills()
        self.skill_pp = {skill: SKILLS_DATA[skill]["pp"] for skill in self.skills}

        # 进化阶段
        self.evolution_stage = "baby"  # baby, child, adult, perfect, ultimate

        self.add_memory("出生了！")

    def get_starting_skills(self):
        """获取初始技能"""
        # 先检查进化形态技能
        if self.species in EVOLUTION_SKILLS:
            return EVOLUTION_SKILLS[self.species].copy()
        # 再检查基础技能
        if self.species in PET_STARTING_SKILLS:
            return PET_STARTING_SKILLS[self.species].copy()
        # 默认技能
        return ["scratch", "tackle", "defense_curl", "heal"]

    def get_element(self):
        """获取宠物属性"""
        # 先检查进化形态
        if self.species in EVOLUTION_FORMS:
            return EVOLUTION_FORMS[self.species].get("element", PETS_DATA.get(self.species, {}).get("element", "normal"))
        return PETS_DATA.get(self.species, {}).get("element", "normal")

    def get_skill_info(self, skill_id):
        """获取技能信息"""
        return SKILLS_DATA.get(skill_id, {})

    def show_skills(self):
        """显示宠物技能"""
        print("\n" + "="*40)
        print(f"🎯 {self.name} 的技能")
        print("="*40)
        for i, skill_id in enumerate(self.skills):
            skill = SKILLS_DATA.get(skill_id)
            if skill:
                pp = self.skill_pp.get(skill_id, 0)
                type_emoji = {"fire": "🔥", "water": "💧", "grass": "🌿", "electric": "⚡",
                            "ice": "❄️", "flying": "🕊️", "earth": "🪨", "fighting": "🥊",
                            "psychic": "🔮", "ghost": "👻", "dark": "🌑", "light": "✨",
                            "normal": "⬜", "poison": "☠️", "rock": "🪨", "dragon": "🐉",
                            "fairy": "🧚", "flower": "🌸", "shadow": "💫"}
                type_ico = type_emoji.get(skill["element"], "⬜")
                print(f"  {i+1}. {skill['name']} {type_ico}")
                print(f"     类型: {skill['element']} | PP: {pp}/{skill['pp']}")
                print(f"     效果: {skill['desc']}")
        print("="*40)

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
        # 更新想法 - 使用性格化的想法
        mood_thoughts = self.personality.get("mood_thoughts", {}).get(self.mood, ["..."])
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

    def feed(self, food_power=20):
        """喂食"""
        self.hunger = min(100, self.hunger + food_power)
        self.happiness = min(100, self.happiness + 5)
        self.stats["feed_count"] += 1
        self.stats["total_interactions"] += 1
        self.add_memory("吃了美味的食物")
        # 性格化回复
        feed_msg = random.choice(self.personality.get("feed_msg", ["好吃！"]))
        return f"🍗 喂食成功！{feed_msg} 饱食度 +{food_power}"

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
        # 性格化回复
        play_msg = random.choice(self.personality.get("play_msg", ["好好玩！"]))
        return f"🎾 玩耍成功！{play_msg} 快乐度 +{fun}, 经验 +10"

    def pet_touch(self):
        """抚摸"""
        self.love = min(100, self.love + 5)
        self.happiness = min(100, self.happiness + 8)
        self.stats["pet_count"] += 1
        self.stats["total_interactions"] += 1
        self.add_memory("被抚摸好舒服")
        # 性格化回复
        pet_msg = random.choice(self.personality.get("pet_msg", ["舒服～"]))
        return f"💕 抚摸成功！{pet_msg} 爱意 +5, 快乐 +8"

    def talk(self, words="喵～"):
        """对话"""
        self.happiness = min(100, self.happiness + 3)
        self.love = min(100, self.love + 2)
        self.stats["talk_count"] += 1
        self.stats["total_interactions"] += 1
        # 性格化回复
        talk_msg = random.choice(self.personality.get("talk_msg", ["主人好！"]))
        self.thought = talk_msg
        self.add_memory(f"听到: {words}")
        return f"💬 对话: {self.thought}"

    def heal(self, amount=30):
        """治疗"""
        self.health = min(100, self.health + amount)
        self.add_memory("接受了治疗")
        return f"❤️ 治疗成功！健康 +{amount}"

    def check_evolution(self):
        """检查是否可以进化"""
        # 先检查多阶段进化链
        evo_result = check_evolution_conditions(self)
        if evo_result:
            next_stage, next_info = evo_result

            # 检查进化链中是否有对应阶段名称的宠物
            chain = EVOLUTION_CHAINS.get(self.species)
            if chain:
                old_name = self.name

                # 查找对应的进化形态
                evo_form = None
                for form_species, form_data in EVOLUTION_FORMS.items():
                    if chain[next_stage]["name"] == form_data["name_cn"]:
                        evo_form = form_data
                        break

                if evo_form:
                    self.species = evo_form.get("species", self.species) or self.species
                    self.name = evo_form["name_cn"]
                    # 按倍数提升DNA
                    mult = next_info["dna_mult"]
                    for k in self.dna:
                        self.dna[k] = int(self.dna[k] * mult / (EVOLUTION_CHAINS[self.species].get(self.evolution_stage, {}).get("dna_mult", 1.0)))

                self.evolution_stage = next_stage
                self.skills = self.get_starting_skills()
                self.skill_pp = {skill: SKILLS_DATA[skill]["pp"] for skill in self.skills}
                self.add_memory(f"进化成了 {self.name}！")
                return f"✨ 恭喜！{old_name} 进化成了 {self.name}！({next_stage})"

        # 旧版单阶段进化兼容
        if self.species in EVOLUTIONS:
            evo = EVOLUTIONS[self.species]
            if self.level >= evo["level"]:
                # 可以进化
                evo_data = EVOLUTION_FORMS.get(evo["next"])
                if evo_data:
                    old_name = self.name
                    self.species = evo["next"]
                    self.name = evo_data["name_cn"]
                    # 更新DNA
                    for k, v in evo_data["dna"].items():
                        self.dna[k] = v
                    # 更新技能
                    self.skills = self.get_starting_skills()
                    self.skill_pp = {skill: SKILLS_DATA[skill]["pp"] for skill in self.skills}
                    # 更新进化阶段
                    if self.level >= 30:
                        self.evolution_stage = "perfect"
                    elif self.level >= 20:
                        self.evolution_stage = "adult"
                    elif self.level >= 10:
                        self.evolution_stage = "child"
                    self.add_memory(f"进化成了 {self.name}！")
                    return f"✨ 恭喜！{old_name} 进化成了 {self.name}！"
        return None


class GameData:
    """游戏数据管理"""

    def __init__(self):
        self.pets = []
        self.eggs = []  # 宠物蛋列表
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

        # 转换蛋数据为JSON可序列化格式
        def egg_to_dict(egg):
            return {
                "id": egg.id,
                "species": egg.species,
                "name": egg.name,
                "hatch_time_minutes": egg.hatch_time_minutes,
                "start_time": egg.start_time.isoformat(),
                "hatched": egg.hatched,
            }

        data = {
            "pets": [pet_to_dict(p) for p in self.pets],
            "eggs": [egg_to_dict(e) for e in self.eggs],
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

                # 恢复宠物蛋
                for egg_data in data.get("eggs", []):
                    egg = PetEgg(egg_data.get("species"), egg_data.get("hatch_time_minutes", 10))
                    egg.id = egg_data.get("id", egg.id)
                    egg.name = egg_data.get("name", egg.name)
                    egg.start_time = datetime.fromisoformat(egg_data.get("start_time", datetime.now().isoformat()))
                    egg.hatched = egg_data.get("hatched", False)
                    game.eggs.append(egg)

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

    def add_egg(self, egg):
        """添加宠物蛋"""
        self.eggs.append(egg)

    def check_eggs(self):
        """检查并孵化可孵化的蛋"""
        hatched_eggs = []
        for egg in self.eggs[:]:
            if egg.is_ready():
                pet = egg.hatch()
                if pet:
                    self.pets.append(pet)
                    hatched_eggs.append(pet)
                    self.eggs.remove(egg)
        return hatched_eggs


def display_pet(pet, frame=0):
    """显示宠物像素界面"""
    # 获取像素图案 - 优先使用EVOLUTION_FORMS
    pet_data = EVOLUTION_FORMS.get(pet.species) or PETS_DATA.get(pet.species, PETS_DATA["mimi"])
    pixel_art = pet_data["pixel"]

    # 清理屏幕
    print("\033[2J\033[H", end="")

    # 获取心情
    mood_emoji = {"happy": "😊", "content": "😐", "sad": "😢", "hungry": "😫", "tired": "😴", "sick": "🤒"}
    mood_str = mood_emoji.get(pet.mood, "😐")

    # 属性图标
    type_emoji = {"fire": "🔥", "water": "💧", "grass": "🌿", "electric": "⚡",
                  "ice": "❄️", "flying": "🕊️", "earth": "🪨", "fighting": "🥊",
                  "psychic": "🔮", "ghost": "👻", "dark": "🌑", "light": "✨",
                  "normal": "⬜", "poison": "☠️", "rock": "🪨", "dragon": "🐉",
                  "fairy": "🧚", "flower": "🌸", "shadow": "💫"}
    element = pet.get_element()
    element_ico = type_emoji.get(element, "⬜")

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
    stage_names = {"baby": "幼年期", "child": "成长期", "adult": "成熟期", "perfect": "完全体", "ultimate": "究极体"}
    stage = stage_names.get(pet.evolution_stage, "幼年期")
    print(f"║ Lv.{pet.level} {pet.name} {element_ico} {stage}                      ║")
    print(f"║ DNA: HP:{pet.dna['hp']:3} ATK:{pet.dna['attack']:2} DEF:{pet.dna['defense']:2} SPD:{pet.dna['speed']:2} LCK:{pet.dna['luck']:2}                    ║")
    # 显示技能
    print("╠══════════════════════════════════════════════════╣")
    print("║ 🎯 技能:                                            ║")
    for i, skill_id in enumerate(pet.skills[:2]):  # 只显示前2个技能
        skill = SKILLS_DATA.get(skill_id, {})
        print(f"║    {i+1}. {skill.get('name', skill_id):8} PP:{pet.skill_pp.get(skill_id, 0):2}/{skill.get('pp', 0):2}                             ║")
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
        if game.eggs:
            print(f"🥚 宠物蛋: {len(game.eggs)}个")
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
        print("A. 🎯 技能查看")
        print("B. ⚔️  战斗系统")
        print("C. 🌲 野外探索/寻找蛋")
        print("D. 🥚 宠物蛋")
        print("0. 🚪 退出")
        print("-" * 40)

        choice = input("选择: ").strip().upper()

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
        elif choice == "A":
            # 技能查看
            pet.show_skills()
        elif choice == "B":
            # 战斗系统
            print("\n⚔️ 战斗系统")
            print("1. 野外遭遇战")
            print("2. 挑战道馆")
            battle_choice = input("选择: ").strip()
            if battle_choice == "1":
                wild_encounter(game)
            elif battle_choice == "2":
                gym_index = input("选择道馆 (1-5): ").strip()
                try:
                    gym_battle(game, int(gym_index) - 1)
                except:
                    print("无效选择")
        elif choice == "C":
            # 野外探索
            print("\n🌲 野外探索")
            print("1. 寻找野生宠物")
            print("2. 寻找宠物蛋")
            explore_choice = input("选择: ").strip()
            if explore_choice == "1":
                wild_encounter(game)
            elif explore_choice == "2":
                egg = find_egg_in_wild(game)
                if egg:
                    game.add_egg(egg)
        elif choice == "D":
            # 宠物蛋管理
            if not game.eggs:
                print("\n🥚 你没有宠物蛋")
            else:
                print(f"\n🥚 宠物蛋 ({len(game.eggs)}个)")
                print("-" * 40)
                for i, egg in enumerate(game.eggs):
                    egg.display()
                    print("-" * 40)

                # 检查是否可以孵化
                hatched = game.check_eggs()
                if hatched:
                    print("\n🎉 宠物蛋孵化了！")
                    for p in hatched:
                        print(f"   ✨ {p.name} 出生了！")
                        game.add_pet(p.species)
                else:
                    print("\n还没有可以孵化的蛋")

                # 强制孵化选项
                if game.eggs:
                    force = input("\n是否强制孵化一个蛋? (y/n): ").strip().lower()
                    if force == "y" and game.eggs:
                        egg = game.eggs[0]
                        # 强制设置孵化时间
                        egg.start_time = datetime.now() - timedelta(minutes=egg.hatch_time_minutes + 1)
                        hatched = game.check_eggs()
                        if hatched:
                            print(f"\n🎉 {hatched[0].name} 孵化了！")
        elif choice == "0":
            game.save()
            print("再见！")
            break

        game.save()
        display_pet(pet)


# ========== 宠物蛋系统 (Tamagotchi风格) ==========
class PetEgg:
    """宠物蛋类"""

    def __init__(self, species=None, hatch_time_minutes=10):
        self.id = f"egg_{int(time.time() * 1000)}"
        # 随机选择物种（如果未指定）
        if species is None:
            species = random.choice(list(PETS_DATA.keys()))
        self.species = species
        self.name = f"{PETS_DATA[species]['name_cn']}的蛋"

        # 孵化时间（默认10分钟）
        self.hatch_time_minutes = hatch_time_minutes
        self.start_time = datetime.now()
        self.hatched = False

        # 蛋的图案
        self.pixel = [
            "  ━━━━━  ",
            " ┫━━━━━━┣ ",
            " ┃ ░░░░ ┃ ",
            " ┣━━━━━━┫ ",
            "  ┗━━━━┛  ",
        ]

    def get_remaining_time(self):
        """获取剩余孵化时间"""
        elapsed = datetime.now() - self.start_time
        remaining = self.hatch_time_minutes * 60 - elapsed.total_seconds()
        if remaining <= 0:
            return 0
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return minutes, seconds

    def is_ready(self):
        """检查是否可以孵化"""
        remaining = self.get_remaining_time()
        if remaining == 0:
            return True
        if isinstance(remaining, tuple):
            return remaining[0] <= 0 and remaining[1] <= 0
        return False

    def display(self):
        """显示蛋的状态"""
        print("\n" + "="*40)
        print("🥚 宠物蛋")
        print("="*40)
        for line in self.pixel:
            print(f"   {line}")
        print("="*40)

        if self.is_ready():
            print("   ⚡ 蛋开始摇晃了！要孵化了！")
        else:
            minutes, seconds = self.get_remaining_time()
            print(f"   ⏳ 预计孵化时间: {minutes}分{seconds}秒")
        print("="*40)

    def hatch(self):
        """孵化宠物蛋"""
        if not self.is_ready():
            return None

        # 创建新宠物
        pet = Pet(self.species)
        pet.name = f"{pet.name} Jr."
        pet.evolution_stage = "baby"

        # 随机变异属性
        for k in pet.dna:
            pet.dna[k] = int(pet.dna[k] * random.uniform(0.9, 1.1))

        return pet


# 野外发现蛋的地点
EGG_LOCATIONS = [
    {"name": "森林", "elements": ["grass", "flower", "normal"]},
    {"name": "湖泊", "elements": ["water", "ice"]},
    {"name": "火山", "elements": ["fire", "rock"]},
    {"name": "山洞", "elements": ["dark", "ghost", "rock"]},
    {"name": "草原", "elements": ["grass", "normal", "flying"]},
    {"name": "海滩", "elements": ["water", "rock"]},
    {"name": "城镇", "elements": ["normal", "electric"]},
    {"name": "雪山", "elements": ["ice", "water"]},
]


def find_egg_in_wild(game):
    """在野外发现宠物蛋"""
    # 30%几率发现蛋
    if random.random() < 0.3:
        # 根据玩家宠物的属性倾向选择
        pet = game.get_current_pet()
        if pet:
            player_element = pet.get_element()
            # 选择相同或相克属性的地点
            possible_locations = [
                loc for loc in EGG_LOCATIONS
                if player_element in loc["elements"] or
                get_type_effectiveness(player_element, loc["elements"][0]) > 1
            ]
            if not possible_locations:
                possible_locations = EGG_LOCATIONS

            location = random.choice(possible_locations)
        else:
            location = random.choice(EGG_LOCATIONS)

        print(f"\n🌲 你在{location['name']}探索...")
        time.sleep(1)

        # 选择该地点可能出现的宠物
        possible_pets = [
            species for species, data in PETS_DATA.items()
            if data.get("element") in location["elements"]
        ]
        if not possible_pets:
            possible_pets = list(PETS_DATA.keys())

        species = random.choice(possible_pets)
        hatch_time = random.randint(5, 15)  # 5-15分钟

        egg = PetEgg(species, hatch_time)
        print(f"\n✨ 你发现了一颗{location['name']}的宠物蛋！")
        print(f"   这是一颗{PETS_DATA[species]['name_cn']}的蛋")
        print(f"   预计{hatch_time}分钟后孵化")

        return egg
    else:
        print("\n🌲 你在野外探索，但没有发现宠物蛋...")
        return None


# ========== 战斗系统 ==========
class BattlePet:
    """战斗宠物类"""

    def __init__(self, pet):
        self.name = pet.name
        self.species = pet.species
        self.level = pet.level
        self.element = pet.get_element()
        self.max_hp = pet.dna["hp"] + pet.level * 5
        self.current_hp = self.max_hp
        self.attack = pet.dna["attack"] + pet.level * 2
        self.defense = pet.dna["defense"] + pet.level * 2
        self.speed = pet.dna["speed"] + pet.level * 2
        self.skills = pet.skills.copy()
        self.skill_pp = pet.skill_pp.copy()


# 野生宠物生成
WILD_PETS = [
    {"species": "mimi", "min_level": 1, "max_level": 5},
    {"species": "spark", "min_level": 3, "max_level": 8},
    {"species": "bubble", "min_level": 3, "max_level": 8},
    {"species": "leaf", "min_level": 2, "max_level": 7},
    {"species": "zap", "min_level": 4, "max_level": 9},
    {"species": "shadow", "min_level": 5, "max_level": 10},
    {"species": "snow", "min_level": 4, "max_level": 9},
]

# 道馆馆主
GYM_LEADERS = [
    {"name": "小火训练师", "species": "spark", "level": 15, "element": "fire"},
    {"name": "水滴训练师", "species": "bubble", "level": 20, "element": "water"},
    {"name": "森林训练师", "species": "leaf", "level": 18, "element": "grass"},
    {"name": "雷电训练师", "species": "zap", "level": 22, "element": "electric"},
    {"name": "暗影训练师", "species": "shadow", "level": 25, "element": "dark"},
]


def generate_wild_pet(player_level):
    """生成野生宠物"""
    available = [p for p in WILD_PETS if p["min_level"] <= player_level + 5]
    if not available:
        available = WILD_PETS
    wild = random.choice(available)
    level = random.randint(max(1, wild["min_level"]), min(wild["max_level"], player_level + 5))

    # 创建临时宠物对象
    class TempPet:
        def __init__(self, species):
            self.species = species
            self.name = PETS_DATA.get(species, {}).get("name_cn", "未知")
            self.level = level
            self.dna = PETS_DATA.get(species, {}).get("dna", {"hp": 50, "attack": 30, "defense": 30, "speed": 30, "luck": 50}).copy()

        def get_element(self):
            return PETS_DATA.get(self.species, {}).get("element", "normal")

        @property
        def skills(self):
            return PET_STARTING_SKILLS.get(self.species, ["scratch", "tackle", "defense_curl", "heal"])

        @property
        def skill_pp(self):
            return {skill: SKILLS_DATA[skill]["pp"] for skill in self.skills}

    return BattlePet(TempPet(wild["species"]))


def calculate_damage(attacker, defender, skill):
    """计算伤害"""
    skill_data = SKILLS_DATA[skill]
    power = skill_data["power"]

    if skill_data["type"] == "heal":
        # 恢复技能
        heal_amount = power + attacker.attack // 2
        return 0, heal_amount, "heal"

    if power == 0:
        return 0, 0, "none"

    # 基础伤害
    damage = (power * attacker.attack / defender.defense) * (50 / 50 + 0.5)

    # 属性相克
    skill_element = skill_data["element"]
    effectiveness = get_type_effectiveness(skill_element, defender.element)
    damage = damage * effectiveness

    # 随机波动
    damage = damage * random.uniform(0.85, 1.0)

    damage = int(damage)
    return damage, effectiveness, "attack"


def battle(player_pet, enemy_pet):
    """战斗"""
    # 创建战斗宠物
    player = BattlePet(player_pet)
    enemy = enemy_pet

    print("\n" + "="*50)
    print(f"⚔️  战斗开始！")
    print(f"  你的: {player.name} Lv.{player.level} {player.element}")
    print(f"  对手: {enemy.name} Lv.{enemy.level} {enemy.element}")
    print("="*50)

    round_num = 0
    while player.current_hp > 0 and enemy.current_hp > 0:
        round_num += 1
        print(f"\n--- 第 {round_num} 回合 ---")
        print(f"你的 {player.name}: HP {player.current_hp}/{player.max_hp}")
        print(f"对手 {enemy.name}: HP {enemy.current_hp}/{enemy.max_hp}")

        # 玩家选择技能
        print("\n🎯 选择技能:")
        for i, skill_id in enumerate(player.skills):
            skill = SKILLS_DATA[skill_id]
            pp = player.skill_pp.get(skill_id, 0)
            type_emoji = {"fire": "🔥", "water": "💧", "grass": "🌿", "electric": "⚡",
                         "ice": "❄️", "flying": "🕊️", "earth": "🪨", "fighting": "🥊",
                         "psychic": "🔮", "ghost": "👻", "dark": "🌑", "light": "✨",
                         "normal": "⬜", "poison": "☠️", "rock": "🪨", "dragon": "🐉",
                         "fairy": "🧚", "flower": "🌸", "shadow": "💫"}
            print(f"  {i+1}. {skill['name']} {type_emoji.get(skill['element'], '⬜')} PP:{pp}/{skill['pp']}")

        try:
            choice = int(input("\n选择技能 (0=逃跑): "))
            if choice == 0:
                print("🏃 你逃跑了！")
                return "fled"
            if choice < 1 or choice > len(player.skills):
                print("无效选择")
                continue

            skill_id = player.skills[choice - 1]
            if player.skill_pp.get(skill_id, 0) <= 0:
                print("PP不足！")
                continue

            # 使用技能
            player.skill_pp[skill_id] -= 1
            skill = SKILLS_DATA[skill_id]

            # 恢复技能
            if skill["type"] == "heal":
                heal_amount = skill.get("power", 20) + player.attack // 2
                heal_amount = min(heal_amount, player.max_hp - player.current_hp)
                player.current_hp += heal_amount
                print(f"✨ {player.name} 使用了 {skill['name']}，恢复了 {heal_amount} HP！")
            elif skill["type"] == "defense" or skill["type"] == "debuff":
                print(f"🛡️ {player.name} 使用了 {skill['name']}！")
            elif skill["type"] == "buff":
                print(f"⭐ {player.name} 使用了 {skill['name']}，攻击力提升！")
                player.attack += 5
            else:
                # 攻击技能
                damage, effectiveness, _ = calculate_damage(player, enemy, skill_id)
                enemy.current_hp = max(0, enemy.current_hp - damage)

                # 显示效果
                eff_text = ""
                if effectiveness > 1.5:
                    eff_text = " 效果拔群！"
                elif effectiveness < 0.6:
                    eff_text = " 效果不太好..."

                print(f"⚔️ {player.name} 使用了 {skill['name']}！")
                print(f"   对 {enemy.name} 造成了 {damage} 伤害！{eff_text}")

            # 检查敌人是否倒下
            if enemy.current_hp <= 0:
                print(f"\n🎉 {enemy.name} 倒下了！")
                print(f"✨ 战斗胜利！")

                # 奖励
                exp_gain = enemy.level * 10 + 20
                coin_gain = enemy.level * 5 + 10
                print(f"   获得经验: {exp_gain}")
                print(f"   获得金币: {coin_gain}")
                return "win", exp_gain, coin_gain

            # 敌人行动 (AI)
            # 敌人选择技能
            enemy_skill = random.choice(enemy.skills)
            if enemy.skill_pp.get(enemy_skill, 0) > 0:
                enemy.skill_pp[enemy_skill] -= 1
                skill = SKILLS_DATA[enemy_skill]

                if skill["type"] == "heal":
                    heal_amount = skill.get("power", 20) + enemy.attack // 2
                    heal_amount = min(heal_amount, enemy.max_hp - enemy.current_hp)
                    enemy.current_hp += heal_amount
                    print(f"✨ {enemy.name} 使用了 {skill['name']}，恢复了 {heal_amount} HP！")
                elif skill["type"] == "defense":
                    print(f"🛡️ {enemy.name} 使用了 {skill['name']}！")
                elif skill["type"] == "buff":
                    print(f"⭐ {enemy.name} 使用了 {skill['name']}，攻击力提升！")
                    enemy.attack += 5
                else:
                    damage, effectiveness, _ = calculate_damage(enemy, player, enemy_skill)
                    player.current_hp = max(0, player.current_hp - damage)

                    eff_text = ""
                    if effectiveness > 1.5:
                        eff_text = " 效果拔群！"
                    elif effectiveness < 0.6:
                        eff_text = " 效果不太好..."

                    print(f"⚔️ {enemy.name} 使用了 {skill['name']}！")
                    print(f"   对 {player.name} 造成了 {damage} 伤害！{eff_text}")

                # 检查玩家是否倒下
                if player.current_hp <= 0:
                    print(f"\n💀 {player.name} 倒下了！")
                    print(f"😵 战斗失败...")
                    return "lose", 0, 0

        except ValueError:
            print("无效输入！")

    return "draw", 0, 0


def wild_encounter(game):
    """遭遇野生宠物"""
    pet = game.get_current_pet()
    if not pet:
        print("没有宠物！")
        return

    print("\n🔍 你在野外探索...")
    time.sleep(1)

    if random.random() < 0.3:  # 30%几率遭遇
        print("⚠️ 发现了一只野生宠物！")
        enemy = generate_wild_pet(pet.level)
        result = battle(pet, enemy)

        if isinstance(result, tuple):
            outcome, exp, coins = result
            if outcome == "win":
                pet.add_exp(exp)
                game.coins += coins
            elif outcome == "fled":
                pass
            else:
                pet.health = max(1, pet.health - 20)
                print(f"\n💔 {pet.name} 受伤了，健康降低！")
    else:
        print("没有发现野生宠物。")


def gym_battle(game, leader_index):
    """道馆挑战"""
    pet = game.get_current_pet()
    if not pet:
        print("没有宠物！")
        return

    if leader_index >= len(GYM_LEADERS):
        print("没有更多道馆了！")
        return

    leader = GYM_LEADERS[leader_index]

    print(f"\n🏆 挑战道馆馆主: {leader['name']}！")

    # 创建敌人宠物
    class GymPet:
        def __init__(self, leader):
            self.species = leader["species"]
            self.name = PETS_DATA.get(leader["species"], {}).get("name_cn", "未知")
            self.level = leader["level"]
            self.element = leader["element"]
            self.dna = PETS_DATA.get(leader["species"], {}).get("dna", {"hp": 80, "attack": 50, "defense": 50, "speed": 50, "luck": 50}).copy()
            # 提升属性
            for k in self.dna:
                self.dna[k] = int(self.dna[k] * 1.3)

        def get_element(self):
            return self.element

        @property
        def skills(self):
            return EVOLUTION_SKILLS.get(self.species, PET_STARTING_SKILLS.get(self.species, ["scratch", "tackle", "defense_curl", "heal"]))

        @property
        def skill_pp(self):
            return {skill: SKILLS_DATA[skill]["pp"] for skill in self.skills}

    enemy = BattlePet(GymPet(leader))
    result = battle(pet, enemy)

    if isinstance(result, tuple):
        outcome, exp, coins = result
        if outcome == "win":
            pet.add_exp(exp)
            game.coins += coins
            print(f"\n🎉 恭喜！你击败了 {leader['name']}！")
            print(f"获得道馆徽章！")
        else:
            pet.health = max(1, pet.health - 30)
            print(f"\n💔 {pet.name} 受到重伤！")


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
