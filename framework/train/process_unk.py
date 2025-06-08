import os
from framework.utils.sophia_constants import SOPHIAConstants as sophiaconst
from framework.utils.sophia_unk_utils import UnknownUtils

def get_vocab(file_vi, file_en):
    vocab_vi = {}
    vocab_en = {}
   
    with open(file_vi, encoding='utf-8') as f1:
        for line in f1:
            line = line.strip("\n") #.strip()
            vocab_vi[line] = 1

    with open(file_en, encoding='utf-8') as f2:
        for line in f2:
            line = line.strip("\n") #.strip()
            vocab_en[line] = 1

    return vocab_vi, vocab_en


def process_unk_for_train(folder="none", file_name="none", option='none'):

    input_vi = os.path.join(folder, file_name + '.vi')
    input_en = os.path.join(folder, str(file_name) + ".en")
    input_align = os.path.join(folder, str(file_name) + ".align")
    print("input_align:", input_align)

    file_vocab_vi = os.path.join(folder, "vocab.vi")
    file_vocab_en = os.path.join(folder, "vocab.en")

    output_vi = os.path.join(folder, str(file_name) + ".unk.vi")
    output_en = os.path.join(folder, str(file_name) + ".unk.en")

    write_file_vi = open(output_vi, 'w', encoding='utf-8')
    write_file_en = open(output_en, 'w', encoding='utf-8')

    vocab_vi, vocab_en = get_vocab(file_vocab_vi, file_vocab_en)

    f1 = open(input_vi, "r", encoding='utf-8')
    f2 = open(input_en, "r", encoding='utf-8')
    f3 = open(input_align, "r", encoding='utf-8')
    i = 0

    for vi_sent, en_sent, align in zip(f1, f2, f3):
        i = i + 1
        if i==1:
            print("aaaa")
        if option == sophiaconst.PROCESS_VI_TO_EN:
            line_out_vi, dic_replace = UnknownUtils.SourceVi.process_for_train(vocab_vi, vi_sent)
            line_out_en = UnknownUtils.TargetEn.process_unknow_train(vocab_en, en_sent, align, dic_replace)
            write_file_vi.write(line_out_vi)
            write_file_en.write(line_out_en)

    write_file_vi.close()
    write_file_en.close()

