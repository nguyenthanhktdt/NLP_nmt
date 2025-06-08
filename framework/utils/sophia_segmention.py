import re, sys, os, math, tempfile, collections
import sbd_util, word_tokenize
import nltk
from nltk.tokenize import sent_tokenize
from framework.utils.sophia_utility import SOPHIAUtility
"""
Utilities for disambiguating sentence boundaries
Copyright Dan Gillick, 2009.

TODO:
- capitalized headlines screw things up?
- deal with ?! maybe just assume these sentence boundaries always
"""


def unannotate(t):
    """
    get rid of a tokenized word's annotations
    """
    t = re.sub('(<A>)?(<E>)?(<S>)?$', '', t)
    return t

def clean(t):
    """
    normalize numbers, discard some punctuation that can be ambiguous
    """
    t = re.sub('[.,\d]*\d', '<NUM>', t)
    t = re.sub('[^a-zA-Z0-9,.;:<>\-\'\/?!$% ]', '', t)
    t = t.replace('--', ' ') # sometimes starts a sentence... trouble
    return t

def get_features(frag, model):
    """
    ... w1. (sb?) w2 ...
    Features, listed roughly in order of importance:

    (1) w1: word that includes a period
    (2) w2: the next word, if it exists
    (3) w1length: number of alphabetic characters in w1
    (4) w2cap: true if w2 is capitalized
    (5) both: w1 and w2
    (6) w1abbr: log count of w1 in training without a final period
    (7) w2lower: log count of w2 in training as lowercased
    (8) w1w2upper: w1 and w2 is capitalized
    """
    words1 = clean(frag.tokenized).split()
    if not words1: w1 = ''
    else: w1 = words1[-1]
    if frag.next:
        words2 = clean(frag.next.tokenized).split()
        if not words2: w2 = ''
        else: w2 = words2[0]
    else:
        words2 = []
        w2 = ''

    c1 = re.sub('(^.+?\-)', '', w1)
    c2 = re.sub('(\-.+?)$', '', w2)

    feats = {}

    feats['w1'] = c1
    feats['w2'] = c2
    feats['both'] = c1 + '_' + c2

    len1 = min(10, len(re.sub('\W', '', c1)))

    if c1.replace('.','').isalpha():
        feats['w1length'] = str(len1)
        try: feats['w1abbr'] = str(int(math.log(1+model.non_abbrs[c1[:-1]])))
        except: feats['w1abbr'] = str(int(math.log(1)))

    if c2.replace('.','').isalpha():
        feats['w2cap'] = str(c2[0].isupper())
        try: feats['w2lower'] = str(int(math.log(1+model.lower_words[c2.lower()])))
        except: feats['w2lower'] = str(int(math.log(1)))
        feats['w1w2upper'] = c1 + '_' + str(c2[0].isupper())

    return feats

def is_sbd_hyp(word):

    if not '.' in word: return False
    c = unannotate(word)
    if c.endswith('.'): return True
    if re.match('.*\.["\')\]]*$', c): return True
    return False

def get_text_data(text, expect_labels=True, tokenize=False, verbose=False):
    """
    get text, returning an instance of the Doc class
    doc.frag is the first frag, and each points to the next
    """

    frag_list = None
    word_index = 0
    frag_index = 0
    curr_words = []
    lower_words, non_abbrs = sbd_util.Counter(), sbd_util.Counter()

    for line in text.splitlines():

        ## deal with blank lines
        if (not line.strip()) and frag_list:
            if not curr_words: frag.ends_seg = True
            else:
                frag = Frag(' '.join(curr_words))
                frag.ends_seg = True
                if expect_labels: frag.label = True
                prev.next = frag
                if tokenize:
                    tokens = word_tokenize.tokenize(frag.orig)
                frag.tokenized = tokens
                frag_index += 1
                prev = frag
                curr_words = []

        for word in line.split():
            curr_words.append(word)

            if is_sbd_hyp(word):
                frag = Frag(' '.join(curr_words))
                if not frag_list: frag_list = frag
                else: prev.next = frag

                ## get label; tokenize
                if expect_labels: frag.label = int('<S>' in word)
                if tokenize:
                    tokens = word_tokenize.tokenize(frag.orig)
                else: tokens = frag.orig
                tokens = re.sub('(<A>)|(<E>)|(<S>)', '', tokens)
                frag.tokenized = tokens

                frag_index += 1
                prev = frag
                curr_words = []

            word_index += 1

    ## last frag
    frag = Frag(' '.join(curr_words))
    if not frag_list: frag_list = frag
    else: prev.next = frag
    if expect_labels: frag.label = int('<S>' in word)
    if tokenize:
        tokens = word_tokenize.tokenize(frag.orig)
    else: tokens = frag.orig
    tokens = re.sub('(<A>)|(<E>)|(<S>)', '', tokens)
    frag.tokenized = tokens
    frag.ends_seg = True
    frag_index += 1

    if verbose: sys.stderr.write(' words [%d] sbd hyps [%d]\n' %(word_index, frag_index))

    ## create a Doc object to hold all this information
    doc = Doc(frag_list)
    return doc


class Model:
    """
    Abstract Model class holds all relevant information, and includes
    train and classify functions
    """
    def __init__(self, path):
        self.feats, self.lower_words, self.non_abbrs = {}, {}, {}
        self.path = path

    def prep(self, doc):
        self.lower_words, self.non_abbrs = doc.get_stats(verbose=False)
        self.lower_words = dict(self.lower_words)
        self.non_abbrs = dict(self.non_abbrs)

    def train(self, doc):
        abstract

    def classify(self, doc, verbose=False):
        abstract

    def save(self):
        """
        save model objects in self.path
        """
        sbd_util.save_pickle(self.feats, self.path + 'feats')
        sbd_util.save_pickle(self.lower_words, self.path + 'lower_words')
        sbd_util.save_pickle(self.non_abbrs, self.path + 'non_abbrs')

    def load(self):
        """
        load model objects from p
        """
        self.feats = sbd_util.load_pickle(self.path + 'feats')
        self.lower_words = sbd_util.load_pickle(self.path + 'lower_words')
        self.non_abbrs = sbd_util.load_pickle(self.path + 'non_abbrs')


class NB_Model(Model):
    """
    Naive Bayes model, with a few tweaks:
    - all feature types are pooled together for normalization (this might help
      because the independence assumption is so broken for our features)
    - smoothing: add 0.1 to all counts
    - priors are modified for better performance (this is mysterious but works much better)
    """

    def classify_nb_one(self, frag):
        ## the prior is weird, but it works better this way, consistently
        probs = sbd_util.Counter([(label, self.feats[label, '<prior>']**4) for label in [0,1]])
        for label in probs:
            for feat, val in frag.features.items():
                key = (label, feat + '_' + val)
                if not key in self.feats: continue
                probs[label] *= self.feats[key]

        probs = sbd_util.normalize(probs)
        return probs[1]

    def classify(self, doc, verbose=False):
        if verbose: sys.stderr.write('NB classifying... ')
        frag = doc.frag
        while frag:
            pred = self.classify_nb_one(frag)
            frag.pred = pred
            frag = frag.next
        if verbose: sys.stderr.write('done!\n')

class Doc:
    """
    A Document points to the head of a Frag object
    """

    def __init__(self, frag):
        self.frag = frag

    def __str__(self):
        s = []
        curr = self.frag
        while curr: s.append(curr)
        return '\n'.join(s)

    def get_stats(self, verbose):
        if verbose: sys.stderr.write('getting statistics... ')
        lower_words = sbd_util.Counter()
        non_abbrs = sbd_util.Counter()

        frag = self.frag
        while frag:
            for word in frag.tokenized.split():
                if word.replace('.', '').isalpha():
                    if word.islower(): lower_words[word.replace('.','')] += 1
                    if not word.endswith('.'): non_abbrs[word] += 1
            frag = frag.next

        if verbose: sys.stderr.write('lowercased [%d] non-abbrs [%d]\n'
                                     %(len(lower_words), len(non_abbrs)))

        return lower_words, non_abbrs

    def featurize(self, model, verbose=False):
        if verbose: sys.stderr.write('featurizing... ')
        frag = self.frag
        while frag:
            frag.features = get_features(frag, model)
            frag = frag.next
        if verbose: sys.stderr.write('done!\n')

    def segment(self, use_preds=False, tokenize=False, output=None, list_only=False):
        """
        output all the text, split according to predictions or labels
        """
        sents = []
        thresh = 0.5
        sent = []
        frag = self.frag
        while frag:
            if tokenize: text = frag.tokenized
            else: text = frag.orig
            sent.append(text)
            if frag.ends_seg or (use_preds and frag.pred>thresh) or (not use_preds and frag.label>thresh):
                if not frag.orig: break
                sent_text = ' '.join(sent)
                if frag.ends_seg: spacer = '\n\n'
                else: spacer = '\n'
                if output: output.write(sent_text + spacer)
                elif not list_only: sys.stdout.write(sent_text + spacer)
                sents.append(sent_text)
                sent = []
            frag = frag.next
        return sents

class Frag:
    """
    A fragment of text that ends with a possible sentence boundary
    """
    def __init__(self, orig):
        self.orig = orig
        self.next = None
        self.ends_seg = False
        self.tokenized = False
        self.pred = None
        self.label = None
        self.features = None

    def __str__(self):
        s = self.orig
        if self.ends_seg: s += ' <EOS> '
        return s

def load_sbd_model(model_path): #, use_svm=False):
    sys.stderr.write('loading model from [%s]... ' %model_path)
    model = NB_Model(model_path)
    model.load()
    sys.stderr.write('done!\n')
    return model


def sentences_segment(text):
    return sent_tokenize(text)