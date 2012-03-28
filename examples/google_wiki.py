#coding=utf8

import sys
sys.path.insert(0, '..')
from par import WikiGrammar, WikiHtmlVisitor, SimpleVisitor

text = """
Title
=============

=中文  aaaa=

_italic_ 
*bold*
`code`
{{{code}}}
^super^script
,,sub,,script
~~strikeout~~

{{{
code line
}}}

-----

_*bold* in italics_
*_italics_ in bold*
*~~strike~~ works too*
~~as well as _this_ way round~~

"""

g = WikiGrammar()

result, rest = g.parse(text, skipWS=False)
#result, rest = g.parse('''{{{
#code line
#}}}
#''', g['pre'], skipWS=False)
print result
print '--', rest, '--'
#print result[0].text
#print SimpleVisitor().visit(result).encode('gbk')
print WikiHtmlVisitor().template(result)
