#!/usr/bin/env python
import os, sys

import eclim
import util
from util import caret_position, current_identifier


def call_eclim(project, file, length, offset, new_name): 
    '''
java_refactor_rename -p com.sap.research.amc.matchingprocess.dynamic -f
src/com/sap/research/amc/matchingprocess/dynamic/DynamicProcessRunner.java -o
1085 -e utf-8 -l 12 -n nag 
    ''' 
    eclim.update_java_src(project, file)
    rename_cmd = "$ECLIM -command java_refactor_rename \
                -p %s \
                -f %s \
                -o %i \
                -e utf-8 \
                -l %i \
                -n %s" % (project, file, offset, length, new_name)
    out = eclim.call_eclim(rename_cmd)
    return out
    
def rename_command():
    project, file = eclim.get_context()    
    # we cannot read the code from TM via stdin, as it will not have 
    # the correct line endings when editing windows files (it will just have \n)
    #code = sys.stdin.read()

    # so we read from disk
    with open(os.environ["TM_FILEPATH"]) as f:
        code = f.read()
    pos = caret_position(code)
    identifier = current_identifier()
    pos = code.find(identifier, pos-len(identifier))
    
    new_name = util.get_input(default=identifier,title="Enter new name")
    
    call_eclim(project, file, len(identifier), pos, new_name)

if __name__ == '__main__':
    if sys.argv[1] == '--rename':
        out = rename_command()
        #print out
