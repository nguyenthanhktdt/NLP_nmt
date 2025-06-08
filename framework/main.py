import os
from optparse import OptionParser

from preprocessing.for_others import generate_vocab
from preprocessing.for_others import splitdata
from framework.preprocessing.mgiza import merge_mgiza
from train import process_unk
from framework.train import pre_process
from framework.train import source_vi
from framework.utils import sophia_tokenize


def preprocess_vi(options):
    
    folder = "/data/"
    print("folder: ", folder)
    input_file = os.path.join(folder,'data_vi.txt')
    output_file = os.path.join(folder,'data_pre.vi')
    print("Preprocess in main")
    pre_process.pre_process(input_file, output_file)

def preprocess_en(options):
    folder = "/data/"
    input_file = os.path.join(folder,'data_en.txt')
    output_file = os.path.join(folder,'data_pre.en')
    pre_process.pre_process(input_file, output_file)


def vietnamese_tokenizer(options):
    path = "data/"
    infile = open(os.path.join(path,"data_pre.vi"), encoding='utf-8')
    tokenfile = open(os.path.join(path,"data_pre_token.vi"),"w", encoding='utf-8')
    for line in infile:
        line = sophia_tokenize.vietnamese_segment_train(line)
        tokenfile.write(line + "\n")

def merge_file_mgiza(options):
    folder = "/mgiza/mgizapp/bin"
    merge_mgiza.merge_giza(folder)


def vocab_vi(options):
    folder = "/data/"

    input_file = os.path.join(folder, 'data.vi')
    print("input_file:", input_file)
    output_file = os.path.join(folder, 'vocab.vi')
    output_file_small = os.path.join(folder, 'vocab.small.vi')
    appear_number = 2 # If the word appears >= n times, it will be added to the vocabulary.
    generate_vocab.gen_vocab(input_file, output_file, output_file_small, appear_number)


def vocab_en(options):
    folder = "/data/"

    input_file = os.path.join(folder, 'data.en')
    print("input_file:", input_file)
    output_file = os.path.join(folder, 'vocab.en')
    output_file_small = os.path.join(folder, 'vocab.small.en')
    appear_number = 2 
    generate_vocab.gen_vocab(input_file, output_file, output_file_small, appear_number)


def process_unknown(options):
    folder = "/data"
    process_unk.process_unk_for_train(folder, 'data', 'vien')

def split_data(options):

    folder = "/data/"
    input_prefix_file_name = "data.unk"
    number_of_line = 1000 #  line
    splitdata.split_data(folder, input_prefix_file_name, number_of_line)

if __name__ == '__main__':
    s = ""
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="folder path input", metavar="FILE")
    parser.add_option("-n", "--name", dest="name",
                      metavar="FILE", help="file name")

    (options, args) = parser.parse_args()

  
    if options.input == "source_vi":
        preprocess_vi(options)
        print("DONE !")

    elif options.input == "target_en": 
        preprocess_en(options)
        print("DONE !")


    elif options.input == "token_vi": 
        vietnamese_tokenizer(options)
        print("DONE !")


    # Merge giza
    elif options.input == "merge_mgiza":
        merge_file_mgiza(options)
        print("DONE !")

    elif options.input == "vocab_vi":
        vocab_vi(options) 
        print("DONE !")
    elif options.input == "vocab_en": 
        vocab_en(options) 
        print("DONE !")

    elif options.input == "process_unk":
        process_unknown(options)
        print("DONE !")


    elif options.input == "split_data":
        split_data(options)
        print("DONE !")
    
    else:

        print(options.input)
