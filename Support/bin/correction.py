#!/usr/bin/env python
import os, re, sys, subprocess, plistlib

import eclim
from util import caret_position

def call_eclim(project, file, line, offset, applied_correction=None):
    eclim.update_java_src(project, file)

    correct_cmd = "$ECLIM -command java_correct \
                -p %s \
                -f %s \
                -l %i \
                -o %i \
                -e utf-8 " % (project, file, line, offset)
    if applied_correction != None:
        correct_cmd += " -a %i" % (applied_correction)
    
    out = eclim.call_eclim(correct_cmd)
    return out
    
def show_corrections_window(corrections):
    options = {"corrections": [dict([("message",m),("number", x+1)]) 
                for x, m in enumerate(corrections)]}
    
    path = os.path.join(os.path.dirname(sys.argv[0]), "corrections.nib")
    cmd = eclim.DIALOG + ' -cm "' + path + '"'
    popen = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    out, err = popen.communicate(plistlib.writePlistToString(options))
    out =  plistlib.readPlistFromString(out)
    if "result" not in out:
        return None
    return int(out["result"]["returnArgument"])-1
    
def to_list(corrections):
    re1 = re.compile("^(\d+)\.\d+:(.*)")
    result = []
    
    corrections = corrections.splitlines()
    for l in corrections:
        match1 = re1.match(l)
        if match1:
            result.append(match1.group(2).strip())
    return result

def correction_command():
    project, file = eclim.get_context()    
    # we cannot read the code from TM via stdin, as it will not have 
    # the correct line endings when editing windows files (it will just have \n)
    #code = sys.stdin.read()

    # so we read from disk
    with open(os.environ["TM_FILEPATH"]) as f:
        code = f.read()
    pos = caret_position(code)
    line = int(os.environ['TM_LINE_NUMBER'])

    corrections = call_eclim(project, file, line, pos)
    corrections = to_list(corrections)
    if corrections:
        correction_to_apply = show_corrections_window(corrections)
    else: correction_to_apply = None
    if correction_to_apply != None:
        new_code = call_eclim(project, file, line, pos, correction_to_apply)
        if new_code:
            return new_code
    return code

if __name__ == '__main__':
    out = correction_command()
    print out
