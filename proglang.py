import nltk
import math
from math import log
from string import ascii_lowercase, punctuation, whitespace
import os
import re

 


def cleaning_text(filename):
    with open(filename, mode='r', encoding='utf_8', errors='ignore') as ifile:
        lines = ifile.readlines()

        is_python_comment = lambda line: line.strip().startswith('#')
        is_c_single_line_comment1 = lambda line: line.strip().startswith('//')
        is_c_single_line_comment2 = lambda line: \
            line.strip().startswith('/*') and line.endswith('*/')

        lines = [
            line
            for line in lines
            if not (
                    is_python_comment(line) or
                    is_c_single_line_comment1(line) or
                    is_c_single_line_comment2(line)
            )
        ]

        def remove_punctuation(line):
            return "".join([char for char in line if char in (ascii_lowercase + whitespace)])

        without_punc = [remove_punctuation(line) for line in lines]

        temp_string = ''

        for tweet in without_punc:
            temp_string += ''.join(re.findall('[\u0020\u0041-\u007a]', tweet, re.UNICODE))

        return temp_string

    # return ''.join(without_punc)


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
    # path = "C:/Users/maiaa/py"
    path = "C:\\Personal\\Projects\\python_projects\\parser-combinator\\14-8"
    dir_list = os.listdir((path))
    full_content = ''
    for csv_file in dir_list:
        if not csv_file.endswith('.txt.py'):
            continue
        print(csv_file)
        file_lines = cleaning_text(os.path.join(path, csv_file))
        print(file_lines)
        print(len(file_lines))
        full_content += file_lines
        # for  i in range(len(full_content)):
        #   start=10000
        #   end=len(full_content)

    chunk_size = 100

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
