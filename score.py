#!/usr/bin/env python
# -*- coding: utf-8 -*-

__project__ = 'TETRIS'
__file__ = './score.py'
__license__ = 'GPL'
__version__ = '1.0'
__date__ = 'May, 2020'
__maintainer__ = 'Jose Trinidad Soto Gonzalez'

# / -------------------------------------------------------------------------- \

import os
import pygame as pg
from copy import copy

from config import config

# / -------------------------------------------------------------------------- \

class Score:
    
    # / ----------------------------------------------------------------------- \

    def __init__(self):
        
        self.score = 0
        self.previous = 0
        self.threshold_score = self.levels_func()        
        
    # / ----------------------------------------------------------------------- \

    def restart(self, level=False):

        if level:
            self.score = copy(self.previous)
            self.previous = None            

        else:            
            self.score = 0
            self.previous = None
            self.threshold_score = self.levels_func()
            
    # / ----------------------------------------------------------------------- \

    def load_records(self, n=5):
        with open(os.path.join(os.getcwd(), 'records.txt'), 'r') as f:
            lines = self.sort_records(f.readlines()[1:])
        
        scores = []
        id_names = []
        if lines:
            for i in range(n):
                scores.append(int(lines[i].split()[1]))
                id_names.append(lines[i].split()[0])
        return id_names, scores
        
    # / ----------------------------------------------------------------------- \
        
    def save_record(self, id_name):
        with open(os.path.join(os.getcwd(), 'records.txt'), 'a') as f:
            f.write(f'{id_name} {self.score}\n')
            
    # / ----------------------------------------------------------------------- \

    def sort_records(self, lines):
        return sorted(lines, key=lambda x: int(x.split()[1]))[::-1]

    # / ----------------------------------------------------------------------- \
    
    def update_score(self, n_eresed):        
        self.score += n_eresed
        
    # / ----------------------------------------------------------------------- \

    def levels_func(self):
        self.threshold_score = config.speed * config.removed_rows  * config.ncols
        return self.threshold_score
        
    # / ----------------------------------------------------------------------- \

    def previous_score(self):
        self.previous = copy(self.score)
        return self.previous
        
    # / ----------------------------------------------------------------------- \

    def level_up(self):
        _level_up = False
        if self.score >= self.threshold_score:            
            config.speed += 1
            
            self.previous = self.previous_score()            
            ds = self.score - self.threshold_score
            
            self.threshold_score = self.levels_func()            
            self.threshold_score += ds
            
            _level_up = True
        
        return _level_up
       
    # / ----------------------------------------------------------------------- \
      
 # / -------------------------------------------------------------------------- \
 # / --------------------------------------------------- \
 # / -------------------------------- \
 # / ------------- \
 # / END