#!/usr/bin/env python
import sys, os, subprocess
from xml.etree import ElementTree
from util import tooltip

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

if __name__ == '__main__':
    
    if sys.argv[1] == '--update':
        project, file = get_context()
        problems = update_java_src(project, file)
        refresh_file(project, file)
        print format_problems(problems)
        #print get_problems(project)