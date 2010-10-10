#!/usr/bin/env python
import sys, subprocess, re
import eclim
from util import caret_position, completion_popup, completion_popup_with_snippet

class ImportProposal(object):
    def __init__(self, name, insert=None, type="None"):
        self.name = name
        self.display = name
        self.insert = insert
        self.type = "None"

def call_eclim(project, file, offset, shell=True):
    eclim.update_java_src(project, file)

    complete_cmd = "$ECLIM -command java_complete \
                            -p %s \
                            -f %s \
                            -o %i \
                            -e utf-8 \
                            -l compact" % (project, file, offset)
    popen = subprocess.Popen(
        complete_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=shell)
    out, _ = popen.communicate()
    return out

def to_proposals(eclim_output):
    results = [] 
    with_snippets = False
    for l in eclim_output.split("\n"):
        if not l: continue
        parts = l.split("|")

        if parts[1]:
            prop = ImportProposal(parts[1])
            results.append(prop)
        else:
            variants = parts[3].split("<br/>")
            param_lists = [re.search(r'\((.*)\)', v).group(1) for v in variants]
            props = []
            for idx, pl in enumerate(param_lists):
                params = [par.split(" ")[-1] for par in pl.split(", ")]
                insert = ", ".join(["${%i:%s}" % (i,s) 
                                    for i,s in 
                                    zip(range(1,len(params)+1), params)
                                    ])
                props.append(ImportProposal(variants[idx], insert))
                with_snippets = True
            results.extend(props)
        
    return results, with_snippets
    
project, file = eclim.get_context()
code = sys.stdin.read()
pos = caret_position(code)

proposals, with_snippets = to_proposals(call_eclim(project, file, pos))
if with_snippets:
    completion_popup_with_snippet(proposals)
else:
    completion_popup(proposals)