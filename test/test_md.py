from __future__ import print_function
from __future__ import unicode_literals
import sys
sys.path.insert(0, '..')
from par.md import parseHtml
from par.semantic_ext import blocks as semantic_blocks
from par.bootstrap_ext import blocks as bootstrap_blocks

def test_symbol():
    """
    >>> text = '''
    ... This is **a** symbol **test**.
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <p>This is <strong>a</strong> symbol <strong>test</strong>.</p>
    <BLANKLINE>
    """

def test_list_1():
    """
    >>> text = '''
    ... * a
    ... * b
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <ul>
    <li>a</li>
    <li>b</li>
    </ul>
    <BLANKLINE>
    """
    
def test_list_2():
    """
    >>> text = '''
    ... 1. a
    ... 2. b
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <ol>
    <li>a</li>
    <li>b</li>
    </ol>
    <BLANKLINE>
    
    """
    
def test_list_3():
    """
    >>> text = '''
    ... * a
    ... * b
    ... 
    ... * c
    ... * d
    ... 
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <ul>
    <li>a</li>
    <li>b</li>
    <li>c</li>
    <li>d</li>
    </ul>
    <BLANKLINE>
    """
    
def test_list_4():
    """
    >>> text = '''
    ... * a
    ...     * b
    ...     * c
    ... * d
    ...     * e
    ... 
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <ul>
    <li><p>a</p>
    <ul>
    <li>b</li>
    <li>c</li>
    </ul></li>
    <li><p>d</p>
    <ul>
    <li>e</li>
    </ul></li>
    </ul>
    <BLANKLINE>
    """

def test_dl_1():
    """
    >>> text = '''
    ... a --
    ...     abc
    ...
    ... b --
    ...     cde
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <dl>
    <dt>a</dt>
    <dd><p>abc</p>
    </dd>
    <dt>b</dt>
    <dd><p>cde</p>
    </dd>
    </dl>
    
    """

def test_dl_2():
    """
    >>> text = '''
    ... a\_ --
    ...     abc
    ... 
    ... **b** --
    ...     * li
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <dl>
    <dt>a_</dt>
    <dd><p>abc</p>
    </dd>
    <dt><strong>b</strong></dt>
    <dd><ul>
    <li>li</li>
    </ul>
    </dd>
    </dl>
    
    """

def test_dl_3():
    """
    >>> text = '''
    ... a
    ... :   abc
    ... 
    ... **b**
    ... :   * li
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <dl>
    <dt>a</dt>
    <dd><p>abc</p>
    </dd>
    <dt><strong>b</strong></dt>
    <dd><ul>
    <li>li</li>
    </ul>
    </dd>
    </dl>
    
    """

def test_dl_4():
    """
    >>> text = '''
    ... a --
    ...     abc
    ...
    ...     ```
    ...     code
    ...     ```
    ... 
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <dl>
    <dt>a</dt>
    <dd><p>abc</p>
    <pre><code>code</code></pre>
    </dd>
    </dl>
    """

def test_dl_5():
    """
    >>> text = '''
    ... a
    ... :   abc
    ...
    ...     ```
    ...     code
    ...     ```
    ... 
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <dl>
    <dt>a</dt>
    <dd><p>abc</p>
    <pre><code>code</code></pre>
    </dd>
    </dl>
    """

def test_dl_6():
    """
    >>> text = '''
    ... 1. aaa
    ... 
    ...     defaults --
    ...         test:
    ...     
    ...         ```
    ...         return {}
    ...         ```
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <ol>
    <li><p>aaa</p>
    <dl>
    <dt>defaults</dt>
    <dd><p>test:</p>
    <pre><code>return {}</code></pre>
    </dd>
    </dl></li>
    </ol>
    <BLANKLINE>
    """

def test_dl_7():
    """
    >>> text = '''
    ... a --
    ...     abc
    ...
    ...     ```
    ...     code
    ...        abcd
    ...     ```
    ...
    ...     test
    ...
    ... b --c --
    ...     abc
    ...
    ...     ```
    ...     code
    ...        abcd
    ...     ```
    ...
    ...     test
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <dl>
    <dt>a</dt>
    <dd><p>abc</p>
    <pre><code>code
       abcd</code></pre>
    <p>test</p>
    </dd>
    <dt>b --c</dt>
    <dd><p>abc</p>
    <pre><code>code
       abcd</code></pre>
    <p>test</p>
    </dd>
    </dl>
    """

def test_hr():
    """
    >>> text = '''
    ... * * * *
    ... ----
    ... __ __ __
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <hr/>
    <hr/>
    <hr/>
    <BLANKLINE>
    """

def test_url_1():
    """
    >>> text = '''
    ... This is [Test][foo] .
    ... 
    ... [foo]: http://example.com/  "Optional Title Here"
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <p>This is <a href="http://example.com/" class="outter" title="Optional Title Here">Test</a>
     .</p>
    <BLANKLINE>
    """

def test_url_2():
    """
    >>> text = '''
    ... This is [Test][foo] .
    ... 
    ... [foo]: http://example.com/  'Optional Title Here'
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <p>This is <a href="http://example.com/" class="outter" title="Optional Title Here">Test</a>
     .</p>
    <BLANKLINE>
    """

def test_url_3():
    """
    >>> text = '''
    ... This is [Test][foo] .
    ... 
    ... [foo]: http://example.com/  (Optional Title Here)
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <p>This is <a href="http://example.com/" class="outter" title="Optional Title Here">Test</a>
     .</p>
    <BLANKLINE>
    """

def test_url_4():
    """
    >>> text = '''
    ... This is [foo][] .
    ... 
    ... [foo]: http://example.com/  (Optional Title Here)
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <p>This is <a href="http://example.com/" class="outter" title="Optional Title Here">foo</a>
     .</p>
    <BLANKLINE>
    """

def test_table():
    """
    >>> text = '''
    ... || a || b || c ||
    ... || b || c || d ||
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <table>
    <tr><td>a</td><td>b</td><td>c</td>
    </tr>
    <tr><td>b</td><td>c</td><td>d</td>
    </tr>
    </table>
    <BLANKLINE>
    """

def test_table_0():
    """
    >>> text = '''
    ... |aa|bb|                                                                                      
    ... |--|--|                                                                                      
    ... |asd||
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <table>
    <thead>
    <tr><th>aa</th><th>bb</th><th></th></tr>
    </thead>
    <tbody>
    <tr><td>asd</td><td></td></tr>
    </tbody></table>
    <BLANKLINE>
    """
    
def test_block_1():
    """
    >>> text = '''
    ... {% tabs %}
    ... -- index.html --
    ... ```    
    ... This is hello
    ... ```
    ... -- hello.html --
    ... ```
    ... This is hello
    ... ```
    ... {% endtabs %}
    ... '''
    >>> from par.bootstrap_ext import blocks
    >>> print (parseHtml(text, '%(body)s', block_callback=blocks))
    <BLANKLINE>
    <div class="tabbable">
    <ul class="nav nav-tabs">
    <li class="active"><a href="#tab_item_1_1" data-toggle="tab">index.html</a></li>
    <li><a href="#tab_item_1_2" data-toggle="tab">hello.html</a></li>
    </ul>
    <div class="tab-content">
    <div class="tab-pane active" id="tab_item_1_1">
    <BLANKLINE>
    <pre><code>This is hello</code></pre>
    <BLANKLINE>
    </div>
    <div class="tab-pane" id="tab_item_1_2">
    <BLANKLINE>
    <pre><code>This is hello</code></pre>
    <BLANKLINE>
    </div>
    </div>
    </div>
    """
    
def test_block_2():
    """
    >>> text = '''
    ... {%alert class=info, close%}
    ...     This is an alert.
    ... {%endalert%}'''
    >>> from par.bootstrap_ext import blocks
    >>> print (parseHtml(text, '%(body)s', block_callback=blocks))
    <BLANKLINE>
    <div class="alert alert-info">
    <button class="close" data-dismiss="alert">&times;</button>
    <p>This is an alert.</p>
    <BLANKLINE>
    </div>
    """
    
def test_pre_1():
    """
    >>> text = '''
    ... ```lang=python,id=test
    ... a
    ... b
    ... c
    ... ```
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <pre id="test"><code class="language-python">a
    b
    c</code></pre>
    <BLANKLINE>
    """
    
def test_pre_2():
    """
    >>> text = '''
    ... ```python
    ... a
    ... b
    ... c
    ... ```
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <pre><code class="language-python">a
    b
    c</code></pre>
    <BLANKLINE>
    """

def test_pre_3():
    """
    >>> text = '''
    ... ```id=test
    ... a
    ... b
    ... c
    ... ```
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <pre id="test"><code>a
    b
    c</code></pre>
    <BLANKLINE>
    """

def test_pre_4():
    """
    >>> text = '''
    ... ```
    ... a
    ... b
    ... c
    ... ```
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <pre><code>a
    b
    c</code></pre>
    <BLANKLINE>
    """

def test_pre5():
    """
    >>> text = '''
    ... ~~~~~~
    ... asfadsf
    ... ~~~~~~
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <pre><code>asfadsf</code></pre>
    <BLANKLINE>
    """
    
def test_pre_6():
    """
    >>> text = '''
    ... ```class=linenums
    ... a
    ... b
    ... c
    ... ```
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <pre class="linenums"><code>a
    b
    c</code></pre>
    <BLANKLINE>
    """
    
def test_footnote():
    """
    >>> text = '''
    ... That's some text with a footnote.[^1]
    ... 
    ... [^1]: **aaaa**
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <p>That's some text with a footnote.<sup id="fnref-1"><a href="#fn-1" class="footnote-rel inner">1</a></sup></p>
    <div class="footnotes"><ol>
    <li id="fn-1">
    <p> <strong>aaaa</strong></p>
    <BLANKLINE>
    <a href="#fnref-1" class="footnote-backref inner">&#8617;</a>
    <BLANKLINE>
    </li>
    </ol></div>
    """
    
def test_attr_1():
    """
    >>> text = '''
    ... test  {#test}
    ... ====
    ... 
    ... ## hello ## {#hello}
    ... 
    ... ### subject ### {#subject}
    ... ### subject {#subject}
    ... 
    ... [link to anchor](#anchor)
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <h1 id="test">test<a class="anchor" href="#test">&para;</a></h1>
    <h2 id="hello">hello<a class="anchor" href="#hello">&para;</a></h2>
    <h3 id="subject">subject<a class="anchor" href="#subject">&para;</a></h3>
    <h3 id="subject">subject<a class="anchor" href="#subject">&para;</a></h3>
    <p><a href="#anchor" class="inner">link to anchor</a></p>
    <BLANKLINE>
    """
    
def test_attr_2():
    """
    >>> text = '''
    ... ## hello ## {#hello}
    ... ## hello ## {.hello}
    ... ## hello  {#hello}
    ... ## hello  {.hello}
    ... ## hello  {.hello #title .class}
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <h2 id="hello">hello<a class="anchor" href="#hello">&para;</a></h2>
    <h2 id="title_0-1" class="hello">hello<a class="anchor" href="#title_0-1">&para;</a></h2>
    <h2 id="hello">hello<a class="anchor" href="#hello">&para;</a></h2>
    <h2 id="title_0-2" class="hello">hello<a class="anchor" href="#title_0-2">&para;</a></h2>
    <h2 id="title" class="hello class">hello<a class="anchor" href="#title">&para;</a></h2>
    <BLANKLINE>
    """

def test_link_1():
    """
    >>> text = '''
    ... [[Page|Hello world]]
    ... [[Page#title|Hello world]]
    ... [[wiki:Page|Hello world]]
    ... 
    ... [[image:a.png]]
    ... [[image:a.png|right]]
    ... [[image:a.png||250]]
    ... <Page>
    ... <http://localhost:8000>
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <p><a href="/wiki/Page" class="inner">Hello world</a>
     <a href="/wiki/Page#title" class="inner">Hello world</a>
     <a href="/wiki/Page" class="inner">Hello world</a>
    </p>
    <p><img src="a.png" /> <div class="floatright"><img src="a.png" /></div> <img src="a.png"  width="250px"/> <Page> <a href="http://localhost:8000" class="outter">http://localhost:8000</a></p>
    <BLANKLINE>
    """
    
def test_link_2():
    """
    >>> text = '''
    ... [](http://aaaa.com)
    ... ![](http://aaaa.com)
    ... [](page)
    ... <http://aaaa.com>
    ... [[Page]]
    ... [[#edit]]
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <p><a href="http://aaaa.com" class="outter">http://aaaa.com</a> <img src="http://aaaa.com"/>
     <a href="page" class="inner">page</a> <a href="http://aaaa.com" class="outter">http://aaaa.com</a> <a href="/wiki/Page" class="inner">Page</a>
     <a href="#edit" class="inner">
    </p>
    <BLANKLINE>
    """
    
def test_table_1():
    """
    >>> text = '''
    ... First Header  | Second Header
    ... ------------- | -------------
    ... Content Cell  | Content Cell
    ... Content Cell  | Content Cell
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <table>
    <thead>
    <tr><th>First Header</th><th>Second Header</th></tr>
    </thead>
    <tbody>
    <tr><td>Content Cell</td><td>Content Cell</td></tr>
    <tr><td>Content Cell</td><td>Content Cell</td></tr>
    </tbody></table>
    <BLANKLINE>
    """

def test_table_2():
    """
    >>> text = '''
    ... First Header  | Second Header | Third Header
    ... :------------ | ------------: | :----------:
    ... Content Cell  | Content Cell  | Content Cell 
    ... Content Cell  | Content Cell  | Content Cell 
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <table>
    <thead>
    <tr><th>First Header</th><th>Second Header</th><th>Third Header</th></tr>
    </thead>
    <tbody>
    <tr><td align="left">Content Cell</td><td align="right">Content Cell</td><td align="center">Content Cell</td></tr>
    <tr><td align="left">Content Cell</td><td align="right">Content Cell</td><td align="center">Content Cell</td></tr>
    </tbody></table>
    <BLANKLINE>
    """

def test_table_3():
    """
    >>> text = '''
    ... | First Header  | Second Header |
    ... | :------------ | ------------: |
    ... | **cell**      | Content Cell  |
    ... | Content Cell  | Content Cell  |
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <table>
    <thead>
    <tr><th>First Header</th><th>Second Header</th></tr>
    </thead>
    <tbody>
    <tr><td align="left"><strong>cell</strong></td><td align="right">Content Cell</td></tr>
    <tr><td align="left">Content Cell</td><td align="right">Content Cell</td></tr>
    </tbody></table>
    <BLANKLINE>
    """

def test_table_4():
    """
    >>> text = '''
    ... |aa|bb|
    ... |--|--|
    ... |asd||
    ... '''
    >>> print (parseHtml(text, '%(body)s', tag_class={'table':'table'}))
    <BLANKLINE>
    <table class="table">
    <thead>
    <tr><th>aa</th><th>bb</th></tr>
    </thead>
    <tbody>
    <tr><td>asd</td><td></td></tr>
    </tbody></table>
    <BLANKLINE>
    """

def test_list_pre():
    """
    >>> text = '''
    ... 1. abc
    ... 
    ...     ```
    ...     code
    ...     ```
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <ol>
    <li><p>abc</p>
    <pre><code>code</code></pre></li>
    </ol>
    <BLANKLINE>
    """
    
def test_list_pre_1():
    """
    >>> text = '''
    ... 1. abc
    ... 
    ...         code
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <ol>
    <li><p>abc</p>
    <pre><code>code</code></pre></li>
    </ol>
    <BLANKLINE>
    """
    
def test_list_pre_2():
    """
    >>> text = '''
    ... 1. abc
    ... 
    ...     cde
    ... 
    ...     ```
    ...     code
    ...     ```
    ... '''
    >>> print (parseHtml(text, '%(body)s'))
    <BLANKLINE>
    <ol>
    <li><p>abc</p>
    <p>cde</p>
    <pre><code>code</code></pre></li>
    </ol>
    <BLANKLINE>
    """
    
def test_semantic_alert():
    """
    >>> text = '''
    ... {% alert %}
    ... This is a test.
    ... {% endalert %}
    ... '''
    >>> print (parseHtml(text, '%(body)s', block_callback=semantic_blocks))
    <BLANKLINE>
    <div class="ui  message">
    <p>This is a test.</p>
    <BLANKLINE>
    </div>
    """
    
def test_semantic_tabs():
    """
    >>> text = '''
    ... {% tabs %}
    ... -- name --
    ... * a
    ... * b
    ... -- name --
    ... 1. c
    ... 1. d
    ... {% endtabs %}
    ... '''
    >>> print (parseHtml(text, '%(body)s', block_callback=semantic_blocks))
    <BLANKLINE>
    <div class="ui tabular filter menu">
    <a class=" class="active"item" data-tab="tab_item_1_1">name</a>
    <a class="item" data-tab="tab_item_1_2">name</a>
    </div>
    <div class="tab-content">
    <div class="ui divided inbox selection list active tab" data-tab="tab_item_1_1">
    <BLANKLINE>
    <ul>
    <li>a</li>
    <li>b</li>
    </ul>
    <BLANKLINE>
    </div>
    <div class="ui divided inbox selection list tab" data-tab="tab_item_1_2">
    <BLANKLINE>
    <ol>
    <li>c</li>
    <li>d</li>
    </ol>
    <BLANKLINE>
    </div>
    </div>
    </div>
    """
    














