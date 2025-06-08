import os
DEBUG = True
DIRNAME = os.path.dirname(__file__)
STATIC_PATH = os.path.join(DIRNAME, 'static')
TEMPLATE_PATH = os.path.join(DIRNAME, 'template')

language = "vien"

out_dir = os.path.join("model",language)
if not os.path.exists(os.path.join(out_dir,'log_unk')):
    os.makedirs(os.path.join(out_dir,'log_unk'))
out_dir_unk = os.path.join(out_dir,'log_unk')

chk_path = os.path.join(out_dir, "translate.ckpt-20000")
vocab_file_preprocess = os.path.join(out_dir, 'vocab')
bpe_model_file = os.path.join(out_dir, 'bpe_model')

if not os.path.exists(os.path.join(out_dir,'log')):
    os.makedirs(os.path.join(out_dir,'log'))
out_dir_log = os.path.join(out_dir,'log')
