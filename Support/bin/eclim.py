#!/usr/bin/env python
import sys, os, subprocess, re
import plistlib
from xml.etree import ElementTree
from util import tooltip

DIALOG = os.environ['DIALOG_1']
JAVA_BUILD_ERRORS_WINDOW = "Java Build Errors"

def call_eclim(cmd):
    popen = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    out, err = popen.communicate()
    if err or "Connection refused" in out:
        error_msg = 'Error connecting to Eclim server: '
        if out: error_msg += out
        if err: error_msg += err
        tooltip(error_msg)
        sys.exit()
    return out

def get_context():
    project, file = None, None
    
    project_dir = os.environ.get('TM_PROJECT_DIRECTORY', None)
    file_path = os.environ['TM_FILEPATH']
    if project_dir:
        project_file = os.path.join(project_dir, '.project')
        project_desc = ElementTree.XML(open(project_file).read())
        project = project_desc.find('name').text
        file = os.path.relpath(file_path, project_dir)
        
    return project, file

def update_java_src(project, file):
    update_cmd = '$ECLIM -command java_src_update \
                        -p %s \
                        -f %s \
                        -v' % (project, file)
    out = call_eclim(update_cmd)
    return out

def refresh_file(project, file):
    refresh_cmd = '$ECLIM -command project_refresh_file \
                        -p %s \
                        -f %s ' % (project, file)
    out = call_eclim(refresh_cmd)
    return out

def get_problems(project):
    get_problems_cmd = '$ECLIM -command problems \
                        -p %s' % project
    out = call_eclim(get_problems_cmd)
    return out
    
def format_problems(problems):
    result = ""
    for pr in problems.split("\n"):
        if not pr: continue
        parts = pr.split("|")
        result += parts[1].replace(" col ",":")+" "
        result += parts[2]
    return result

def problems_to_dict(problems):
    results = {"errors":[]}
    for pr in problems.split("\n"):
        if not pr: continue
        parts = pr.split("|")
        _file = os.path.split(parts[0])[1]
        line = parts[1].split(" col ")[0]
        message = parts[2]
        results["errors"].append({"file":_file, "line":line, "message":message})
    return results

def close_error_window(window_token):
    cmd = DIALOG + " -x "+window_token
    popen = subprocess.Popen(
        cmd, stdin=None, stdout=None,shell=True)
    popen.communicate()

def show_error_window(problems):
    ''' prints out the window token returned by tm_dialog to the 
    calling TM command (or -1 indicating failure)'''
    if not problems['errors']:
        print "-1"
        return
    cmd = DIALOG + " -a /Users/ebi/dev/tm_dialog_test.nib"
    popen = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    out, err = popen.communicate(plistlib.writePlistToString(problems))
    print out
    
def update_error_window(window_token, problems):
    if not problems['errors']:
        close_error_window(window_token)
    else:
        cmd = DIALOG + " -t "+window_token
        popen = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
        out, err = popen.communicate(plistlib.writePlistToString(problems))

def display_problems(problems):
    cmd = DIALOG + " -l"
    popen = subprocess.Popen(
        cmd, stdin=None, stdout=subprocess.PIPE,shell=True)
    out, err = popen.communicate()
    if JAVA_BUILD_ERRORS_WINDOW in out:
        windows = out.splitlines()
        for w in windows:
            m1 = re.match(r'(\d*) \((.*)\)',w)
            if m1.group(2) == JAVA_BUILD_ERRORS_WINDOW:
                token = m1.group(1)
        update_error_window(token, problems)
    else:
        show_error_window(problems)

if __name__ == '__main__':
    
    if sys.argv[1] == '--update':
        project, file = get_context()
        problems = update_java_src(project, file)
        #tooltip(problems)
        refresh_file(project, file)
        display_problems(problems_to_dict(problems))
        