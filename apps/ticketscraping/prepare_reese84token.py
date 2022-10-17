import os
import re
import json
import requests
import subprocess
from . import constants


def getReese84Token()->tuple[str, int]:
    def readFileContentToString(filename):
        f = open(filename, 'r')
        content = f.read()
        f.close()
        return content

    # fetch the javascript that generates the reese84
    antibot_js_code_full = requests.get(constants.ANTIBOT_JS_CODE_URL).text

    # trim the code to the function that is only used
    match_obj = re.search(constants.FN_MATCHING_REGEX, antibot_js_code_full)
    if not match_obj:
        raise Exception('reese84 manufacture fails')
    start, end = match_obj.span()
    antibot_js_code_trim = antibot_js_code_full[start:end]

    # inject the code to the javascript
    injector_js_code_loc = os.path.join(
        os.path.dirname(__file__), constants.INJECTOR_LOCATION)
    injector_header_js_code_loc = os.path.join(os.path.dirname(
        __file__), constants.INJECTOR_HEADER_LOCATION)
    injector_js_code, injector_header_js_code = readFileContentToString(
        injector_js_code_loc), readFileContentToString(injector_header_js_code_loc)
    runnable_js_code = injector_header_js_code + \
        antibot_js_code_trim + injector_js_code

    # save the runnable js code
    runnable_file_loc = os.path.join(os.path.dirname(
        __file__), constants.RENNABLE_FILENAME)
    runnable_file = open(runnable_file_loc, "w")
    runnable_file.write(runnable_js_code)
    runnable_file.close()

    # run the js code using local node.js
    res = subprocess.run(
        ["node", runnable_file_loc], capture_output=True)
    token_str = res.stdout

    # produce the reese84 object
    token = json.loads(token_str)

    # invoke the get token api to get the reese84 token
    token_json_res = requests.post(
        constants.TOKEN_INTERROGATION_URL, headers=constants.BASIC_REQ_HEADER, json=token)
    json_obj = token_json_res.json()
    return json_obj['token'], json_obj['renewInSec']
