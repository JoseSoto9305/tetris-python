#!/usr/bin/env python
# -*- coding: utf-8 -*-

__project__ = 'TETRIS'
__file__ = './tetris.py'
__license__ = 'GPL'
__version__ = '1.0'
__date__ = 'May, 2020'
__maintainer__ = 'Jose Trinidad Soto Gonzalez'

# / -------------------------------------------------------------------------- \

import os
import random
import string
import pygame as pg

from shapes import Shapes
from config import config
from score import Score
from color import colors, ColorEffect

# / -------------------------------------------------------------------------- \

score = Score()        
shape = Shapes()
next_shape = Shapes()
color_effect = ColorEffect(length=15)

class Button:
    
    # / ----------------------------------------------------------------------- \
    
    def __init__(self, key, function, draw_on):
        
        self.key = key
        
        # Button position and dimentions
        self.x = config.buttons_size[self.key]['x']
        self.y = config.buttons_size[self.key]['y']
        self.w = config.buttons_size[self.key]['w']
        self.h = config.buttons_size[self.key]['h']
        
        self.x_center = self.x + (self.w / 2)
        self.y_center = self.y + (self.h / 2)

        self.button = pg.Rect(self.x, self.y, self.w, self.h)
        self.button_on = False
        self.function = function
        
        # Draw the button on this surface
        self.screen = draw_on        

        self.draw_params = {'button' : self.button,
                            'text' : self.key,
                            'x_center' : self.x_center,
                            'y_center' : self.y_center}

    # / ----------------------------------------------------------------------- \

    def draw_button(self, color_active=False):
        
        color = color_effect.change_color()
        if color_active:
            color = color_effect.modify_color(color, l=-20)
            
        draw_params = self.draw_params.copy()
        if isinstance(draw_params['button'], list):
            pg.draw.polygon(self.screen, color, draw_params['button'])
        else:
            pg.draw.rect(self.screen, color, draw_params['button'], 5)
            
        draw_params.pop('button')
        surface, rect = config.text_objects(**draw_params, color=color)
        self.screen.blit(surface, rect)        
    
    # / ----------------------------------------------------------------------- \

    def status(self):

        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
                
        if self.button.collidepoint(pos):  
            self.draw_button(color_active=True)
            if click[0] == 1:
                self.button_on = True
        else:
            self.draw_button()                

        return self.button_on

        
    # / ----------------------------------------------------------------------- \
    
    def __call__(self):
        # Run button function if button is turn on
        if self.button_on:
            self.button_on = False
            self.function()
    
    # / ----------------------------------------------------------------------- \


class  Spinner(Button):
    
    # / ----------------------------------------------------------------------- \
    
    def __init__(self, key, function, draw_on):

        Button.__init__(self, key, function, draw_on)        
        
        # Values to put on the spinner
        if self.key == 'speed':
            self.current_val = f'{config.speed}'
            self.vals = list(range(1,11))                        
            self.vals_font_size = config.small_text
        
        elif self.key == 'ncols':
            self.current_val = f'{config.ncols}'
            self.vals = sorted(list(set([i[1] for i in config.grid_sizes])))
            self.vals_font_size = config.small_text
        
        elif self.key == 'next shape':
            self.key = f'Enable next shape'
            if config.see_next_shape:
                self.current_val = ' On'
            else:
                self.current_val = ' Off'
            self.vals = ['On', 'Off']
            self.vals_font_size = int(config.small_text - config.small_text * 0.3)

        elif self.key == 'big shapes':
            self.key = f'Enable big shapes'
            if config.big_shapes:
                self.current_val = ' On'
            else:
                self.current_val = ' Off'
            self.vals = ['On', 'Off']
            self.vals_font_size = int(config.small_text - config.small_text * 0.3)

        self.text = f'{self.key } {self.current_val}'            

        surface, rect = config.text_objects(self.text, 
                                            left=self.x, 
                                            top=self.y, 
                                            font_size=config.medium_text)        
        self.button_x, self.button_y = rect.bottomright
        self.button = pg.Rect(self.button_x, self.button_y, self.w, self.h)
        
        self.triangle = [[self.button_x, self.button_y],
                         [self.button_x + self.w, self.button_y],
                         [self.button_x + self.w / 2, self.button_y + self.h]]

        self.draw_params = {'button' : self.triangle,
                            'text' : self.text,
                            'left' : self.x,
                            'top' : self.y,
                            'font_size' : config.medium_text}

    # / ----------------------------------------------------------------------- \

    def __call__(self):
        
        # Display the values of the spinner when the button is turn on
        if self.button_on:
            pg.time.wait(250)
        
            color_text = colors['berry']
            color_text_act = color_effect.modify_color(colors['purple'], l=-50)

            rect_spinner = pg.Rect(self.button_x, self.button_y, self.w, self.h * len(self.vals))
            cx = self.button_x + self.w / 2
            cy = self.button_y

            running = True
            while running:

                pg.event.pump()
                pos = pg.mouse.get_pos()
                click = pg.mouse.get_pressed()

                color_rect = color_effect.change_color()
                pg.draw.rect(self.screen, color_rect, rect_spinner)
            
                for i in range(len(self.vals)):
                    surface, rect = config.text_objects(f'{self.vals[i]}', 
                                                        x_center=cx, 
                                                        y_center=cy + self.h/2 + i * self.h, 
                                                        color=color_text, 
                                                        font_size=self.vals_font_size)
                    rect_button = rect.copy()
                    rect_button.left = self.button_x
                    rect_button.width = self.w
                    if rect_button.collidepoint(pos):
                        if click[0] == 1:
                            self.function(self.vals[i])
                            self.current_val = f'{self.vals[i]}'
                            self.text = f'{self.key } {self.current_val}'
                            self.draw_params['text'] = self.text
                            running = False                            
                        surface, rect = config.text_objects(f'{self.vals[i]}', 
                                                            x_center=cx, 
                                                            y_center=cy + self.h/2 + i * self.h, 
                                                            color=color_text_act, 
                                                            font_size=self.vals_font_size*2)
                        self.screen.blit(surface, rect)

                    else:
                        self.screen.blit(surface, rect)

                pg.display.update()

                if not rect_spinner.collidepoint(pos):
                    running = False

            self.button_on = False
            pg.time.wait(250)

    # / ----------------------------------------------------------------------- \
    

class Tetris:
    
    # / ----------------------------------------------------------------------- \
    
    def __init__(self):                
        
        self.screen = pg.display.set_mode((config.window_w, config.window_h))        
        pg.display.set_caption('TETRIS')
        pg.display.set_icon(config.images['ICON'])   # This doesn't work on Linux Mint :(
                                                     # or at least only in my computer
                    
        self.functions = {pg.K_LEFT :      shape.move_left,
                          pg.K_RIGHT :     shape.move_right,
                          pg.K_DOWN :      shape.move_down,
                          pg.K_r :         shape.rotate,
                          pg.K_q :         self.exit,
                          pg.K_SPACE :     self.pause,
                          'START' :        self.play,
                          'OPTIONS' :      self.options,
                          'RANKING' :      self.ranking,
                          'BACK' :         self.menu,
                          'HOME' :         self.home,                       
                          'CONTINUE' :     self._continue,
                          'RESTART GAME' : self.restart_game,
                          'EXIT':          self.exit,
                          'speed' :        self.change_speed,
                          'ncols' :        self.change_ncols,
                          'next shape' :   self.enable_next_shape,
                          'big shapes' :   self.enable_big_shapes}
                       
        self.running = False

    # / ----------------------------------------------------------------------- \
    # Drawing functions
    # / ----------------------------------------------------------------------- \

    def draw_score(self, color):
        text = f'Score : {score.score}'
        surface, rect = config.text_objects(text,  
                                            x_center=config.texts['score']['x'],
                                            y_center=config.texts['score']['y'],
                                            color=color)
        self.screen.blit(surface, rect)

    # / ----------------------------------------------------------------------- \

    def draw_speed(self, color):
        text = f'Speed : {config.speed}'
        surface, rect = config.text_objects(text,  
                                            x_center=config.texts['speed']['x'],
                                            y_center=config.texts['speed']['y'],
                                            color=color)
        self.screen.blit(surface, rect)

    # / ----------------------------------------------------------------------- \

    def draw_next_shape(self, color):
        if config.see_next_shape:
            
            cx, cy = config.rects['next_shape'].center
            next_shape.draw_next_shape(cx, cy, self.screen)
            
            pg.draw.rect(self.screen, color, config.rects['next_shape'], 5)
            
            surface, rect = config.text_objects('Next Shape', 
                                                x_center=config.texts['next_shape']['x'], 
                                                y_center=config.texts['next_shape']['y'],
                                                color=color)
            self.screen.blit(surface, rect)                                            
            
    # / ----------------------------------------------------------------------- \

    def draw_background(self):

        color = color_effect.change_color()

        # Background
        self.screen.blit(config.images['GAME BACKGROUND'], (0,0))

        # Game boundaries
        pg.draw.rect(self.screen, color, config.rects['game_boundaries'], 5)

        # Another objects
        self.draw_next_shape(color)
        self.draw_score(color)
        self.draw_speed(color)

    # / ----------------------------------------------------------------------- \

    def draw_records(self, names, records, color):

        text = 'TOP FIVE'
        x = config.texts['top five']['x']
        y = config.texts['top five']['y']
        surface, rect = config.text_objects(text, left=x, top=y, color=color)
        self.screen.blit(surface, rect)

        for i in range(len(records)):
            
            text = f'{names[i]} ......... {records[i]:2}'
            x = config.texts['records']['x']
            y = config.texts['records']['y'] +  i * config.texts['records']['y_space']
            surface, rect = config.text_objects(text, left=x, top=y, color=color)
            self.screen.blit(surface, rect)

    # / ----------------------------------------------------------------------- \

    def draw_game_over(self):

        text = 'GAME OVER'
        surface, rect = config.text_objects(text, 
                                            x_center=config.texts['game_over']['x'],  
                                            y_center=config.texts['game_over']['y'],
                                            rotation_angle=45,
                                            font_size=config.huge_text,
                                            color=colors['berry'])
        self.screen.blit(surface, rect)
        pg.display.update()
        pg.time.wait(2000)

    # / ----------------------------------------------------------------------- \

    def start_count(self):

        texts = ['3', '2', '1', 'GO!']

        for text in texts:
            color = color_effect.change_color()
            surface, rect = config.text_objects(text,
                                                x_center=config.texts['start']['x'],
                                                y_center=config.texts['start']['y'],
                                                font_size=config.huge_text,
                                                color=color)
            self.draw_background()
            self.screen.blit(surface, rect)
            pg.display.update()
            pg.time.wait(1000)
                    
    # / ----------------------------------------------------------------------- \

    # Functions

    # / ----------------------------------------------------------------------- \
    
    def exit(self):
        pg.quit()
        quit()

    # / ----------------------------------------------------------------------- \

    def pause(self):
        pause = True
        while pause:            
            event = pg.event.wait()
            
            if event.type == pg.QUIT:
                self.exit()   

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pause = False    
        
    # / ----------------------------------------------------------------------- \
        
    def level_up(self):
        pg.time.wait(2000)
        shape.restart()
        self.start_count()

    # / ----------------------------------------------------------------------- \

    def _continue(self):        
        shape.restart()
        score.restart(level=True)
        self.play()

    # / ----------------------------------------------------------------------- \

    def restart_game(self):        
        config.speed = 1
        shape.restart()        
        score.restart()
        self.play()

    # / ----------------------------------------------------------------------- \

    def home(self):
        config.speed = 1
        shape.restart()        
        score.restart()
        self.menu()        

    # / ----------------------------------------------------------------------- \
    
    def is_losser(self):
        loss = False
        if any(rect.bottom <= config.game_boundaries[1] for rect in shape.dropped):
            loss = True
        return loss
        
    # / ----------------------------------------------------------------------- \
    
    def change_speed(self, value):
        config.speed = value
        score.restart()
        
    # / ----------------------------------------------------------------------- \
        
    def change_ncols(self, value):
        grid_size = [i for i in config.grid_sizes if i[1] == value][-1]
        config.nrows, config.ncols, config.block_size, config.game_boundaries = grid_size
        config.set_objects_sizes()
        score.restart()

    # / ----------------------------------------------------------------------- \

    def enable_next_shape(self, value):
        if value == 'On':
            config.see_next_shape = True
        elif value == 'Off':
            config.see_next_shape = False

    # / ----------------------------------------------------------------------- \

    def enable_big_shapes(self, value):
        
        if value == 'On':
            config.big_shapes = True
            
        elif value == 'Off':
            config.big_shapes = False

        shape.restart()
        next_shape.restart()

    # / ----------------------------------------------------------------------- \

    # Interactive functions

    # / ----------------------------------------------------------------------- \

    def menu(self):
                
        key_buttons = ['START', 'OPTIONS', 'RANKING', 'EXIT']
        buttons = [Button(key, self.functions[key], self.screen) for key in key_buttons]
        
        text = 'Press F1 to see keyboard instructions'
        cx = config.texts['instructions']['x']
        cy = config.texts['instructions']['y']

        self.running = True
        while self.running:
                
            for event in pg.event.get():                
                if event.type == pg.QUIT:
                    self.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_F1:
                        button = self.see_instructions
                        buttons.append(button)
                        self.running = False                        

            self.screen.blit(config.images['MENU BACKGROUND'], (0,0))


            surface, rect = config.text_objects(text, 
                                                x_center=cx, 
                                                y_center=cy,
                                                font_size=config.medium_text,
                                                color=color_effect.change_color())
            self.screen.blit(surface, rect)

            for button in buttons:
                if isinstance(button, Button):
                    button.status()
                    if button.button_on:
                        self.running = False
                    
            pg.display.update()
            config.clock.tick(config.fps)            

        pg.time.wait(250)
        
        for button in buttons:
            button()

    # / ----------------------------------------------------------------------- \

    def see_instructions(self):

        key_button = 'BACK'
        button = Button(key_button, self.functions[key_button], self.screen)

        self.running = True
        while self.running:
        
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()

            self.screen.blit(config.images['INSTRUCTIONS'], (0,0))
           
            button.status()
            if button.button_on:
                self.running = False
                                
            pg.display.update()
            config.clock.tick(config.fps)
            
        button()            

    # / ----------------------------------------------------------------------- \

    def ranking(self):
                                
        names, records = score.load_records()
        
        key_button = 'BACK'
        button = Button(key_button, self.functions[key_button], self.screen)

        self.running = True
        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()

            self.screen.blit(config.images['RECORDS BACKGROUND'], (0,0))
           
            button.status()
            if button.button_on:
                self.running = False
                                
            color = color_effect.change_color()
            self.draw_records(names, records, color)
            
            pg.display.update()
            config.clock.tick(config.fps)
            
        button()            

    # / ----------------------------------------------------------------------- \

    def options(self):
                
        key_button = 'BACK'
        button = Button(key_button, self.functions[key_button], self.screen)

        key_spinners = ['speed', 'ncols', 'next shape', 'big shapes']
        spinners = [Spinner(key, self.functions[key], self.screen) for key in key_spinners]
        
        self.running = True
        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()

            self.screen.blit(config.images['OPTIONS BACKGROUND'], (0,0))

            button.status()
            if button.button_on:
                self.running = False

            for spinner in spinners:                
                spinner.status()
            
            for spinner in spinners:
                spinner()

            pg.display.update()
            config.clock.tick(config.fps)
            
        button()                   

    # / ----------------------------------------------------------------------- \

    def restart_continue(self):
                                
        key_buttons = ['HOME', 'CONTINUE', 'RESTART GAME', 'EXIT']
        buttons = [Button(key, self.functions[key], self.screen) for key in key_buttons]

        self.running = True
        while self.running:
                
            for event in pg.event.get(): 
                if event.type == pg.QUIT:
                    self.exit()

            self.screen.blit(config.images['MENU BACKGROUND'], (0,0))

            for button in buttons:
                button.status()
                if button.button_on:
                    self.running = False

            pg.display.update()
            config.clock.tick(config.fps)

        for button in buttons:
            if button.button_on:
                return button

    # / ----------------------------------------------------------------------- \                                            

    def write_record(self):

        chars = string.ascii_uppercase
        chars += string.digits
        chars += '!$&?@^~_'

        name = list(f'{chars[-1]}    ')

        chars_index = 0
        name_index = 0
        count = 0

        self.running = True
        while self.running:            

            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    self.exit()

                if event.type == pg.KEYDOWN: 
                    if event.key == pg.K_RETURN:
                        count += 1
                        if count < 3:
                            name_index += 2
                            chars_index = 0
                                        
                    if event.key == pg.K_BACKSPACE:
                        if name_index > 0:
                            chars_index = -1
                            name_index -= 2
                            count -= 1
                
                    else:
                        if event.key == pg.K_DOWN:
                            chars_index -= 1
                            if chars_index < ~(len(chars)-1):
                                chars_index = -1

                        elif event.key == pg.K_UP: 
                            chars_index += 1
                            if chars_index > len(chars)-1:
                                chars_index = 0
                            
                if event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN or event.key == pg.K_UP:
                        chars_index += 0

            name[name_index] = chars[chars_index]            

            text = ''.join(name)
            color = color_effect.change_color()
            surface, rect = config.text_objects(text, 
                                                x_center=config.texts['write_record']['x'], 
                                                y_center=config.texts['write_record']['y'],
                                                color=color)
            # Draw background
            pg.draw.rect(self.screen, colors['gray'], rect)
            self.screen.blit(surface, rect)

            pg.display.update()
            config.clock.tick(config.fps)

            if count == 3:
                self.running = False
        
        name = ''.join(name)
        name = name.replace(' ', '')
        score.save_record(name)

        pg.time.wait(2000)

    # / ----------------------------------------------------------------------- \
                            
    def play(self):

        shape.next_shape()
        next_shape.next_shape()        

        # Flag to see if user is holding left or right keys
        left_on = False
        right_on = False

        self.start_count()
        
        self.running = True  
        while self.running:

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    self.exit()
                
                elif event.type == pg.KEYDOWN: 
                    if event.key in self.functions:
                        if event.key == pg.K_DOWN:
                            self.functions[event.key](pressed_y=True)
                        else:
                            self.functions[event.key]()

                        if event.key == pg.K_LEFT:
                            left_on = True

                        elif event.key == pg.K_RIGHT:
                            right_on = True
                
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN:
                        self.functions[event.key](pressed_y=False)

                    if event.key == pg.K_LEFT:
                        left_on = False

                    if event.key == pg.K_RIGHT:
                        right_on = False
            
            self.draw_background()    
            shape.move_down()
                    
            if not shape.move:
                
                # If shape can't move down, but the user is
                # holding left or right keys'
                if left_on:
                    shape.move_left()
                    left_on = False

                if right_on:
                    shape.move_right()
                    right_on = False
                
                # If moved shape can stil move down
                if shape.move_down():
                    shape.move = True

                else:
                    # Append shape to dropped shapes                    
                    shape.update_filled_spaces()
               
            shape.draw_filled(self.screen)
            shape.draw_shape(self.screen)
                                           
            pg.display.update()
            config.clock.tick(config.fps)            

            n_eresed = shape.erese_blocks()
            if n_eresed > 0:
                score.update_score(n_eresed)
                shape.draw_eresed(self.screen)
                
            if not shape.move:
                shape.next_shape(shape=next_shape)
                next_shape.next_shape()

            if self.is_losser():
                self.draw_game_over()
                self.write_record()
                button = self.restart_continue()
                
            if score.level_up():
                self.level_up()

        pg.time.wait(250)
        button()
        
    # / ----------------------------------------------------------------------- \

if __name__ == '__main__':
              
    tetris = Tetris()
    tetris.menu()

 # / -------------------------------------------------------------------------- \
 # / --------------------------------------------------- \
 # / -------------------------------- \
 # / ------------- \
 # / END