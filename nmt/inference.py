# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""To perform inference on test set given a trained model."""
from __future__ import print_function

import codecs
import time
from queue import Queue
import tensorflow as tf

from . import attention_model
from . import gnmt_model
from . import model as nmt_model
from . import model_helper
from .utils import misc_utils as utils
from .utils import nmt_utils

__all__ = ["load_data", "inference",
           "single_worker_inference", "multi_worker_inference"]

# Thanh sua
def _decode_inference_indices(model, sess,
                              inference_indices,
                              tgt_eos,
                              subword_option):
  """Decoding only a specific set of sentences."""
  utils.print_out("  decoding, num sents %d." % (len(inference_indices)))
  start_time = time.time()
  translation = ""
  for decode_id in inference_indices:
    nmt_outputs, infer_summary = model.decode(sess)

  # get text translation
    assert nmt_outputs.shape[0] == 1
    translation += nmt_utils.get_translation(
      nmt_outputs,
      sent_id=0,
      tgt_eos=tgt_eos,
      subword_option=subword_option) + "\n"

    utils.print_out(b"%s\n" % translation)
  utils.print_time("  done", start_time)
  return translation


  # with codecs.getwriter("utf-8")(
  #     tf.gfile.GFile(output_infer, mode="wb")) as trans_f:
  #   trans_f.write("")  # Write empty string to ensure file is created.
  #   for decode_id in inference_indices:
  #     nmt_outputs, infer_summary = model.decode(sess)
  #
  #     # get text translation
  #     assert nmt_outputs.shape[0] == 1
  #     translation = nmt_utils.get_translation(
  #         nmt_outputs,
  #         sent_id=0,
  #         tgt_eos=tgt_eos,
  #         subword_option=subword_option)
  #
  #     if infer_summary is not None:  # Attention models
  #       image_file = output_infer_summary_prefix + str(decode_id) + ".png"
  #       utils.print_out("  save attention image to %s*" % image_file)
  #       image_summ = tf.Summary()
  #       image_summ.ParseFromString(infer_summary)
  #       with tf.gfile.GFile(image_file, mode="w") as img_f:
  #         img_f.write(image_summ.value[0].image.encoded_image_string)
  #
  #     trans_f.write("%s\n" % translation)
  #     utils.print_out(translation + b"\n")
  # utils.print_time("  done", start_time)


def load_data(infer_data, hparams=None):
  """Load inference data."""
  inference_data = infer_data.splitlines()

  if hparams and hparams.inference_indices:
      inference_data = [inference_data[i] for i in hparams.inference_indices]

  return inference_data


# def get_model_creator(hparams):
#   """Get the right model class depending on configuration."""
#   if (hparams.encoder_type == "gnmt" or
#       hparams.attention_architecture in ["gnmt", "gnmt_v2"]):
#     model_creator = gnmt_model.GNMTModel
#   elif hparams.attention_architecture == "standard":
#     model_creator = attention_model.AttentionModel
#   elif not hparams.attention:
#     model_creator = nmt_model.Model
#   else:
#     raise ValueError("Unknown attention architecture %s" %
#                      hparams.attention_architecture)
#   return model_creator
#
#
# def start_sess_and_load_model(infer_model, ckpt_path):
#   """Start session and load model."""
#   sess = tf.Session(
#       graph=infer_model.graph, config=utils.get_config_proto())
#   with infer_model.graph.as_default():
#     loaded_infer_model = model_helper.load_model(
#         infer_model.model, ckpt_path, sess, "infer")
#   return sess, loaded_infer_model

# ThanhNT58 chỉnh lại, 2 hàm trên viết thành 1 hàm bên dưới

session_pool_size = 1
preloaded_sessions = Queue(session_pool_size)
def preload_infer_model(hparams, ckpt):
    global preloaded_infer_model
    global preloaded_session
    global loaded_infer_model
    print("===================================================preload infer model=====================")
    if (hparams.encoder_type == "gnmt" or
          hparams.attention_architecture in ["gnmt", "gnmt_v2"]):
        model_creator = gnmt_model.GNMTModel
    elif hparams.attention_architecture == "standard":
        model_creator = attention_model.AttentionModel
    elif not hparams.attention:
        model_creator = nmt_model.Model
    else:
        raise ValueError("Unknown attention architecture %s" % hparams.attention_architecture)
    for i in list(range(session_pool_size)):
        preloaded_infer_model = model_helper.create_infer_model(model_creator, hparams, None)
        preloaded_session = tf.InteractiveSession(graph=preloaded_infer_model.graph, config=utils.get_config_proto())
        loaded_infer_model = model_helper.load_model(preloaded_infer_model.model, ckpt, preloaded_session, "infer")

        preloaded_sessions.put({ 'infer_model': preloaded_infer_model, 'session': preloaded_session, 'loaded_infer_model': loaded_infer_model})


def inference(ckpt_path,
              infer_data,
              hparams,
              jobid=0,
              scope=None):
  """Perform translation."""
  # if hparams.inference_indices:
  #   assert num_workers == 1

  # model_creator = get_model_creator(hparams)
  # infer_model = model_helper.create_infer_model(model_creator, hparams, scope)
  # sess, loaded_infer_model = start_sess_and_load_model(infer_model, ckpt_path)

  # ThanhNT58 sua
  global preloaded_sessions
  preloaded_session = preloaded_sessions.get()
  transformed_infer_data = load_data(infer_data, hparams)
  result = single_worker_inference(
      preloaded_session,
      ckpt_path,
      transformed_infer_data,
      hparams)
  preloaded_sessions.put(preloaded_session)
  return result


def single_worker_inference(preloaded_session,
                            ckpt,
                            infer_data,
                            hparams):
  """Inference with a single worker."""
  # output_infer = inference_output_file

  # Read data
  # infer_data = load_data(inference_input_file, hparams)

  sess = preloaded_session['session']
  infer_model = preloaded_session['infer_model']
  loaded_infer_model = preloaded_session['loaded_infer_model']

  sess.run(
      infer_model.iterator.initializer,
      feed_dict={
          infer_model.src_placeholder: infer_data,
          infer_model.batch_size_placeholder: hparams.infer_batch_size
      })
  # Decode
  utils.print_out("# Start decoding")
  if hparams.inference_indices:
      return _decode_inference_indices(
          loaded_infer_model,
          sess,
          inference_indices=hparams.inference_indices,
          tgt_eos=hparams.eos,
          subword_option=hparams.subword_option)
  else:
      return nmt_utils.decode(
          "infer",
          loaded_infer_model,
          sess,
          ref_file=None,
          metrics=hparams.metrics,
          subword_option=hparams.subword_option,
          beam_width=hparams.beam_width,
          tgt_eos=hparams.eos)


def multi_worker_inference(sess,
                           infer_model,
                           loaded_infer_model,
                           inference_input_file,
                           inference_output_file,
                           hparams,
                           num_workers,
                           jobid):
  """Inference using multiple workers."""
  assert num_workers > 1

  final_output_infer = inference_output_file
  output_infer = "%s_%d" % (inference_output_file, jobid)
  output_infer_done = "%s_done_%d" % (inference_output_file, jobid)

  # Read data
  infer_data = load_data(inference_input_file, hparams)

  # Split data to multiple workers
  total_load = len(infer_data)
  load_per_worker = int((total_load - 1) / num_workers) + 1
  start_position = jobid * load_per_worker
  end_position = min(start_position + load_per_worker, total_load)
  infer_data = infer_data[start_position:end_position]

  with infer_model.graph.as_default():
    sess.run(infer_model.iterator.initializer,
             {
                 infer_model.src_placeholder: infer_data,
                 infer_model.batch_size_placeholder: hparams.infer_batch_size
             })
    # Decode
    utils.print_out("# Start decoding")
    nmt_utils.decode_and_evaluate(
        "infer",
        loaded_infer_model,
        sess,
        output_infer,
        ref_file=None,
        metrics=hparams.metrics,
        subword_option=hparams.subword_option,
        beam_width=hparams.beam_width,
        tgt_eos=hparams.eos,
        num_translations_per_input=hparams.num_translations_per_input,
        infer_mode=hparams.infer_mode)

    # Change file name to indicate the file writing is completed.
    tf.gfile.Rename(output_infer, output_infer_done, overwrite=True)

    # Job 0 is responsible for the clean up.
    if jobid != 0: return

    # Now write all translations
    with codecs.getwriter("utf-8")(
        tf.gfile.GFile(final_output_infer, mode="wb")) as final_f:
      for worker_id in range(num_workers):
        worker_infer_done = "%s_done_%d" % (inference_output_file, worker_id)
        while not tf.gfile.Exists(worker_infer_done):
          utils.print_out("  waiting job %d to complete." % worker_id)
          time.sleep(10)

        with codecs.getreader("utf-8")(
            tf.gfile.GFile(worker_infer_done, mode="rb")) as f:
          for translation in f:
            final_f.write("%s" % translation)

      for worker_id in range(num_workers):
        worker_infer_done = "%s_done_%d" % (inference_output_file, worker_id)
        tf.gfile.Remove(worker_infer_done)
