#!/usr/bin/env python3
"""
Snake Game - 主游戏窗口
任务：创建游戏主窗口
要求：窗口尺寸800×800像素，标题"Snake Game"，禁止调整大小，居中显示。
"""

import pygame
import os
import sys
from start_page import StartPage
from snake import Snake
from fruit import FruitGenerator
from end_page import EndPage

# 可选：高DPI缩放处理（针对Windows）
if os.name == 'nt':
    from ctypes import windll
    windll.user32.SetProcessDPIAware()

def main():
    # 初始化pygame
    pygame.init()
    
    # 禁止窗口调整大小 (SDL环境变量)
    os.environ['SDL_VIDEO_RESIZABLE'] = '0'
    
    # 设置窗口尺寸
    width, height = 800, 800
    screen_resolution = (width, height)
    
    # 使用SDL内置居中功能
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    # 创建窗口，不使用RESIZABLE标志以禁止调整大小
    screen = pygame.display.set_mode(screen_resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Snake Game")

    # 开始页面
    start_page = StartPage(width, height)
    snake = Snake(width, height)
    fruit_generator = FruitGenerator(width, height)

    # 结束页面
    end_page = EndPage(width, height)

    # 倒计时状态
    countdown_active = False
    countdown_timer = 0.0          # 剩余秒数
    countdown_number = 3           # 当前显示的数字
    countdown_font = pygame.font.SysFont(None, 120)  # 大字体

    # 游戏结束状态
    game_over = False

    # 键盘方向映射
    KEY_TO_DIRECTION = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),
    }

    # 调试输出：窗口尺寸
    win_size = pygame.display.get_window_size()
    print(f"窗口尺寸: {win_size} (期望: {screen_resolution})")
    # 注意：Pygame 2.6.1 没有 get_window_position，但 SDL_VIDEO_CENTERED 应保证居中
    
    # 设置窗口图标（可选，未来可添加）
    # icon = pygame.Surface((32, 32))
    # pygame.display.set_icon(icon)
    
    # 游戏主循环
    running = True
    clock = pygame.time.Clock()
    while running:
        # 计算时间增量（秒），并限制帧率
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 处理开始页面事件
            button_clicked = start_page.handle_event(event)
            # 处理结束页面事件
            restart_clicked = end_page.handle_event(event)
            if button_clicked:
                # 开始按钮被点击，启动倒计时
                countdown_active = True
                countdown_timer = 3.0
                countdown_number = 3
            if restart_clicked:
                # 重新开始按钮被点击，重置游戏状态
                game_over = False
                end_page.hide()
                start_page.hide()
                snake.reset()
                fruit_generator.reset()
                countdown_active = False
                countdown_timer = 0.0
                countdown_number = 3
            # 仅当开始页面隐藏且倒计时未激活且游戏未结束时才处理方向键
            if not start_page.visible and not countdown_active and not game_over and event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_DIRECTION:
                    snake.change_direction(KEY_TO_DIRECTION[event.key])
            # 禁止通过事件调整窗口大小（即使意外发生）
            if event.type == pygame.VIDEORESIZE:
                # 如果窗口被强制调整，立即恢复到固定尺寸
                pygame.display.set_mode(screen_resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        # 清屏（黑色背景）
        screen.fill((0, 0, 0))
        
        # 绘制开始页面（如果可见）
        start_page.draw(screen)
        
        # 倒计时逻辑
        if countdown_active:
            # 更新倒计时计时器
            countdown_timer -= delta_time
            if countdown_timer <= 0:
                # 倒计时结束
                countdown_active = False
            else:
                # 更新显示的数字
                new_number = int(countdown_timer) + 1  # 3 -> 3, 2.9 -> 2, 等等
                if new_number != countdown_number:
                    countdown_number = new_number
            # 绘制倒计时数字
            countdown_text = countdown_font.render(str(countdown_number), True, (255, 255, 255))
            text_rect = countdown_text.get_rect(center=(width // 2, height // 4))
            screen.blit(countdown_text, text_rect)
        
        # 如果开始页面已隐藏，绘制游戏元素占位
        if not start_page.visible and not countdown_active:
            # 游戏结束检测
            if not game_over:
                if snake.check_boundary_collision() or snake.check_self_collision():
                    game_over = True
                    end_page.show()
                else:
                    # 更新小蛇位置
                    snake.update(delta_time)
                    # 更新水果生成器
                    fruit_generator.update(delta_time, snake.segments)
                    # 碰撞检测：小蛇头部与水果
                    head_x, head_y = snake.get_head()
                    head_rect = pygame.Rect(int(head_x), int(head_y), snake.segment_size, snake.segment_size)
                    fruits_to_remove = []
                    for fruit in fruit_generator.get_fruits():  # 返回副本
                        fruit_rect = pygame.Rect(fruit.x, fruit.y, fruit.size, fruit.size)
                        if head_rect.colliderect(fruit_rect):
                            fruits_to_remove.append(fruit)
                    for fruit in fruits_to_remove:
                        fruit_generator.remove_fruit(fruit)
                        snake.grow()
                        # 可选：碰撞回调（未来扩展）
            # 绘制小蛇（无论游戏是否结束）
            snake.draw(screen)
            # 绘制水果
            fruit_generator.draw(screen)
            # 绘制结束页面（如果可见）
            end_page.draw(screen)
        
        # 显示帧率（调试用）
        fps = clock.get_fps()
        font = pygame.font.SysFont(None, 24)
        fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()