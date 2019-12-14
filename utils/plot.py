#!/usr/bin/bash python3
#-*- coding: utf8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

###############################################
# toolkit method
###############################################

def gen_normal_data(mean=0, var=1, dim=2, num=400, seed=0):
    """生成正态分布的数据"""
    np.random.seed(seed)
    shape = [num, dim]
    data = np.sqrt(var) * np.random.randn(*shape) + mean
    return data


def get_probability(X, Y, mean, var):
    """用公式求得二元正态分布的概率密度"""
    p = 1.0 / (2 * np.pi * var) * np.exp(- ((X - mean)**2 + (Y - mean)**2) / var / 2)
    return p


def plot_2d_data(X1, Y1, X2, Y2):
    """绘制数据"""
    plt.scatter(X1, Y1, marker='o')
    plt.scatter(X2, Y2, marker='^')
    plt.show()


def create_figure():
    """创建画布"""
    fig = plt.figure()
    return fig


def plot_3d_data(fig, X, Y, Z, title='test', fig_size=111):
    """绘制3D数据"""
    ax = fig.add_subplot(fig_size, projection='3d')
    ax.plot_trisurf(X, Y, Z, cmap='rainbow')
    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return fig


def show_figure():
    """展示图形"""
    plt.show()


def single_plot(X, Y, Z, title='test'):
    """绘制单个图形"""
    fig = create_figure()
    plot_3d_data(fig, X, Y, Z, title)
    show_figure()