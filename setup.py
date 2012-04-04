__doc__ = """
=====================
Par 
=====================

:Author: Limodou <limodou@gmail.com>

.. contents:: 

About Par
----------------

Par is a simple structured text parser project. It based on pyPEG for now. 
And pyPEG is also shipped with par.

License
------------

Plugs is released under GPL license. 

"""

from uliweb.utils.setup import setup
import par

setup(name='par',
    version=par.__version__,
    description="A simple structured text parser project",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    packages = ['par'],
    platforms = 'any',
    keywords='parser peg',
    author=par.__author__,
    author_email=par.__author_email__,
    url=par.__url__,
    license=par.__license__,
    include_package_data=True,
    zip_safe=False,
)
