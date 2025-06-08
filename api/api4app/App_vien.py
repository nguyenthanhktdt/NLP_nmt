import time
from framework.utils.sophia_utility import SOPHIAUtility
from nmt import nmt as predict
import settings
from framework.infer import vien_infer


class AppController_vien(object):
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance(src_lang, target_lang):
        """ Static access method. """
        if AppController_vien.__instance == None:
            AppController_vien(src_lang, target_lang)
        return AppController_vien.__instance

    def __init__(self, src_lang, target_lang):
        """ Virtually private constructor. """
        self.src_lang = src_lang
        self.target_lang = target_lang
        if AppController_vien.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.load_vocab(settings.vocab_file_preprocess)
            # preload hparams
            predict.preload_hparams(settings.out_dir, settings.chk_path,
                                    settings.vocab_file_preprocess)
        AppController_vien.__instance = self


    @classmethod
    def nmt_translate_sent(self, nmt_sent, src_lang, vocab_soure):

        vocab_file = settings.vocab_file_preprocess

        # ======= pre process==============================
        source_sents = vien_infer.ViEnInfer.split_sentence(nmt_sent)

        # ======= call function translate =================
        result = []
        for i in range(len(source_sents)):
            SOPHIAUtility.write_log("-----------------pre_process_sent:")
            out_lines, origin_lines, dic_unk_replace, line_none_lower = vien_infer.ViEnInfer.pre_process_sent(
                source_sents[i])
            source_non_lower = str(line_none_lower).split(" ")
            source_lower = [s.lower() for s in source_non_lower]
            line_for_predict = "".join(out_lines)
            # ======= call function translate =================
            SOPHIAUtility.write_log("-----------------run_predict:")
            output_lines = predict.run_predict(
                check_point=settings.chk_path,
                infer_data=line_for_predict,
                vocab_file=vocab_file).split("\n")
            # ======pos process================================
            SOPHIAUtility.write_log("-----------------pos_process_sent:")
            pre_result = vien_infer.ViEnInfer.pos_process_sent(origin_lines, output_lines, dic_unk_replace,
                                                               source_sents[i])
            # ====== process latinh words =========================
            line_ja_out = []
            pre_result_lower = pre_result.lower().split(" ")
            for j in range(len(pre_result_lower)):
                if pre_result_lower[j] in source_lower:
                    position = source_lower.index(pre_result_lower[j])
                    line_ja_out.append(source_non_lower[position])
                else:
                    line_ja_out.append(pre_result_lower[j])
            pre_result_fix_latinh = " ".join(line_ja_out)
            line_stand = SOPHIAUtility.format_output_javi(pre_result_fix_latinh)
            line_stand = line_stand[0].upper() + line_stand[1:]
            line_stand = line_stand.strip()
            result.append(line_stand)
            SOPHIAUtility.write_log("-----------------end:")
        result_final = " ".join(result)
        result_final = result_final[0].upper() + result_final[1:]

        return result_final


