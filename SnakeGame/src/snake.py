#!/usr/bin/env python3
"""
小蛇实体模块
任务：小蛇实体初始化
要求：创建长度为3节的小蛇，每节为20×20像素的蓝色圆角方块，
      初始位置在游戏区域上方，方向向下。
"""

import pygame
from typing import List, Tuple


class Snake:
    """
    小蛇实体类
    
    属性：
        segments: 存储每节坐标的列表，每个坐标为 (x, y)
        direction: 当前移动方向向量 (dx, dy)
        color: 小蛇颜色 (R, G, B)
        segment_size: 每节的像素尺寸
        border_radius: 圆角半径
    """
    
    def __init__(self,
                 screen_width: int = 800,
                 screen_height: int = 800,
                 length: int = 3,
                 segment_size: int = 20,
                 color: Tuple[int, int, int] = (0, 100, 255),  # 蓝色
                 border_radius: int = 5):
        """
        初始化小蛇。
        
        Args:
            screen_width: 游戏区域宽度（像素）
            screen_height: 游戏区域高度（像素）
            length: 小蛇初始节数（默认3）
            segment_size: 每节的边长（像素）
            color: 小蛇颜色 (R, G, B)
            border_radius: 圆角半径（像素）
        """
        self.segment_size = segment_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = color
        self.border_radius = border_radius
        
        # 初始方向向下
        self.direction = (0, 1)
        self.speed = 20.0  # 像素/秒
        self.move_accumulator = 0.0  # 累积移动距离
        self._grow_pending = 0  # 待增长节数
        
        # 计算初始位置：头部在游戏区域上方居中
        head_x = screen_width // 2
        head_y = length*segment_size  # 距离顶部一个节的高度
        
        # 生成小蛇各节坐标（从头部到尾部），使用浮点数以便平滑移动
        self.segments: List[Tuple[float, float]] = []
        for i in range(length):
            # 每节向下排列（因为初始方向向下）
            x = float(head_x)
            y = float(head_y - i * segment_size)
            self.segments.append((x, y))
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        绘制小蛇到指定的surface。
        
        Args:
            screen: 目标surface
        """
        for x, y in self.segments:
            # 将浮点坐标转换为整数，避免渲染问题
            rect = pygame.Rect(int(x), int(y), self.segment_size, self.segment_size)
            pygame.draw.rect(screen, self.color, rect,
                             border_radius=self.border_radius)
            # 可选：绘制边框以增强视觉效果
            pygame.draw.rect(screen, (0, 0, 0), rect,
                             width=1, border_radius=self.border_radius)
    
    def get_head(self) -> Tuple[float, float]:
        """返回头部坐标（浮点数）"""
        return self.segments[0]
    
    def get_tail(self) -> Tuple[float, float]:
        """返回尾部坐标（浮点数）"""
        return self.segments[-1]
    
    def __len__(self) -> int:
        """返回小蛇当前节数"""
        return len(self.segments)
    
    def update(self, delta_time: float) -> None:
        """
        基于时间增量更新小蛇位置。
        使用累积器确保每次移动一整节，保持身体各节紧密相连。
        
        Args:
            delta_time: 距离上一帧的时间（秒）
        """
        if delta_time <= 0:
            return
        
        # 累积移动距离
        self.move_accumulator += self.speed * delta_time
        segment_size = self.segment_size
        
        # 当累积距离超过一节大小时，移动一节
        while self.move_accumulator >= segment_size:
            # 当前头部坐标
            head_x, head_y = self.segments[0]
            dx, dy = self.direction
            
            # 计算新头部坐标（移动一整节）
            new_head_x = head_x + dx * segment_size
            new_head_y = head_y + dy * segment_size
            
            # 将新头部插入列表开头
            self.segments.insert(0, (new_head_x, new_head_y))
            # 根据待增长节数决定是否移除尾部
            if self._grow_pending > 0:
                self._grow_pending -= 1
            else:
                self.segments.pop()
            
            # 减少累积器
            self.move_accumulator -= segment_size
    
    def _is_opposite(self, dir1: Tuple[int, int], dir2: Tuple[int, int]) -> bool:
        """
        判断两个方向是否相反（180度）。
        
        Args:
            dir1: 方向向量 (dx, dy)
            dir2: 方向向量 (dx, dy)
        
        Returns:
            True 如果方向相反
        """
        return dir1[0] == -dir2[0] and dir1[1] == -dir2[1]
    
    def _move_one_segment(self) -> None:
        """
        立即移动一节（用于加速）。
        该操作不依赖累积器，直接插入新头部并移除尾部。
        """
        head_x, head_y = self.segments[0]
        dx, dy = self.direction
        segment_size = self.segment_size
        
        new_head_x = head_x + dx * segment_size
        new_head_y = head_y + dy * segment_size
        
        self.segments.insert(0, (new_head_x, new_head_y))
        self.segments.pop()
    
    def change_direction(self, new_direction: Tuple[int, int]) -> None:
        """
        改变小蛇移动方向，遵循禁止180度立即掉头规则。
        若新方向与当前方向相同，则触发加速（额外移动一节）。
        
        Args:
            new_direction: 新方向向量 (dx, dy)
        """
        # 禁止反向
        if self._is_opposite(self.direction, new_direction):
            return
        
        # 方向相同则加速
        if self.direction == new_direction:
            self._move_one_segment()
            # 方向不变，无需更新 self.direction
            return
        
        # 正常改变方向
        self.direction = new_direction

    def grow(self) -> None:
        """
        增加小蛇长度一节。实际增长将在下一次移动时生效。
        """
        self._grow_pending += 1

    def check_boundary_collision(self) -> bool:
        """
        检测小蛇头部是否超出游戏区域边界。
        
        Returns:
            True 如果头部超出边界，否则 False
        """
        head_x, head_y = self.get_head()
        segment_size = self.segment_size
        # 使用浮点数比较，但边界是整数
        if (head_x < 0 or head_x + segment_size > self.screen_width or
            head_y < 0 or head_y + segment_size > self.screen_height):
            return True
        return False

    def reset(self) -> None:
        """
        重置小蛇到初始状态（长度、位置、方向、速度等）。
        """
        # 重置方向向下
        self.direction = (0, 1)
        self.speed = 20.0
        self.move_accumulator = 0.0
        self._grow_pending = 0
        
        # 重新计算初始位置
        length = 3
        head_x = self.screen_width // 2
        head_y = length * self.segment_size
        
        self.segments.clear()
        for i in range(length):
            x = float(head_x)
            y = float(head_y - i * self.segment_size)
            self.segments.append((x, y))

    def check_self_collision(self) -> bool:
        """
        检测小蛇头部是否与自身身体（除头部外）发生碰撞。
        
        Returns:
            True 如果头部与身体重叠，否则 False
        """
        if len(self.segments) <= 1:
            return False
        head_x, head_y = self.get_head()
        head_rect = pygame.Rect(int(head_x), int(head_y),
                                self.segment_size, self.segment_size)
        # 跳过头部（索引0）
        for i, (x, y) in enumerate(self.segments[1:], start=1):
            segment_rect = pygame.Rect(int(x), int(y),
                                       self.segment_size, self.segment_size)
            if head_rect.colliderect(segment_rect):
                return True
        return False