#!/usr/bin/bash python3
#-*- coding: utf8 -*-

import os
import numpy as np
import time
from utils.plot import *
from utils.sort import Sort


###############################################
# kernel method
###############################################

def get_mean(data):
    """get the mean value of all data"""
    return np.sum(data, axis=0) / len(data)


def get_bijection(num):
    """get double shot list"""
    num_lst = np.arange(num).tolist()
    res = rcn_bijection(num_lst)
    return res


def rcn_bijection(num_lst):
    """recurrent bijection calculation"""
    res_lst_lst = []
    if len(num_lst) == 1:
        res_lst_lst.append(num_lst)
    else:
        for item in num_lst:
            res_lst = [it for it in num_lst if it != item]
            rcn_res = rcn_bijection(res_lst)
            [res_item.insert(0, item) for res_item in rcn_res]
            res_lst_lst.extend(rcn_res)
    return res_lst_lst


def get_reverse_seq_num(reverse_lst):
    """get the reverse order number"""
    num = len(reverse_lst)
    # map lst to minist range
    sort_handler = Sort()
    sort_lst = sort_handler.quick(reverse_lst.copy())
    sort_lst_dct = {item: i for i, item in enumerate(sort_lst)}
    insert_lst = [sort_lst_dct[item] for item in reverse_lst]
    # count
    new_lst = [0] * num
    reverse_num = 0
    for item in insert_lst:
        reverse_num += new_lst[item]
        for i in range(item):
            new_lst[i] += 1
    return reverse_num


def get_determinant(square_mat):
    """get the determinant of square matrix `square_mat`"""
    if isinstance(square_mat, list):
        square_mat = np.array(square_mat)
    shape = square_mat.shape
    assert (len(shape) == 2 and shape[0] == shape[1]), "the `square_mat` is not square"
    double_shot_list = get_bijection(shape[0])
    sum_value =0
    for one_lst in double_shot_list:
        operator = 1 if get_reverse_seq_num(one_lst) % 2 == 0 else -1
        for i, item in enumerate(one_lst):
            operator *= square_mat[i][item]
        sum_value += operator
    return sum_value


def get_S(data, mean):
    """get the covariance matrix `S`"""
    S = np.dot((data - mean), np.transpose(data - mean)) / len(data)
    return S


def cal_eigenvalue(cov):
    """calculate eigenvalue of `cov` matrix"""
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    eigen_dict = {value: idx for idx, value in enumerate(eigenvalues)}
    sort_handler = Sort()
    sort_eigenvalues = sort_handler.quick(eigenvalues)
    sort_eigenvalues = sort_eigenvalues[::-1]
    sort_eigenvectors = [eigenvectors[eigen_dict[sort_value]] for sort_value in sort_eigenvalues]
    return sort_eigenvalues, sort_eigenvectors


def proj_at_dim_err(eigenvectors, S, dim=1):
    """project to dimension `dim` which is default `1`"""
    W = np.array(eigenvectors[:dim]).T
    return W, np.mean(W.T.dot(S).dot(W))


def search_best_dim(data):
    """search the best dimension for projection, maybe higer or lower"""
    mean = get_mean(data)
    S = get_S(data, mean)
    _, eigenvectors = cal_eigenvalue(S)
    max_dim = len(eigenvectors)
    best_dim = 1
    best_W = None
    min_err = np.Infinity
    for dim in range(max_dim):
        W, err = proj_at_dim_err(eigenvectors, S, dim+1)
        if err < min_err:
            min_err = err
            best_dim = dim + 1
            best_W = W
    return best_dim, best_W

if __name__ == '__main__':
    
    """gen data"""
    data = gen_normal_data()

    """run"""

    """test"""
    # print(get_double_shot(3))
    # org_lst = [3, 5, 1, 4, 2]
    # get_reverse_seq_num(org_lst)
    # start = time.time()
    # print(get_determinant([[1, 2, 3], [3, 4, 5], [5, 6, 7]]))
    # print('time cost', time.time() - start)
    # print(os.path.dirname(np.__file__))
    test_data = np.array([[1, 2, 3], [3, 4, 5], [5, 6, 7], [7, 8, 9]])
    best_dim, best_W = search_best_dim(test_data)
    print('best projection dimension:', best_dim)
    print('best parameters:', best_W.shape, best_W)

