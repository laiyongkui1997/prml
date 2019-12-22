#!/usr/bin/bash python3
#-*- coding: utf8 -*-

"""
algorithm introduction

Description: This is one of algorithms belong to Example Learning

Input: Example set
Output: Rule
Principles: 1. Select one attribute value which covers the most positive examples from all attribute values.
            2. Select the attribute value which covers less negative examples 
               when some attribute values cover the same positive examples
"""

import os
import math
import random
# import numpy as np
from collections import Counter

DATA_DIR = './data'
DATA_FILE = 'weather'

def read_data(filename):
    data = []
    attr2value = {}
    value2attr = {}
    with open(filename, 'r') as fr:
        line = fr.readline().strip()
        heads = line.split('\t')
        while True:
            line = fr.readline()
            if not line:
                break
            line = line.strip()
            attrs = line.split('\t')
            data.append(attrs)
            for head, attr in zip(heads, attrs):
                if head not in attr2value:
                    attr2value[head] = set([attr])
                else:
                    attr2value[head].add(attr)
                if attr not in value2attr:
                    value2attr[attr] = head
    return {'heads': heads, 'data': data, 'attr2value': attr2value, 'value2attr': value2attr}


def flatten_arr(data):
    if not isinstance(data[0], list):
        return data
    flt_data = []
    for item in data:
        
        flt_data.extend(item)
    return flt_data


def div_pos_neg_data(data):
    pos_data, neg_data = [], []
    for attrs in data['data']:
        if attrs[-1] == 'P':
            del attrs[-1]
            pos_data.append(attrs)
        else:
            del attrs[-1]
            neg_data.append(attrs)
    return pos_data, neg_data


def search_best_attr(rmv_attrs, PE, NE):
    flt_PE = flatten_arr(PE)
    flt_PE = [item for item in flt_PE if item not in rmv_attrs]
    # find the attrs which can cover most position examples
    flt_PE_count = Counter(flt_PE)
    best_attrs = []
    max_num = 0
    for attr, num in flt_PE_count.items():
        if num >= max_num:
            max_num = num
            best_attrs.append(attr)
    
    if len(best_attrs) == 1:
        return best_attrs[0]
    else:
        # find the attrs which can cover least negative examples
        flt_NE = flatten_arr(NE)
        flt_NE = [item for item in flt_NE if item not in rmv_attrs]
        select_attrs = [attr for attr in best_attrs if attr not in flt_NE]
        if not select_attrs:
            flt_NE_count = Counter(flt_NE)
            min_num = math.inf
            for attr, num in list(flt_NE_count.items())[::-1]:
                if attr in best_attrs and num <= min_num:
                    min_num = num
                    select_attrs.append(attr)
        
        if len(select_attrs) == 1:
            return select_attrs[0]
        else:
            # if there are more than one Suitable Attrs, random select one
            random.shuffle(select_attrs)
            return select_attrs[0]


def cover_examples(rule, heads, PE, NE):
    s_PE, s_NE = PE.copy(), NE.copy()
    for head, attr in rule.items():
        idx = heads.index(head)
        s_PE = [item for item in s_PE if item[idx]==attr]
        s_NE = [item for item in s_NE if item[idx]==attr]
    return s_PE, s_NE


def remove_example(org_data, rmv_data):
    result_data = []
    for org_item in org_data:
        if org_item not in rmv_data:
            result_data.append(org_item)
    return result_data


def GS(data):
    heads = data['heads']
    value2attr = data['value2attr']
    attr2value = data['attr2value']
    F = []
    pos_data, neg_data = div_pos_neg_data(data)
    PE, NE = None, None
    PE, NE = pos_data, neg_data
    while PE:
        CPX = {}
        while NE:
            rmv_attrs = [attr2value[key] for key in CPX.keys()]
            flt_rmv_attrs = flatten_arr(rmv_attrs) if rmv_attrs else []
            attr = search_best_attr(flt_rmv_attrs, PE, NE)
            head = value2attr[attr]
            CPX[head] = attr
            PE, NE = cover_examples(CPX, heads, PE, NE)
        pos_data = remove_example(pos_data, PE)
        PE = pos_data
        NE = neg_data
        F.append(CPX)
    return F


def print_rule(rule):
    rule_str = ''
    for count, one_rule in enumerate(rule):
        if count:
            rule_str += ' ∨ '
        rule_str += '['
        for idx, (attr, value) in enumerate(one_rule.items()):
            if idx:
                rule_str += ' ∧ '
            rule_str += attr + '=' + value
        rule_str += ']'
    return rule_str


if __name__ == '__main__':
    filename = os.path.join(DATA_DIR, DATA_FILE)
    data = read_data(filename)
    print('attr2value: ', data['attr2value'])
    print('value2attr: ', data['value2attr'])
    rule = GS(data)
    print('result rule: ', print_rule(rule))

