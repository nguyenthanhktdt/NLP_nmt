import re
import unicodedata as ud

from framework.utils.sophia_constants import SOPHIAConstants
from framework.utils.sophia_utility import  SOPHIAUtility

def pre_process(input_file, output_file):
    
    f = open(output_file, 'w', encoding='utf-8')
    with open(input_file, encoding='utf-8') as f1:
        for line in f1:
            s = line.lower()
            print("line in 13: ", s)
            if len(s) != 0 or s != ' ':
                s = remove_jp_separate_symbol(s)
            line = SOPHIAUtility.add_dot_punctual_vi(s)
            line = ud.normalize(SOPHIAConstants.SOPHIA_CHAR_NFKC, line)  #convert to unicode
            line = re.sub('(\d)(,)(\s)', r'\1 \2\3', line)
            print("line after process: ", line)
            f.write(line + '\n')
    f.close()


def remove_jp_separate_symbol(input_s):
 
    # process link url
    new_input_s = []
    findlink = re.findall(SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK_REGULAR, input_s)
    input_s = re.sub(SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK_REGULAR, SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK, input_s)

    if type(input_s) != type(" "):
        return input_s

    #----Seperate word in sentence---------
    input_s2 = split_word_in_sentence_en(input_s)

    #-----get back hyperlink--------------
    j = 0
    for input_ in input_s2.split():
        if input_ == SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK.strip():
            input_ = str(''.join(findlink[j]))
            j += 1
        new_input_s.append(input_)

    return " ".join(new_input_s)


def split_word_in_sentence_en(sent_en):
    """
    Process some special characters
    :param sent_vi:
    :return:
    """
    return SOPHIAUtility.split_word_in_sentence(sent_en)

