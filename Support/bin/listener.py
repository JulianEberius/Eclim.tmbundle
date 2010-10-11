#!/usr/bin/env python

import sys, os, subprocess
import plistlib, urllib
import eclim

DIALOG = os.environ['DIALOG_1']

while True:
    cmd1 = DIALOG + " -w "+sys.argv[1]
    popen = subprocess.Popen(
        cmd1, stdin=None, stdout=subprocess.PIPE,shell=True)
    out1, err1 = popen.communicate()

    msg = plistlib.readPlistFromString(out1)
    if "returnArgument" not in msg:
        eclim.close_window(sys.argv[1])
        sys.exit()
    
    url =  'txmt://open?url=file://%s&line=%s' % (
            urllib.quote(os.environ['TM_FILEPATH']), msg['returnArgument'] )
    
    cmd2 = "open \"%s\"" % url
    popen = subprocess.Popen(
        cmd2, stdin=None, stdout=None,shell=True)
    popen.communicate()
