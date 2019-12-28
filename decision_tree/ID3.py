#!/usr/bin/bash python3
#-*- coding: utf8 -*-

"""
algorithm introduction

Description: ID3, a Top-Down Greedy Search Algorithm

"""

import os
import random
import numpy as np


PURE_NEG = 'neg'
PURE_POS = 'pos'


def read_data(filename, no_use_heads=[]):
    data = []
    attr2value = {}
    with open(filename, 'r') as fr:
        line = fr.readline().strip()
        heads = line.split('\t')
        no_use_idxs = [heads.index(no_use_head) for no_use_head in no_use_heads]
        heads = [head for head in heads if head not in no_use_heads]
        while True:
            line = fr.readline()
            if not line:
                break
            line = line.strip()
            attrs = line.split('\t')
            attrs = [attr for a_idx, attr in enumerate(attrs) if a_idx not in no_use_idxs]
            data.append(attrs)
            for head, attr in zip(heads, attrs):
                if head not in attr2value:
                    attr2value[head] = set([attr])
                else:
                    attr2value[head].add(attr)
    return {'heads': heads, 'data': data, 'attr2value': attr2value}


def cal_entropy(data, class_idx, pos_class_val, check_pure=False):
    all_data_num = len(data)
    pos_data_num = len([item for item in data if item[class_idx] == pos_class_val])
    neg_data_num = all_data_num - pos_data_num
    
    is_pure = None
    if pos_data_num == 0:
        is_pure = PURE_NEG
    elif pos_data_num == all_data_num:
        is_pure = PURE_POS
    else:
        is_pure = 1 if pos_data_num >= neg_data_num else 0

    ce_org = 0
    if pos_data_num:
        ce_org += - pos_data_num / all_data_num * np.log(pos_data_num / all_data_num)
    if neg_data_num:
        ce_org += - neg_data_num / all_data_num * np.log(neg_data_num / all_data_num)
    
    if check_pure:
        return ce_org, is_pure
    else:
        return ce_org


def cal_max_gain(data, used_attrs, attr2value, heads, class_name='Class'):
    data_num = len(data)
    class_idx = heads.index(class_name)
    pos_class_val, neg_class_val = attr2value[class_name]  # maybe not match exactly, but don't care

    org_ce, is_pure =  cal_entropy(data, class_idx, pos_class_val, check_pure=True)

    if is_pure == PURE_POS:
        return {'label': pos_class_val}
    elif is_pure == PURE_POS:
        return {'label': neg_class_val}
    else:
        all_attrs = set(heads) - set(used_attrs)
        # all_attrs = [head for head in heads if head not in used_attrs]
        if len(all_attrs) == 0:
            return {'label': pos_class_val} if is_pure == 1 else {'label': neg_class_val}
        else:
            max_gain = 0
            best_attr = None
            best_data_lst = None

            for attr in all_attrs:
                attr_vals = attr2value[attr]
                attr_idx = heads.index(attr)

                split_data_lst = {val: [] for val in attr_vals}
                for item in data:
                    split_data_lst[item[attr_idx]].append(item)
                
                attr_ce = 0
                for val in attr_vals:
                    if len(split_data_lst[val]) != 0:
                        attr_ce += len(split_data_lst[val]) / data_num * cal_entropy(split_data_lst[val], class_idx, pos_class_val)

                attr_gain = org_ce - attr_ce
                if attr_gain > max_gain:
                    max_gain = attr_gain
                    best_attr = attr
                    best_data_lst = split_data_lst
            
            if best_attr == None:
                return {'label': pos_class_val} if is_pure == 1 else {'label': neg_class_val}
            else:
                decision_tree = {best_attr: {val: {} for val in attr2value[best_attr]}}
                used_attrs.append(best_attr)
                for val in attr2value[best_attr]:
                    if len(best_data_lst[val]) == 0:
                        decision_tree[best_attr][val] = {'label': pos_class_val} if is_pure == 1 else {'label': neg_class_val}
                    else:
                        decision_tree[best_attr][val] = cal_max_gain(best_data_lst[val], used_attrs.copy(), attr2value, heads, class_name)
    
    return decision_tree


def ID3(data, class_name='Class'):
    examples = data['data']
    heads = data['heads']
    attr2value = data['attr2value']

    used_attrs = [class_name]
    decision_tree = {'Root': None}
    decision_tree['Root'] = cal_max_gain(examples, used_attrs, attr2value, heads, class_name)

    return decision_tree


def print_rule(rule, tap_num=0):
    prefix_tap = '\t' * tap_num
    for attr in rule.keys():
        if isinstance(rule[attr], dict):
            print(prefix_tap + '-' + attr)
            print_rule(rule[attr], tap_num=tap_num+1)
        else:
            print(prefix_tap + '-' + attr + ': ' + rule[attr])


if __name__ == '__main__':
    DATA_DIR = './data'
    DATA_FILE = 'play_tennis'
    filename = os.path.join(DATA_DIR, DATA_FILE)
    data = read_data(filename, no_use_heads=['Day'])
    decision_tree = ID3(data, class_name='PlayTennis')
    print('decision tree: ', decision_tree)
    print_rule(decision_tree)

