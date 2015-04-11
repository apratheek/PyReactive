==========
PyReactive
==========

This is a Reactive Programming Module for Python 2/3 based on callbacks.

=============
Documentation
=============
For the README and the API, visit the project's home page at `github <https://github.com/apratheek/PyReactive>`_. For the complete writeup, examples, and use cases, check out my `blog post <http://pratheekadidela.in/2015/04/06/pyreactive-a-silly-reactive-module-for-python/>`_.


Installation
^^^^^^^^^^^^
1. Install it directly as::

    $sudo pip3 install pyreactive

2. Or, clone it from github::

    $git clone https://github.com/apratheek/PyReactive.git

   And install it as::

    $cd PyReactive
    $python3 setup.py install

Usage
^^^^^
- Import the module as::

    >>>from pyreactive import *

- This gives access to List, Dict, Set, ByteArray, which are pythonic data types on steroids. The other two classes that can be used are Observe and Subscribe. ::

    >>>a = List([1,2,3])
    >>>b = Dict({1: [2,3,4], 5: [5,4,3]})
    >>>lastelement = Observe(a, method='lastel')    #Always holds the last element of list a
    >>>holdKey = Observe(b, method='key', methodParameter=1)  #Always holds the value of key:1

Methods on Observe
^^^^^^^^^^^^^^^^^^
1. ``modifyMethod(method='new_method', methodParameter='new_methodParameter')`` -

   This method takes in the new **method** and the corresponding **methodParameter** if any and triggers a corresponding change in the value of the Observe object. And every time there's a change in the underlying value, it automatically computes its value according to the mentioned method.

2. ``notify()`` -

   This method needs to be overridden when an Observe object is to notify when a condition is met. For usage, check out the `project homepage <https://github.com/apratheek/PyReactive>`_.

3. ``changeTo(value)`` -

   Changes the current value of the Observe object to the new value. This is applicable only on immutable data types such as int, float, etc.

Methods on Subscribe
^^^^^^^^^^^^^^^^^^^^

  **Usage**::


    >>>a = Subscribe(var=(b,c), op=('+',))

  **var** is the tuple of all the variables that need to be subscribed to, and **op** is the tuple of operators. The equation is parsed in the **INFIX** notation, meaning, the above subscription would be evaluated as: `a = b + c`

1. ``equation()`` -

   This returns the current equation of the Subscribe object. If the variables have names defined, then it returns the names of variables. Otherwise, it returns the values.

2. ``append(var=(newvar,), op=('newOp',))`` -

   This appends the **newvar** variable to the existing equation with the **newOp** operator. The API is similar to the __init__ API.

3. ``notify()`` -

   Again, similar to the **notify** method on Observe objects, this needs to be overridden to notify whenever a condition has been satisfied.

Change log:
-----------
**v0.1.3** - Updated pypi README in .rst (11/04/15)

**v0.1.2** - Published README not parsed on pypi (10/04/15)

**v0.1.1** - Published README in markdown (10/04/15)

**v0.1.0** - First upload (10/04/15)