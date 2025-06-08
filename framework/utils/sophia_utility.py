import logging
import os
import re
from datetime import date

# sys.path.insert(0, sys.path)
from sophia_constants import SOPHIAConstants
from sophia_constants import NAME

import settings

lang = settings.language[:]

class SOPHIAUtility(object):
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SOPHIAUtility.__instance == None:
            SOPHIAUtility()
        return SOPHIAUtility.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SOPHIAUtility.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SOPHIAUtility.__instance = self

    @classmethod
    def lowerDataForTrain(self, line):
        return line.lower()
    @staticmethod
    def is_contains_digit(input_string):
        is_digit = any(char.isdigit() for char in input_string)

        return is_digit


    @staticmethod
    def is_latin(text):
        return re.findall("([A-Za-z])", text)

    @staticmethod
    def split_word_in_sentence(sentence):
        print("split_word_in_sentence: ", sentence)

        reg = re.findall(r"([\W_〇])", sentence)
        symbol_punctuation = []
        for i in sentence:
            if (i in reg) or (9312 < ord(i) < 11090):  # find symbol ascii code ①-20-⭒
                symbol_punctuation.append(i)
        symbol = "".join(symbol_punctuation)
        if len(symbol) > 0:
            try:
                regular = "(?<=\S)([" + str(
                    symbol) + "])"  
                new_string = re.sub(str(regular), r' \1', sentence)
                regular2 = "([" + str(
                    symbol) + "])(?=\S)" 
                new_string = re.sub(str(regular2), r'\1 ', new_string)
                sentence = new_string
            except:
                pass
        print("sentence after split_word_in_sentence: ", sentence)
        return sentence
    @classmethod
    def remove_char_specical_with_pattern(self, char_specical_pattern, pattern, in_str):
        out_str = re.sub(char_specical_pattern, pattern, in_str)
        return out_str
    
    @classmethod
    def stand_line_vi_in(self, line):
        line = re.sub(r'(^・)', r'-', line)
        line = re.sub(r'(・)', r'/', line)
        dictfile = open("../../framework/train/symbol.vi", encoding='utf-8')
        d = {}
        for lines in dictfile.readlines():
            key = lines.split("\t")[0]
            val = lines.split("\t")[1:]
            val = "".join(val)
            d[key] = val.rstrip()
        for word in line.split():
            if word in d.keys():
                line = line.replace(word, str(d[word]))
        return line

    @classmethod
    def stand_line_ja_out(self, line):
        if len(line) > 3:
            reg1 = '([^a-zA-Z0-9])(\s)([^a-zA-Z0-9])'
            reg2 = '([a-zA-Z0-9])(\s)([^a-zA-Z0-9])'
            reg3 = '([^a-zA-Z0-9])(\s)([a-zA-Z0-9])'
            line_out = re.sub(reg1, r'\1\3', line)
            line_out = re.sub(reg2, r'\1\3', line_out)
            line_out = re.sub(reg3, r'\1\3', line_out)
            line_out = re.sub('(.+)(\s)(\W)', r'\1\3', line_out)
            line_out = re.sub('(\W)(\s)(.+)', r'\1\3', line_out)
            line_out = re.sub(reg1, r'\1\3', line_out)
            line_out = re.sub(reg2, r'\1\3', line_out)
            line_out = re.sub(reg3, r'\1\3', line_out)
        else:
            line_out = line
        return line_out
    @classmethod
    def remove_char(self, str, n):
        '''
        use: remove_char(string, n), n: position
        :param str:
        :param n:
        :return:
        '''
        first_part = str[:n]
        last_part = str[n+1:]

        return first_part + last_part
    
    @classmethod
    def process_nhaykep(self, str):
        position = [pos for pos, char in enumerate(str) if char == "\"" or char == "“" or char == "”"]
        position_delete = []
        for i in range(len(position)):
            if i % 2 == 0:
                position_delete.append(position[i] + 1)
            else:
                position_delete.append(position[i] - 1)
        k = 0
        for n in position_delete:
            str = SOPHIAUtility.remove_char(str, n-k)
            k += 1

        return str



    @classmethod
    def format_output_vien(self,result_vi):
        responsibility = SOPHIAUtility.remove_char_specical_with_pattern(
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_CURRENCY,
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_R_2, result_vi) # 1 %, 1 $ -> 1%, 1$
        responsibility = SOPHIAUtility.remove_char_specical_with_pattern(
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_OTHER,
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_R_2, responsibility) # (abc , -> abc,)
        responsibility = SOPHIAUtility.remove_char_specical_with_pattern(
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_OTHER_2,
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_R_1, responsibility)  # sua abc / xyz thanh abc/xyz
        responsibility = SOPHIAUtility.remove_char_specical_with_pattern(
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_4,
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_R_1, responsibility)
        responsibility = SOPHIAUtility.remove_char_specical_with_pattern(
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_6,
            SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_R_6, responsibility)
        #============ Viet hoa ==================
        for i in responsibility:
            if i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàáạảãăắằẵặẳâấầẫẩậèéẹẻẽêếềểệễìíĩịỉòóọỏõôốồổỗộơớờởỡợùúụụủũưứừửữựýỳỵỹỷđ":
                responsibility = responsibility.replace(i, i.upper(), 1)
                break
        return responsibility


    @classmethod
    def process_dot_sr_tg(self, source, target):
        reg_more_dot = re.findall(r'(\.\.$)', target)
        if reg_more_dot:
            pass
        else:
            reg_source = re.findall(SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_5, source)
            reg_target = re.findall(SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_5, target)
            if not reg_source:  
                if not reg_target: 
                    pass
                else:  
                    target = re.sub(SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_R5,
                                    SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_R_0, target)
                    print("result: ", target)
            else:  
                if not reg_target:  
                    target = SOPHIAUtility.add_dot_punctual_vi_predict(target)
                    print("result: ", target)
        return target

    @classmethod
    def load_vocab_source(self, file_path):
        file_vocab = file_path + "." + settings.language[:2]
        vocab_source = {}
        with open(file_vocab, "r", encoding="utf-8") as f1:
            for line in f1:
                line = line.strip("\n").strip()
                vocab_source[line] = 1
        return vocab_source

    def load_vocab_target(self, file_path):
        file_vocab_target = file_path + "." + settings.language[2:]
        vocab_target = {}
        with open(file_vocab_target, "r", encoding="utf-8") as f2:
            for line in f2:
                line = line.strip("\n").strip()
                vocab_target[line] = 1
        return vocab_target

    @classmethod
    def add_dot_punctual_vi(self, line):
        reg = re.findall('(\.$)',line)
        if reg:
            return line
        else:
            return line + " ."
    @classmethod
    def add_dot_punctual_ja(self, line):
        reg = re.findall('(\。$)',line)
        if reg:
            return line
        else:
            return line + " 。"

    @classmethod
    def add_dot_punctual_vi_predict(self, line):
        reg = re.findall('(\.$)',line)
        if reg:
            return line
        else:
            return line + "."

    amt_log = None
    @staticmethod
    def create_log():
        """
                Log information to the file.
                :return: logger
                """
        # Directory to save logs
        file_log = os.path.join(settings.out_dir_log, str(date.today()) + ".log")

        log_file = os.path.join(file_log) 
        print(log_file)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # create a file handler
        if os.path.exists(file_log):
            handler = logging.FileHandler(log_file, encoding='utf-8')
        else:
            with open(log_file, 'w+', encoding='utf-8'): pass
            handler = logging.FileHandler(log_file, mode='w+', encoding='utf-8')

        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)
        return logger
    @staticmethod
    def write_log(content, error=False):
        if SOPHIAUtility.amt_log == None:
            SOPHIAUtility.amt_log = SOPHIAUtility.create_log()
        if error:
            SOPHIAUtility.amt_log.error(content)
        else:
            SOPHIAUtility.amt_log.info(content)


    @staticmethod
    def pos_name_vi(sent):
        names = NAME.POS_name.keys()
        for name in names:
            pattern = '(\s' + name + '\s)|(^' + name + '\s)|(\s' + name + '$)'
            sent = re.sub(pattern, " " + NAME.POS_name[name] + " ", sent)
        return sent

    @staticmethod
    def pos_name_en(sent):
        names = NAME.POS_name_en.keys()
        for name in names:
            pattern = '(\s' + name + '\s)|(^' + name + '\s)|(\s' + name + '$)'
            sent = re.sub(pattern, " " + NAME.POS_name_en[name] + " ", sent)
        return sent

