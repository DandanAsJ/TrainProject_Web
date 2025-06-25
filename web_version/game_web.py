# game_web.py
from js import document, setInterval, clearInterval
import pygame
from pygame import mixer

# 初始化音频系统
mixer.init()

def setup_game():
    # 加载资源
    assets = {
        "train_img": "assets/greentrain.png",
        "sounds": {
            "station1": "assets/audio/stop1.ogg",
            "horn": "assets/audio/horn.ogg"
        }
    }

    # 游戏状态
    return {
        "speed": 3,
        "running": False,
        "train_x": 100,
        "assets": assets
    }

game_state = setup_game()

def draw_game():
    canvas = document.getElementById("gameCanvas")
    ctx = canvas.getContext("2d")

    # 清空画布
    ctx.clearRect(0, 0, 800, 400)

    # 绘制轨道
    ctx.fillStyle = "blue"
    ctx.fillRect(0, 350, 800, 50)

    # 绘制火车（简化版，实际应使用图片）
    ctx.fillStyle = "green"
    ctx.fillRect(game_state["train_x"], 300, 100, 50)

def game_loop():
    if game_state["running"]:
        game_state["train_x"] += game_state["speed"]
        if game_state["train_x"] > 800:
            game_state["train_x"] = -100
        draw_game()

# 设置游戏循环（每30ms执行一次）
game_interval = setInterval(create_proxy(game_loop), 30)

# 绑定按钮事件
def toggle_pause():
    game_state["running"] = not game_state["running"]

document.getElementById("startBtn").addEventListener("click", create_proxy(toggle_pause))