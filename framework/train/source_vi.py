import re
import unicodedata as ud
import os
from framework.utils.sophia_constants import SOPHIAConstants
from framework.utils.sophia_utility import SOPHIAUtility


def pre_process_vi(input_file, output_file):

    f = open(output_file, 'w', encoding='utf-8')
    with open(input_file, encoding='utf-8') as f1:
        for line in f1: 
            print("line in: ", line)
            s = line.lower()
            if len(s) != 0 or s != ' ':
                s = separate_symbol(s)
            # process number
            line = SOPHIAUtility.add_dot_punctual_vi(s)
            line = ud.normalize(SOPHIAConstants.SOPHIA_CHAR_NFKC, line)  #convert to unicode
            line = re.sub('(\d)([àáạảãăắằẵặẳâấầẫẩậèéẹẻẽêếềểệễìíĩịỉòóọỏõôốồổỗộơớờởỡợùúụủũưứừửữựýỳỵỹỷđ])', r'\1 \2', line)  # tách số khỏi chữ
            line = re.sub('([àáạảãăắằẵặẳâấầẫẩậèéẹẻẽêếềểệễìíĩịỉòóọỏõôốồổỗộơớờởỡợùúụủũưứừửữựýỳỵỹỷđ])(\d)', r'\1 \2', line)  # tách số khỏi chữ
            print("line 222: ", line)
            line = re.sub('(\d+)([,\.+])(\s)', r'\1 \2\3', line)
            line = re.sub('(\d+)([,\.+])($)', r'\1 \2\3', line)
            # print(line)
            line = re.sub('(\s)(\.{3,})(\d+)', r'\1\2 \3 ', line)
            # print(line)
            f.write(line + '\n')
    f.close()


def separate_symbol(input_s):
    # process link url
    new_input_s = []
    # print("input: ", input_s)
    findlink = re.findall(SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK_REGULAR, input_s)
    input_s = re.sub(SOPHIAConstants.SOPHIA_CHAR_CODE_UTF8, SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK, input_s)

    #----Seperate word in sentence---------
    input_s2 = split_word_in_sentence_vi(input_s)

    #-----get back hyperlink--------------
    j = 0
    for input_ in input_s2.split():
        if input_ == SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK.strip():
            input_ = str(''.join(findlink[j]))
            j += 1
        new_input_s.append(input_)

    return " ".join(new_input_s)


def split_word_in_sentence_vi(sent_vi):
    """
    Process some special characters
    :param sent_vi:
    :return:
    """
    return SOPHIAUtility.split_word_in_sentence(sent_vi)

def delete_ja_word(input_s):
    """

    :param input_s:
    :return:
    """
    japan_words = []
    for word in input_s:
        if SOPHIAUtility.is_cjk(word):
            japan_words.append(word)

    if len(japan_words) > 0:  # chi replace khi co tieng Nhat
        pattern1 = "([" + str("".join(japan_words)) + "]([/\)\]]))" + "|" + "(([/\(\[])[" + str(
            "".join(japan_words)) + "])" + "|" + \
                   "([" + str("".join(japan_words)) + "](\s[/\)\]]))" + "|" + "(([/\(\[]\s)[" + str(
            "".join(japan_words)) + "])"
        pattern2 = "([" + str("".join(japan_words)) + "])"
        input_s1 = re.sub(pattern1, ' ', input_s)
        input_s2 = re.sub(pattern2, ' ', input_s1)
    else:
        input_s2 = input_s

    return input_s2

def remove_symbol_empty(line):

    line = re.sub('(<\s>)', '',line)
    line = re.sub('({\s})', '',line)
    line = re.sub('(\［\s\］)', '',line)
    line = re.sub('(\（\s\）)', '',line)
    line = re.sub('(\(\))', '',line)
    line = re.sub('(<>)', '',line)
    line = re.sub('({})', '',line)
    line = re.sub('(\［\］)', '',line)
    line = re.sub('(\(\s\))', '',line)
    line = re.sub('(\[\s\])', '',line)
    line = re.sub('(\（\）)', '',line)
    return line

