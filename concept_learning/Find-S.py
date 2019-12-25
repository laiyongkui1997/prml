#!/usr/bin/bash python3
#-*- coding: utf8 -*-

"""
algorithm introduction

Description: 

Note: simply ignore every negative example
"""

import os

EMPTY = False
ANY = True


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


def get_most_special_hypothesis(num):
    return [EMPTY] * num


def generalize_hypothesis(hypothesis, example):
    new_hps = []
    for emp_attr, hps_attr in zip(example, hypothesis):
        if hps_attr == EMPTY:
            new_hps.append(emp_attr)
        elif hps_attr == ANY or hps_attr != emp_attr:
            new_hps.append(ANY)
        # elif hps_attr == emp_attr:
        #     new_hps.append(hps_attr)
        else:  # same as previous note script
            new_hps.append(hps_attr)
    return new_hps


def Find_S(data, class_name='Class'):
    examples = data['data']
    heads = data['heads']
    
    attr_num = len(examples[0])
    no_class_attr_num = attr_num - 1

    hps = get_most_special_hypothesis(no_class_attr_num)

    pos_examples, _ = div_pos_neg_data(data, class_name)

    u_idx = 0
    for emp in pos_examples:
        for emp_attr, hps_attr in zip(emp, hps):
            if hps_attr==EMPTY or emp_attr != hps_attr and hps_attr is not ANY:
                u_idx += 1
                hps = generalize_hypothesis(hps, emp)
                print(' -- update {} times-- '.format(u_idx))
                break
    
    res_hps = {head: '?' if hps_attr==ANY else hps_attr for head, hps_attr in zip(heads, hps)}

    return res_hps


def print_rule(rule):
    rule_str = '<' + ', '.join([head + '=' + attr for head, attr in rule.items()]) + '>'
    return rule_str


if __name__ == '__main__':
    DATA_DIR = './data'
    DATA_FILE = 'enjoy_sport'
    filename = os.path.join(DATA_DIR, DATA_FILE)
    data = read_data(filename)
    rule = Find_S(data, class_name='EnjoySport')
    print('result rule: ', print_rule(rule))
