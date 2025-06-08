#!/bin/bash
dir_path="/home/sophia/work_space/00.code_vistula/04_NLP_LargeLanguageModels/NLP/data_vi-en/test"
vocab=$dir_path"/vocab"
train=$dir_path"/train"
dev=$dir_path"/dev"
test=$dir_path"/test"
out_dir=$dir_path"/run_out_4layers"

python3 -m nmt.nmt     --src=vi \
                      --tgt=en \
                      --vocab_prefix=$vocab \
                      --train_prefix=$train \
                      --dev_prefix=$dev \
                      --test_prefix=$test \
                      --out_dir=$out_dir \
                      --steps_per_stats=1000 \
                      --dropout=0.2 \
                      --metrics=bleu \
                      --num_units=512 \
                      --num_layers=4 \
                      --encoder_type=bi \
                      --attention=scaled_luong \
                      --attention_architecture=standard \
                      --optimizer=sgd \
                      --learning_rate=1 \
                      --start_decay_step=10000 \
                      --decay_steps=5000 \
                      --decay_factor=0.8 \
                      --num_train_steps=20000 \
                      --beam_width=10 \	
                      > $out_dir/output
