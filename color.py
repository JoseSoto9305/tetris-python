#!/usr/bin/env python
# -*- coding: utf-8 -*-

__project__ = 'TETRIS'
__file__ = './color.py'
__license__ = 'GPL'
__version__ = '1.0'
__date__ = 'May, 2020'
__maintainer__ = 'Jose Trinidad Soto Gonzalez'

# / -------------------------------------------------------------------------- \

import pygame as pg

# / -------------------------------------------------------------------------- \

colors = {'gray' :   pg.Color( 31,  31,  31),
          'white' :  pg.Color(235, 235, 235),
          'pink' :   pg.Color(253, 167, 255),
          'purple' : pg.Color(222, 167, 255),
          'cherry' : pg.Color(255, 167, 189),
          'berry' :  pg.Color(139,  29,  86),
          'blue' :   pg.Color(173, 167, 255),
          'artic' :  pg.Color(167, 255, 222),
          'yellow' : pg.Color(255, 236, 167),
          'orange' : pg.Color(255, 170, 126),
          'green' :  pg.Color(127, 216, 132)}


class ColorEffect:
    
    # / ----------------------------------------------------------------------- \
    
    def __init__(self, color=colors['cherry'], interval=60, length=10):

        self.rgb_color = color
        self.hsl_color = self.rgb_color.hsla

        self.interval = interval
        self.length = length

        hue = int(self.hsl_color[0])
        self.hue_values = self.set_hue_values(hue)
        self.index = self.hue_values.index(hue)
        self.add = 1

    # / ----------------------------------------------------------------------- \
    
    def set_hue_values(self, hue_value):
            
        hue_min = int(hue_value - self.interval)
        hue_max = int(hue_value + self.interval)
            
        h = list(range(hue_min, hue_max+1))
        for i in range(len(h)):
            h[i] = self.hue_limits(h[i])
            
        hue_values = []
        [hue_values.extend([i]*self.length) for i in h]
        return hue_values
        
    # / ----------------------------------------------------------------------- \
    
    def hue_limits(self, hue):
        if hue > 360:
            hue -= 360
        elif hue < 0:
            hue += 360
        return hue
        
    # / ----------------------------------------------------------------------- \
        
    def clip_sat_light(self, value):
        if value > 100:
            value = 100
        elif value < 0:
            value = 0
        return value
        
    # / ----------------------------------------------------------------------- \

    def change_color(self):
        
       self.index += self.add  
       
       if self.index == len(self.hue_values):
           self.add = -1
           self.index += self.add       
       
       elif self.index < 0:
           self.add = 1
           self.index += self.add
       
       h = self.hue_values[self.index]
       s = self.hsl_color[1]
       l = self.hsl_color[2]
       return self.hsl2rgb(h, s, l)
       
    # / ----------------------------------------------------------------------- \

    def hsl2rgb(self, h, s, l):
        
        # Fron wikipedia:
        # https://en.wikipedia.org/wiki/HSL_and_HSV#Color_conversion_formulae

        if h == 360:
            h = 0

        if s > 1:
            s /= 100

        if l > 1:
            l /= 100

        _h = h / 60
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs(_h % 2 - 1))
        m = l - (c / 2)
        
        mt = [[c, x, 0],
              [x, c, 0],
              [0, c, x],
              [0, x, c],
              [x, 0, c],
              [c, 0, x]]
        
        r1, g1, b1 = mt[int(_h)]   
        r, g, b = r1 + m, g1 + m, b1 + m
        
        return pg.Color(round(r * 255), round(g * 255), round(b * 255))
        
    # / ----------------------------------------------------------------------- \

    def modify_color(self, color, h=0, s=0, l=0):
        
        # If color is in rgb, then convert to hsl
        if color[1] > 100 or color[2] > 100:
            color = color.hsla

        # Modify color
        h += color[0]
        s += color[1]
        l += color[2]
        
        # Clip values
        h = self.hue_limits(h)
        s = self.clip_sat_light(s)
        l = self.clip_sat_light(l)
        
        rgb_color = self.hsl2rgb(h, s, l)
        return rgb_color
       
    # / ----------------------------------------------------------------------- \
      
 # / -------------------------------------------------------------------------- \
 # / --------------------------------------------------- \
 # / -------------------------------- \
 # / ------------- \
 # / END