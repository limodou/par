#! /usr/bin/env python
#coding=utf-8
from pyPEG import *
import re
import types

class WikiGrammar(dict):
    def __init__(self):
        peg, self.root = self._get_rules()
        self.update(peg)
        
    def _get_rules(self):
        #basic
        def ws(): return re.compile(r'\s+')
        def space(): return re.compile(r'[ \t]+')
        def eol(): return re.compile(r'\r\n|\r|\n')
        def seperator(): return re.compile(r'[\.,!?\-$ \t\r\n\^]')
    
        #hr
        def hr(): return 0, ws, re.compile(r'\-{4,}'), 0, space, eol
    
        #paragraph
        def blankline(): return 0, space, eol
        def identifer(): return re.compile(r'[a-zA-Z_][a-zA-Z_0-9]*', re.U)
        def literal(): return re.compile(r'u?r?"[^"\\]*(?:\\.[^"\\]*)*"', re.I|re.DOTALL)
        def literal1(): return re.compile(r"u?r?'[^'\\]*(?:\\.[^'\\]*)*'", re.I|re.DOTALL)
        def escape_string(): return '\\', re.compile(r'.')
        def op_string(): return re.compile(r'\*|_|~~|\^|,,|`')
        def op(): return [(-1, seperator, op_string), (op_string, -1, seperator)]
        def string(): return re.compile(r'[^\\\*_\^~ \t\r\n`,]+', re.U)
        def code_string(): return pre_begin, re.compile(r'[^\}\r\n$]*'), pre_end
        def default_string(): return re.compile(r'\S+', re.U)
        def word(): return [space, literal, literal1, escape_string, code_string, op, string, default_string]
        def words(): return -2, word
        def line(): return words, eol
        def paragraph(): return -2, line, -2, blankline
    
        #pre
        def pre_begin(): return re.compile(r'\{\{\{')
        def pre_end(): return re.compile(r'\}\}\}')
        def pre(): return pre_begin, 0, space, eol, re.compile(r'[^\}]*', re.M), pre_end
    
        #subject
        def section_text(): return re.compile(r'[^=]+', re.U)
        def subject(): return re.compile(r'\s*.*'), eol, re.compile(r'(?:=|-){4,}'), -2, eol
        def section1(): return '=', section_text, '=', -2, eol
        def section2(): return '==', section_text, '==', -2, eol
        def section3(): return '===', section_text, '===', -2, eol
        def section4(): return '====', section_text, '====', -2, eol
        def section5(): return '=====', section_text, '=====', -2, eol
        def section6(): return '======', section_text, '======', -2, eol
        def section(): return [section4, section3, section2, section1]
    
        #article
        def article(): return -1, [hr, subject, section, pre, paragraph]
    
        peg_rules = {}
        for k, v in ((x, y) for (x, y) in locals().items() if isinstance(y, types.FunctionType)):
            peg_rules[k] = v
        return peg_rules, article
    
    def parse(self, text, root=None, skipWS=False, **kwargs):
        return parseLine(text, root or self.root, skipWS=skipWS, **kwargs)
        
class SimpleVisitor(object):
    def visit(self, nodes):
        buf = []
        for node in nodes:
            if isinstance(node, (str, unicode)):
                buf.append(node)
            else:
                method = getattr(self, 'visit_' + node.__name__, None)
                if method:
                    buf.append(method(node))
                else:
                    if isinstance(node.what, (str, unicode)):
                        buf.append(node.what)
                    else:
                        buf.append(self.visit(node.what))
        return ''.join(buf)

default_template="""<!DOCTYPE html>
<html>
<head>
<meta charset="utf8">
<title>%(subject)s</title>
<body>
%(body)s</body>
</head>
</html>
"""

class WikiHtmlVisitor(SimpleVisitor):
    op_maps = {
        '*':['<b>', '</b>'],
        '_':['<i>', '</i>'],
        '~~':['<span style="text-decoration: line-through">', '</span>'],
        '^':['<sup>', '</sup>'],
        ',,':['<sub>', '</sub>'],
        '`':['<code>', '</code>'],
    }
    
    def __init__(self, template=None):
        self._template = template or default_template
        self.title = 'Untitled'
        self.sections = []
        self.ops = {}
        
    def __str__(self):
        return self.template()
    
    def template(self, node):
        body = self.visit(node)
        return self._template % {'subject':self.subject, 'body':body}
            
    def visit_subject(self, node):
        self.subject = node[0].strip()
        return '<h1>' + self.subject + '</h1>\n'
    
    def visit_section1(self, node):
        self.sections.append((1, node[0].text))
        return '<h1>' + node[0].text + '</h1>\n'
    
    def visit_section2(self, node):
        self.sections.append((2, node[0].text))
        return '<h2>' + node[0].text + '</h2>\n'

    def visit_section3(self, node):
        self.sections.append((3, node[0].text))
        return '<h3>' + node[0].text + '</h3>'

    def visit_section4(self, node):
        self.sections.append((4, node[0].text))
        return '<h4>' + node[0].text + '</h4>\n'
    
    def visit_section5(self, node):
        self.sections.append((5, node[0].text))
        return '<h5>' + node[0].text + '</h5>\n'

    def visit_section6(self, node):
        self.sections.append((6, node[0].text))
        return '<h6>' + node[0].text + '</h6>\n'

    def visit_paragraph(self, node):
        return '<p>' + self.visit(node).rstrip() + '</p>\n'
    
    def visit_op_string(self, node):
        c = node.text
        index = (self.ops.setdefault(c, 1) + 1)%2
        self.ops[c] = index
        return self.op_maps[c][index]
        
    def visit_escape_string(self, node):
        return node[0]
    
    def visit_pre(self, node):
        return '<pre>'+node[1].text+node[2]+'</pre>'
    
    def visit_code_string(self, node):
        return '<code>'+node[1]+'</code>'
    
    def visit_hr(self, node):
        return '<hr/>'