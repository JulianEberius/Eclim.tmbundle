#!/usr/bin/env python
import sys, os, subprocess
from xml.etree import ElementTree

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
                        -p com.sap.research.amc.matchingprocess.dynamic \
                        -f src/com/sap/research/amc/matchingprocess/dynamic/rules/RuleRegistry.java \
                        -v'
    popen = subprocess.Popen(
        update_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, err = popen.communicate()
    return out

def refresh_file(project, file):
    update_cmd = '$ECLIM -command project_refresh_file \
                        -p com.sap.research.amc.matchingprocess.dynamic \
                        -f src/com/sap/research/amc/matchingprocess/dynamic/rules/RuleRegistry.java'
    popen = subprocess.Popen(
        update_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, err = popen.communicate()
    return out

def get_problems(project):
    update_cmd = '$ECLIM -command problems \
                        -p com.sap.research.amc.matchingprocess.dynamic'
    popen = subprocess.Popen(
        update_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    out, _ = popen.communicate()
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