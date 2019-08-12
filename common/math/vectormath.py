#!/usr/bin/env python

# File with helper functions for vector math
# Author: Sandeep Baskar

# Import required modules
import random

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

def scalar_multiply(scalar, vector):
    result = []
    for i in range(0, len(vector)):
        result.append(vector[i] * scalar)
    return result

def rand(length):
    list = []
    for i in range(0, length):
        list.append(random.random())
    return list

def zeros(length):
    list = []
    for i in range(0,length):
        list.append(0)
    return list
