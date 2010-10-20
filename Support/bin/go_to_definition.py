#!/usr/bin/env python
import os, subprocess, urllib

import eclim
from util import current_identifier, caret_position

def call_eclim(project, file, offset, ident_len, shell=True):
    eclim.update_java_src(project, file)

    go_to_cmd = "$ECLIM -command java_search \
                            -n %s \
                            -f %s \
                            -o %i \
                            -e utf-8 \
                            -l %i" % (project, file, offset, ident_len)
    out = eclim.call_eclim(go_to_cmd)
    return out
    
def to_list(locations):
    result = []
    
    locations = locations.splitlines()
    for l in locations:
        parts = l.split("|")
        l_def = {"file":parts[0],
                "line":parts[1].split(" col ")[0],
                "col":parts[1].split(" col ")[1]}
        result.append(l_def)
    return result

def go_to_location(loc):
    url =  'txmt://open?url=file://%s&line=%s&column=%s' % (
            urllib.quote(loc['file']), loc['line'], loc['col'] )
    
    cmd = "open \"%s\"" % url
    popen = subprocess.Popen(
        cmd, stdin=None, stdout=None,shell=True)
    popen.communicate()

def go_to_definition_command():
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

    locations = call_eclim(project, file, pos, len(identifier))
    locations = to_list(locations)
    if len(locations) == 1:
        go_to_location(locations[0])

if __name__ == '__main__':
    go_to_definition_command()
