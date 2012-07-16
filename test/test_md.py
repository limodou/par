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
