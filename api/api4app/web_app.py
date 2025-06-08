import sys
import time
import traceback

start_time = time.time()
sys.path.append('../../framework/utils')
sys.path.append('../../nmt')
from flask import Flask, request, g
import os
import html  
import json
import time

from api.api4app.AppController_vien import AppController_vien
from framework.utils.sophia_utility import SOPHIAUtility

import settings
from framework.utils.Logger import logged

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
def initRouteWithPrefix(route_function, prefix='', mask='{0}{1}'):
    '''
      Defines a new route function with a prefix.
      The mask argument is a `format string` formatted with, in that order:
        prefix, route
    '''

    def newroute(route, *args, **kwargs):
        '''New function to prefix the route'''
        return route_function(mask.format(prefix, route), *args, **kwargs)

    return newroute


app = Flask(__name__)

if os.environ.get('BASE_URL') is not None:
    app = Flask(__name__, static_url_path=os.environ['BASE_URL'])
    app.route = initRouteWithPrefix(app.route, os.environ['BASE_URL'])
else:
    app = Flask(__name__, static_url_path="")


@app.before_request
def before_request():
    g.request_start_time = time.time()


@app.teardown_request
def teardown_request(exception=None):
    print("From before_request to teardown_request: %.2fms" % ((time.time() - g.request_start_time) * 1000))


@app.route("/", defaults={"path": ""}, methods=['GET', 'POST'])
@app.route("/<path:path>", methods=['GET', 'POST'])
def do_upload_file(path):
    if request.method == 'GET':
        return "hello, world" 
    if request.method == 'POST':
        SOPHIAUtility.write_log("Start request:")
        try:
            req = request.get_json()
            for i in range(len(req["translations"])):
                SOPHIAUtility.write_log("Start translating:")
                check = req["translations"][i].get("tb")
 
                res = translate(req["translations"][i]["node_source"], req["translations"][i]["node_src_lang"], req["translations"][i]["node_target_lang"], None)
                req["translations"][i]["node_result"] = res
            SOPHIAUtility.write_log("End request.")
            return json.dumps(req, ensure_ascii=False)

        except Exception as inst:
            trace_back_str = "".join(traceback.format_tb(inst.__traceback__))
            SOPHIAUtility.write_log(trace_back_str, True)
            SOPHIAUtility.write_log(inst, True)

vocab_source = SOPHIAUtility.load_vocab_source(settings.vocab_file_preprocess)

@logged()
def translate(sentence, src_lang, target_lang, tb=None):
    SOPHIAUtility.write_log("len of input = " + str(len(sentence)))
    if tb != None and len(tb) > 0:
        dict_tb_in = tb[0]
    else:
        dict_tb_in = {}
    
    if src_lang=='vi' and target_lang == 'en':
        return html.unescape(AppController_vien.getInstance(src_lang, target_lang).nmt_translate_sent(sentence, src_lang, vocab_source))

if __name__ == '__main__':

    app.run(debug=False, host='127.0.0.1', port=1990, threaded=True)
