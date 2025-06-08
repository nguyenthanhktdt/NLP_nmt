import os
import sys

from framework.utils.sophia_constants import SOPHIAConstants as sophiaconst
from framework.utils.sophia_constants import UNKNOWN as sophiaconst_unk
from framework.utils.sophia_utility import SOPHIAUtility as sophiautils

sys.path.insert(0, sys.path)
import settings
import re
import datetime

log_unk_file_write = datetime.datetime.now().strftime("%Y-%m%d%H%M%s")
class UnknownUtils:

    class SourceVi:
        # Replace unknown words in source to <unk>
        @staticmethod
        def process_for_infer(vocab_vi, sent, dict_tb_in):
            POS_index = {
                '<unks>': 0,
                '<unkt>': 0,
                '<num>': 0,
            }
            vocab_sr = vocab_vi
            processed_sr = []
            dic_replace = {}
            sent = sophiautils.stand_line_vi_in(sent)
      
            sources = sent.strip("\n").strip().split(" ")
            for i in range(len(sources)):
                w = sources[i].strip()
                if sophiautils.is_contains_digit(w) and not w.startswith("<TB"):
                    word_sr = sophiaconst_unk.UNK_NUM % \
                              str(POS_index[sophiaconst_unk.PREFIX_NUM])
                    POS_index[sophiaconst_unk.PREFIX_NUM] += 1
                    dic_replace[word_sr] = w
                else:
                    if w in vocab_sr.keys():
                        word_sr = w
                    else:
                        word_sr = sophiaconst_unk.UNK_SRC % \
                                  str(POS_index[sophiaconst_unk.PREFIX_SRC])  # <unks1> <unks2>.....
                        POS_index[sophiaconst_unk.PREFIX_SRC] += 1
                        dic_replace[word_sr] = w

                processed_sr.append(word_sr)
            # log unk
            dict_unk = open(os.path.join(settings.out_dir_unk, 'vi_unknow_' + log_unk_file_write), 'a',
                            encoding='utf-8')
            for word in dic_replace.values():
                reg = re.findall('([àáạảãăắằẵặẳâấầẫẩậêếềểệưứừửữựôốồổỗộơớờởỡợđ])', word)
                if reg and len(word) > 0:
                    dict_unk.write(sent + "\n")
                    break

            line_out_sr = ' '.join(processed_sr) + "\n"
            return line_out_sr, dic_replace

        @staticmethod
        def process_for_train(vocab_vi, vi_sent):
            POS_index = {
                '<unks>': 0,
                '<unkt>': 0,
                '<num>': 0,
            }
            processed_vi = []
            dic_replace = {}

            vi_words = vi_sent.strip("\n").strip().split(" ")

            # --------process source sentence-------------
            for i in range(len(vi_words)):
                w = vi_words[i].strip()
                if sophiautils.is_contains_digit(w) and not w.startswith("<TB"):
                    word_sr = sophiaconst_unk.UNK_NUM % \
                              str(POS_index[sophiaconst_unk.PREFIX_NUM])

                    POS_index[sophiaconst_unk.PREFIX_NUM] += 1

                    dic_replace[i] = word_sr
                else:
                    if w in vocab_vi.keys():
                        word_sr = w
                    else:
                        word_sr = sophiaconst_unk.UNK_SRC % \
                                  str(POS_index[sophiaconst_unk.PREFIX_SRC])  # <unks1> <unks2>.....

                        POS_index[sophiaconst_unk.PREFIX_SRC] += 1

                        dic_replace[i] = word_sr

                processed_vi.append(word_sr)

            line_out_vi = ' '.join(processed_vi) + "\n"

            return line_out_vi, dic_replace

    
    class TargetEn:

        @staticmethod
        def process_unknow_train(vocab_en, sent_en, alignment, dic_replace):

            en_words = sent_en.strip("\n").strip().split(" ")
            aligns = alignment.strip("\n").strip().split(" ")

            last_word = ""
            last_align = 0
            processed_en = []

            for i_tg in range(len(en_words)):  # for each word in target
                has_align = False
                index_tg = i_tg + 1
                pairs_align = []
                word = en_words[i_tg].strip()
                if word == '':
                    continue
                for align in aligns:
                    if align.endswith("-" + str(index_tg)):  # if target word has source alignment
                        pairs_align = align.split("-")
                        has_align = True
                        break

                if has_align:  # it has alignment
                    pos = int(pairs_align[0]) - 1

                    if pos in dic_replace.keys():  # if align with unknown word, replace by source
                        word_tg = dic_replace[pos]
                        if word_tg == last_word:
                            continue
                        else:
                            last_word = word_tg
                    else:
                        if word in vocab_en.keys():
                            word_tg = word
                        else:
                            d = int(pairs_align[1]) - int(pairs_align[0])
                            word_tg = sophiaconst_unk.UNK_TG % str(d)

                    last_align = pos
                else:  # it doesnt have alignment
                    if word in vocab_en.keys():
                        word_tg = word
                    else:
                        continue
                processed_en.append(word_tg)
            # return value
            line_out_en = ' '.join(processed_en) + "\n"

            return line_out_en

        @staticmethod
        def process_unknown_infer(source, target, dic_replace):

            processed_tg = []
            src_words = source.strip("\n").strip().split(" ")
            tg_words = target.strip("\n").strip().split(" ")
            # --------process target sentence-------------
            j = -1
            last_word = ""
            for word in tg_words:
                j += 1
                if word == '':
                    continue

                if word.startswith(sophiaconst.SOPHIA_INFER_TAG_prefix_unkt):  # if word is <unkt...>
                    if last_word == word:
                        continue
                    else:
                        last_word = word
                    # replace by source tag
                    index = word.replace(sophiaconst.SOPHIA_INFER_TAG_prefix_unkt, "").replace(">", "")
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
                    processed_tg.append(s)

            line_out_tg = ' '.join(processed_tg)
            return line_out_tg
   