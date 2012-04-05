#coding=utf8

import sys
sys.path.insert(0, '..')
from par import WikiGrammar, WikiHtmlVisitor, SimpleVisitor

template="""<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="bootstrap.min.css"/>
<link rel="stylesheet" type="text/css" href="example.css"/>
<title>%(title)s</title>
</head>
<body>
<div class="container">
%(body)s
</div>
</body>
</html>
"""

tag_class = {
    'table':'',
}

text = u"""
= Wiki语法说明 =
== 标题 ==
{{{
= 标题1 =
== 标题2 ==
=== 标题3 ===
==== 标题4 ====
===== 标题5 =====
====== 标题6 ======
}}}

== 段落 ==

使用一行或多行空行来分隔段落

== 类型 ==

|| 名字/例子 || *标记* ||
|| _italic_ || `_italic_` ||
|| *bold* || `*bold*` ||
|| `code` || {{{`code`}}} ||
|| ^super^script || `^super^script` ||
|| ,,sub,,script || `,,sub,,script` ||
|| ~~strikeout~~ || `~~strikeout~~` ||

混合效果

|| *标记* || *结果* ||
|| `_*bold* in italics_` ||_*bold* in italics_||
|| `*_italics_ in bold*` || *_italics_ in bold* ||
|| `*~~strike~~ works too*` || *~~strike~~ works too* ||
|| `~~as well as _this_ way round~~` || ~~as well as _this_ way round~~ ||

== 代码 ==

如果你有多行代码，使用多行代码标记:
 
<code>
{{{
def fib(n):
  if n == 0 or n == 1:
    return n
  else:
    # This recursion is not good for large numbers.
    return fib(n-1) + fib(n-2)
}}}
</code>

将得到:
    
{{{
def fib(n):
  if n == 0 or n == 1:
    return n
  else:
    # This recursion is not good for large numbers.
    return fib(n-1) + fib(n-2)
}}}

另外作为 `{{{}}}` 的替換，你也可以使用 `<code></code>` 来定义多行代码块，如:
    
{{{
<code>
def fib(n):
  if n == 0 or n == 1:
    return n
  else:
    # This recursion is not good for large numbers.
    return fib(n-1) + fib(n-2)
</code>
}}}

将同样得到：

<code>
def fib(n):
  if n == 0 or n == 1:
    return n
  else:
    # This recursion is not good for large numbers.
    return fib(n-1) + fib(n-2)
</code>

== 分隔线 ==

使用至少4个 `-` 符号:
    
{{{
-----
}}}

得到：

-----

== 列表 ==

列表支持有序和无序列表。一个列表必须缩近一个或多个空格。列表是可以嵌套的。

{{{
The following is:
    
  * A list
  * Of bulleted items
    # This is a numbered sublist
    # Which is done by indenting further
  * And back to the main bulleted list

 * This is also a list
 * With a single leading space
 * Notice that it is rendered
  # At the same levels
  # As the above lists.
 * Despite the different indentation levels.
}}}

将得到如下内容：

The following is:
    
  * A list
  * Of bulleted items
    # This is a numbered sublist
    # Which is done by indenting further
  * And back to the main bulleted list

 * This is also a list
 * With a single leading space
 * Notice that it is rendered
  # At the same levels
  # As the above lists.
 * Despite the different indentation levels.

== 块引用 ==

块引用用来在你的页面中强调一段特别的文本。它是用每行缩近至少一个空格的块来定义的，
如:
    
{{{
Someone once said:

  This sentence will be quoted in the future as the canonical example
  of a quote that is so important that it should be visually separate
  from the rest of the text in which it appears.
}}}

将会得到：

 This sentence will be quoted in the future as the canonical example
 of a quote that is so important that it should be visually separate
 from the rest of the text in which it appears.

== 链接 ==

|| 标记 || 结果 ||
|| `mailto:xxx@gmail.com` || mailto:xxx@gmail.com ||
|| `http://www.google.com` || http://www.google.com ||
|| `http://code.google.com/images/code_sm.png` || http://code.google.com/images/code_sm.png ||
|| `[http://code.google.com/ http://code.google.com/images/code_sm.png]` || [http://code.google.com/ http://code.google.com/images/code_sm.png] ||
|| `[http://www.google.com Google home page]` || [http://www.google.com Google home page] ||

使用js生成的图形：

{{{
http://chart.apis.google.com/chart?chs=200x125&chd=t:48.14,33.79,19.77|83.18,18.73,12.04&cht=bvg&nonsense=something_that_ends_with.png
}}}

结果为：

http://chart.apis.google.com/chart?chs=200x125&chd=t:48.14,33.79,19.77|83.18,18.73,12.04&cht=bvg&nonsense=something_that_ends_with.png

== 表格 ==

{{{
|| *Year* || *Temperature (low)* || *Temperature (high)* ||
|| 1900 || -10 || 25 ||
|| 1910 || -15 || 30 ||
|| 1920 || -10 || 32 ||
|| 1930 || _N/A_ || _N/A_ ||
|| 1940 || -2 || 40 ||
}}}

结果为:
    
|| *Year* || *Temperature (low)* || *Temperature (high)* ||
|| 1900 || -10 || 25 ||
|| 1910 || -15 || 30 ||
|| 1920 || -10 || 32 ||
|| 1930 || _N/A_ || _N/A_ ||
|| 1940 || -2 || 40 ||

"""
#text = """
#The following is:
#    
#  * A list
#  * Of bulleted items
#    # This is a numbered sublist
#    # Which is done by indenting further
#  * And back to the main bulleted list
#"""

g = WikiGrammar()

resultSoFar = []

result, rest = g.parse(text, resultSoFar=resultSoFar, skipWS=False)
#result, rest = g.parse(txt, g['paragraph'], resultSoFar=resultSoFar, skipWS=False)
#print result[0].render()

#print '====== rest ======'
#print rest
#print '====== resultSoFar ======'
#print resultSoFar[0].render()
#print '====== render ======'
#print result[0].render()
print SimpleVisitor().visit(result).encode('gbk')
#print WikiHtmlVisitor(template, tag_class).template(result)

