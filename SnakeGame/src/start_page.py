#!/usr/bin/env python3
"""
开始页面UI模块
任务：实现开始页面UI
要求：绘制400×400像素、带有黑色边框的矩形，居中于主窗口。
标题“Snake Game”居中显示，按钮“Start”在矩形下方，支持点击事件。
"""

import pygame

class StartPage:
    """开始页面UI组件"""
    
    def __init__(self, screen_width=800, screen_height=800):
        """
        初始化开始页面。
        
        Args:
            screen_width (int): 主窗口宽度，默认800
            screen_height (int): 主窗口高度，默认800
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = True
        
        # 矩形尺寸与位置
        self.rect_width = 400
        self.rect_height = 400
        self.rect_x = (screen_width - self.rect_width) // 2
        self.rect_y = (screen_height - self.rect_height) // 2
        
        # 矩形边框颜色与填充色
        self.border_color = (0, 0, 0)          # 黑色边框
        self.fill_color = (240, 240, 240)      # 浅灰色填充
        
        # 标题文字
        self.title_font = None
        self.title_text = "Snake Game"
        self.title_color = (0, 0, 0)           # 黑色
        self._init_fonts()
        
        # 按钮属性
        self.button_width = 120
        self.button_height = 50
        self.button_x = (screen_width - self.button_width) // 2
        self.button_y = self.rect_y + self.rect_height - 40 - self.button_height   # 矩形内部下方，距底部40像素
        self.button_color = (70, 130, 180)     # 钢蓝色
        self.button_hover_color = (100, 160, 210)  # 悬停色
        self.button_active_color = (40, 100, 150)  # 点击色
        self.button_text = "Start"
        self.button_text_color = (255, 255, 255)   # 白色
        
        # 按钮状态
        self.button_hovered = False
        self.button_pressed = False
        
    def _init_fonts(self):
        """初始化字体"""
        try:
            self.title_font = pygame.font.SysFont(None, 64)   # 标题字体
            self.button_font = pygame.font.SysFont(None, 36)  # 按钮字体
        except:
            # 如果系统字体失败，使用默认字体
            self.title_font = pygame.font.Font(None, 64)
            self.button_font = pygame.font.Font(None, 36)
    
    def draw(self, screen):
        """
        绘制开始页面到指定的surface。
        
        Args:
            screen (pygame.Surface): 目标surface
        """
        if not self.visible:
            return
        
        # 绘制矩形填充
        pygame.draw.rect(screen, self.fill_color,
                         (self.rect_x, self.rect_y, self.rect_width, self.rect_height))
        # 绘制矩形边框
        pygame.draw.rect(screen, self.border_color,
                         (self.rect_x, self.rect_y, self.rect_width, self.rect_height), 4)
        
        # 绘制标题
        title_surface = self.title_font.render(self.title_text, True, self.title_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2,
                                                    self.rect_y + self.rect_height // 2))
        screen.blit(title_surface, title_rect)
        
        # 绘制按钮
        button_color = self.button_color
        if self.button_pressed:
            button_color = self.button_active_color
        elif self.button_hovered:
            button_color = self.button_hover_color
        
        pygame.draw.rect(screen, button_color,
                         (self.button_x, self.button_y, self.button_width, self.button_height),
                         border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0),
                         (self.button_x, self.button_y, self.button_width, self.button_height),
                         width=2, border_radius=8)
        
        # 按钮文字
        button_text_surface = self.button_font.render(self.button_text, True, self.button_text_color)
        button_text_rect = button_text_surface.get_rect(center=(self.button_x + self.button_width // 2,
                                                                self.button_y + self.button_height // 2))
        screen.blit(button_text_surface, button_text_rect)
    
    def handle_event(self, event):
        """
        处理事件，用于检测按钮悬停和点击。
        
        Args:
            event (pygame.event.Event): pygame事件
        
        Returns:
            bool: 如果点击了开始按钮并释放，返回True；否则返回False
        """
        if not self.visible:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            # 检测鼠标是否悬停在按钮上
            mouse_x, mouse_y = event.pos
            self.button_hovered = (self.button_x <= mouse_x <= self.button_x + self.button_width and
                                   self.button_y <= mouse_y <= self.button_y + self.button_height)
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                mouse_x, mouse_y = event.pos
                if (self.button_x <= mouse_x <= self.button_x + self.button_width and
                    self.button_y <= mouse_y <= self.button_y + self.button_height):
                    self.button_pressed = True
                    return False
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                clicked = (self.button_x <= mouse_x <= self.button_x + self.button_width and
                           self.button_y <= mouse_y <= self.button_y + self.button_height)
                if clicked and self.button_pressed:
                    self.button_pressed = False
                    self.visible = False   # 点击后页面消失
                    return True
                self.button_pressed = False
        
        return False
    
    def show(self):
        """显示页面"""
        self.visible = True
    
    def hide(self):
        """隐藏页面"""
        self.visible = False
    
    def reset(self):
        """重置页面状态（例如重新显示）"""
        self.visible = True
        self.button_hovered = False
        self.button_pressed = False