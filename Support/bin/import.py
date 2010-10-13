#!/usr/bin/env python
import sys, os, subprocess
import eclim
from util import tooltip

def call_eclim(project, identifier):
#    eclim.update_java_src(project, file)
    complete_cmd = "$ECLIM -command java_import \
                            -n %s \
                            -p %s" % (project, identifier)
    popen = subprocess.Popen(
        complete_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    class_name, err = popen.communicate()
    
    
    complete_cmd = "$ECLIM -command java_import_order \
                             -p %s" % project
    popen = subprocess.Popen(
         complete_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    order, err = popen.communicate()
    return class_name.strip(), order

def add_import(code, class_name, order):
    if class_name=="":
        tooltip("No class found")
    elif "\n" in class_name:
        tooltip("Exception: "+class_name)
    else:
        lines = code.split("\n")
        last_import_idx = 0
        for idx, l in enumerate(lines):
            if "{" in l: break
            if "import" in l: last_import_idx = idx
        doc = "\n".join(lines[:last_import_idx+1] + ["import "+class_name+";"] + lines[last_import_idx+1:])
        return doc
    return code
    
project, file = eclim.get_context()
code = sys.stdin.read()
word = os.environ["TM_CURRENT_WORD"]
class_name, order = call_eclim(project, word)
new_code = add_import(code, class_name, order)
print new_code
