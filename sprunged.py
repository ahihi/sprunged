#!/usr/bin/env python
from __future__ import print_function
import os
import shlex
import subprocess as sub
import sys
import tempfile
import urllib
import urllib2

def abort():
    print(u"Aborted.", file = sys.stderr)
    sys.exit(1)        

editor = os.environ.get("EDITOR")
if not editor:
    print(u"No $EDITOR is set. Using ed, the standard!", file = sys.stderr)
    editor = "/bin/ed"
editor_cmd = shlex.split(editor)

try:
    the_file = open(sys.argv[1], "rb")
except IndexError:
    the_file = tempfile.NamedTemporaryFile("rb")
with the_file:
    editor_cmd.append(the_file.name)
    exit_code = sub.call(editor_cmd, stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr)
    if exit_code != 0:
        abort()
    text = the_file.read()
    if len(text) == 0:
        abort()
    data = urllib.urlencode({"sprunge": text})
    response = urllib2.urlopen("http://sprunge.us/", data)
    print(response.read().strip())
