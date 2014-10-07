'''
Ignore the string which begins with '#',
and the string closed with '"' will not be substitute.

 >>> print string
 tttt"aaaa#qqqq
 #qq"qq
 aaaa"====
 >>> print re.sub(patt, f, string, flags=flags)
 ===="aaaa#qqqq
 #qq"qq
 aaaa"====
 >>> print re.sub(patt, f, '"asdfzxcv"', flags=flags)
 "asdfzxcv"
 >>> print re.sub(patt, f, '#..."---"...', flags=flags)
 #..."---"...

Try to implement patten and sub function ``f``.
'''

import re

patt = r'([^"#]*)("(?:[^"#]*(?:#.*$)?)*")?(#.*$)?'
string = 'tttt"aaaa#qqqq\n#qq"qq\naaaa"===='
flags = re.M | re.S

def f(m):
  return (m.group(1) and '====') + (m.group(2) or '') + (m.group(3) or '')
