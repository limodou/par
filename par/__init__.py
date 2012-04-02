#! /usr/bin/env python
#coding=utf-8
#
# Author: limodou@gmail.com
# This program is based on pyPEG
#
# license: GPL
#
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
        def seperator(): return _(r'[\.,!?\-$ \t\^]')
    
        #hr
        def hr(): return _(r'\-{4,}'), -2, blankline
    
        #paragraph
        def blankline(): return 0, space, eol
        def identifer(): return _(r'[a-zA-Z_][a-zA-Z_0-9]*', re.U)
        def literal(): return _(r'u?r?"[^"\\]*(?:\\.[^"\\]*)*"', re.I|re.DOTALL)
        def literal1(): return _(r"u?r?'[^'\\]*(?:\\.[^'\\]*)*'", re.I|re.DOTALL)
        def escape_string(): return '\\', _(r'.')
        def op_string(): return _(r'\*|_|~~|\^|,,')
        def op(): return [(-1, seperator, op_string), (op_string, -1, seperator)]
        def string(): return _(r'[^\\\*_\^~ \t\r\n`,]+', re.U)
        def code_string_short(): return '`', _(r'[^`]*'), '`'
        def code_string(): return '{{{', _(r'[^\}\r\n$]*'), '}}}'
        def default_string(): return _(r'\S+', re.U)
        def word(): return [literal, literal1, escape_string, code_string, code_string_short, op, link, string, default_string]
        def words(): return word, -1, [space, word]
        def line(): return words, eol
        def paragraph(): return -2, line, -1, blankline
    
        #pre
        def pre_alt(): return '<code>', _(r'.+?(?=</code>)', re.M|re.DOTALL), '</code>', -2, blankline
        def pre_normal(): return '{{{', 0, space, eol, _(r'.+?(?=\}\}\})', re.M|re.DOTALL), '}}}', -2, blankline
        def pre(): return [pre_alt, pre_normal]
    
        
        #subject
        def title_text(): return _(r'.+(?= =)', re.U)
#        def subject(): return _(r'\s*.*'), eol, _(r'(?:=|-){4,}'), -2, eol
        def title1(): return '= ', title_text, ' =', -2, eol
        def title2(): return '== ', title_text, ' ==', -2, eol
        def title3(): return '=== ', title_text, ' ===', -2, eol
        def title4(): return '==== ', title_text, ' ====', -2, eol
        def title5(): return '===== ', title_text, ' =====', -2, eol
        def title6(): return '====== ', title_text, ' ======', -2, eol
        def title(): return [title6, title5, title4, title3, title2, title1]
    
        #table
        def table_column(): return -2, [space, escape_string, code_string_short, code_string, op, link, _(r'[^\\\*_\^~ \t\r\n`,\|]+', re.U)], '||'
        def table_line(): return '||', -2, table_column, eol
        def table(): return -2, table_line, -1, blankline
    
        #lists
        def list_leaf_content(): return words, eol
        def list_indent(): return space
        def bullet_list_item(): return list_indent, '*', space, list_leaf_content
        def number_list_item(): return list_indent, '#', space, list_leaf_content
        def list_item(): return [bullet_list_item, number_list_item]
        def list(): return -2, list_item, -1, blankline
    
        #quote
        def quote_line(): return space, line
        def quote(): return -2, quote_line, -1, blankline
            
        #links
        def protocal(): return [_(r'http://'), _(r'https://'), _(r'ftp://')]
        def direct_link(): return protocal, _(r'[\w\d\-\.,@\?\^=%&:/~+#]+')
        def image_link(): return protocal, _(r'.*?(?:\.png|\.jpg|\.gif|\.jpeg)')
        def alt_direct_link(): return '[', 0, space, direct_link, space, _(r'[^\]]+'), 0, space, ']'
        def alt_image_link(): return '[', 0, space, direct_link, space, image_link, 0, space, ']'
        def mailto(): return 'mailto:', _(r'[a-zA-Z_0-9-@/\.]+')
        def link(): return [alt_image_link, alt_direct_link, image_link, direct_link, mailto], -1, space
        
        #article
        def article(): return 0, ws, -1, [hr, title, pre, table, list, quote, paragraph]
    
        peg_rules = {}
        for k, v in ((x, y) for (x, y) in locals().items() if isinstance(y, types.FunctionType)):
            peg_rules[k] = v
        return peg_rules, article
    
    def parse(self, text, root=None, skipWS=False, **kwargs):
        return parseLine(text, root or self.root, skipWS=skipWS, **kwargs)
        
class SimpleVisitor(object):
    def visit(self, nodes):
        buf = []
        if not isinstance(nodes, (list, tuple)):
            nodes = [nodes]
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
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="bootstrap.min.css"/>
<link rel="stylesheet" type="text/css" href="example.css"/>
<title>%(title)s</title>
</head>
<body>
%(body)s</body>
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
    tag_class = {}
    
    def __init__(self, template=None, tag_class=None):
        self._template = template or default_template
        self.title = 'Untitled'
        self.titles = []
        self.ops = {}
        self.tag_class = tag_class or self.__class__.tag_class
        
    def __str__(self):
        return self.template()
    
    def template(self, node):
        body = self.visit(node)
        return self._template % {'title':self.title, 'body':body}
    
    def tag(self, tag, child='', enclose=0, newline=True):
        """
        enclose:
            0 => <tag>
            1 => <tag/>
            2 => <tag></tag>
        """
        _class = self.tag_class.get(tag, '')
        if _class:
            _class = ' class="%s"' % _class
        nline = '\n' if newline else ''
        if child:
            enclose = 2
        if enclose == 1:
            return '<%s%s/>%s' % (tag, _class, nline)
        elif enclose == 2:
            return '<%s%s>%s</%s>%s' % (tag, _class, child, tag, nline)
        else:
            return '<%s%s>%s' % (tag, _class, nline)
            
    def visit_subject(self, node):
        self.subject = node[0].strip()
        return self.tag('h1', self.subject)
    
    def visit_title1(self, node):
        self.subject = node[0].text
        return self.tag('h1', node[0].text)
    
    def visit_title2(self, node):
        self.titles.append((2, node[0].text))
        return self.tag('h2', node[0].text)

    def visit_title3(self, node):
        self.titles.append((3, node[0].text))
        return self.tag('h3', node[0].text)

    def visit_title4(self, node):
        self.titles.append((4, node[0].text))
        return self.tag('h4', node[0].text)
    
    def visit_title5(self, node):
        self.titles.append((5, node[0].text))
        return self.tag('h5', node[0].text)

    def visit_title6(self, node):
        self.titles.append((6, node[0].text))
        return self.tag('h6', node[0].text)

    def visit_paragraph(self, node):
        return self.tag('p', self.visit(node).rstrip())
    
    def visit_op_string(self, node):
        c = node.text
        index = (self.ops.setdefault(c, 1) + 1)%2
        self.ops[c] = index
        return self.op_maps[c][index]
        
    def visit_escape_string(self, node):
        return node[0]
    
    def to_html(self, text):
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    def visit_pre(self, node):
        return self.tag('pre', self.to_html(node[0].text.strip()))
    
    def visit_code_string(self, node):
        return self.tag('code', self.to_html(node[0]), newline=False)
    
    def visit_code_string_short(self, node):
        return self.tag('code', self.to_html(node[0]), newline=False)

    def visit_hr(self, node):
        return self.tag('hr', enclose=1)
    
    def visit_table_begin(self, node):
        return self.tag('table')
    
    def visit_table_end(self, node):
        return '</table>\n'
    
    def visit_table_line_begin(self, node):
        return self.tag('tr', newline=False)
    
    def visit_table_line_end(self, node):
        return '</tr>\n'
    
    def visit_table_column_begin(self, node):
        return '<td>'
    
    def visit_table_column_end(self, node):
        return '</td>'
    
    def visit_list_begin(self, node):
        self.lists = []
        return ''
        
    def visit_list_end(self, node):
        def create_list(index, lists):
            buf = []
            old = None
            old_indent = None
            parent = None
            i = index
            while i<len(lists):
                _type, indent, txt = lists[i]
                i += 1
                #find sub_list
                if old_indent and indent > old_indent:
                    _t, i = create_list(i-1, lists)
                    buf.append(_t)
                    continue
                if old_indent and indent < old_indent:
                    buf.append('</' + parent + '>\n')
                    return ''.join(buf), i-1
                if _type == old:
                    buf.append(txt)
                else:
                    #find another list
                    if parent:
                        buf.append('</' + parent + '>\n')
                    if _type == 'b':
                        parent = 'ul'
                    else:
                        parent = 'ol'
                    buf.append(self.tag(parent))
                    buf.append(txt)
                    old_indent = indent
                    old = _type
            if buf:
                buf.append('</' + parent + '>\n')
            return ''.join(buf), i
    
        return create_list(0, self.lists)[0]
        
    def visit_bullet_list_item(self, node):
        self.lists.append(('b', len(node[0].text), self.visit([node[2]])))
        return ''
        
    def visit_number_list_item(self, node):
        self.lists.append(('n', len(node[0].text), self.visit([node[2]])))
        return ''
        
    def visit_list_leaf_content(self, node):
        return self.tag('li', self.visit(node.what).strip())
    
    def visit_quote_begin(self, node):
        return '<blockquote>'
    
    def visit_quote_end(self, node):
        return '</blockquote>'
    
    def visit_mailto(self, node):
        text = node[0]
        return '<a href="mailto:%s">%s</a>' % (text, text)
    
    def visit_direct_link(self, node):
        return '<a href="%s%s">%s%s</a>' % (node[0].text, node[1], node[0].text, node[1])
    
    def visit_alt_direct_link(self, node):
        return '<a href="%s">%s</a>' % (node[0].text, node[2].strip())
    
    def visit_alt_image_link(self, node):
        return '<a href="%s">%s</a>' % (node[0].text, self.visit_direct_link(node[2]))

    def visit_image_link(self, node):
        return '<img src="%s%s"/>' % (node[0].text, node[1])
    