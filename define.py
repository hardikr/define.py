#!/usr/bin/env python

import re
import json
import sys
import urllib2

if len(sys.argv)==1:
  print 'Please tell me a word to define.\nUsage: python define.py vertigo'
  exit(0)

r = urllib2.urlopen("http://www.google.com/dictionary/json?callback=a&sl=en&tl=en&q="+sys.argv[1])
res = r.read()

prefix = 'a('
suffix = ',200,null)'

if res.startswith(prefix) and res.endswith(suffix):
  res = res[len(prefix):-len(suffix)]

res = re.sub(r'\\x3[\w]*\\x3e([\w]*)',r'\1',res)
res = re.sub(r'([\w]*)\\x3c/b\\x3e',r'\1',res)
res = re.sub(r'\\x3c/em\\x3e','',res)
res = re.sub(r'\\x27[\w]','',res)

res = json.loads(res)

try:
  for i in xrange(len(res['primaries'][0]['entries'])):
    print str(i+1)+") "+res['primaries'][0]['entries'][i]['terms'][0]['text']
except KeyError as e:
  print "Sorry. No definition found."