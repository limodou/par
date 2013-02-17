Par ChangeLog
===============

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