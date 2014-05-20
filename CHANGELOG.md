Par ChangeLog
===============

1.0
---------

* Support py2&3

0.9.10
---------

* Fix table parse and tag_class bug

0.9.9
---------

* Fix missing sementic_ext.py bug

0.9.8
---------

* Add `filename` parameter to Visitor Class.
* Fix tag process `class` bug

0.9.7
---------

* Change `tag_class` process. If the tag class value starts with `+` then
  it'll combine the default class value. If not, tag class value will replace
  the default class value. For example:

  <code>
  ```class=linenums
  print 'hello, world'
  ```
  </code>

  will make pre class value `linenums`, but if you pass `tag_class = {'pre':'prettify'}`
  to parseHtml() function, it'll overwrite the `linenums`, the result will be:

  ```
  <pre class="prettify">
  ```

  But if you pass `tag_class = {'pre':'+prettify'}`, the result will be:

  ```
  <pre class="prettify linenums">
  ```

0.9.6
---------

* Fix symbol parsing bug. <code>**abc**.</code> will now `<strong>abc</strong>.`

0.9.5
---------

* Add semantic support

0.9.4
---------

* Fix list parsing bug

0.9.3
---------

* Fix table parsing bug

0.9.2
---------

* Fix definition list process and fix blanklines and blankline rendered

0.9.1
---------

* Fix list parsing bug
* definition list should be seperated by blankline

0.9
---------

* Fix performance bug

0.8
---------

* Fix refer_links parsing bug, it should be processed before visit.
* Add markdown extra PHP table, definition lists support

0.7
---------

* Add wiki_link support [[xxx]]
* Remove old block support
* Add head line id support

    ## header2 ## {#id}

* Add `~~~` code block support
* Add inner and outter anchor class
* Add header anchor notation
* Add footnote support
* Fix td parse code text bug

0.6
---------

* Fix user defined block process bug in indent text
* Refactor old user defined tag to new style
* Fix output empty string when the undefined blocks are parsed

0.5
---------

* Fix td column parse error

0.4
---------

* Add custome block tag support, in the versions before 0.4, there are already such things, you
  can define it just like:

    ```
    [[tag(arg=value)]]:
        content
    ```

  But above format looks not very simple, so I write new format, just like:

    ```
    {% tag arg=value %}
    content
    {% endtag %}

  And there are also some extend tag written before, so now you can mix them in markdown document.