"""
@dandanzhang: 小火车游戏
第一次用DS写的小程序，输入提示，整合代码，运行，完结！
"""
import os
import tkinter as tk
from pathlib import Path
import pygame


class TrainGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jerry's little train line 1")

        # 游戏状态
        self.speed = 3
        self.is_running = False
        self.current_station_index = 0

        # 初始化UI
        self.setup_ui()

        # 加载资源
        self.load_resources()

        # 设置事件绑定
        self.setup_bindings()

        # 启动游戏循环
        self.update_game()

    def setup_ui(self):
        """初始化用户界面"""
        # 主画布
        self.canvas = tk.Canvas(
            self.root,
            width=1600,
            height=600,
            bg="dark green"
        )
        self.canvas.pack()

        # 控制面板
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        # 配置控制面板列宽
        for i in range(6):
            self.control_frame.columnconfigure(i, weight=1)

        # 添加按钮
        self.add_buttons()

        # 绘制轨道
        self.draw_tracks()

    def load_resources(self):
        """加载游戏资源"""
        self.assets_dir = Path(__file__).parent / "assets"

        # 加载图片
        self.train_img = tk.PhotoImage(file=self.assets_dir / "redtrain.png")
        self.train = self.canvas.create_image(100, 308, image=self.train_img)

        # 初始化音频系统
        pygame.mixer.init()

        # 加载音频
        audio_dir = self.assets_dir / "audio"
        self.choochoo_sound = pygame.mixer.Sound(os.path.join(audio_dir, "stop6.mp3"))

        self.station_sounds = {
            "stop1": pygame.mixer.Sound(os.path.join(audio_dir, "stop1.mp3")),
            "stop2": pygame.mixer.Sound(os.path.join(audio_dir, "stop2.mp3")),
            "stop3": pygame.mixer.Sound(os.path.join(audio_dir, "stop3.mp3")),
            "stop4": pygame.mixer.Sound(os.path.join(audio_dir, "stop4.mp3")),
            "stop5": pygame.mixer.Sound(os.path.join(audio_dir, "stop5.mp3"))
        }

        self.station_names = [
            "Sutherland Rd",
            "Government Center",
            "Cleveland Circle",
            "Chiswick Rd",
            "Dighton St"
        ]

    def setup_bindings(self):
        """设置键盘绑定"""
        self.root.bind("<Left>", lambda e: self.adjust_speed(-1))
        self.root.bind("<Right>", lambda e: self.adjust_speed(1))
        self.root.bind("<space>", self.toggle_pause)

    def add_buttons(self):
        """添加控制按钮"""
        # 按钮配置列表
        buttons = [
            {"text": "Start/Pause", "command": self.toggle_pause, "bg": "lightgreen", "col": 0},
            {"text": "Speed ▲", "command": lambda: self.adjust_speed(1), "bg": "orange", "col": 1},
            {"text": "Slow ▼", "command": lambda: self.adjust_speed(-1), "bg": "lightblue", "col": 2},
            {"text": "Reset", "command": self.reset_game, "bg": "pink", "col": 3},
            {"text": "Announce", "command": self.announce_station, "bg": "yellow", "col": 4},
            {"text": "Horn", "command": self.play_choo_sound, "bg": "red", "col": 5}
        ]

        # 创建按钮
        for btn in buttons:
            tk.Button(
                self.control_frame,
                text=btn["text"],
                command=btn["command"],
                bg=btn["bg"],
                width=10
            ).grid(row=0, column=btn["col"], padx=5, sticky="nsew")

    def draw_tracks(self):
        """绘制轨道"""
        self.canvas.create_rectangle(0, 450, 1600, 500, fill="blue", outline="black", width=2)
        for x in range(0, 1600, 50):
            self.canvas.create_line(x, 450, x, 470, fill="white", width=2)

    def update_game(self):
        """游戏主循环"""
        if self.is_running:
            # 移动火车
            self.canvas.move(self.train, self.speed, 0)

            # 检查边界
            train_pos = self.canvas.coords(self.train)
            if train_pos[0] > 1600:
                self.canvas.coords(self.train, -50, 308)

        # 继续游戏循环
        self._after_id = self.root.after(30, self.update_game)

    def toggle_pause(self, event=None):
        """切换暂停状态"""
        self.is_running = not self.is_running
        # 更新按钮文本
        for widget in self.control_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget["text"] in ["Start/Pause", "Start", "Pause"]:
                widget.config(text="Pause" if self.is_running else "Start")

    def adjust_speed(self, delta):
        """调整速度"""
        self.speed = max(1, min(self.speed + delta, 10))

    def announce_station(self):
        """报站功能"""
        station_keys = list(self.station_sounds.keys())
        if not station_keys:
            return

        # 播放当前站点的声音
        self.station_sounds[station_keys[self.current_station_index]].play()

        # 显示站点信息
        self.show_message(f"Next Stop: {self.station_names[self.current_station_index]}")

        # 更新站点索引
        self.current_station_index = (self.current_station_index + 1) % len(station_keys)

    def play_choo_sound(self):
        """播放警报声"""
        self.choochoo_sound.play()
        self.show_message("Train is Moving!")

    def show_message(self, text, duration=4000):
        """显示临时消息"""
        self.canvas.delete("message")
        self.canvas.create_text(
            400, 50,
            text=text,
            font=("Arial", 24, "bold"),
            fill="red",
            tags="message"
        )
        self.root.after(duration, lambda: self.canvas.delete("message"))

    def reset_game(self):
        """重置游戏"""
        self.is_running = False
        self.canvas.coords(self.train, 100, 308)
        self.speed = 3

        # 更新按钮状态
        for widget in self.control_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget["text"] in ["Start/Pause", "Pause", "Start"]:
                widget.config(text="Start")

        # 取消之前的游戏循环
        if hasattr(self, '_after_id'):
            self.root.after_cancel(self._after_id)

        # 启动新的游戏循环
        self.update_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = TrainGame(root)
    root.mainloop()