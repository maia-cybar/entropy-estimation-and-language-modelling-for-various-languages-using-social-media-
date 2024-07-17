
import nltk
import math
from math import log
from string import punctuation, ascii_lowercase, whitespace
import csv, math, numpy
import os
import re
import string
import sys


 


def cleaning_text(filename):
    with open(filename, mode='r',encoding='utf-8', errors='ignore') as ifile:
        lines = ifile.readlines()
    
    
     
    
    
    
    
    lines_splitt = [re.sub(r"'(\x0b\x0c)+'", '', tweet) for tweet in lines_split]
    

    def remove_punctuation(line):
        return "".join([char for char in line if char in (ascii_lowercase + whitespace)])

    without_punc = [remove_punctuation(line) for line in lines_splitt]
    return ''.join(without_punc)




def frequency(without_punc):
    myFD = dict(nltk.FreqDist(without_punc))
    total = len(without_punc)
    relfrq = {(x[0], x[1] / total) for x in myFD.items()}
    return relfrq


def entropy(p):
    p_freqs = []
    for x in p:
        p_freqs.append(x[1])
    res = 0.0
    for x in p_freqs:
        res += x * log(x, 2)
    return -res


def main():
    #path='C:/Users/maiaa/aajsi'
    #dir_list = os.listdir(path)
    dir_list=['C:/Users/maiaa/aajsi.txt']
    
    
    full_content = ''
    for csv_file in dir_list:
        print(csv_file)
        #print(len(csv_file))
        ##file_lines = cleaning_text(os.path.join(path,csv_file))
        #print(len(file_lines))
        #full_content += file_lines
        
    chunk_size = 5500000





    print(len(full_content))
    print(len(full_content) // chunk_size)

    output_lines = []

    for i in range(1, 1 + len(full_content) // chunk_size):
        print(f'---- 0 - {i * chunk_size} ----')
        current_chunk = full_content[0: i * chunk_size]
        frequencies = frequency(current_chunk)
        entropy_value = entropy(frequencies)
        print(frequencies)
        print(entropy_value)
        output_lines.append(f'0 - {i * chunk_size},{entropy_value}\n')

    with open('english_entropy344_output.csv', 'w') as f:
        f.writelines(output_lines) 


if __name__ == '__main__':
    main()

    