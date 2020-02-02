#!/usr/bin/bash python3
#-*- coding: utf8 -*-

"""
algorithm introduction

Description: Candidate Elimination Algorithm
             1. We use Maximum General Member (G) and Maximum Special Member (S) to represent Version Space

"""

import os
import random

EMPTY = 'None'
ANY = '?'


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


def get_most_general_hypothesis(num):
    return [ANY] * num


def is_more_special(G_Set, s_hps):
    for hps in G_Set:
        for hps_attr, s_hps_attr in zip(hps, s_hps):
            if hps_attr == ANY and s_hps_attr != ANY:
                return True
    return False


def remove_diff_hypothesis_by_pos(G_Set, S_Set, example):
    new_G_Set = []
    new_S_Set = []
    
    # remove unsuit general boundary
    for hps in G_Set:
        general = True
        for emp_attr, hps_attr in zip(example, hps):
            if emp_attr != hps_attr and hps_attr != ANY:
                general = False
                break
        if general:
            new_G_Set.append(hps)
    
    # remove unsuit special boundary
    for hps in S_Set:
        special = True
        for emp_attr, hps_attr in zip(example, hps):
            if hps_attr == EMPTY or emp_attr != hps_attr and hps_attr != ANY:
                special = False
                new_hps = generalize_hypothesis(hps, example)  # QUESTION: Are there many new hypothesis?
                # the generalized hypothesis should be more special than hypothesis in G_Set
                if is_more_special(new_G_Set, new_hps):
                    new_S_Set.append(new_hps)
                break
        if special:
            new_S_Set.append(hps)
    
    # In this process of generalizing special boundary, 
    # we needn't remove the more general hypothesis in new_S_Set
    # because we didn't add all the maximum general hypothesis to new_S_Set
    
    return new_G_Set, new_S_Set


def check_in_special_set_and_conflict(g_hps, S_Set):
    attr_num = len(g_hps)
    for hps in S_Set:
        # should more general
        same_attrs = [g_hps_attr for g_hps_attr, hps_attr in zip(g_hps, hps) if g_hps_attr == hps_attr]
        if len(same_attrs) == attr_num: 
            return True
        # the follow noted script is same as the previous
        # diff_attrs = [g_hps_attr for g_hps_attr, hps_attr in zip(g_hps, hps) if g_hps_attr != hps_attr]
        # if len(diff_attrs) == 0:
        #     return True

        # should not be conflict
        conflict_attrs = [g_hps_attr for g_hps_attr, hps_attr in zip(g_hps, hps) if g_hps_attr != hps_attr and g_hps_attr != ANY]
        if len(conflict_attrs) > 0:
            return True
    return False


def remove_more_special_hypothesis(G_Set):
    new_G_Set = []

    num_G_set = len(G_Set)
    remove_idxs = []
    for i in range(num_G_set - 1):
        prev_hps = G_Set[i]
        for j in range(i+1, num_G_set):
            next_hps = G_Set[j]
            
            is_same = [0 if prev_hps_attr == next_hps_attr or any([prev_hps_attr, next_hps_attr]) == ANY else 1 
                       for prev_hps_attr, next_hps_attr in zip(prev_hps, next_hps)]
            if sum(is_same) == 0:
                prev_any_num = len([attr for attr in prev_hps if attr == ANY])
                next_any_num = len([attr for attr in next_hps if attr == ANY])
                rmv_idx = i if prev_any_num < next_any_num else j
                remove_idxs.append(rmv_idx)
    
    for i in range(num_G_set):
        if i not in remove_idxs:
            new_G_Set.append(G_Set[i])
    return new_G_Set


def remove_diff_hypothesis_by_neg(G_Set, S_Set, example, heads, attr2value):
    new_G_Set = []
    new_S_Set = []

    # remove unsuit special boundary
    for hps in S_Set:
        special = False
        for emp_attr, hps_attr in zip(example, hps):
            if hps_attr == EMPTY:
                special = True
                break
            elif hps_attr != ANY and hps_attr != emp_attr:  # not equal to negative example means True Rule
                special = True
                break
        if special:
            new_S_Set.append(hps)
    
    # remove unsuit special boundary
    for hps in G_Set:
        general = False
        for emp_attr, hps_attr in zip(example, hps):
            # not equal to negative example means True Rule
            if hps_attr != ANY and hps_attr != emp_attr:
                general = True
                break
        if general:
            new_G_Set.append(hps)
        else:  # specialize general boundary
            for idx, (emp_attr, hps_attr) in enumerate(zip(example, hps)):
                if hps_attr == ANY or hps_attr == emp_attr:
                    all_values = attr2value[heads[idx]]
                    for val in all_values:
                        if val != emp_attr:
                            new_hps = hps.copy()
                            new_hps[idx] = val
                            if not check_in_special_set_and_conflict(new_hps, new_S_Set):
                                new_G_Set.append(new_hps)
    
    # remove the more special hypothesis in new_G_Set
    new_G_Set = remove_more_special_hypothesis(new_G_Set)
                    
    return new_G_Set, new_S_Set


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


def candidate_elimination(data, class_name='Class'):
    examples = data['data']
    heads = data['heads']
    attr2value = data['attr2value']
    
    attr_num = len(examples[0])
    no_class_attr_num = attr_num - 1

    g_hps = get_most_general_hypothesis(no_class_attr_num)
    s_hps = get_most_special_hypothesis(no_class_attr_num)
    G_Set = [g_hps]
    S_Set = [s_hps]

    pos_examples, neg_examples = div_pos_neg_data(data, class_name)
    tags = [1] * len(pos_examples) + [0] * len(neg_examples)
    all_examples = pos_examples + neg_examples


    print('--- step: {} ---'.format(0))
    print_set(G_Set, S_Set)

    step = 1
    for emp, tag in zip(all_examples, tags):
        if tag:  # positive
            G_Set, S_Set = remove_diff_hypothesis_by_pos(G_Set, S_Set, emp)
        else:  # negative
            G_Set, S_Set = remove_diff_hypothesis_by_neg(G_Set, S_Set, emp, heads, attr2value)
        print('--- step: {} ---'.format(step))
        print_set(G_Set, S_Set)
        step += 1

    return G_Set, S_Set


def print_rule(heads, rule):
    rule_str = '<' + ', '.join([head + '=' + (attr if attr != 'None' else 'Ø') for head, attr in zip(heads, rule)]) + '>'
    return rule_str


def print_set(G_Set, S_Set):
    print('\t--- special boundary ---')
    for idx, hps in enumerate(S_Set):
        print('\tspecial {}: '.format(idx), print_rule(data['heads'], hps))
    print('\t--- general boundary ---')
    for idx, hps in enumerate(G_Set):
        print('\tgeneral {}: '.format(idx), print_rule(data['heads'], hps))

if __name__ == '__main__':
    DATA_DIR = './data'
    DATA_FILE = 'enjoy_sport'
    filename = os.path.join(DATA_DIR, DATA_FILE)
    data = read_data(filename)
    G_Set, S_Set = candidate_elimination(data, class_name='EnjoySport')
    print('--- final ---')
    print_set(G_Set, S_Set)

