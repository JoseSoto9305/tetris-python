#!/usr/bin/env python
# -*- coding: utf-8 -*-

__project__ = 'TETRIS'
__file__ = './shapes.py'
__license__ = 'GPL'
__version__ = '1.0'
__date__ = 'May, 2020'
__maintainer__ = 'Jose Trinidad Soto Gonzalez'

# / -------------------------------------------------------------------------- \

import random
from copy import copy

import pygame as pg

from config import config
from color import colors, ColorEffect

# / -------------------------------------------------------------------------- \

# Shapes and rotations
T = [['000',
      '.0.'],

     ['.0',
      '00',
      '.0'],

     ['.0.',
      '000',],

     ['0.',
      '00',
      '0.']]


TT = [['000',
       '.0.',
       '.0.'],

     ['..0',
      '000',
      '..0'],

     ['.0.',
      '.0.',
      '000',],

     ['0..',
      '000',
      '0..']]


S1 = [['.00',
       '00.',],

      ['0.',
       '00',
       '.0']]


S2 = [['00.',
       '.00'],

      ['.0',
       '00',
       '0.']]


Z1 = [['.000',
       '00..',],

      ['0.',
       '0.',
       '00',
       '.0']]


Z2 = [['000.',
       '..00'],

      ['.0',
       '.0',
       '00',
       '0.']]


Z3 = [['..00',
       '000.',],

      ['0.',
       '00',
       '.0',
       '.0']]


Z4 = [['00..',
       '.000'],

      ['.0',
       '00',
       '0.',
       '0.']]



L1 = [['0.',
       '0.',
       '00'],
      
     ['000',
      '0..',],
      
     ['00',
      '.0',
      '.0'],
      
     ['..0',
      '000',]]
      

L2 = [['.0',
       '.0',
       '00'],

     ['0..',
      '000'],
      
     ['00',
      '0.',
      '0.'],

     ['000',
      '..0']]


I = [['.0.',
      '.0.',
      '.0.',
      '.0.'],

     ['....',
      '0000',
      '....']]


E = [['00',
      '.0',
      '00'],

     ['0.0',
      '000'],
      
     ['00',
      '0.',
      '00'],

     ['000',
      '0.0']]


K = [['.0.',
      '000',
      '.0.']]


O = [['00',
      '00']]


DOT = [['...',
        '.0.',
        '...']]


dict_shapes = {'T' :   T,
               'S1' :  S1,
               'S2' :  S2, 
               'L1' :  L1,
               'L2' :  L2,
               'I' :   I,               
               'O' :   O,
               'DOT' : DOT}

dict_big_shapes = {'TT' : TT,
                   'E' :  E,
                   'Z1' : Z1,
                   'Z2' : Z2,
                   'Z3' : Z3,
                   'Z4' : Z4,                   
                   'K' :  K}               

shape_colors = {'T' :   colors['pink'],
                'TT' :  colors['pink'],
                'S1' :  colors['purple'],
                'S2' :  colors['purple'],
                'Z1' :  colors['orange'],
                'Z2' :  colors['orange'],                
                'Z3' :  colors['orange'],
                'Z4' :  colors['orange'],                                
                'L1' :  colors['cherry'],
                'L2' :  colors['cherry'],
                'I' :   colors['blue'],
                'E' :   colors['yellow'],
                'K' :   colors['green'],
                'O' :   colors['artic'],
                'DOT' : colors['yellow']}
                
# Weights for random choice                                 
weights = {'T' :   0.95,
           'S1' :  0.95,
           'S2' :  0.95,
           'L1' :  0.95,
           'L2' :  0.95,
           'I' :   0.95,
           'O' :   0.95,
           'DOT' : 0.05}

weights_big_shapes = {'TT' :  0.25,
                      'Z1' :  0.10,
                      'Z2' :  0.10,
                      'Z3' :  0.10,
                      'Z4' :  0.10,                      
                      'E' :   0.25,
                      'K' :   0.25}

class Shapes:
    
    # / ----------------------------------------------------------------------- \

    def __init__(self):

        # Dropped blocks
        self.dropped = []
        self.dropped_index = []
        self.dropped_colors = []

        # Eresed blocks
        self.eresed = []
        self.eresed_colors = []
        
        if config.big_shapes:
            self.dict_shapes = {**dict_shapes, **dict_big_shapes}
            self.weights = {**weights, **weights_big_shapes}

        else:
            self.dict_shapes = dict_shapes
            self.weights = weights
        
    # / ----------------------------------------------------------------------- \

    def restart(self):

        self.dropped = []
        self.dropped_index = []
        self.dropped_colors = []
        
        self.eresed = []
        self.eresed_colors = []

        if config.big_shapes:
            self.dict_shapes = {**dict_shapes, **dict_big_shapes}
            self.weights = {**weights, **weights_big_shapes}

        else:
            self.dict_shapes = dict_shapes
            self.weights = weights            
        
    # / ----------------------------------------------------------------------- \
                
    def next_shape(self, shape=None):
        
        self.pressed_x_speed = config.block_size
        self.pressed_y_speed = 0
        
        if shape is None:
            self.shape_key = random.choices(list(self.dict_shapes.keys()), weights=list(self.weights.values()))[0]
            self.n_positions = len(self.dict_shapes[self.shape_key])
            self.position = random.randint(0, self.n_positions-1)

        else:
            # Copy the shape key and position from input Shape instance
            self.shape_key = copy(shape.shape_key)
            self.n_positions = copy(shape.n_positions)
            self.position = copy(shape.position)

        # Initial (x, y) position
        self.x =  config.game_boundaries[0] +  (config.ncols // 2  - 1) * config.block_size
        self.y = -(len(self.dict_shapes[self.shape_key][self.position]) * config.block_size)

        # Color
        self.shape_color = ColorEffect(shape_colors[self.shape_key], interval=45, length=10)

        self.get_shape()        
        self.move = True
        
    # / ----------------------------------------------------------------------- \
                
    def get_shape(self):
  
        # self.shape is a list of pg.Rect
        self.shape = []
        
        for i, row in enumerate(self.dict_shapes[self.shape_key][self.position]):
            for j, column in enumerate(row):
                if column == '0':
                    x = self.x + config.block_size * j
                    y = self.y + config.block_size * i
                    rect = pg.Rect(x, y, config.block_size, config.block_size)
                    self.shape.append(rect)

        self.shape_corners = self.get_shape_corners()
        self.center = self.get_shape_center()
        
    # / ----------------------------------------------------------------------- \

    def get_shape_corners(self):
        xs = [rect[0] for rect in self.shape]
        ys = [rect[1] for rect in self.shape]
        xmin = min(xs)
        ymin = min(ys)
        xmax = max(xs) + config.block_size
        ymax = max(ys) + config.block_size
        self.shape_corners = [xmin, ymin, xmax, ymax]
        return self.shape_corners        
        
    # / ----------------------------------------------------------------------- \

    def get_shape_center(self):
        cx = self.shape_corners[0] + (self.shape_corners[2] - self.shape_corners[0]) / 2
        cy = self.shape_corners[1] + (self.shape_corners[3] - self.shape_corners[1]) / 2
        self.center = [cx, cy]
        return self.center
        
    # / ----------------------------------------------------------------------- \

    def get_index(self, x, y):
        # Get row and column index when shape can't move down'
        row = int((y - config.game_boundaries[1]) / config.block_size)
        col = int((x - config.game_boundaries[0]) / config.block_size)
        return row, col    
        
    # / ----------------------------------------------------------------------- \

    def difference(self, bound, current_shape_bound, direction='bottom'):
        
        diff = 0
        if direction == 'left':
            if current_shape_bound < bound:
                diff = bound - current_shape_bound

        elif direction == 'right':
            if current_shape_bound > bound:
                diff = bound - current_shape_bound

        elif direction == 'bottom':
            if current_shape_bound > bound:
                diff = bound - current_shape_bound

        return diff        
        
    # / ----------------------------------------------------------------------- \

    def move_down(self, pressed_y=None):
        
        self.move = True
        
        if pressed_y is not None:
            if pressed_y:
                self.pressed_y_speed = 10
            else:
                self.pressed_y_speed = 0
         
        y_move = config.speed + self.pressed_y_speed        
        self.move_shape(0, y_move)
        
        # See if next position is filled:
        if self.dropped and self.shape_key != 'DOT':
            for rect1 in self.dropped:
                for rect2 in self.shape:
                    if rect1.colliderect(rect2):
                        diff = self.difference(rect1.top, rect2.bottom, 'bottom')
                        self.move_shape(0, diff)
                        self.move = False                        
                        return self.move

        # See if shape is out the bottom boundarie
        diff = self.difference(config.game_boundaries[3], self.shape_corners[3], 'bottom')
        if diff != 0:
            self.move_shape(0, diff)
            self.move = False
            return self.move

        return self.move
        
    # / ----------------------------------------------------------------------- \
        
    def move_left(self):
        
        self.move_shape(-self.pressed_x_speed, 0)
        
        # See if shape is out of left boundarie
        diff = self.difference(config.game_boundaries[0], self.shape_corners[0], 'left')        
        if diff != 0:
            self.move_shape(diff, 0)
        
        # See if next position is filled:
        if self.dropped and self.shape_key != 'DOT':
            for rect1 in self.dropped:
                for rect2 in self.shape:
                    if rect1.colliderect(rect2):
                        diff = self.difference(rect1.right, rect2.left,  'left')
                        self.move_shape(diff, 0)
                        return None
                        
    # / ----------------------------------------------------------------------- \

    def move_right(self):
        
        # See if shape is out of right boundarie
        self.move_shape(self.pressed_x_speed, 0)        
        diff = self.difference(config.game_boundaries[2], self.shape_corners[2], 'right')
        if diff != 0:
            self.move_shape(diff, 0)
            
        # See if next position is filled:
        if self.dropped and self.shape_key != 'DOT':
            for rect1 in self.dropped:
                for rect2 in self.shape:
                    if rect1.colliderect(rect2):
                        diff = self.difference(rect1.left, rect2.right, 'right')
                        self.move_shape(diff, 0)                        
                        return None
                        
    # / ----------------------------------------------------------------------- \

    def move_shape(self, x, y):
        self.x += x
        self.y += y
        self.shape = [rect.move(x, y) for rect in self.shape]
        self.shape_corners = self.get_shape_corners()
        self.center = self.get_shape_center()
        
    # / ----------------------------------------------------------------------- \

    def rotate(self):
        
        # Change position
        self.position += 1
        if self.position >= self.n_positions:
            self.position = 0
        
        # Update the shape to the new position
        self.get_shape()

        # If rotated shape is out of bounds
        diff_left = self.difference(config.game_boundaries[0],  self.shape_corners[0], 'left')
        if diff_left != 0:
            self.move_shape(diff_left, 0)
        
        diff_right = self.difference(config.game_boundaries[2], self.shape_corners[2], 'right')
        if diff_right != 0:
            self.move_shape(diff_right, 0)

        # If rotated shape colaps with any block
        if self.dropped:
            if any(rect1.colliderect(rect2) for rect1 in self.shape for rect2 in self.dropped):
                self.position -= 1
                if self.position < 0:
                    self.position = self.n_positions - 1

                self.get_shape()

                if diff_left != 0:
                    self.move_shape(-diff_left, 0)

                if diff_right != 0:
                    self.move_shape(-diff_right, 0)
                    
    # / ----------------------------------------------------------------------- \
              
    def update_filled_spaces(self):
        # Append current shape to the dropped shapes
        for rect in self.shape:
            row, col = self.get_index(rect.left, rect.top)
            self.dropped.append(rect)
            self.dropped_index.append([row, col])
            self.dropped_colors.append(self.shape_color)

    # / ----------------------------------------------------------------------- \

    def erese_blocks(self):

        n_eresed = 0

        # Remove blocks when the row is fiilled
        if self.dropped and self.shape_key != 'DOT':
            
            # Get the IDs for the filled rows
            indexes_removed = []
            removed_rows = []
            for row in range(config.nrows)[::-1]:
                cols_filled = [i for i, idx in enumerate(self.dropped_index) if idx[0] == row]
                if len(cols_filled) == config.ncols:                    
                    removed_rows.append(row)
                    indexes_removed.extend(cols_filled)
            
            if removed_rows:
                
                # Get the blocks that most be removed
                self.eresed = [self.dropped[i] for i in indexes_removed]
                self.eresed_colors = [self.dropped_colors[i] for i in indexes_removed]
                
                # Remove the blocks
                indexes = [i for i in range(len(self.dropped_index)) if i not in indexes_removed]
                self.dropped = [self.dropped[i] for i in indexes]
                self.dropped_index = [self.dropped_index[i] for i in indexes]
                self.dropped_colors = [self.dropped_colors[i] for i in indexes]

                # See which blocks must be move down
                to_update = []
                for i, row in enumerate(removed_rows):
                    for j, rect in enumerate(self.dropped):
                        if self.dropped_index[j][0] < row:
                            to_update.append(j)

                # Move down the blocks
                for index in to_update:
                    self.dropped[index] = self.dropped[index].move(0, config.block_size)
                    self.dropped_index[index][0] += 1

                n_eresed = len(self.eresed)
                            
        if self.shape_key =='DOT' and not self.move:
             
             # Remove the blocks by column
             row, col = self.dropped_index[-1]
             rows_filled = [i for i, idx in enumerate(self.dropped_index) if idx[1] == col]             
             indexes = [i for i, idx in enumerate(self.dropped_index) if idx[1] != col]
             
             self.eresed = [self.dropped[idx] for idx in rows_filled]
             self.eresed_colors = [self.dropped_colors[idx] for idx in rows_filled]

             self.dropped = [self.dropped[idx] for idx in indexes]
             self.dropped_index = [self.dropped_index[idx] for idx in indexes]
             self.dropped_colors = [self.dropped_colors[idx] for idx in indexes]

             n_eresed = len(self.eresed)

        return n_eresed
        
    # / ----------------------------------------------------------------------- \

    def draw_eresed(self, screen):
        for i, rect, in enumerate(self.eresed):
            color = self.eresed_colors[i].change_color()
            color = self.eresed_colors[i].modify_color(color, l=-20)
            pg.draw.rect(screen, color, rect)
            pg.draw.rect(screen, colors['white'], rect, 1)
            
        self.eresed = []
        self.eresed_colors = []
            
        pg.display.update()
        pg.time.wait(350)

    # / ----------------------------------------------------------------------- \        

    def draw_shape(self, screen):
        color = self.shape_color.change_color()
        for rect in self.shape:
            if rect.bottom > config.game_boundaries[1]:
                pg.draw.rect(screen, color, rect)
                pg.draw.rect(screen, colors['white'], rect, 1)

    # / ----------------------------------------------------------------------- \

    def draw_filled(self, screen):
        if self.dropped:
            for i, rect in enumerate(self.dropped):
                color = self.dropped_colors[i].change_color()
                pg.draw.rect(screen, color, rect)
                pg.draw.rect(screen, colors['white'], rect, 1)

    # / ----------------------------------------------------------------------- \
    
    def draw_next_shape(self, x, y, screen):
        
        dx = x - self.center[0]
        dy = y - self.center[1]
        self.move_shape(dx, dy)

        color = self.shape_color.change_color()
        for rect in self.shape:
            pg.draw.rect(screen, color, rect)
            pg.draw.rect(screen, colors['white'], rect, 1)               
    
    # / ----------------------------------------------------------------------- \         
   
 # / -------------------------------------------------------------------------- \
 # / --------------------------------------------------- \
 # / -------------------------------- \
 # / ------------- \
 # / END