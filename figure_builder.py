#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:46:15 2023

@author: valentin
"""

from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

def plot_3D(X,Y,Z):
    # Load and format data
    dem = cbook.get_sample_data('jacksboro_fault_dem.npz', np_load=True)
    z = dem['elevation']
    nrows, ncols = z.shape
    x = np.linspace(dem['xmin'], dem['xmax'], ncols)
    y = np.linspace(dem['ymin'], dem['ymax'], nrows)
    x, y = np.meshgrid(x, y)
    
    region = np.s_[5:50, 5:50]
    x, y, z = np.array(X), np.array(Y), np.array(Z)
    
    # Set up plot
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    
    ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    rgb = ls.shade(z, cmap=cm.coolwarm, vert_exag=0.1, blend_mode='soft')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
                           linewidth=0, antialiased=False, shade=False)
    
    ax.set_zlabel("Gain")
    ax.set_ylabel("Projet par employé")
    ax.set_xlabel("Durée plus long projet")
    
    ax.yaxis.set_major_locator(MaxNLocator(len(Y[0]))) 
    ax.xaxis.set_major_locator(MaxNLocator(len(X))) 
    
    plt.savefig('surface_result.png')
    plt.show()