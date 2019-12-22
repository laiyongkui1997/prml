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
from collections import Counter


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


def div_pos_neg_data(data, class_name='Class'):
    pos_data, neg_data = [], []
    idx = data['heads'].index(class_name)
    true_attr = data['data'][0][idx]

    # print('true attr:', true_attr)

    for attrs in data['data']:
        if attrs[idx] == true_attr:
            del attrs[idx]
            pos_data.append(attrs)
        else:
            del attrs[idx]
            neg_data.append(attrs)
    return pos_data, neg_data


def search_best_attr(rmv_heads, heads, PE, NE):
    # get useful idxs
    useful_idxs = []
    for idx in range(len(heads)):
        if heads[idx] not in rmv_heads:
            useful_idxs.append(idx)
    # find the attrs which can cover most position examples
    flt_PE_count = Counter()
    for idx in useful_idxs:
        flt_PE_count += Counter(flatten_arr([heads[idx] + ':' + item[idx] for item in PE]))
    best_attrs = []
    max_num = 0
    for attr, num in flt_PE_count.items():
        if num > max_num:
            max_num = num
            best_attrs = [attr]
        elif num == max_num:
            best_attrs.append(attr)

    # print('best_attrs:', best_attrs)

    if len(best_attrs) == 1:
        return best_attrs[0]
    else:
        # find the attrs which can cover least negative examples
        flt_NE = [heads[idx] + ':' + item[idx] for idx in useful_idxs for item in NE]
        select_attrs = [attr for attr in best_attrs if attr not in flt_NE]
        if not select_attrs:
            flt_NE_count = Counter()
            for idx in useful_idxs:
                flt_NE_count += Counter(flatten_arr([heads[idx] + ':' + item[idx] for item in NE]))
            min_num = math.inf
            for attr, num in list(flt_NE_count.items())[::-1]:
                if attr in best_attrs:
                    if num < min_num:
                        min_num = num
                        select_attrs = [attr]
                    elif num == min_num:
                        select_attrs.append(attr)
        
        # print('select_attrs:', select_attrs)
        
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


def GS(data, class_name='Class'):
    heads = data['heads'].copy()
    heads.remove(class_name)
    F = []
    pos_data, neg_data = div_pos_neg_data(data, class_name)
    PE, NE = None, None
    PE, NE = pos_data, neg_data
    while PE:
        CPX = {}
        while NE:
            rmv_heads = [key.split(':')[0] for key in CPX.keys()]
            attr = search_best_attr(rmv_heads, heads, PE, NE)
            head, value = attr.split(':')
            CPX[head] = value
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
    DATA_DIR = './data'
    # DATA_FILE = 'weather'
    DATA_FILE = 'pneumonia'
    filename = os.path.join(DATA_DIR, DATA_FILE)
    data = read_data(filename)
    rule = GS(data)
    print('result rule: ', print_rule(rule))

