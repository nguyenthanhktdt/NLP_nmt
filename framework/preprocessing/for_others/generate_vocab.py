# make vocab
from collections import Counter


def is_too_long(input_string):
    return len(input_string) > 30


def is_contain_number(input_string):
    if "<num" in input_string or "<unk" in input_string or "st" in input_string or "nd" in input_string or "th" in input_string:
        return False
    else:
        return any(char.isdigit() for char in input_string)



def is_ok_vocab(vocab):
    if is_too_long(vocab):
        return False
    if is_contain_number(vocab):
        return False
    return True


def gen_vocab(input_file, output_file, output_file_small, appear_number):
    print("gen_vocab:")
    print(output_file)
    c = Counter()
    i = 0
    with open(input_file, encoding='utf-8') as f1:
        for line in f1:
            i = i+1
            for word in line.split():
                c[word] += 1

    f2 = open(output_file, 'w', encoding='utf-8')
    f_small = open(output_file_small, 'w', encoding='utf-8')
    f2.write("<unk>\n")
    f2.write("<s>\n")
    f2.write("</s>\n")
    f2.write("1\n" + "2\n" + "3\n" + "4\n" + "5\n" + "6\n" + "7\n" + "8\n" + "9\n" + "10\n")
    f2.write("11\n" + "12\n" + "13\n" + "14\n" + "15\n" + "16\n" + "17\n" + "18\n" + "19\n" + "20\n")
    f2.write("21\n" + "22\n" + "23\n" + "24\n" + "25\n" + "26\n" + "27\n" + "28\n" + "29\n" + "30\n" + "31\n")
    keys = []

    for key in sorted(c.keys()):
        if not is_ok_vocab(key):
            continue
        if c[key] >= appear_number:
            f2.write(str(key) + "\n")
        else:
            f_small.write(str(key) + "\n")

    f2.close()
    f_small.close()
