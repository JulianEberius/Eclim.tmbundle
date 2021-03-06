import os
import sys
import subprocess

bundle_lib_path = os.environ['TM_BUNDLE_SUPPORT'] + '/lib'
sys.path.insert(0, bundle_lib_path)

tm_support_path = os.environ['TM_SUPPORT_PATH'] + '/lib'
if tm_support_path not in sys.path:
    sys.path.insert(0, tm_support_path)

from tm_helpers import to_plist, from_plist, current_word

__all__ = ('TM_DIALOG', 'TM_DIALOG2', 'tooltip', 'register_completion_images', 
    'current_identifier', 'identifier_before_dot', 'completion_popup', 
    'call_dialog', 'get_input', 'caret_position', 'find_unindexed_files', 'from_without_import')

TM_DIALOG = os.environ['DIALOG_1']
TM_DIALOG2 = os.environ['DIALOG']

def tooltip(text):
    options = {'text':str(text)}
    call_dialog(TM_DIALOG2+" tooltip", options)

def register_completion_images():
    icon_dir = os.environ['TM_BUNDLE_SUPPORT'] + '/icons'
    
    images = {
        "function"   : icon_dir+"/Function.png",
        "instance" : icon_dir+"/Property.png",
        "class"   : icon_dir+"/Class.png",
        "module"    : icon_dir+"/Module.png",
        "None"    : icon_dir+"/None.png",
    }
    call_dialog(TM_DIALOG2+" images", {'register' : images})

def current_identifier():
    return current_word(r"[A-Za-z_0-9]*")

def identifier_before_dot():
    if 'TM_CURRENT_WORD' not in os.environ:
        os.environ['TM_CURRENT_WORD'] = os.environ.get('TM_CURRENT_LINE')
    
    word = current_word(r"^[\.A-Za-z_0-9]*", direction='left')
    if word:
        return word[:-1]
    return ""
    
def completion_popup(proposals):
    #register_completion_images()
    command = TM_DIALOG2+" popup"
    word = current_identifier()
    if word:
        command += " --alreadyTyped "+word
       
    options = [dict([['display',p.name],
                    ['image', p.type if p.type else "None"],
                    ])
                    for p in proposals]
    call_dialog(command, {'suggestions' : options})

def completion_popup_with_snippet(proposals):
    #register_completion_images()
    # tricking TM_DIALOG into just inserting the snippet, but not the
    # displayed name... do not ask further.
    prefix = "." * max([len(p.display) for p in proposals])
    command = TM_DIALOG2+" popup --staticPrefix "+prefix
    
    word = current_identifier()
    if word:
        command += " --alreadyTyped "+word
       
    options = [dict([['display',p.name], 
                    ['image', p.type if p.type else "None"],
                    ['insert', p.insert]
                    ])
                    for p in proposals]
    call_dialog(command, {'suggestions' : options})

        
def call_dialog(command, options=None, shell=True):
    # command += " --suggestions '(%s)'" % to_plist(options)
    popen = subprocess.Popen(
                 command,
                 stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=shell)
    # options = None
    if options:
        out, _ = popen.communicate(to_plist(options))
    else:
        out, _ = popen.communicate()
    return out
    
def get_input(title="Input",default=""):
    if os.environ.get('TM_RopeMate_HUD', False):
        nib = os.environ['TM_BUNDLE_SUPPORT']+"/bin/input_hud"
    else:
        nib = os.environ['TM_BUNDLE_SUPPORT']+"/bin/input"
    out = call_dialog([TM_DIALOG, '-cm', nib], {'title':title, 'result':default}, False)
    if not out:
        return None
    return from_plist(out).get('result', None)

def caret_position(code):
    line_number = int(os.environ['TM_LINE_NUMBER'])
    line_index = int(os.environ['TM_LINE_INDEX'])
    pos = 0
    # find <line_number> line endings and add line_index to get offset into file
    for i in range(line_number-1):
        pos = code.find("\n",pos)+1
    offset = pos + line_index
    return offset