#!/usr/bin/bash python3
#-*- coding: utf8 -*-
# reference: https://www.cnblogs.com/onepixel/p/7674659.html

import math

class Sort(object):

    def __init__(self):
        pass

    def bubbling(self, org_lst):
        """
        bubbling sort algorithm --- O(n^2)
        
        1. make the current max value to the current last position step by step
        2. then we do NOT need compare the last `i` num
        """
        lst_len = len(org_lst)
        for i in range(lst_len-1):
            for j in range(lst_len-1-i):
                if org_lst[j] > org_lst[j+1]:
                    tmp = org_lst[j+1]
                    org_lst[j+1] = org_lst[j]
                    org_lst[j] = tmp
        return org_lst

    def selection(self, org_lst):
        """
        selection sort algorithm --- O(n^2)
        
        1. make the current min value to the current first position step by step
        2. then we do NOT need compare the first `i` num
        3. just swap the min value with the current first value in position
        """
        lst_len = len(org_lst)
        for i in range(lst_len-1):
            min_value_pos = i
            for j in range(i+1, lst_len):
                if org_lst[j] < org_lst[min_value_pos]:
                    min_value_pos = j
            tmp = org_lst[min_value_pos]
            org_lst[min_value_pos] = org_lst[i]
            org_lst[i] = tmp
        return org_lst

    def insertion(self, org_lst):
        """
        insertion sort algorithm --- O(n^2)
        
        1. traverse all item, each current item will compare with the item in front of it, 
           insert current item at suitable position
        """
        lst_len = len(org_lst)
        for i in range(lst_len):
            j = i
            cur_value = org_lst[i]
            while (j>0 and org_lst[j-1] > cur_value):
                org_lst[j] = org_lst[j-1]
                j -= 1
            org_lst[j] = cur_value
        return org_lst

    def shell(self, org_lst):
        """
        shell sort algorithm --- O(n^1.3)
        
        1. compare item in a hop list which is sort from large to small, the last hop is 1
        """
        lst_len = len(org_lst)
        gap = math.floor(lst_len / 2)
        while gap > 0:
            for i in range(gap, lst_len):
                j = i
                cur_value = org_lst[i]
                while (j - gap >= 0 and cur_value < org_lst[j-gap]):
                    org_lst[j] = org_lst[j-gap]
                    j -= gap
                org_lst[j] = cur_value
            gap = math.floor(gap / 2)
        return org_lst

    def merge(self, org_lst):
        """
        merge sort algorithm --- O(n*log(n))
        
        1. recursive method, split `org_lst` into two subset in each epoch, and then merge them
        """
        lst_len = len(org_lst)
        if lst_len == 1:
            return org_lst
        else:
            mid = math.ceil(lst_len / 2)
            left, right = self.merge(org_lst[:mid]), self.merge(org_lst[mid:])
            i, j = 0, 0
            new_lst = []
            while (i < len(left) and j < len(right)):
                if left[i] < right[j]:
                    new_lst.append(left[i])
                    i += 1
                else:
                    new_lst.append(right[j])
                    j += 1
            new_lst.extend(left[i:])
            new_lst.extend(right[j:])
            return new_lst

    def quick(self, org_lst):
        """
        quick sort algorithm --- O(n*log(n))
        
        1. choose one item as mid item, use this mid item split all items into two part, and recursive
        """
        lst_len = len(org_lst)
        if lst_len <= 1:
            return org_lst
        else:
            mid_value = org_lst[0]
            i = 1
            j = lst_len - 1
            while (i < j):
                if org_lst[i] >= mid_value and org_lst[j] < mid_value:
                    tmp = org_lst[j]
                    org_lst[j] = org_lst[i]
                    org_lst[i] = tmp
                    j -= 1
                    i += 1
                else:
                    if org_lst[i] >= mid_value:
                        j -= 1
                    elif org_lst[j] < mid_value:
                        i += 1
                    else:
                        i += 1
                        j -= 1
            if i > j:
                i -= 1
            if mid_value > org_lst[i]:
                org_lst[0] = org_lst[i]
                org_lst[i] = mid_value
            
            org_lst[:i] = self.quick(org_lst[:i])
            org_lst[i:] = self.quick(org_lst[i:])
            
            return org_lst

    def max_heap(self, org_lst):
        """
        max_heap sort algorithm --- O(n*log(n))
        
        1. build a max heap, and exchange the max value (at the top) with the current last value, 
        """
        lst_len = len(org_lst)
        for i in range(lst_len):
            j = math.ceil((lst_len - 1 - i) / 2)
            while j > 0:
                if org_lst[j * 2 - 1] > org_lst[j - 1]:
                    tmp = org_lst[j * 2 - 1]
                    org_lst[j * 2 - 1] = org_lst[j - 1]
                    org_lst[j - 1] = tmp
                if j * 2 < lst_len - i and org_lst[j * 2] > org_lst[j - 1]:
                    tmp = org_lst[j * 2]
                    org_lst[j * 2] = org_lst[j - 1]
                    org_lst[j - 1] = tmp
                j -= 1
            tmp = org_lst[0]
            org_lst[0] = org_lst[lst_len - 1 - i]
            org_lst[lst_len - 1 - i] = tmp
        return org_lst


if __name__ == '__main__':

    org_lst = [3, 5, 1, 4, 2]
    org_lst2 = [1, 7, 4, 10, 9, 3, 5, 8, 6, 2]
    sort = Sort()
    print('bubbling: ', sort.bubbling(org_lst2.copy()))
    print('selection: ', sort.selection(org_lst2.copy()))
    print('insertion: ', sort.insertion(org_lst2.copy()))
    print('shell: ', sort.shell(org_lst2.copy()))
    print('merge: ', sort.merge(org_lst2.copy()))
    print('quick: ', sort.quick(org_lst2.copy()))
    print('max_heap: ', sort.max_heap(org_lst2.copy()))

