
opt = "-deftag UNKNOWN!!" #
from framework.utils.sophia_constants import SOPHIAConstants
from framework.utils.sophia_utility import SOPHIAUtility
from underthesea import word_tokenize


def vietnamese_segment_predict(sentence):
    sentence = word_tokenize(sentence, format="text") 
    return sentence

def vietnamese_segment_train(sentence):
    sentence_token = word_tokenize(sentence, format="text")

    return sentence_token
