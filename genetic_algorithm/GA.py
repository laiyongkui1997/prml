#!/usr/bin/bash python3
#-*- coding: utf8 -*-

"""
algorithm introduction

Description: GA, a kind of genetic Algorithm

"""

import os
import math
import random
import numpy as np
from collections import namedtuple

MIN_NUM_RULES = 1
MAX_NUM_RULES = 3

Hypothesis = namedtuple('Hypothesis', ['rules', 'digit_hps', 'rule_num', 'fitness'])


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


def transfer_reps_to_digit(hps, heads, attr2value, class2digits_dict, class_name='Class'):
    if isinstance(hps, list):
        digit = []
        for one_hps in hps:
            digit.append(transfer_reps_to_digit(one_hps, heads, attr2value, class2digits_dict, class_name=class_name))
        return digit
    digit = ''
    for head, hps_attr in zip(heads, hps):
        if head != class_name:
            attr_vals = attr2value[head]
            sub_digit = ['0'] * len(attr_vals)
            sub_digit[attr_vals[hps_attr].index(hps_attr)] = '1'
            digit += ''.join(sub_digit)
    digit += class2digits_dict[attr2value[class_name]]
    return digit


def cal_fitness(examples, hps, heads, attr2value):
    rules = hps.rules
    right_num = 0
    all_num = len(examples)
    for one_example in examples:
        for rule in rules:
            is_right = 1
            for head, exp_attr in zip(heads, one_example):
                if exp_attr not in rule[head]:
                    is_right = 0
                    break
            if is_right:
                right_num += 1
                break
    hps = hps._replace(fitness=(right_num / all_num)**2)
    return hps


def cal_probs(all_fitness):
    hps_probs = []
    num = len(all_fitness)
    all_sum = sum(all_fitness)
    if all_sum == 0:
        return [1 / num] * num
    if 0 in all_fitness:
        add_num = all_sum / num
        all_fitness = [(item + add_num) / 2 for item in all_fitness]
    for hps_fitness in all_fitness:
        hps_probs.append(hps_fitness / all_sum)
    return hps_probs


def number_to_bit_str(number, bit_num):
    bit_str = ['0'] * bit_num
    res_val = number
    
    while res_val > 1:
        pos = math.floor(math.log(res_val, 2))
        res_val -= 2**pos
        bit_str[pos] = '1'
    
    if res_val:
        bit_str[0] = '1' 
    bit_str = ''.join(bit_str[::-1])
    return bit_str


def generate_init_hypothesis(heads, attr2value, class2digits_dict, p, class_name='Class'):
    count = 0
    init_hps = []
    class_num = len(attr2value[class_name])
    while count < p:
        hps = ''
        rule_num = random.randint(0, MAX_NUM_RULES - MIN_NUM_RULES) + MIN_NUM_RULES
        rules = []
        for _ in range(rule_num):   # two rules conjunction
            one_rule = {}
            for head in heads:
                if head != class_name:  # class should be the last
                    cur_vals = list(attr2value[head])
                    val_num = len(cur_vals)
                    one_rule[head] = []
                    while val_num:
                        if random.random() > 0.5:
                            hps += '1'
                            one_rule[head].append(cur_vals[val_num - 1])
                        else:
                            hps += '0'
                        val_num -= 1
            # class should be the last
            class_idx = random.randint(0, class_num-1)
            hps += class2digits_dict[class_idx]
            one_rule[class_name] = [list(attr2value[class_name])[class_idx]]
            rules.append(one_rule)
        if hps not in init_hps:
            init_hps.append(Hypothesis(rules, hps, rule_num, None))
            count += 1
    return init_hps


def update_hypothesis(init_hps, heads, attr2value, class2digits_dict, p, r, m, class_name='Class'):
    new_hps = []
    select_num = math.floor((1 - r) * p)
    print('-- debug -- select_num:', select_num)
    all_fitness = [hps.fitness for hps in init_hps]
    print('-- debug -- all_fitness:', all_fitness)
    all_probs = cal_probs(all_fitness)
    print('-- debug -- all_probs:', all_probs)
    # raise ValueError('error')
    # select
    select_idxs = list(range(p))
    print('-- debug -- select_idxs:', select_idxs)
    while select_num:
        idx = np.random.choice(select_idxs, p=all_probs)
        select_hps = init_hps[idx]
        if select_hps not in new_hps:
            new_hps.append(select_hps)
        select_num -= 1
    # print('-- debug -- new_hps:', new_hps)
    # crossover
    pair_num = math.ceil(r * p / 2)
    print('-- debug -- crossover pair_num:', pair_num)

    return new_hps


def crossover_operator():
    pass


def mutation_operator():
    pass


def GA(data, p, r, m, class_name='Class'):
    examples = data['data']
    heads = data['heads']
    attr2value = data['attr2value']

    # generate the binary reps of class value
    class_num = len(attr2value[class_name])
    all_digit_num = math.ceil(math.log(class_num))
    # print('-- debug -- all_digit_num:', all_digit_num)
    class2digits_dict = {digit_num: number_to_bit_str(digit_num, all_digit_num) for digit_num in range(all_digit_num+1)}
    # print('-- debug -- class2digits_dict:', class2digits_dict)

    # generate the initial hypothesis
    init_hps = generate_init_hypothesis(heads, attr2value, class2digits_dict, p=p, class_name=class_name)
    
    # calculate the fitness
    init_hps = [cal_fitness(examples, digit_hps, heads, attr2value) for digit_hps in init_hps]
    # print('-- debug -- init_hps:', init_hps)

    # iteration
    max_fitness = max([hps.fitness for hps in init_hps])
    print('-- debug -- max_fitness:', max_fitness)
    fitness_threshold = 0.9
    while max_fitness < fitness_threshold:
        init_hps = update_hypothesis(init_hps, heads, attr2value, class2digits_dict, p, r, m, class_name=class_name)
    pass


if __name__ == '__main__':
    DATA_DIR = './data'
    DATA_FILE = 'play_tennis'
    filename = os.path.join(DATA_DIR, DATA_FILE)
    data = read_data(filename, no_use_heads=['Day'])
    # artifical parameter
    p = 10  # 
    r = 0.06  # selection rate
    m = 0.001  # mutation rate

    # test
    # print(number_to_bit_str(15, 4))
    GA(data, p, r, m, class_name='PlayTennis')
    



