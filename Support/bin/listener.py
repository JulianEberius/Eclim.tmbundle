#!/usr/bin/env python

import sys, os, subprocess
import plistlib, urllib
import eclim

DIALOG = os.environ['DIALOG_1']

while True:
    msg = None
    cmd1 = DIALOG + " -w "+sys.argv[1]
    popen = subprocess.Popen(
        cmd1, stdin=None, stdout=subprocess.PIPE,shell=True)
    out1, err1 = popen.communicate()
    
    try:
        msg = plistlib.readPlistFromString(out1)
    except Exception, e:
        sys.exit()

    if not msg:
        # could not connect to window
        sys.exit()
    
    if "returnArgument" not in msg:
        # the window was closed by the user
        eclim.close_error_window(sys.argv[1])
        sys.exit()

    # everything is fine, generate an URL for OSX's "open" command
    url =  'txmt://open?url=file://%s&line=%s' % (
            urllib.quote(os.environ['TM_FILEPATH']), msg['returnArgument'][0]['line'] )
    
    cmd2 = "open \"%s\"" % url
    popen = subprocess.Popen(
        cmd2, stdin=None, stdout=None,shell=True)
    popen.communicate()
