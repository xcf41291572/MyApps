#!/usr/bin/env python3
"""
水果生成模块
任务：实现水果生成逻辑
要求：每5秒在游戏区域内随机位置生成一个20×20像素的红色圆角方块（水果），且不与小蛇身体重叠。
"""

import pygame
import random
from typing import List, Tuple, Optional


class Fruit:
    """
    表示单个水果的类。

    属性：
        x (int): 水果左上角X坐标（像素）
        y (int): 水果左上角Y坐标（像素）
        size (int): 水果边长（像素）
        color (Tuple[int, int, int]): 水果颜色 (R, G, B)
        border_radius (int): 圆角半径（像素）
    """

    def __init__(self,
                 x: int,
                 y: int,
                 size: int = 20,
                 color: Tuple[int, int, int] = (255, 50, 50),  # 红色
                 border_radius: int = 5):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.border_radius = border_radius

    def draw(self, screen: pygame.Surface) -> None:
        """
        在指定的surface上绘制水果。
        """
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect,
                         border_radius=self.border_radius)
        # 可选：绘制边框以增强视觉效果
        pygame.draw.rect(screen, (0, 0, 0), rect,
                         width=1, border_radius=self.border_radius)

    def get_position(self) -> Tuple[int, int]:
        """返回水果的左上角坐标 (x, y)"""
        return (self.x, self.y)


class FruitGenerator:
    """
    水果生成器，负责定时生成水果并管理水果列表。

    属性：
        screen_width (int): 游戏区域宽度（像素）
        screen_height (int): 游戏区域高度（像素）
        grid_size (int): 网格尺寸（像素），水果坐标必须是该值的整数倍
        interval (float): 生成间隔（秒）
        fruits (List[Fruit]): 当前存在的水果列表
        timer (float): 距离下次生成的剩余时间（秒）
    """

    def __init__(self,
                 screen_width: int = 800,
                 screen_height: int = 800,
                 grid_size: int = 20,
                 interval: float = 5.0):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.interval = interval
        self.fruits: List[Fruit] = []
        self.timer = interval  # 初始立即生成一个？不，等第一个间隔后生成。这里设置为0可以立即生成第一个水果。
        # 根据需求，游戏开始后5秒生成第一个水果，所以定时器初始为间隔时间。

    def update(self, delta_time: float, snake_segments: List[Tuple[float, float]]) -> None:
        """
        更新生成器状态。

        Args:
            delta_time: 自上一帧以来的时间（秒）
            snake_segments: 小蛇各节的坐标列表，用于重叠检测
        """
        self.timer -= delta_time
        if self.timer <= 0:
            self._generate_fruit(snake_segments)
            self.timer = self.interval

    def _generate_fruit(self, snake_segments: List[Tuple[float, float]]) -> None:
        """
        生成一个新的水果，确保其位置不与小蛇身体重叠。

        Args:
            snake_segments: 小蛇各节的坐标列表
        """
        max_attempts = 100  # 防止无限循环
        for _ in range(max_attempts):
            # 生成网格对齐的随机坐标
            x = random.randrange(0, self.screen_width - self.grid_size + 1, self.grid_size)
            y = random.randrange(0, self.screen_height - self.grid_size + 1, self.grid_size)

            # 检查是否与任何蛇节重叠
            if not self._overlaps_snake(x, y, snake_segments):
                fruit = Fruit(x, y, self.grid_size)
                self.fruits.append(fruit)
                return

        # 如果尝试多次仍未找到空位，则跳过本次生成（理论上不会发生，除非蛇占满整个区域）
        print("警告：无法找到空位生成水果，跳过本次生成。")

    def _overlaps_snake(self, x: int, y: int, snake_segments: List[Tuple[float, float]]) -> bool:
        """
        检查给定坐标是否与小蛇任何一节重叠。

        由于小蛇每节大小与网格相同，只需检查坐标是否等于蛇节的网格坐标。
        使用四舍五入处理可能的浮点误差。
        """
        for sx, sy in snake_segments:
            # 将蛇节坐标四舍五入到最近的网格点
            grid_x = int(round(sx / self.grid_size) * self.grid_size)
            grid_y = int(round(sy / self.grid_size) * self.grid_size)
            if x == grid_x and y == grid_y:
                return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """绘制所有水果"""
        for fruit in self.fruits:
            fruit.draw(screen)

    def get_fruits(self) -> List[Fruit]:
        """返回当前水果列表（只读）"""
        return self.fruits.copy()

    def remove_fruit(self, fruit: Fruit) -> None:
        """从列表中移除指定水果（例如被小蛇吃掉时）"""
        if fruit in self.fruits:
            self.fruits.remove(fruit)

    def clear(self) -> None:
        """清空所有水果（例如游戏重置时）"""
        self.fruits.clear()

    def reset(self) -> None:
        """
        重置水果生成器到初始状态（清空水果并重置计时器）。
        """
        self.fruits.clear()
        self.timer = self.interval  # 重置计时器，等待下一个生成间隔