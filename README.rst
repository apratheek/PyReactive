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

Usage (Observe):
^^^^^^^^^^^^^^^^
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



Usage (Subscribe):
^^^^^^^^^^^^^^^^^^
From v0.3.0, the Subscribe API has changed. The new API is far simpler and intuitive. Simply pass an infix (commonly used mathematical notation) expression and you're good to go.

        Subscribe(expression, name='')

    >>>eqn1 = Subscribe('1+2/3-(9/8)+round(7/6)')

    While subscribing to Observe objects, the latter need to have a name when initialized or the name can be set later on. Otherwise, the subscription cannot be initialized and will throw an exception.

    >>>a = Observe(2, name='a')     #>>>alpha = Observe(2, name='a') would also work.
    >>>b = Observe(3, name='b')
    >>>pi = Observe(math.pi, name='pi')     #imports math automatically as it is used behind the scenes
    >>>c = Observe(4, name='c')
    >>>eqn = Subscribe('a+b/2-c/3+sin(pi/a)')
    >>>eqn
    3.166666666666667
    >>>a.changeTo(-1)
    >>>eqn
    -0.8333333333333334
    >>>c.changeTo(9)
    >>>eqn
    -2.5
    >>>eqn.equation()       #Display the current equation
    a+b/2-c/3+sin(pi/a)
    >>>eqn.append('-cos(2*pi/a**2)+ceil(a/b)')          #Extend the equation with the new expression
    >>>eqn
    -3.5
    >>>eqn.equation()
    a+b/2-c/3+sin(pi/a)-cos(2*pi/a**2)+ceil(a/b)


Methods on Subscribe
^^^^^^^^^^^^^^^^^^^^

1. ``equation()`` -

   This returns the current equation of the Subscribe object. If the variables have names defined, then it returns the names of variables. Otherwise, it returns the values.

2. ``append(new_expression)`` -

   This appends the new_expression variable to the existing expression.

3. ``notify()`` -

   Again, similar to the **notify** method on Observe objects, this needs to be overridden to notify whenever a condition has been satisfied.

Change log:
-----------

**v0.3.2** - Updated documentation (24/07/15)

**v0.3.0** - Subscribe API has been revamped. It is now a lot more intuitive and supports generic mathematical expressions. All infix expressions are parsed and stored as postfix expressions, and hence, parantheses and unary operators are also supported. The current unary operators which are supported are sin, cos, tan, abs, floor, ceil, round. Also, the values are updated using map instead of for loops, and hence, should generally be faster (Not benchmarked, though) (24/07/15)

**v0.2.3** - Notify method is now silent in case there's no change in the value of the Observe object. It is now called only when there's an actual change to the object. Also, there's a change in the API in case of Observe objects of Lists/ByteArrays in the 'slice' method. Does not accept slice object now. Rather, accepts a tuple (start, end, step), and this tuple could also consist of other Observe objects (01/07/15)

**v0.2.2** - Added documentation for Observe class and in GitHub. Refer GitHub/Blog for full API (28/06/15)

**v0.2.1** - Removed debugging prints (25/06/15)

**v0.2.0** - Support for deep ByteArrays, Lists, Sets, Dicts, Observe, Subscribe objects. Also, lightweight tests have been written. A whole lot of methods on ByteArray have been introduced. Also, 'max' and 'min' are standard methods over ByteArrays, Lists, Dicts, Sets. Additional bug fixes - previously, 'firstel' wasn't functioning as it was intended to on Lists; now rectified. The updated API description will come up very soon (25/06/15)

**v0.1.6** - Bug fixes in method = 'lastel' and 'firstel' in Observe class over List. Originally couldn't observe on empty Lists. Now fixed (23/04/15)

**v0.1.5** - Added 'sum' on Observe over List, Dict, and Set. This always holds the sum of the underlying data type (19/04/15)

**v0.1.4** - Changed notify() call in Observe class to an appropriate location (15/04/15)

**v0.1.3** - Updated pypi README in .rst (11/04/15)

**v0.1.2** - Published README not parsed on pypi (10/04/15)

**v0.1.1** - Published README in markdown (10/04/15)

**v0.1.0** - First upload (10/04/15)
