#coding=utf8

import sys
sys.path.insert(0, '..')
from par import WikiGrammar, WikiHtmlVisitor, SimpleVisitor

text = """
Title
=============

=中文  aaaa=

as *df*
asd_fds_f

af
asdfs
ddsf

"""

g = WikiGrammar()

result, rest = g.parse(text, skipWS=False)
#result, rest = parseLine('asd', words, skipWS=False)
print result
print '--', rest, '--'
#print result[0].text
#print SimpleVisitor().visit(result).encode('gbk')
print WikiHtmlVisitor().visit(result)
