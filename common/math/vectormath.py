#!/usr/bin/env python

# File with helper functions for vector math
# Author: Sandeep Baskar

def square_vector(arg):
    answer = []
    for i in range(0,len(arg)):
        answer.append(arg[i] * arg[i])
    return answer

def element_multiply(vec1, vec2):
    if (len(vec1) is not len(vec2)):
        print('Vectors are not same length')
        return -1
    else:
        result = []
        for i in range(0,len(vec1)):
            result.append(vec1[i] * vec2[i])
        return result

def element_subtract(vec1, vec2):
    if (len(vec1) is not len(vec2)):
        print('Vectors are not same length')
        return -1
    else:
        result = []
        for i in range(0,len(vec1)):
            result.append(vec1[i] - vec2[i])
        return result

def element_add(vec1, vec2):
    if (len(vec1) is not len(vec2)):
        print('Vectors are not same length')
        return -1
    else:
        result = []
        for i in range(0,len(vec1)):
            result.append(vec1[i] + vec2[i])
        return result

def element_divide(vec1, vec2):
    if (len(vec1) is not len(vec2)):
        print('Vectors are not same length')
        return -1
    else:
        result = []
        for i in range(0,len(vec1)):
            result.append(vec1[i] / vec2[i])
        return result
