#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27.09.2025 10:29
@author: marcwelz
@project: mo25
"""
import pylab as pl
from matplotlib.patches import Rectangle

resolution_x: int = 6
resolution_y: int = 6

pl.figure(figsize=(resolution_x, resolution_y)) # Pixels x 100
ax = pl.gca()

ax.add_patch(Rectangle((0, 0), 1, 1, color='red'))

bar_width: float = 0.2

ax.add_patch(Rectangle((0.5 - bar_width / 2, 0.2), bar_width, 0.6, color='white'))
ax.add_patch(Rectangle((0.2, 0.5 - bar_width / 2), 0.6, bar_width, color='white'))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
pl.axis('off')

pl.tight_layout(pad=0)
pl.show()