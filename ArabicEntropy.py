import nltk
import math
from math import log
from string import punctuation
import os
import re


def cleaning_text(filename):
    with open(filename, mode='r', encoding='utf_8', errors='ignore') as ifile:
        lines = ifile.readlines()

        temp_string = ''

        for tweet in lines:
            temp_string += ''.join(re.findall('[\u0020\u0627-\u064A]', tweet, re.UNICODE))

        return temp_string


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


def entropy_computation(path):
    # print(file_path)
    cleaned_text = ''.join(cleaning_text(path))
    frequencies = frequency(cleaned_text)
    ent = entropy(frequencies)
    return ent


def main():
    path = "C:/Users/maiaa/arabic tweets"
    # path = "C:\\Personal\\Projects\\python_projects\\parser-combinator\\9-8-21"
    dir_list = os.listdir((path))
    full_content = ''
    for csv_file in dir_list:
        # if csv_file.endswith('.py'):
        #     continue
        print(csv_file)
        file_lines = cleaning_text(os.path.join(path, csv_file))
        # print(file_lines)
        print(len(file_lines))
        full_content += file_lines
        # for  i in range(len(full_content)):
        #   start=10000
        #   end=len(full_content)

    chunk_size = 10000

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

    with open('entropy_output.csv', 'w') as f:
        f.writelines(output_lines)

     


if __name__ == '__main__':
    main()
