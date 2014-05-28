__doc__ = """
=====================
Par 
=====================

:Author: Limodou <limodou@gmail.com>

About Par
----------------

Par is a simple structured text parser project. It based on pyPEG for now. 
And pyPEG is also shipped with par.

It support Google Code Wiki syntax and markdown syntax. And it also extends
markdown syntax, for example, it support: definition list, table, direct link, etc.

License
------------

Par is released under BSD license. 

"""

from setuptools import setup
import par

setup(name='par',
    version='1.2',
    description="A simple structured text parser project",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    packages = ['par'],
    platforms = 'any',
    keywords='parser peg',
    author='limodou',
    author_email='limodou@gmail.com',
    url='https://github.com/limodou/par',
    license='BSD',
    include_package_data=True,
    zip_safe=False,
    install_requires=['future']
)
