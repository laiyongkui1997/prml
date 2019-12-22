"""
algorithm introduction

Description: This is one of algorithms belong to Example Learning

Input: Example set, Parameter #SOL, #CONS, the volume #M of Star, the standard of optimization
Output: Rule
Principles: 1. Select one example from position examples from which we split all attribute values.
            2. Retain #M numbers of attribute values which are best, store it at Candidate Set #PS.
            3. If the retained attribute values are Completed, move it to a Complete Set #CptSet.
            4. If the retained attribute values are Consistent, move it to a Consistent Set #CstSet.
            5. Specialize the retained attribute values (from one formula to two)
            6. If number(#CptSet) >= #SOL  or  number(#CstSet) >= #CONS, retain #M numbers of formula.
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


def cover_examples(rule, heads, PE, NE, is_count=False):
    # print('rule:', rule)
    s_PE, s_NE = PE.copy(), NE.copy()
    for head, attr in rule.items():
        idx = heads.index(head)
        s_PE = [item for item in s_PE if item[idx]==attr]
        s_NE = [item for item in s_NE if item[idx]==attr]
    if is_count:
        return len(s_PE), len(s_NE)
    else:
        return s_PE, s_NE


def remove_example(org_data, rmv_data):
    result_data = []
    for org_item in org_data:
        if org_item not in rmv_data:
            result_data.append(org_item)
    return result_data


def sort_PS(PS):
    PS.sort(key=lambda x: x[1][1])  # Small to Big
    sorted_PS = []
    PS_len = len(PS)
    for idx, item in enumerate(PS):
        tmp_idx = idx + 1
        cur_pos_num = item[1][0]
        while tmp_idx < PS_len and PS[tmp_idx][1][0] == cur_pos_num:
            tmp_idx += 1
        if tmp_idx > idx + 1:
            tmp_PS = PS[idx:tmp_idx]
            tmp_PS.sort(key=lambda x: -x[1][0])  # Big to Small
            sorted_PS.extend(tmp_PS)
        else:
            sorted_PS.append(item)
    return sorted_PS


def specialize_formula(PS, retained_formula):
    expand_formula = []
    for idx, one_formula in enumerate(retained_formula):
        tmp_formua = retained_formula[idx:]
        tmp_PS = [{**one_formula[0], **item[0]} for item in PS if item not in tmp_formua]
        expand_formula.extend(tmp_PS)
    return expand_formula


def AQ(data, Sol=2, Cons=2, M=2, class_name='Class'):
    heads = data['heads'].copy()
    heads.remove(class_name)
    pos_data, neg_data = div_pos_neg_data(data, class_name)
    pos_num = len(pos_data)
    PE, NE = None, None
    PE, NE = pos_data, neg_data
    CptSet = []  # complete rule set
    while PE:
        CstSet = []  # consistent rule set
        # select a random example
        random.shuffle(PE)
        example = PE[0]
        # print('--- example ---:', example)
        retained_formula = []
        PS = []
        while len(CstSet) < Cons:
            expand_rule = specialize_formula(PS, retained_formula) if PS else [{head: rule} for head, rule in zip(heads, example)]
            PS = [(one_rule, cover_examples(one_rule, heads, PE, NE, is_count=True)) for one_rule in expand_rule]
            # print('++ PS ++:', PS)
            sorted_PS = sort_PS(PS)
            selected_formula = sorted_PS[0:M]
            retained_formula = []
            for one_formula in selected_formula:
                # if we have a complete rule, then we will finish search
                if one_formula[1][0] == pos_num:
                    PE = None
                    Cons = -1
                    CptSet = one_formula[0]
                    break
                # check the consistent rule
                if one_formula[1][1] == 0:
                    CstSet.append(one_formula)
                    PS.remove(one_formula)
                    continue
                retained_formula.append(one_formula)
        random.shuffle(CstSet)
        candidate_rule = CstSet[0][0]
        # print('*** candidate_rule ***:', candidate_rule)
        CptSet.append(candidate_rule)
        s_PE, _ = cover_examples(candidate_rule, heads, PE, NE)
        PE = remove_example(PE, s_PE)
    return CptSet


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
    rule = AQ(data)
    print('result rule: ', print_rule(rule))

