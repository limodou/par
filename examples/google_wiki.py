#coding=utf8

import sys
sys.path.insert(0, '..')
from par import WikiGrammar, WikiHtmlVisitor, SimpleVisitor

text = """
Title
=============

= Title1 =
== Title2 ==
=== Title3 ===
==== Title4 ====
===== Title5 =====
====== Title6 ======

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

|| *Test1* || aaaaa1||
|| Test2 || aaaaa2||
"""

g = WikiGrammar()

result, rest = g.parse(text, skipWS=False)
#result, rest = g.parse(''' Test1 ||''', g['table_column'], skipWS=False)

print result
print '======', rest
print result[0].render()
#print '--', rest, '--'
#print result[0].text
#print SimpleVisitor().visit(result).encode('gbk')
print WikiHtmlVisitor().template(result)

