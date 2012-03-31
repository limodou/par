#! /usr/bin/env python
#coding=utf-8
from pyPEG import *
import re
import types

_ = re.compile

class WikiGrammar(dict):
    def __init__(self):
        peg, self.root = self._get_rules()
        self.update(peg)
        
    def _get_rules(self):
        #basic
        def ws(): return _(r'\s+')
        def space(): return _(r'[ \t]+')
        def eol(): return _(r'\r\n|\r|\n')
        def seperator(): return _(r'[\.,!?\-$ \t\r\n\^]')
    
        #hr
        def hr(): return 0, ws, _(r'\-{4,}'), 0, space, eol
    
        #paragraph
        def blankline(): return 0, space, eol
        def identifer(): return _(r'[a-zA-Z_][a-zA-Z_0-9]*', re.U)
        def literal(): return _(r'u?r?"[^"\\]*(?:\\.[^"\\]*)*"', re.I|re.DOTALL)
        def literal1(): return _(r"u?r?'[^'\\]*(?:\\.[^'\\]*)*'", re.I|re.DOTALL)
        def escape_string(): return '\\', _(r'.')
        def op_string(): return _(r'\*|_|~~|\^|,,|`')
        def op(): return [(-1, seperator, op_string), (op_string, -1, seperator)]
        def string(): return _(r'[^\\\*_\^~ \t\r\n`,]+', re.U)
        def code_string(): return pre_begin, _(r'[^\}\r\n$]*'), pre_end
        def default_string(): return _(r'\S+', re.U)
        def word(): return [space, literal, literal1, escape_string, code_string, op, string, default_string]
        def words(): return -2, word
        def line(): return words, eol
        def paragraph(): return -2, line, -2, blankline
    
        #pre
        def pre_begin(): return _(r'\{\{\{')
        def pre_end(): return _(r'\}\}\}')
        def pre(): return pre_begin, 0, space, eol, _(r'[^\}]*', re.M), pre_end
    
        #subject
        def title_text(): return _(r'.+(?= =)', re.U)
        def subject(): return _(r'\s*.*'), eol, _(r'(?:=|-){4,}'), -2, eol
        def title1(): return '= ', title_text, ' =', -2, eol
        def title2(): return '== ', title_text, ' ==', -2, eol
        def title3(): return '=== ', title_text, ' ===', -2, eol
        def title4(): return '==== ', title_text, ' ====', -2, eol
        def title5(): return '===== ', title_text, ' =====', -2, eol
        def title6(): return '====== ', title_text, ' ======', -2, eol
        def title(): return [title6, title5, title4, title3, title2, title1]
    
        #table
        def table_column(): return -2, [space, escape_string, code_string, op, _(r'[^\\\*_\^~ \t\r\n`,\|]+', re.U)], '||'
        def table_line(): return '||', -2, table_column, eol
        def table(): return -2, table_line
    
        #article
        def article(): return -1, [hr, subject, title, pre, table, paragraph]
    
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
                method = getattr(self, 'visit_' + node.__name__ + '_begin', None)
                if method:
                    buf.append(method(node))
                method = getattr(self, 'visit_' + node.__name__, None)
                if method:
                    buf.append(method(node))
                else:
                    if isinstance(node.what, (str, unicode)):
                        buf.append(node.what)
                    else:
                        buf.append(self.visit(node.what))
                method = getattr(self, 'visit_' + node.__name__ + '_end', None)
                if method:
                    buf.append(method(node))
                
        return ''.join(buf)

default_template="""<!DOCTYPE html>
<html>
<head>
<meta charset="utf8">
<title>%(title)s</title>
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
        self.titles = []
        self.ops = {}
        
    def __str__(self):
        return self.template()
    
    def template(self, node):
        body = self.visit(node)
        return self._template % {'title':self.title, 'body':body}
            
    def visit_subject(self, node):
        self.subject = node[0].strip()
        return '<h1>' + self.subject + '</h1>\n'
    
    def visit_title1(self, node):
        self.titles.append((1, node[0].text))
        return '<h1>' + node[0].text + '</h1>\n'
    
    def visit_title2(self, node):
        self.titles.append((2, node[0].text))
        return '<h2>' + node[0].text + '</h2>\n'

    def visit_title3(self, node):
        self.titles.append((3, node[0].text))
        return '<h3>' + node[0].text + '</h3>'

    def visit_title4(self, node):
        self.titles.append((4, node[0].text))
        return '<h4>' + node[0].text + '</h4>\n'
    
    def visit_title5(self, node):
        self.titles.append((5, node[0].text))
        return '<h5>' + node[0].text + '</h5>\n'

    def visit_title6(self, node):
        self.titles.append((6, node[0].text))
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
    
    def visit_table_begin(self, node):
        return '<table>'
    
    def visit_table_end(self, node):
        return '</table>'
    
    def visit_table_line_begin(self, node):
        return '<tr>'
    
    def visit_table_line_end(self, node):
        return '</tr>'
    
    def visit_table_column_begin(self, node):
        return '<td>'
    
    def visit_table_column_end(self, node):
        return '</td>'
    