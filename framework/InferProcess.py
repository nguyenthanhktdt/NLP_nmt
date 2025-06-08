import sys
import MeCab
import re
import pandas as pd
from framework.utils.sophia_constants import SOPHIAConstants


class InferProcess(object):
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if InferProcess.__instance == None:
            InferProcess()
        return InferProcess.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if InferProcess.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            InferProcess.__instance = self

    @classmethod
    def is_latin(self, text):
        return re.findall("([A-Za-z])", text)

    @classmethod
    def mecab_token(self, input_str):
        analyzed_words = []
        tagger = MeCab.Tagger(SOPHIAConstants.SOPHIA_MECAB_TAG)
        parsed = tagger.parse(input_str)
        words = parsed.split('\n')
        for word in words:
            elements = re.split('\t|,', word)
            if len(elements) < 2:
                continue
            analyzed_words.append(elements)
        return pd.DataFrame(analyzed_words)

    @classmethod
    def get_POS(self, tokens):
        dic_ja_token = {}
        num_rows = len(tokens.index)
        for i in range(num_rows):
            row = tokens.iloc[i]
            if row[3] != "*":
                dic_ja_token[row[0]] = row[3]
            else:
                dic_ja_token[row[0]] = row[2]
        return dic_ja_token

    @classmethod
    def is_contains_digit(self, input_string):
        is_digit = any(char.isdigit() for char in input_string)
        is_digit = is_digit or (input_string in SOPHIAConstants.NUMBER_JA.DIC_NUMBERS.keys())

        return is_digit

    # Replace unknown words in source to <unk>
    @classmethod
    def replace_unk_source(self, vocab_ja, vocab_vi, lang, sent):
        POS_index = {
            '数': 0,  # number
            '組織': 0,  # organization
            '地域': 0,  # Region
            '人名': 0,  # A person's name
            '<unks>': 0,
            '<unkt>': 0,
            '<num>': 0,
        }

        if lang == "ja":
            vocab_sr = vocab_ja
        else:
            vocab_sr = vocab_vi
        processed_sr = []
        dic_replace = {}
        sources = sent.strip("\n").split(" ")
        print("source_replace_unk= ", sources) #OK
        #print("++++++++++++++++++++++replace_unk_source++++++++++ sources=", sources)

        # --------process source sentence-------------
        for i in range(len(sources)):
            w = sources[i].strip()
            if InferProcess.is_contains_digit(w):
                word_sr = SOPHIAConstants.SOPHIA_INFER_TAG_unk_num % str(POS_index[SOPHIAConstants.SOPHIA_INFER_TAG_prefix_num])
                POS_index[SOPHIAConstants.SOPHIA_INFER_TAG_prefix_num] += 1
                dic_replace[word_sr] = w
            else:
                if w in vocab_sr.keys() and not InferProcess.is_latin(w):
                    word_sr = w
                else:
                    word_sr = SOPHIAConstants.SOPHIA_INFER_TAG_unk_sr % str(
                        POS_index[SOPHIAConstants.SOPHIA_INFER_TAG_prefix_sr])  # <unks1> <unks2>.....
                    POS_index[SOPHIAConstants.SOPHIA_INFER_TAG_prefix_sr] += 1
                    dic_replace[word_sr] = w

            processed_sr.append(word_sr)
        processed_sr.append(sources[-1])
        line_out_sr = ' '.join(processed_sr) + "\n"
        print("line_out_sr", line_out_sr)
        print("dic_replace", dic_replace)
        return line_out_sr, dic_replace

    # Replace <unkp1> in target by words in source
    @classmethod
    def replace_unk_target(self, source, target, dic_replace):
        print("target= ", target) #not OK
        processed_tg = []
        src_words = source.strip("\n").split(" ")
        tg_words = target.strip("\n").split(" ")
        # --------process target sentence-------------
        j = -1
        last_word = ""
        for word in tg_words:
            j += 1
            if word.startswith(SOPHIAConstants.SOPHIA_INFER_TAG_prefix_unkt):  # if word is <unkt...>
                if last_word == word:
                    continue
                else:
                    last_word = word
                # replace by source tag
                index = word.replace(SOPHIAConstants.SOPHIA_INFER_TAG_prefix_unkt, "").replace(">", "")
                d = int(index)
                i = j - d
                if (i >= 0) and (i < len(src_words)):
                    s = src_words[i]
                    processed_tg.append(s)
            elif word not in dic_replace.keys():  # if word is not unknown word
                processed_tg.append(word)
            else:  # if word is like <num0> <org0>......
                if last_word == word:
                    continue
                else:
                    last_word = word

                s = dic_replace[word]
                print("processed_tg=",processed_tg)
                processed_tg.append(s)

        line_out_tg = ' '.join(processed_tg)
        return line_out_tg

    # split line in a paragraph and replace by [S1], [S2], [S3] ....
    @classmethod
    def split_sentence(self, text):

        replace_sens = ""
        i = 0
        out_lines = []
        lines = text.split("\n")
        for line in lines:
            sens = re.split(SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_SYMBOL_2, line.strip())
            for s in sens:
                if s.strip() != "":
                    i += 1
                    text = text.replace(s, "[S" + str(i) + "]", 1)
                    out_lines.append(s.strip())

        replace_sens = text.replace("。", " ")
        return replace_sens, out_lines

    # Replace [S1], [S2], [S3] by target line at right position
    @classmethod
    def merge_sentence(self,lines, replacement):
        i = 0
        result = replacement

        for line in lines:
            i += 1
            result = result.replace("[S" + str(i) + "]", line)
        return result
