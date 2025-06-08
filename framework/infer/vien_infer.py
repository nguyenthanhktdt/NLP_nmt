import re
import time
import unicodedata as ud

from api.api4app import App_vien as ac
from framework.utils.sophia_constants import SOPHIAConstants
from framework.utils.sophia_segmention import sentences_segment
from framework.utils.sophia_unk_utils import UnknownUtils
from framework.utils.sophia_utility import SOPHIAUtility
from framework.utils.sophia_tokenize import vietnamese_segment_predict


class ViEnInfer:

    # split line in a paragraph and replace by [S1], [S2], [S3] ....
    @staticmethod
    def split_sentence(text):

        # replace_sens = ""
        i = 0
        out_lines = []
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            sens = sentences_segment(line)
            for s in sens:
                if s == '[' or s == ']':
                    s = s + ' '
                if s.strip() != "":
                    i += 1
                    text = text.replace(s, "[S" + str(i) + "]", 1)
                    out_lines.append(s.strip())
        return out_lines

    @classmethod
    def pre_process_sent(self, nmt_sent):
        time_start_preprocess = time.time()
        line = ' '.join(nmt_sent.split())
        out_lines = []
        origin_lines = []
        dic_unk_replace = {}
        i = 0
        line = ud.normalize(SOPHIAConstants.SOPHIA_CHAR_NFKC, str(line))
        line = SOPHIAUtility.add_dot_punctual_vi(line) 

        findlink = re.findall(SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK_REGULAR, line)
        line = re.sub(SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK_REGULAR, SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK, line)
        line_none_lower = SOPHIAUtility.split_word_in_sentence(line)
        #-----get back hyperlink--------------
        new_line = []
        j = 0
        for input in line_none_lower.split():
            if input == SOPHIAConstants.SOPHIA_PROCESS_HTTP_LINK.strip():
                input = str(''.join(findlink[j]))
                j += 1
            new_line.append(input)

        line_vi = " ".join(new_line)
        line = line_vi.lower()
        line = vietnamese_segment_predict(line) 
        origin_lines.append(line)
        # replace unk
        line = line.replace("\n", "")
        out, dic_unk = UnknownUtils.SourceVi.process_for_infer(ac.App_vien.vocab_vi, line)
        dic_unk_replace[i] = dic_unk
        i += 1
        out_lines.append(out)
        return out_lines, origin_lines, dic_unk_replace, line_none_lower

    @classmethod
    def pos_process_sent(self, sources, targets, dic_unk_replace, nmt_sent):
        out_lines = []
        i = 0
        for sr, tg in zip(sources, targets):
            dic_unk = dic_unk_replace[i]
            i += 1
            line = UnknownUtils.TargetEn.process_unknown_infer(sr, tg, dic_unk)
            out_lines.append(line)
        result = " ".join(out_lines)
        regvi = re.findall(SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_5, nmt_sent)
        regen = re.findall(SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_5, result)
        if not regen:  
            if not regvi:  
                pass
            else:  
                result = SOPHIAUtility.add_dot_punctual_ja(result)
        else:  
            if not regvi:  
                result = re.sub(SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_ALPHABET_R5_ja,
                                SOPHIAConstants.SOPHIA_CHAR_SPECIAL_PATTERN_R_0, result)
        return result
