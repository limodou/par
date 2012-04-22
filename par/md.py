#coding=utf8
# Parsing Markdown
# This version has some differences between Standard Markdown
# Syntax according from http://daringfireball.net/projects/markdown/syntax
# 
# They are:
#   || `^super^script` || <sup>super</sup>script ||
#   || `,,sub,,script` || <sub>sub</sub>script ||
#   || `~~strikeout~~` || <span style="text-decoration: line-through">strikeout</span> ||
#  
#   directly url and image support, e.g.:
#     http://code.google.com/images/code_sm.png
#     http://www.google.com
#   Table support
#   github flavored Markdown support:
#     Multiple underscores in words
#     Fenced code blocks
#     Syntax highlighting
#
from par.pyPEG import *
import re
import types
from par.gwiki import WikiGrammar, WikiHtmlVisitor, SimpleVisitor

_ = re.compile

class MarkdownGrammar(WikiGrammar):
    def __init__(self):
        super(MarkdownGrammar, self).__init__()
        
    def _get_rules(self):
        #basic
        def ws(): return _(r'\s+')
        def space(): return _(r'[ \t]+')
        def eol(): return _(r'\r\n|\r|\n')
        def seperator(): return _(r'[\.,!?\-$ \t\^]')
    
        #hr
        def hr1(): return _(r'\*[ \t]*\*[ \t]*\*[ \t]*[\* \t]*'), -2, blankline
        def hr2(): return _(r'-[ \t]*-[ \t]*-[ \t]*[- \t]*'), -2, blankline
        def hr3(): return _(r'_[ \t]*_[ \t]*_[ \t]*[_ \t]*'), -2, blankline
        def hr(): return [hr1, hr2, hr3]
          
        #html block
        def html_block(): return _(r'<(table|pre|div|p|ul|h1|h2|h3|h4|h5|h6|blockquote|code).*?>.*?<(/\1>)', re.I|re.DOTALL), -2, blankline
        def html_inline_block(): return _(r'<(span|del|font|a|b|code|i|em|strong|sub|sup).*?>.*?<(/\1>)|<(img|br).*?/>', re.I|re.DOTALL)
                        
        #paragraph
        def blankline(): return 0, space, eol
        def identifer(): return _(r'[a-zA-Z_][a-zA-Z_0-9]*', re.U)
        def htmlentity(): return _(r'&\w+;')
        def literal(): return _(r'u?r?"[^"\\]*(?:\\.[^"\\]*)*"', re.I|re.DOTALL)
        def literal1(): return _(r"u?r?'[^'\\]*(?:\\.[^'\\]*)*'", re.I|re.DOTALL)
        def escape_string(): return _(r'\\'), _(r'.')
        def simple_op(): return _(r'[ \t]+(\*\*|__|\*|_|~~|\^|,,)(?=\r|\n|[ \t]+)')
        def op_string(): return _(r'\*\*\*|\*\*|\*|___|__|_|~~|\^|,,')
        def op(): return [(-1, seperator, op_string), (op_string, -1, seperator)]
        def string(): return _(r'[^\\\*_\^~ \t\r\n`,<\[]+', re.U)
        def code_string_short(): return _(r'`'), _(r'[^`]*'), _(r'`')
        def code_string(): return _(r'``'), _(r'.+(?=``)'), _(r'``')
        def default_string(): return _(r'\S+', re.U)
        def underscore_words(): return _(r'[\w\d]+_[\w\d]+[\w\d_]*')
        def anchor(): return _(r'\[\['), 0, space, _(r'#'), _(r'\d*'), 0, space, _(r'\]\]')
        def word(): return [anchor, escape_string, code_string, 
            code_string_short, htmlentity, underscore_words, op, link, 
            html_inline_block, string, default_string]
        def words(): return [simple_op, word], -1, [simple_op, space, word]
        def line(): return words, eol
#        def paragraph(): return -2, line, -1, blankline
        def blanklines(): return -2, blankline
    
        #pre
        def indent_line_text(): return _(r'.+')
        def indent_line(): return _(r'[ ]{4}|\t'), indent_line_text, eol
        def indent_block(): return -2, [indent_line, blankline]
        def pre_lang(): return _(r'\S+')
        def pre_b(): return _(r'```')
        def pre_e(): return _(r'```')
        def pre_text(): return _(r'.+?(?=```)', re.M|re.DOTALL)
        def pre_extra(): return pre_b, 0, pre_lang, 0, space, eol, pre_text, pre_e, -2, blankline
        def pre(): return [indent_block, pre_extra]
    
        
        #subject
        def setext_title1(): return _(r'.+'), blankline, _(r'={1,}'), -2, blankline
        def setext_title2(): return _(r'.+'), blankline, _(r'-{1,}'), -2, blankline
        def title_text(): return _(r'.+(?= #)|.+', re.U)
        def atx_title1(): return _(r'# '), title_text, 0, _(r' #+'), -2, blankline
        def atx_title2(): return _(r'## '), title_text, 0, _(r' #+'), -2, blankline
        def title1(): return [atx_title1, setext_title1]
        def title2(): return [atx_title2, setext_title2]
        def title3(): return _(r'### '), title_text, 0, _(r' #+'), -2, blankline
        def title4(): return _(r'#### '), title_text, 0, _(r' #+'), -2, blankline
        def title5(): return _(r'##### '), title_text, 0, _(r' #+'), -2, blankline
        def title6(): return _(r'###### '), title_text, 0, _(r' #+'), -2, blankline
        def title(): return [title6, title5, title4, title3, title2, title1]
    
        #table
        def table_column(): return -2, [space, escape_string, code_string_short, code_string, op, link, _(r'[^\\\*_\^~ \t\r\n`,\|]+', re.U)], _(r'\|\|')
        def table_line(): return _(r'\|\|'), -2, table_column, eol
        def table(): return -2, table_line, -1, blankline
    
        #lists
        def list_rest_of_line(): return _(r'.+'), eol
        def list_content_text(): return _(r'[^*+\-\s].+'), eol
        def list_content_line(): return _(r'([\*+\-]\S+|\d+\.[\S$]*|\d+[^\.]*|[^\*\-+\r\n]).*')
        def list_content_lines(): return list_rest_of_line, -1, [list_content_indent_line, list_content_line]
        def list_content_indent_line(): return _(r' {4}|\t'), list_rest_of_line
        def list_content_norm_line(): return _(r' {0,3}'), list_rest_of_line
        def list_content_indent_lines(): return list_content_indent_line, -1, list_content_line
        def list_content(): return list_content_lines, -1, [list_content_indent_lines, blankline]
        def bullet_list_item(): return 0, _(r' {1,3}'), _(r'\*|\+|-'), space, list_content
        def number_list_item(): return 0, _(r' {1,3}'), _(r'\d+\.'), space, list_content
        def list_item(): return [bullet_list_item, number_list_item]
        def list(): return -2, list_item, -1, blankline
    
        #quote
        def quote_blank_line(): return _(r'>'), eol
        def quote_line(): return _(r'> .*'), eol
        def quote_lines(): return [quote_line, quote_blank_line]
        def blockquote(): return -2, quote_lines, -1, blankline
            
        #links
        def protocal(): return [_(r'http://'), _(r'https://'), _(r'ftp://')]
        def direct_link(): return _(r'(<)?(?:http://|https://|ftp://)[\w\d\-\.,@\?\^=%&:/~+#]+(?(1)>)')
        def image_link(): return _(r'(<)?(?:http://|https://|ftp://).*?(?:\.png|\.jpg|\.gif|\.jpeg)(?(1)>)', re.I)
        def mailto(): return _(r'<(mailto:)?[a-zA-Z_0-9-/\.]+@[a-zA-Z_0-9-/\.]+>')
        
        def inline_text(): return _(r'[^\]]*')
        def inline_image_alt(): return _(r'!\['), inline_text, _(r'\]')
        def inline_image_title(): return literal
        def inline_href(): return _(r'[^\s\)]+')
        def inline_image_link(): return _(r'\('), inline_href, 0, space, 0, inline_link_title, 0, space, _(r'\)')
        def inline_image(): return inline_image_alt, inline_image_link
        
        def refer_image_alt(): return _(r'!\['), inline_text, _(r'\]')
        def refer_image_refer(): return _(r'[^\]]*')
        def refer_image(): return refer_image_alt, 0, space, _(r'\['), refer_image_refer, _(r'\]')
        def refer_image_link(): return 0, _(r'(<)?(\S+)(?(1)>)')
        def refer_image_title(): return [literal, literal1, '\(.*?\)']
        
        def inline_link_caption(): return _(r'\['), _(r'[^\]]+'), _(r'\]')
        def inline_link_title(): return literal
        def inline_link_link(): return _(r'\('), _(r'[^\s\)]+'), 0, space, 0, inline_link_title, 0, space, _(r'\)')
        def inline_link(): return inline_link_caption, inline_link_link
        
        def refer_link_caption(): return _(r'\['), _(r'[^\]]+'), _(r'\]')
        def refer_link_refer(): return _(r'[^\]]*')
        def refer_link(): return refer_link_caption, 0, space, _(r'\['), refer_link_refer, _(r'\]')
        def refer_link_link(): return 0, _(r'(<)?(\S+)(?(1)>)')
        def refer_link_title(): return [literal, literal1, '\(.*?\)']
        def refer_link_note(): return 0, _(r' {1,3}'), inline_link_caption, _(r':'), space, refer_link_link, 0, (ws, refer_link_title), -2, blankline
        def link(): return [inline_image, refer_image, inline_link, refer_link, image_link, direct_link, mailto], -1, space
        
        #article
        def article(): return -1, [blanklines, hr, title, refer_link_note, pre, html_block, table, list, blockquote, line]
    
        peg_rules = {}
        for k, v in ((x, y) for (x, y) in locals().items() if isinstance(y, types.FunctionType)):
            peg_rules[k] = v
        return peg_rules, article
    
    def parse(self, text, root=None, skipWS=False, **kwargs):
        if not text:
            text = '\n'
        if text[-1] not in ('\r', '\n'):
            text = text + '\n'
        return parseLine(text, root or self.root, skipWS=skipWS, **kwargs)

class MarkdownHtmlVisitor(WikiHtmlVisitor):
    op_maps = {
        '*':['<em>', '</em>'],
        '_':['<em>', '</em>'],
        '**':['<strong>', '</strong>'],
        '***':['<strong><em>', '</em></strong>'],
        '__':['<strong><em>', '</em></strong>'],
        '__':['<strong>', '</strong>'],
        '~~':['<span style="text-decoration: line-through">', '</span>'],
        '^':['<sup>', '</sup>'],
        ',,':['<sub>', '</sub>'],
        '`':['<code>', '</code>'],
    }
    tag_class = {}
    
    def __init__(self, template=None, tag_class=None, grammar=None):
        super(MarkdownHtmlVisitor, self).__init__(template, tag_class, grammar)
        self.refer_links = {}
        self.last_visit = None
        self.visit_nodes = ['hr', 'title', 'refer_link_note', 'pre', 
            'html_block', 'table', 'list', 'blockquote', 'line', 'blanklines']
        self.paragraph = []
    
    def before_visit(self, node):
        name = node.__name__
        if name in self.visit_nodes:
            if name != self.last_visit:
                if name != 'line':
                    if self.paragraph:
                        t = ''.join(self.paragraph)
                        self.paragraph = []
                        return self.tag('p', t)
            self.last_visit = name
        return ''
        
    def __end__(self):
        if self.paragraph:
            t = ''.join(self.paragraph)
            self.paragraph = []
            return self.tag('p', t)
        return ''
    
    def visit_string(self, node):
        return self.to_html(node.text)
    
    def visit_line(self, node):
        self.paragraph.append(self.visit(node))
        return ''
    
    def visit_blanklines(self, node):
        return ''
    
    def visit_title1(self, node):
        _id = self.get_title_id(1)
        self.titles.append((1, _id, self.visit(node).strip()))
        return self.tag('h1', self.visit(node).strip(), id=_id)
    
    def visit_setext_title1(self, node):
        return node[0]

    def visit_atx_title1(self, node):
        return node[1].text

    def visit_title2(self, node):
        _id = self.get_title_id(2)
        self.titles.append((2, _id, self.visit(node).strip()))
        return self.tag('h2', self.visit(node).strip(), id=_id)
    
    def visit_setext_title2(self, node):
        return node[0]
    
    def visit_atx_title2(self, node):
        return node[1].text
    
    def visit_indent_block_line(self, node):
        return node[1].text
    
    def visit_indent_line(self, node):
        return node.find('indent_line_text').text + '\n'

    def visit_pre(self, node):
        lang = node.find('pre_lang')
        if lang:
            kwargs = {'class':'language-'+lang.text}
        else:
            kwargs = {}
        return self.tag('pre', self.tag('code',self.to_html(self.visit(node).rstrip()), newline=False, **kwargs))
    
    def visit_pre_extra(self, node):
        return node.find('pre_text').text.strip()
    
    def visit_inline_link(self, node):
        kwargs = {'href':node[1][1]}
        if len(node[1])>3:
            kwargs['title'] = node[1][3].text[1:-1]
        return self.tag('a', node[0][1], newline=False, **kwargs)
    
    def visit_inline_image(self, node):
        kwargs = {}
        kwargs['src'] = node.find('inline_href').text
        title = node.find('inline_link_title')
        if title:
            kwargs['title'] = title.text[1:-1]
        alt = node.find('inline_text')
        if alt:
            kwargs['alt'] = alt.text
        return self.tag('img', enclose=1, **kwargs)
    
    def visit_refer_link(self, node):
        caption = node.find('refer_link_caption')[1]
        key = node.find('refer_link_refer')
        if not key:
            key = caption
        else:
            key = key.text
        return self.tag('a', caption, **self.refer_links.get(key.upper(), {}))
        
    def visit_refer_image(self, node):
        kwargs = {}

        alt = node.find('refer_image_alt')
        if alt:
            alt = alt.find('inline_text').text
        else:
            alt = ''
        key = node.find('refer_image_refer')
        if not key:
            key = alt
        else:
            key = key.text
        d = self.refer_links.get(key.upper(), {})
        kwargs.update({'src':d.get('href', ''), 'title':d.get('title', '')})
        return self.tag('img', enclose=1, **kwargs)

    def visit_refer_link_note(self, node):
        key = node.find('inline_link_caption').text[1:-1].upper()
        self.refer_links[key] = {'href':node.find('refer_link_link').text}
        r = node.find('refer_link_title')
        if r:
            self.refer_links[key]['title'] = r.text[1:-1]
        return ''
    
    def template(self, node):
        for obj in node[0].find_all('refer_link_note'):
            self.visit_refer_link_note(obj)
        body = self.visit(node, self.grammar or self.grammar.root)
        return self._template % {'title':self.title, 'body':body}
    
    def visit_direct_link(self, node):
        t = node.text
        if t.startswith('<'):
            e = -1
        else:
            e = len(t)
        b = t.find('://') + 3
        href = t[b:e]
        return self.tag('a', href, href=href)
    
    def visit_image_link(self, node):
        t = node.text
        if t.startswith('<'):
            e = -1
        else:
            e = len(t)
        b = t.find('://') + 3
        href = t[b:e]
        return self.tag('img', href, 1)
    
    def visit_mailto(self, node):
        href = node.text[1:-1]
        if href.startswith('mailto:'):
            href = href[7:]
        
        def shuffle(text):
            import random
            t = []
            for x in text:
                if random.choice('01') == '1':
                    t.append('&#x%X;' % ord(x))
                else:
                    t.append(x)
            return ''.join(t)
        
        return self.tag('a', shuffle(href), href=shuffle("mailto:"+href), newline=False)
    
    def visit_quote_line(self, node):
        return node.text[2:]
    
    def visit_quote_blank_line(self, node):
        return '\n'
    
    def visit_blockquote(self, node):
        text = []
        for line in node.find_all('quote_lines'):
            text.append(self.visit(line))
        result = self.parse_text(''.join(text))
        return self.tag('blockquote', result)
        
    def visit_list_begin(self, node):
        self.lists = []
        return ''
        
    def visit_list_content_line(self, node):
        return node.text
    
    def visit_list_content_indent_line(self, node):
        return node.find('list_rest_of_line').text

    def visit_bullet_list_item(self, node):
        self.lists.append(('b', node.find('list_content')))
        return ''
        
    def visit_number_list_item(self, node):
        self.lists.append(('n', node.find('list_content')))
        return ''
        
    def visit_list_end(self, node):
        def process_node(n):
            b = n.find('blankline')
            text = self.visit(n)
            t = self.parse_text(text, 'article').rstrip()
            if t.count('<p>') == 1 and t.startswith('<p>') and t.endswith('</p>'):
                return t[3:-5].rstrip()
            else:
                return t
            
        def create_list(lists):
            buf = []
            old = None
            parent = None
            for  _type, _node in lists:
                if _type == old:
                    buf.append(self.tag('li', process_node(_node)))
                else:
                    #find another list
                    if parent:
                        buf.append('</' + parent + '>\n')
                    if _type == 'b':
                        parent = 'ul'
                    else:
                        parent = 'ol'
                    buf.append(self.tag(parent))
                    buf.append(self.tag('li', process_node(_node)))
                    old = _type
            if buf:
                buf.append('</' + parent + '>\n')
            return ''.join(buf)
    
        return create_list(self.lists)
    
