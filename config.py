#!/usr/bin/env python
# -*- coding: utf-8 -*-

__project__ = 'TETRIS'
__file__ = './config.py'
__license__ = 'GPL'
__version__ = '1.0'
__date__ = 'May, 2020'
__maintainer__ = 'Jose Trinidad Soto Gonzalez'

# / -------------------------------------------------------------------------- \

import pygame as pg
from color import colors

# / -------------------------------------------------------------------------- \

class Configuration:
    
    # / ----------------------------------------------------------------------- \

    def __init__(self):

        pg.init()
        pg.mixer.init()

        # Screen information
        info = pg.display.Info()

        self.reference_w = info.current_w
        self.reference_h = info.current_h

        self.window_w = int(self.reference_w * 0.80)
        self.window_h = self.reference_h
        
        # Background images
        self.images = {'MENU BACKGROUND' :    self.load_image('./Images/menu_background.png'),
                       'OPTIONS BACKGROUND' : self.load_image('./Images/options_background.png'),
                       'RECORDS BACKGROUND' : self.load_image('./Images/records_background.png'),
                       'GAME BACKGROUND' :    self.load_image('./Images/game_background.png'),
                       'INSTRUCTIONS' :       self.load_image('./Images/instructions.png'),
                       'ICON' :               self.load_image('./Images/icon.png')}
        
        # Time settings
        self.clock = pg.time.Clock()
        # Frames per second
        self.fps = 30

        # Grid size (gameboard)
        min_ncols = 9
        min_block_size = 24
        max_block_size = 40
        self.grid_sizes = [self.grid_size(size) for size in range(min_block_size, max_block_size+1, 2)]
        self.grid_sizes = [grid_size for grid_size in self.grid_sizes if grid_size[1] >= min_ncols]
        self.nrows, self.ncols, self.block_size, self.game_boundaries = self.grid_sizes[-1]

        # Falling speed
        self.speed = 1
        
        # Rows to remove to pass level
        self.removed_rows = 20

        # Font sizes
        self.small_text = 18
        self.medium_text = 24
        self.larger_text = 45
        self.huge_text = 150

        self.set_objects_positions()
        self.set_buttons_positions()

        # Enable big shapes
        self.big_shapes = False

        # Enable display next shape
        self.see_next_shape = True

        # Work later
        self.sound_on = True
        self.sounds_files = {'MENU' :      './sounds/menu.wav',
                             'PLAYING' :   './sounds/playing.wav',
                             'GAME OVER' : './sounds/game_over.wav',
                             'ROTATE' :    './sounds/rotate.wav',
                             'MOVE' :      './sounds/move.wav',
                             'ERESE' :     './sounds/erese.wav',
                             'DROP' :      './sounds/drop.wav'}

    # / ----------------------------------------------------------------------- \
    
    def grid_size(self, block_size=40):

        # Gameboard boundaries
        x_proportion = 0.35
        y_proportion = 0.10

        xmin = int(self.window_w * x_proportion)
        xmax = int(self.window_w - self.window_w * x_proportion)
        ymin = int(self.window_h * y_proportion)
        ymax = int(self.window_h - self.window_h * y_proportion)
        
        rx = xmin % block_size
        if rx > 0:
            xmin -= rx
        rx = xmax % block_size
        if rx > 0:
            rx = block_size - rx
            xmax += rx

        ry = ymin % block_size
        if ry > 0:
            ymin -= ry
        ry = ymax % block_size
        if ry > 0:
            ry = block_size - ry
            ymax += ry
        
        w = xmax - xmin
        h = ymax - ymin                
        
        # Grid size
        ncols = int(w / block_size)    
        nrows = int(h / block_size)
            
        # Ncols must be an odd number
        if not ncols % 2:
            ncols += 1
            xmin -= int(block_size / 2)
            xmax += int(block_size / 2)
            w += block_size

        game_boundaries = [xmin, ymin, xmax, ymax]

        return nrows, ncols, block_size, game_boundaries
        
    # / ----------------------------------------------------------------------- \

    def text_objects(self, 
                     text='', 
                     x_center=None, y_center=None,     # Center text position or
                     left=None, top=None,              # Upper left text position
                     rotation_angle=None,
                     color=colors['cherry'], 
                     font_size=None, 
                     window_w=None,
                     window_h=None):

        if font_size is None:
            font_size = self.larger_text
        if window_w is None:
            window_w = self.window_w
        if window_h is None:
            window_h = self.window_h

        # Scaling the text
        font = pg.font.SysFont('purisa', int(font_size * window_h / self.reference_h))
        text_surface = font.render(text, True, color)

        text_w, text_h = text_surface.get_size()
        text_surface = pg.transform.smoothscale(text_surface, (text_w * window_w // self.reference_w, 
                                                               text_h * window_h // self.reference_h))

        # Rotate the text
        if rotation_angle is not None:
            text_surface = pg.transform.rotate(text_surface, rotation_angle)

        # Text position
        text_rect = text_surface.get_rect()
        if x_center is not None and y_center is not None:
            text_rect.center = x_center, y_center

        if left is not None and top is not None:
            text_rect.topleft = [left, top]

        return text_surface, text_rect

    # / ----------------------------------------------------------------------- \

    def set_buttons_positions(self):
        
        scale = 1092 / 350

        w_button1 = self.window_w / 3.5
        w_button2 = self.window_w / 7.5
        w_button3 = self.window_w / 27.3
        h_button1 = self.window_h / 10.25
        h_button2 = self.window_h / 25.6
        y_space_buttons = self.window_h / 7.5

        # Uppercase is for buttons; 
        # 'x' and 'y' is for the upper left coordinate of the button

        # Lowercase is for spinners; 
        # 'x' and 'y' is for the upper left coordinate of the text:  `ncols {current value} [spinner arrow]`
        self.buttons_size = {'START' : {'x' : self.window_w / 4 * 3 - w_button1/ 2,
                                        'y' : self.window_h / 3,
                                        'w' : w_button1,
                                        'h' : h_button1},
                                     
                             'HOME' : {'x' : self.window_w / 4 * 3 - w_button1/ 2,
                                       'y' : self.window_h / 3,
                                       'w' : w_button1,
                                       'h' : h_button1},
                                                 
                             'OPTIONS' : {'x' : self.window_w / 4 * 3 - w_button1/ 2,
                                          'y' : self.window_h / 3 + y_space_buttons,
                                          'w' : w_button1,
                                          'h' : h_button1},
                                                                                   
                             'CONTINUE' : {'x' : self.window_w / 4 * 3 - w_button1/ 2,
                                           'y' : self.window_h / 3 + y_space_buttons,
                                           'w' : w_button1,
                                           'h' : h_button1},                                                                        

                             'RANKING' : {'x' : self.window_w / 4 * 3 - w_button1/ 2,
                                         'y' : self.window_h / 3 + y_space_buttons * 2,
                                         'w' : w_button1,
                                         'h' : h_button1},
                                        
                             'RESTART GAME' : {'x' : self.window_w / 4 * 3 - w_button1/ 2,
                                               'y' : self.window_h / 3 + y_space_buttons * 2,
                                               'w' : w_button1,
                                               'h' : h_button1},

                             'BACK' : {'x' : self.window_w * 0.2 - w_button2/ 2,
                                       'y' : self.window_h * 0.1,
                                       'w' : w_button2,
                                       'h' : h_button1},                                            
                                                          
                             'EXIT' : {'x' : self.window_w / 4 * 3 - w_button1/ 2,
                                       'y' : self.window_h / 3 + y_space_buttons * 3,
                                       'w' : w_button1,
                                       'h' : h_button1},
                                                         
                             'speed' : {'x' : self.window_w / 6 - w_button3/ 2,
                                        'y' : self.window_h / 5 + y_space_buttons,
                                        'w' : w_button3,
                                        'h' : h_button2}, 
                             
                             'ncols' : {'x' : self.window_w / 6 - w_button3/ 2,
                                        'y' : self.window_h / 5 + y_space_buttons * 2,
                                        'w' : w_button3,
                                        'h' : h_button2},                     

                             'next shape' : {'x' : self.window_w / 6 - w_button3/ 2,
                                             'y' : self.window_h / 5 + y_space_buttons * 3,
                                             'w' : w_button3,
                                             'h' : h_button2},                     

                             'big shapes' : {'x' : self.window_w / 6 - w_button3/ 2,
                                             'y' : self.window_h / 5 + y_space_buttons * 4,
                                             'w' : w_button3,
                                             'h' : h_button2}
                            }     

    # / ----------------------------------------------------------------------- \
    
    def set_objects_positions(self):        

        # Another objetc to display in the game
        self.rects = {'game_boundaries' : pg.Rect(self.game_boundaries[0], 
                                                  self.game_boundaries[1], 
                                                  self.game_boundaries[2] - self.game_boundaries[0],
                                                  self.game_boundaries[3] - self.game_boundaries[1]),
                                                                
                      'next_shape' :pg.Rect(self.game_boundaries[2] + (self.window_w - self.game_boundaries[2]) * 0.2,
                                            self.game_boundaries[1] + self.window_h * 0.1,
                                            self.block_size * 6,
                                            self.block_size * 6)
                      }

        self.texts = {# X and Y center
                      'next_shape' : {'x' : self.rects['next_shape'].center[0],
                                      'y' : self.rects['next_shape'].top - self.window_h * 0.05},
                      
                      # X and Y center
                      'score' : {'x' : self.rects['next_shape'].center[0],
                                 'y' : self.rects['next_shape'].bottom + self.window_h * 0.07},

                      # X and Y center
                      'speed' : {'x' : self.rects['next_shape'].center[0],
                                 'y' : self.rects['next_shape'].bottom + self.window_h * 0.16},

                      # X and Y center                                      
                      'start' : {'x' : self.window_w / 2,
                                 'y' : self.window_h / 2}, 
                      
                      # X and Y center               
                      'write_record' : {'x' : self.rects['next_shape'].center[0],
                                        'y' : self.rects['next_shape'].bottom + self.window_h * 0.35},
                      
                      # Upper left coordinate                           
                      'records' : {'x' :self. window_w / 8,
                                   'y' : self.window_h * 0.4,
                                   'y_space' : self.window_h / 10.25},

                      'top five' : {'x' :self. window_w / 5,
                                    'y' : self.window_h * 0.3},
                                          
                      # X and Y center
                      'game_over': {'x' : self.window_w / 2, 
                                    'y' : self.window_h / 2} ,

                      # X and Y center
                      'instructions' : {'x' : self.window_w / 2,
                                        'y' : self.window_h - self.window_h*0.10}
                     }                                                                           

    # / ----------------------------------------------------------------------- \

    def load_image(self, filename, window_w=None, window_h=None):
        
        if window_w is None:
            window_w = self.window_w
        if window_h is None:
            window_h = self.window_h

        # Load and scale the image
        img = pg.image.load(filename)
        img = pg.transform.smoothscale(img, (window_w, window_h))
        return img

    # / ----------------------------------------------------------------------- \

    def load_sound(self, filename, volume=0.5):
        self.sound = pg.mixer.Sound(filename)
        self.sound.set_volume(volume)
        
    # / ----------------------------------------------------------------------- \

config = Configuration()

 # / -------------------------------------------------------------------------- \
 # / --------------------------------------------------- \
 # / -------------------------------- \
 # / ------------- \
 # / END
        





                  