import sys
sys.path.insert(0, '..')
from par.md import parseHtml

def test_li_unorder1():
    """
    >>> text = '''
    ... * a
    ... * b
    ... '''
    >>> print parseHtml(text, '%(body)s')
    <BLANKLINE>
    <ul>
    <li>a</li>
    <li>b</li>
    </ul>
    <BLANKLINE>
    
    """
    
def test_li_order1():
    """
    >>> text = '''
    ... 1. a
    ... 2. b
    ... '''
    >>> print parseHtml(text, '%(body)s')
    <BLANKLINE>
    <ol>
    <li>a</li>
    <li>b</li>
    </ol>
    <BLANKLINE>
    
    """
def test_dl_1():
    """
    >>> text = '''
    ... a --
    ...     abc
    ... b --
    ...     cde
    ... '''
    >>> print parseHtml(text, '%(body)s')
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
    ... **b** --
    ...     * li
    ... '''
    >>> print parseHtml(text, '%(body)s')
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

def test_hr():
    """
    >>> text = '''
    ... * * * *
    ... ----
    ... __ __ __
    ... '''
    >>> print parseHtml(text, '%(body)s')
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
    >>> print parseHtml(text, '%(body)s')
    <BLANKLINE>
    <p>This is <a href="http://example.com/" title="Optional Title Here">Test</a>
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
    >>> print parseHtml(text, '%(body)s')
    <BLANKLINE>
    <p>This is <a href="http://example.com/" title="Optional Title Here">Test</a>
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
    >>> print parseHtml(text, '%(body)s')
    <BLANKLINE>
    <p>This is <a href="http://example.com/" title="Optional Title Here">Test</a>
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
    >>> print parseHtml(text, '%(body)s')
    <BLANKLINE>
    <p>This is <a href="http://example.com/" title="Optional Title Here">foo</a>
     .</p>
    <BLANKLINE>
    """

def test_table():
    """
    >>> text = '''
    ... || a || b || c ||
    ... || b || c || d ||
    ... '''
    >>> print parseHtml(text, '%(body)s')
    <BLANKLINE>
    <table>
    <tr><td> a </td><td> b </td><td> c </td>
    </tr>
    <tr><td> b </td><td> c </td><td> d </td>
    </tr>
    </table>
    <BLANKLINE>
    """

def test_block():
    """
    >>> text = '''
    ... [[tabs(id=hello.html)]]:
    ...     ```
    ...     This is hello
    ...     ```
    ... [[tabs(id=hello.html)]]:
    ...     ```
    ...     This is hello
    ...     ```
    ... '''
    >>> from par.bootstrap_ext import blocks
    >>> print parseHtml(text, '%(body)s', block_callback=blocks)
    <BLANKLINE>
    <div class="tabbable">
    <ul class="nav nav-tabs">
    <li class="active"><a href="#hello-html" data-toggle="tab">hello.html</a></li>
    <li><a href="#hello-html" data-toggle="tab">hello.html</a></li>
    </ul>
    <div class="tab-content">
    <div class="tab-pane active" id="hello-html">
    <pre><code>This is hello</code></pre>
    <BLANKLINE>
    </div>
    <div class="tab-pane" id="hello-html">
    <pre><code>This is hello</code></pre>
    <BLANKLINE>
    </div>
    </div>
    </div>
    """
    
def test_block():
    """
    >>> text = '''
    ... [[alert(class=info,close)]]:
    ...     This is an alert.
    ... '''
    >>> from par.bootstrap_ext import blocks
    >>> print parseHtml(text, '%(body)s', block_callback=blocks)
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
    >>> print parseHtml(text, '%(body)s')
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
    >>> print parseHtml(text, '%(body)s')
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
    >>> print parseHtml(text, '%(body)s')
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
    >>> print parseHtml(text, '%(body)s')
    <BLANKLINE>
    <pre><code>a
    b
    c</code></pre>
    <BLANKLINE>
    """
