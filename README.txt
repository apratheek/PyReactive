PyReactive
==========

Reactive Programming Module for Python 2/3. Complete writeup at
`http://pratheekadidela.in/ <http://pratheekadidela.in/2015/04/06/pyreactive-a-silly-reactive-module-for-python/>`__

What is Reactive Programing?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Wikipedia defines Reactive Programming as

    "In computing, reactive programming is a programming paradigm
    oriented around data flows and the propagation of change. This means
    that it should be possible to express static or dynamic data flows
    with ease in the programming languages used, and that the underlying
    execution model will automatically propagate changes through the
    data flow."

Look at the following code.

.. code:: python

    >>>a = 5
    >>>b = 8
    >>>sum = a + b
    >>>print(sum)
    13
    >>>a = 10
    >>>b = 20
    >>>print(sum)
    13

There's nothing out of the ordinary here. This is regulation code.
**sum** will always remain 13 no matter what **a** and **b** are changed
to, because at the time of declaration, 'sum' had evaluated to 13,
hence, it will stay 13.

But what if we wanted **sum** to change according to the values of **a**
and **b**? Or, to put it a little more formally, what if we wanted
**sum** to **SUBSCRIBE** to the two variables **a** and **b**?

--> ENTER REACTIVE PROGRAMMING

In this paradigm, variables are OBSERVED and/or SUBSCRIBED to. What I
mean by **observed** is that when a value is declared, a memory location
is alloted and when the value changes, the memory location is
overwritten, rather than having it assigned in a new memory slot. This
means that a variable can only update until it is explicitly purged.
This is pretty similar to what happens with languages that expose memory
locations by the usage of pointers. What I mean by **subscribed** is
that another variable subscribes to the observed variables, and this
colloquially means that it always has the latest value of the observed
variables. The following example should clear things up. The pseudo code
is:

.. code:: python

    >>>a = Observe(5)
    >>>b = Observe(8)
    >>>sum = Subscribe(var=(a,b), op=('+',))
    >>>print(sum)
    13
    >>>a.changeTo(10)
    >>>print(sum)       #sum should change to 10+8
    18
    >>>b.changeTo(20)
    >>>print(sum)       #sum should now become 10+20
    30

The above example shows how reactive programming works. It observes
variables, and whenever there's a subscription, it automatically
computes the operation everytime there's a change in the underlying
value of the variable. This example shows how beautiful code can get by
utilizing this wonderful paradigm. No more redundant declarations.
Declare once, use forever. Okay, I might be getting carried away now.

The nuts and bolts (and other definitions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following section describes the various definitions of terms used in
the module and the corresponding APIs. For all the code to work, install
it first using

CAVEAT: I'd strongly recommend using virtualenv. If you haven't yet
installed it, install it as follows:

.. code:: python

    pip3 install virtualenv
    virtualenv venv/
    source venv/bin/activate

1. pip

   .. code:: python

       (venv): sudo pip3 install pyreactive

2. clone the code using git and

   .. code:: python

       (venv): cd PyReactive/
       (venv): python3 setup.py install

After installing, use this module as:

.. code:: python

    from pyreactive import *

Mutables
''''''''

A mutable is any data type that can be altered in-place. The meaning of
in-place is that the value is modified in the same memory location. In
other words, if you're familiar with Python, the \_\_\_\_new\_\_\_\_
method isn't called when its value changes. In PyReactive, ByteArray,
Dict, List, Set, Observe and Subscribe are mutables.

Immutables
''''''''''

An immutable is any object/data type that cannot be altered in-place,
i.e., a new instantiation takes place when it is modified. In other
words, the \_\_\_\_new\_\_\_\_ method is called every time the value
changes. Or, once an immutable is assigned, the only way its value can
be changed is by declaring a new immutable. In Python, int, str, tuple,
etc. are immutables.

ByteArray, Dict, List, Set (BDLS)
'''''''''''''''''''''''''''''''''

These are bytearray, dict, list, and set on steroids. They are specific
to PyReactive only and have a few overridden methods over their native
equivalents. They can be accessed with the same Pythonic APIs, but
whenever there's a change in their values, they begin to do some exotic
things (Okay, may be not. Maybe they only check the dependencyGraph and
issue callback updates to all mutables dependent on them).

Mind the **CamelCasing** in their names, though. This is what makes them
unique. The usage is as follows:

.. code:: python

    >>>a = List([1,3,2])
    >>>a[0]
    1
    >>>b = Dict({1:a, 2:[3,2,1,3]})
    >>>b[2]
    [3,2,1,3]
    >>>c = Set({1,2,3,1,2,4,2,1})
    >>>c
    {1,2,3,4}
    >>>d = ByteArray('hello', 'UTF-8')
    >>>d
    bytearray(b'hello')

Observe objects
'''''''''''''''

Observe objects are the ones where the magic begins. In PyReactive, I've
defined them as any data type that depends on only one operator, or
method. In other words, they could be viewed as data types that have
unary operands. Let's jump in to a few examples.

**Use Case: str, tuple, frozenset (native python data types)**

.. code:: python

    >>>a = Observe('hey')
    >>>b = Observe(a)
    >>>b
    'hey'

There's not much to do here, since they are immutable data types. But,
although this is fairly redundant, there's a method that's allowed.

**a) len** - Holds the length of the data type

.. code:: python

    >>>a = Observe('hey')
    >>>leng = Observe(a, method='len')
    >>>leng
    3
    >>>a.changeTo('hello there')
    >>>leng
    11

**Use Case: int, float, bool (native python data types)**

.. code:: python

    >>>a = Observe(9)
    >>>b = Observe(a)
    >>>b
    9

There are 2 methods allowed here. They are:

**a) not** - this is the LOGICAL NOT operator

.. code:: python

    >>>a = Observe(2)
    >>>b = Observe(a, method='not')
    >>>b
    False
    >>>a.changeTo(0)
    >>>b
    True

**b) '~'** - this is the Ones COMPLEMENT operator

.. code:: python

    >>>a = Observe(1)
    >>>b = Observe(a, method='~')
    >>>b
    -2
    >>>a.changeTo(3)
    >>>b
    -4

**Use Case: List**

.. code:: python

    >>>a = List([1,3,2])
    >>>b = Observe(a)
    >>>b
    [1,3,2]
    >>>a.append(9)
    >>>b
    [1,3,2,9]
    >>>a.insert(0,-20)
    >>>b
    [-20,1,3,2,9]

As you can see, every change on the list propogates in to a change on
the observing object.

An Observe object also takes in an optional method. The legal keywords
for the optional method are: count, reverse, sort, firstel, lastel,
slice and set.

**a) count** - always holds the number of occurrences of the value
passed with the methodParameter option.

.. code:: python

    >>>a = list([1,1,1,4,3,5,1,1])
    >>>b = Observe(a, method='count', methodParameter=1)
    >>>b    #Stores the number of 1s
    5
    >>>a.extend([1,1])
    >>>a
    [1,1,1,4,3,5,1,1,1,1]
    >>>b    #Automatically updates the number of 1s
    7

**b) reverse** - holds a copy of the reversed List

.. code:: python

    >>>a = List([1,3,2])
    >>>b = Observe(a, method='reverse')
    >>>b
    [2,3,1]
    >>>a.append(9)
    >>>a
    [1,3,2,9]
    >>>b    #holds the reverse of the list
    [9,2,3,1]

**c) sort** - holds a copy of the sorted List

.. code:: python

    >>>a = List([1,3,2])
    >>>b = Observe(a, method='sort')
    >>>b
    [1,2,3]
    >>>a.extend([-1,-9,0,8])
    >>>b    #prints the sorted list
    [-9,-1,0,1,2,3,8]
    >>>a
    [1,3,2,-1,-9,0,8]

**d) firstel** - holds the first element of the List

.. code:: python

    >>>a = List([1,3,2])
    >>>b = Observe(a, method='firstel')
    >>>b
    1
    >>>a.insert(0,-100)
    >>>b
    -100

An example that combines sort and firstel to always holds the least
element of a List

.. code:: python

    >>>a = List([1,3,2])
    >>>b = Observe(a, method='sort')
    >>>leastEl = Observe(b, method='firstel')
    >>>leastEl
    1
    >>>a.append(-9)
    >>>leastEl
    -9
    >>>a
    [1,3,2,-9]
    >>>b
    [-9,1,2,3]

**e) lastel** - always holds the last element of the List

.. code:: python

    >>>a = List([1,3,2])
    >>>b = Observe(a, method='lastel')
    >>>b
    2
    >>>a.append(9)
    >>>b
    9
    >>>a
    [1,3,2,9]

**f) slice** - holds the sliced List, with the methodParameter being a
slice object

.. code:: python

    >>>a = List([1,3,2,4,1])
    >>>b = Observe(a, method='slice', methodParameter=slice(0,3))
    >>>b
    [1,3,2]
    >>>a.insert(0,-4)
    >>>b
    [-4,1,3]

**g) set** - holds only the unique elements of the List

.. code:: python

    >>>a = List([1,3,2,2,4,1,5,2])
    >>>b = Observe(a, method='set')
    >>>b
    {1,2,3,4,5}
    >>>a.extend([5,5,5,6,7,7,6])
    >>>b
    {1,2,3,4,5,6,7}

**h) len** - holds the length of the List

.. code:: python

    >>>a = List([1,2,4,3,1])
    >>>length = Observe(a, method='len')
    >>>length
    5
    >>>a.pop()
    1
    >>>length
    4

**Use Case: Dict**

.. code:: python

    >>>a = Dict({1: [12,3,65], 2: [43,23,1]})
    >>>b = Observe(a)
    >>>a[3] = [78,54,23]
    >>>b
    {1: [12,3,65], 2: [43,23,1], 3: [78,54,23]}

A change in the underlying Dict triggers a change in the Observe object.
The optional method keywords are:

**a) key** - holds the current value of the 'key' passed in as the
methodParameter

.. code:: python

    >>>a = Dict({1: [12,3,65], 2: [43,23,1]})
    >>>b = Observe(a, method='key', methodParameter=1)
    >>>b
    [12,3,65]
    >>>a[1] = [5,2]
    >>>b
    [5,2]

**b) len** - holds the length of the Dict

.. code:: python

    >>>a = Dict({1:2, 2:3})
    >>>length = Observe(a, method='len')
    >>>length
    2
    >>>a[3] = 4
    >>>length
    3

**Use Case: Set**

.. code:: python

    >>>a = Set({1,2,3,4,1,1,4})
    >>>a
    Set({1,2,3,4})
    >>>b = Observe(a)
    >>>a.update({9})
    >>>b
    Set({1,2,3,4,9})
    >>>a
    Set({1,2,3,4,9})

Just like in the previous case, any change to the Set data type
percolates to the Observe object.

The Observe object in this case also takes a few optional methods along
with a few methodParameters. The legal keywords for the optional method
are: len, difference, intersection, symmetric\_difference, union,
isdisjoint, issubset, issuperset.

**a) len** - holds the length of the Set

.. code:: python

    >>>a = Set({1,3,4,2,1})
    >>>b = Observe(a, method='len')
    >>>b
    4
    >>>a.update({5})
    >>>b
    5

**b) difference** - calculate the set difference of S1 and S2, which is
the elements that are in S1 but not in S2

.. code:: python

    >>>S1 = Set({1,2,3})
    >>>S2 = Set({2,3,4})
    >>>diff = Observe(S1, method='difference', methodParameter=S2)
    >>>diff
    Set({1})
    >>>S1.update({5})
    >>>diff
    Set({1,5})

**c) intersection** - holds elements that have a presence in both S1 and
S2

.. code:: python

    >>>S1 = Set({1,2,3})
    >>>S2 = Set({2,3,4})
    >>>intersect = Observe(S1, method='intersection', methodParameter=S2)
    >>>intersect
    Set({2,3})
    >>>S2.update({1})
    >>>intersect
    Set({1,2,3})

**d) symmetric\_difference** - holds the set of elements which are in
one of either set, but not in both

.. code:: python

    >>>S1 = Set({1,2,3})
    >>>S2 = Set({2,3,4})
    >>>symm_diff = Observe(S1, method='symmetric_difference', methodParameter=S2)
    >>>symm_diff
    Set({1,4})
    >>>S2.update({1})
    >>>symm_diff
    Set({4})

**e) union** - holds the merger of the two sets

.. code:: python

    >>>S1 = Set({1,2,3})
    >>>S2 = Set({5,7,8})
    >>>union = Observe(S1, method='union', methodParameter=S2)
    >>>union
    Set({1,2,3,5,7,8})
    >>>S1.update({0,9})
    >>>union
    Set({0,1,2,3,5,7,8,9})

**f) isdisjoint** - returns **True** if S1 is disjoint with S2,
**False** otherwise

.. code:: python

    >>>S1 = Set({1,2,3})
    >>>S2 = Set({4,5,6})
    >>>check = Observe(S1, method='isdisjoint', methodParameter=S2)
    >>>check
    True
    >>>S2.update({3})
    >>>check
    False
    >>>S1.remove(3)
    >>>check
    True

**g) issubset** - returns **True** if S1 is a subset of S2, **False**
otherwise

.. code:: python

    >>>S1 = Set({1,2,3})
    >>>S2 = Set({4,5,6})
    >>>check = Observe(S1, method='issubset', methodParameter=S2)
    >>>check
    False
    >>>S2.update({1,2,3})
    >>>check
    True

**h) issuperset** - returns **True** if S1 is superset of S2, **False**
otherwise

.. code:: python

    >>>S1 = Set({1,2,3})
    >>>S2 = Set({4,5,6})
    >>>check = Observe(S1, method='issuperset', methodParameter=S2)
    >>>check
    False
    >>>S1.update({4,5,6})
    >>>check
    True

Now, it's true that all the above optional methods could've been made as
**Subscribe** operators, but since PyReactive doesn't support
parantheses yet, there's no way to ensure the precedence of set
operators. To avoid ambiguity (since in this case only one operation can
be performed at a time), chaining of set operations can be used to solve
complex and intricate set equations.

**Use Case: ByteArray**

.. code:: python

    >>>a = ByteArray('hello','UTF-8')
    >>>b = Observe(a)
    >>>b
    bytearray(b'hello')
    >>>a[0] = 120
    >>>b
    bytearray(b'xello')

Again, the change percolates to a change in the Observe object. The
optional methods are:

**a) len** - Holds the length of the ByteArray

.. code:: python

    >>>a = ByteArray('hello', 'UTF-8')
    >>>length = Observe(a, method='len')
    >>>a.pop()
    111
    >>>length
    4
    >>>a
    bytearray(b'hell')

Observe class methods
'''''''''''''''''''''

Each Observe object has a few fancy methods too.

**a) modifyMethod** - this method modifies the current method to
something different. Also takes in an optional methodParameter that acts
in tandem with the method.

.. code:: python

    >>>a = List([1,3,2,4,9])
    >>>b = Observe(a, method='sort')
    >>>b
    [1,2,3,4,9]
    >>>b.modifyMethod(method='firstel')
    >>>b
    1

**b) notify** - This method needs to be overridden if you want something
exotic to happen whenever the Observe object changes. Every time that
the value of the object changes, the **notify** method is called. An
e.g.: Let's say that we want to push the updated value via a WebSocket,
all that we have to do is override the **notify** method to push the
value via the WebSocket. It takes fewer lines than this description.
Seriously.

.. code:: python

    class ObserveSocket(Observe):
        def notify(self):
            ws.send(self)       #Where ws is the WebSocket object

.. code:: python

    >>>a = List([1,2])
    >>>b = ObserveSocket(a)
    >>>a.append(9)
    #The updated value of b is sent via the WebSocket
    >>>

**c) changeTo** - this method is used to change the value of the Observe
object, in case it observes an immutable data type such as **int**,
**str**, etc. Like in all other cases, a change here would trigger a
change in all the dependents on this object.

.. code:: python

    >>>a = Observe(9)
    >>>a
    9
    >>>a.changeTo(19)
    >>>a
    19
    >>>b = Observe(a)
    >>>b
    19
    >>>a.changeTo(10)
    >>>b
    10
    >>>b.changeTo(1000)
    InvalidSubscriptionError: changeTo method not permitted on mutables.

Subscribe Objects
'''''''''''''''''

Subscribe objects are similar to Observe objects, but the only
difference is that they take in multiple operands and operators.
Subscribe objects look and behave like mathematical equations. Let's
look at the API and a few use cases.

**API:** **SubscribeObject = Subscribe(var=(var1, var2,...),
op=('+','-',....))**

**var** is a tuple of all the operands and **op** is a tuple of all the
operators (in quotes). The equation is written in **INFIX** notation,
which is geek speak for normal representation of mathematical equations.
The operator precedence followed is that of Python's.

If **c** is to subscribe to **a + b**, the API is:

.. code:: python

    >>>c = Subscribe(var=(a,b), op=('+',))

If **result** is to subscribe to **a + b \* 5 - c ** 0.87 + d - e/6\*\*,
the same API looks like this:

.. code:: python

    >>>result = Subscribe(var=(a,b,5,c,0.87,d,e,6), op=('+','*','-','**','+','-','/'))

As of this moment, the **supported operators** are: > 1. **+**
(Addition), 2. **-** (Subtraction), 3. **/** (Division), 4. **\***
(Multiplication), 5. **\*\*** (Exponent), 6. **%** (Modulus), 7. **//**
(Floor Division), 8. **<<** (Binary Left Shift), 9. **>>** (Binary Right
Shift), 10. **&** (Binary/Bitwise AND), 11. **\|** (Binary/Bitwise OR),
12. **^** (Binary/Bitwise XOR), 13. **'and'** (Logical AND), 14.
**'or'** (Logical OR).

Additionally, one can subscribe to other data types such as ByteArrays,
Lists, Dicts, Sets, Observe objects, Subscribe objects.

Subscribe class methods
                       

Each Subscribe object has a few fancy methods too.

**a) equation** - displays the current equation subscribed to. If the
name of the variable is set, the corresponding names are shown.
Otherwise, the value is displayed.

.. code:: python

    >>>a = Observe(9)
    >>>b = Observe(10)
    >>>c = Subscribe(var=(a,b), op=('<<',))
    >>>c
    9216
    >>>c.equation()
    ' 9 << 10 '

**b) append** - appends variables and their corresponding operators to
the existing equation. The API is same as the one used during
initialization.

.. code:: python

    >>>a = Observe(12)
    >>>b = Observe(16)
    >>>subs = Subscribe(var=(a,b), op=('*',))
    >>>subs
    192
    >>>c = Observe(20)
    >>>subs.append(var=(c,), op=('-',))
    >>>subs
    172
    >>>subs.equation()
    ' 12 * 16 - 20 '

**c) notify** - Similar to the **notify** method on an **Observe**
object, this method too needs to be overridden to do something
meaningful. The **notify** method is called every time there's a change
in the underlying value of the **Subscribe** object.

.. code:: python

    >>>a = Observe(10)
    >>>b = Observe(11)
    >>>class SubNotify(Subscribe):
        def notify(self):
            if self.value > 23:
                print("Value hit the upper limit!")
    >>>c = SubNotify(var=(a,b), op=('+',))
    >>>a.changeTo(11)
    >>>b.changeTo(12)
    >>>a.changeTo(12)
    Value hit the upper limit!
    >>>

Known Issues
''''''''''''

a) .. code:: python

       >>>a = List([1,3,2])
       >>>b = Dict({1:a})
       >>>c = Observe(b)
       >>>b[1].append(9)
       >>>a
       [1,3,2,9]
       >>>b
       {1: [1,3,2,9]}
       >>>c
       {1: [1,3,2,9}

   Although **c** works as expected, the change isn't triggered in c
   because of the change in b. So, overriding onchange method of c
   wouldn't work in this case. Will issue an update very soon.

Further work:
'''''''''''''

1. Open up access to other data types and objects such as those of
   numpy/scipy, etc.
2. Extend this module such that user-defined operators can be included.
3. Write this using asyncio, if needed.
