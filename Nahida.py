        #               #
        #               #
##################################
        #               #
        #               #
    ##########################
    #                        #
    #                        #
    ##########################
    #                        #
    #                        #
    ##########################
                #
                #
 ################################
                #
                #
                #
                #
                #
                #

import sys
import time
import random
from math import atan, pi

import pygame

class ImgBlock():
    '''图片块'''
    def __init__(self, posi: tuple, data: str) -> None:
        '''
            生成并初始化块：
                posi: 生成的位置
                char: 生成的内容
        '''
        self.posi = posi
        self.block_create_tick = pygame.time.get_ticks() # 储存生成的时间戳
        
        self.block_yv = random.randint(-130, -80)/10 # 沿y轴的初速度
        self.y_a = 0.5 # y轴方向的加速度
        self.block_xv = 0 # 沿x轴的初速度
        # 沿x轴的初速度不可以为 0 !!
        while not self.block_xv:
            self.block_xv = random.randint(-60,60)/10 

        self.r = 0 # 初始角度

        # 输入的是图片
        self.img_path = data
        img = pygame.image.load(self.img_path)
        self.block = img
        self.size = 1.3 

        self.block_rect = self.block.get_rect()
        self.block_rect.center = self.posi # 更新位置

        self.revoable = True
        self.moveable = True

    def set_revoable(self, state: bool):
        '''是否允许旋转'''
        self.revoable = state

    def revo(self):
        '''实现旋转'''
        # 设置旋转角度
        self.r = 180*(atan(-self.block_yv/self.block_xv)/pi) -(90 if (self.block_xv <= 0 ) else -90)

        img = pygame.image.load(self.img_path)
        self.block = pygame.transform.rotozoom(img, self.r, 0.7)

        new_block_rect = self.block.get_rect()
        new_block_rect.center = self.block_rect.center
        self.block_rect = new_block_rect

    def set_moveable(self, state: bool):
        self.moveable = state

    def move(self):
        '''实现移动'''
        self.block_rect.y += self.block_yv
        self.block_rect.x += self.block_xv
        self.block_yv += self.y_a

    def update(self):
        '''每帧更新'''
        if self.revoable:
            self.revo()
        if self.moveable:
            self.move()
        screen.blit(self.block, self.block_rect)
        self.event = list()

class TextBlock():
    '''文字块'''
    def __init__(self, posi: tuple , data: str) -> None:
        '''
            生成并初始化块：
                posi: 生成的位置
                char: 生成的内容
        '''
        self.posi = posi
        self.block_create_tick = pygame.time.get_ticks() # 储存生成的时间戳
        
        self.block_yv = random.randint(-130, -80)/10 # 沿y轴的初速度
        self.y_a = 0.5 # y轴方向的加速度
        self.block_xv = random.randint(-60,60)/10 # 沿x轴的初速度

        self.r_v = random.randint(-5,5) # 旋转的角速度
        self.r = 0 # 初始角度

        self.size = 1
        self.sizev = 0

        self.char = data
        self.f = pygame.font.Font('src/zh-cn.ttf',50) # 设置文字字体和尺寸
        text_color = '#'+bytes([
            random.randint(0, 128), # R
            random.randint(128, 255), # G
            random.randint(0, 128)  # B
            ]).hex() # 文字块的字体颜色
        text = self.f.render(self.char,True,(text_color))
        self.text_color = text_color
        self.block = text # 内容设为文字

        self.block_rect = self.block.get_rect()
        self.block_rect.center = self.posi # 更新位置

        self.revoable = True
        self.moveable = True

    def set_revoable(self, state: bool):
        '''是否允许旋转'''
        self.revoable = state

    def revo(self):
        '''实现方块旋转'''
        self.size += self.sizev
        self.r += self.r_v

        text = self.f.render(self.char, True,(self.text_color))
        self.block = pygame.transform.rotozoom(text, self.r, self.size)

        self.size += self.sizev
        self.r += self.r_v
        new_block_rect = self.block.get_rect()
        new_block_rect.center = self.block_rect.center
        self.block_rect = new_block_rect

    def set_moveable(self, state: bool):
        self.moveable = state

    def move(self):
        '''实现方块移动'''
        self.block_rect.y += self.block_yv
        self.block_rect.x += self.block_xv
        self.block_yv += self.y_a

    def update(self):
        '''每帧更新'''
        if self.revoable:
            self.revo()
        if self.moveable:
            self.move()
        screen.blit(self.block, self.block_rect)
        self.event = list()

pygame.init()

icon = pygame.image.load('src/Nahida_Happy.png')
pygame.display.set_icon(icon)

pygame.display.set_caption('Nahida')

screen = pygame.display.set_mode((1072, 603))

screen_rect = screen.get_rect()

clock = pygame.time.Clock()

# 鼠标
pygame.mouse.set_visible(False) # 隐藏鼠标指针
mouse_state = [0, 0] # 记录鼠标左右键状态以检测持续按下
mouse_pos = (0, 0) # 记录鼠标位置

# 用列表存储生成的方块
blocks_list = []

# 声音对象
pygame.mixer.init()

sound_1 = pygame.mixer.Sound('src/Da.wav')
sound_1_len = sound_1.get_length()

sound_2 = pygame.mixer.Sound('src/NaXi.wav')
sound_2_len = sound_2.get_length()

sound_3 = pygame.mixer.Sound('src/Da_JP.wav')
sound_3_len = sound_2.get_length()

sound_4 = pygame.mixer.Sound('src/NaHii_JP.wav')
sound_4_len = sound_2.get_length()

sound_5_list = [
    pygame.mixer.Sound('src/Shoot.wav'),
    pygame.mixer.Sound('src/Shoot2.wav'),
    pygame.mixer.Sound('src/Shoot3.wav')
    ]   

sound_play_tick = pygame.time.get_ticks() # 播放声音时间
sound_wait_tick = 0 # 播放等待时间，播放的声音的长度

# anime_tick1 = 0

while True:
    clock.tick(60) # 设置帧率
    # 循环获取事件，监听事件状态
    for event in pygame.event.get():
        # 关闭按钮点击
        if event.type == pygame.QUIT:
            # 卸载和关闭
            pygame.quit()
            sys.exit()

        # 键盘按下事件
        if event.type == pygame.KEYDOWN:
            print(event.key)
            # a键关闭
            if event.key == 97:
                # 卸载和关闭
                pygame.quit()
                sys.exit()

            elif event.key == 1073741884: # F3截图
                pygame.image.save(screen, 'Screen_'+ hex(int(time.time()*1000)).replace('0x', '') +'.png')

        # 鼠标按下事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down_tick = pygame.time.get_ticks()
            # 更新鼠标状态
            if event.button == 1:
                mouse_state[0] = 1

                button1_down_tick = pygame.time.get_ticks() # 记录按下的时间戳
                sound_2.play()
                sound_wait_tick = sound_2_len*900
                sound_play_tick = pygame.time.get_ticks()

            elif event.button == 3:
                mouse_state[1] = 1

                button3_down_tick = pygame.time.get_ticks() # 记录按下的时间戳
                sound_4.play()
                sound_wait_tick = sound_4_len*900
                sound_play_tick = pygame.time.get_ticks()

            elif event.button == 2:

                sound_5_list[random.randint(0,2)].play()
                blocks_list.append(ImgBlock(event.pos, 'src/Qiu.png'))
        
        # 鼠标松开事件
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_up_tick = pygame.time.get_ticks()
            if event.button == 1:
                mouse_state[0] = 0
                
            elif event.button == 3:
                mouse_state[1] = 0

            elif event.button == 2:
                pass

        # 鼠标移动事件
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos # 记录更新的鼠标位置

    screen.fill('#ccff66') # 使用纯色覆盖屏幕

    try:
        # 鼠标左键持续按下
        if mouse_state[0] == 1:
            if pygame.time.get_ticks() - sound_play_tick > sound_wait_tick: # 等待时间结束播放声音
                sound_1.play()
                sound_wait_tick = sound_1_len*700
                sound_play_tick = pygame.time.get_ticks()

            if  pygame.time.get_ticks() - button1_down_tick < sound_2_len*1000:
                blocks_list.append(TextBlock(event.pos, '纳'))
                blocks_list.append(TextBlock(event.pos, '西'))
            else:
                blocks_list.append(TextBlock(event.pos, '妲'))

        # 鼠标右键持续按下
        if mouse_state[1] == 1:
            if pygame.time.get_ticks() - sound_play_tick > sound_wait_tick:
                sound_3.play()
                sound_wait_tick = sound_3_len*400
                sound_play_tick = pygame.time.get_ticks()

            if  pygame.time.get_ticks() - button3_down_tick < sound_4_len*850:
                blocks_list.append(TextBlock(event.pos, 'ナ'))
                blocks_list.append(TextBlock(event.pos, 'ヒ'))
                blocks_list.append(TextBlock(event.pos, 'ー'))

            else:
                blocks_list.append(TextBlock(event.pos, 'ダ'))
    except AttributeError:
        pass

    # 遍历列表更新元素属性
    for n in range(len(blocks_list)):
        block = blocks_list[n]
        block.update()
        # 检测是否超出屏幕显示范围
        if  block.block_rect.top > screen_rect[3] or \
            block.block_rect.right < 0 or \
            block.block_rect.left > screen_rect[2]:
            blocks_list[n] = 0 # 超出屏幕范围删除元素
        # if pygame.time.get_ticks() - block.block_create_tick > 5000:
        #     blocks_list[n] = 0 # 超时删除元素

    # 遍历列表删除空元素
    for n in range(len(blocks_list)-1, -1, -1):
        if blocks_list[n] == 0:
            del blocks_list[n]
    
    # 图片跟随鼠标指针位置
    mouse_img = pygame.image.load('src/Nahida_Happy_Small.png')
    mouse_img_rect = mouse_img.get_rect()
    mouse_img_rect.center = mouse_pos
    screen.blit(mouse_img, mouse_img_rect)

    pygame.display.update() # 刷新显示内容 

