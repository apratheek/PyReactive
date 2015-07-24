# PyReactive
Reactive Programming Module for Python 2/3.
Complete writeup at [http://pratheekadidela.in/](http://pratheekadidela.in/2015/04/06/pyreactive-a-silly-reactive-module-for-python/)

####What is Reactive Programing?
Wikipedia defines Reactive Programming as


> "In computing, reactive programming is a programming paradigm oriented around data flows and the propagation of change. This means that it should be possible to express static or dynamic data flows with ease in the programming languages used, and that the underlying execution model will automatically propagate changes through the data flow."

Look at the following code.

```python
>>>a = 5
>>>b = 8
>>>sum = a + b
>>>print(sum)
13
>>>a = 10
>>>b = 20
>>>print(sum)
13
```
There's nothing out of the ordinary here. This is regulation code. **sum** will always remain 13 no matter what **a** and **b** are changed to, because at the time of declaration, 'sum' had evaluated to 13, hence, it will stay 13.

But what if we wanted **sum** to change according to the values of **a** and **b**? Or, to put it a little more formally, what if we wanted **sum** to **SUBSCRIBE** to the two variables **a** and **b**?

--> ENTER REACTIVE PROGRAMMING

In this paradigm, variables are OBSERVED and/or SUBSCRIBED to. What I mean by **observed** is that when a value is declared, a memory location is alloted and when the value changes, the memory location is overwritten, rather than having it assigned in a new memory slot. This means that a variable can only update until it is explicitly purged. This is pretty similar to what happens with languages that expose memory locations by the usage of pointers. What I mean by **subscribed** is that another variable subscribes to the observed variables, and this colloquially means that it always has the latest value of the observed variables. The following example should clear things up. The pseudo code is:
```python
>>>a = Observe(5)
>>>b = Observe(8)
>>>sum = Subscribe(var=(a,b), op=('+',))
>>>print(sum)
13
>>>a.changeTo(10)
>>>print(sum)		#sum should change to 10+8
18
>>>b.changeTo(20)
>>>print(sum)		#sum should now become 10+20
30
```
The above example shows how reactive programming works. It observes variables, and whenever there's a subscription, it automatically computes the operation everytime there's a change in the underlying value of the variable. This example shows how beautiful code can get by utilizing this wonderful paradigm. No more redundant declarations. Declare once, use forever. Okay, I might be getting carried away now.

####The nuts and bolts (and other definitions)
The following section describes the various definitions of terms used in the module and the corresponding APIs. For all the code to work, install it first using

CAVEAT: I'd strongly recommend using virtualenv. If you haven't yet installed it, install it as follows:
```python
pip3 install virtualenv
virtualenv venv/
source venv/bin/activate
```

1. pip
```python
(venv): sudo pip3 install pyreactive
```
2. clone the code using git and
```python
(venv): cd PyReactive/
(venv): python3 setup.py install
```

After installing, use this module as:
```python
from pyreactive import *
```

#####Mutables
A mutable is any data type that can be altered in-place. The meaning of in-place is that the value is modified in the same memory location. In other words, if you're familiar with Python, the ____new____ method isn't called when its value changes. In PyReactive, ByteArray, Dict, List, Set, Observe and Subscribe are mutables.

#####Immutables
An immutable is any object/data type that cannot be altered in-place, i.e., a new instantiation takes place when it is modified. In other words, the ____new____ method is called every time the value changes. Or, once an immutable is assigned, the only way its value can be changed is by declaring a new immutable. In Python, int, str, tuple, etc. are immutables.

#####ByteArray, Dict, List, Set (BDLS)
These are bytearray, dict, list, and set on steroids. They are specific to PyReactive only and have a few overridden methods over their native equivalents. They can be accessed with the same Pythonic APIs, but whenever there's a change in their values, they begin to do some exotic things (Okay, may be not. Maybe they only check the dependencyGraph and issue callback updates to all mutables dependent on them).

Mind the __CamelCasing__ in their names, though. This is what makes them unique. The usage is as follows:
```python
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
```
#####Observe objects
Observe objects are the ones where the magic begins. In PyReactive, I've defined them as any data type that depends on only one operator, or method. In other words, they could be viewed as data types that have unary operands. Let's jump in to a few examples.

**Use Case: str, tuple, frozenset (native python data types)**
```python
>>>a = Observe('hey')
>>>b = Observe(a)
>>>b
'hey'
```
There's not much to do here, since they are immutable data types. But, although this is fairly redundant, there's a method that's allowed.

**a) len** - Holds the length of the data type
```python
>>>a = Observe('hey')
>>>leng = Observe(a, method='len')
>>>leng
3
>>>a.changeTo('hello there')
>>>leng
11
```

**Use Case: int, float, bool (native python data types)**
```python
>>>a = Observe(9)
>>>b = Observe(a)
>>>b
9
```
There are 2 methods allowed here. They are:

**a) not** - this is the LOGICAL NOT operator
```python
>>>a = Observe(2)
>>>b = Observe(a, method='not')
>>>b
False
>>>a.changeTo(0)
>>>b
True
```

**b) '~'** - this is the Ones COMPLEMENT operator
```python
>>>a = Observe(1)
>>>b = Observe(a, method='~')
>>>b
-2
>>>a.changeTo(3)
>>>b
-4
```

**Use Case: List**
```python
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

```
As you can see, every change on the list propogates in to a change on the observing object.

An Observe object also takes in an optional method. The legal keywords for the optional method are: count, reverse, sort, firstel, lastel, slice, set, len, sum, max and min.

**a) count** - always holds the number of occurrences of the value passed with the methodParameter option.
```python
>>>a = list([1,1,1,4,3,5,1,1])
>>>b = Observe(a, method='count', methodParameter=1)
>>>b	#Stores the number of 1s
5
>>>a.extend([1,1])
>>>a
[1,1,1,4,3,5,1,1,1,1]
>>>b	#Automatically updates the number of 1s
7
```

**b) reverse** - holds a copy of the reversed List
```python
>>>a = List([1,3,2])
>>>b = Observe(a, method='reverse')
>>>b
[2,3,1]
>>>a.append(9)
>>>a
[1,3,2,9]
>>>b	#holds the reverse of the list
[9,2,3,1]
```

**c) sort** - holds a copy of the sorted List
```python
>>>a = List([1,3,2])
>>>b = Observe(a, method='sort')
>>>b
[1,2,3]
>>>a.extend([-1,-9,0,8])
>>>b	#prints the sorted list
[-9,-1,0,1,2,3,8]
>>>a
[1,3,2,-1,-9,0,8]
```


**d) firstel** - holds the first element of the List
```python
>>>a = List([1,3,2])
>>>b = Observe(a, method='firstel')
>>>b
1
>>>a.insert(0,-100)
>>>b
-100
```
An example that combines sort and firstel to always holds the least element of a List
```python
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
```

**e) lastel** - always holds the last element of the List
```python
>>>a = List([1,3,2])
>>>b = Observe(a, method='lastel')
>>>b
2
>>>a.append(9)
>>>b
9
>>>a
[1,3,2,9]
```

**f) slice** - always holds the sliced part of the List. methodParameter is a tuple and can compose of PyReactive Observe Objects, e.g. methodParameter = (0, 4, 1), or (a, b), where a and b are PyReactive Observe objects. It also takes an optional step as the third argument. This needs to be an integer.
```python
>>>a
[1, 2, 3, 4]
>>>slicedList = Observe(a, method='slice', methodParameter=(0, 2))
>>>slicedList
[1, 2]
>>>a.insert(0, -1)	#Inserts -1 at 0th position
>>>slicedList
[-1, 1]
>>>a
[-1, 1, 2, 3, 4]
>>>b = Observe(0)
>>>c = Observe(2)
>>>d = Observe(a, method='slice', methodParameter=(b, c))
>>>d
[-1, 1]
>>>c.changeTo(4)
>>>d
[-1, 1, 2, 3]
```

**g) set** - holds only the unique elements of the List
```python
>>>a = List([1,3,2,2,4,1,5,2])
>>>b = Observe(a, method='set')
>>>b
{1,2,3,4,5}
>>>a.extend([5,5,5,6,7,7,6])
>>>b
{1,2,3,4,5,6,7}
```

**h) len** - holds the length of the List
```python
>>>a = List([1,2,4,3,1])
>>>length = Observe(a, method='len')
>>>length
5
>>>a.pop()
1
>>>length
4
```

**i) sum** - holds the sum of all elements of the List
```python
>>>a = List([1, 2, 3, 4])
>>>listSum = Observe(a, method='sum')
>>>listSum
10
>>>a.extend([5, 6, 7])
>>>listSum
28
```

**j) max** - holds the maximum value of the List
```python
>>>a = List([1, 2, 3, 4])
>>>listMax = Observe(a, method='max')
>>>listMax
4
>>>a.extend([5, -1, 5, 7])
>>>listMax
7
```

**k) min** - holds the minimum value of the List
```python
>>>a = List([1, 2, 3, 4])
>>>listMin = Observe(a, method='min')
>>>listMin
1
>>>a.extend([-1, -2, 5, 9, -5])
>>>listMin
-5
```

**Use Case: Dict**
```python
>>>a = Dict({1: [12,3,65], 2: [43,23,1]})
>>>b = Observe(a)
>>>a[3] = [78,54,23]
>>>b
{1: [12,3,65], 2: [43,23,1], 3: [78,54,23]}
```
A change in the underlying Dict triggers a change in the Observe object. The optional method keywords are:

**a) key** - holds the current value of the 'key' passed in as the methodParameter
```python
>>>a = Dict({1: [12,3,65], 2: [43,23,1]})
>>>b = Observe(a, method='key', methodParameter=1)
>>>b
[12,3,65]
>>>a[1] = [5,2]
>>>b
[5,2]
```

**b) len** - holds the length of the Dict
```python
>>>a = Dict({1:2, 2:3})
>>>length = Observe(a, method='len')
>>>length
2
>>>a[3] = 4
>>>length
3
```

**c) sum** - holds the sum of all the keys in the Dict
```python
>>>a = Dict({1: 2, 2: List([3, 4, 5])})
>>>dictSum = Observe(a, method='sum')
>>>dictSum
3
>>>a[4] = {4, 5, 6, 7}
>>>dictSum
7   # 1 + 2 + 4
```

**d) max** - holds the maximum of all the keys in the Dict
```python
>>>a = Dict({1: 2, 2: List([3, 4, 5])})
>>>maxDict = Observe(a, method='max')
>>>maxDict
2
>>>a[3] = [4, 5, 6, 7]
>>>maxDict
3
```

**e) min** - holds the minimum of all the keys in the Dict
```python
>>>a = Dict({1: 2, 2: List([3, 4, 5])})
>>>minDict = Observe(a, method='min')
>>>minDict
1
>>>a[-1] = {1, 2}
>>>minDict
-1
```

**Use Case: Set**
```python
>>>a = Set({1,2,3,4,1,1,4})
>>>a
Set({1,2,3,4})
>>>b = Observe(a)
>>>a.update({9})
>>>b
Set({1,2,3,4,9})
>>>a
Set({1,2,3,4,9})
```
Just like in the previous case, any change to the Set data type percolates to the Observe object.

The Observe object in this case also takes a few optional methods along with a few methodParameters. The legal keywords for the optional method are: len, difference, intersection, symmetric_difference, union, isdisjoint, issubset, issuperset, sum, max and min.

**a) len** - holds the length of the Set
```python
>>>a = Set({1,3,4,2,1})
>>>b = Observe(a, method='len')
>>>b
4
>>>a.update({5})
>>>b
5
```

**b) difference** - calculate the set difference of S1 and S2, which is the elements that are in S1 but not in S2
```python
>>>S1 = Set({1,2,3})
>>>S2 = Set({2,3,4})
>>>diff = Observe(S1, method='difference', methodParameter=S2)
>>>diff
Set({1})
>>>S1.update({5})
>>>diff
Set({1,5})
```

**c) intersection** - holds elements that have a presence in both S1 and S2
```python
>>>S1 = Set({1,2,3})
>>>S2 = Set({2,3,4})
>>>intersect = Observe(S1, method='intersection', methodParameter=S2)
>>>intersect
Set({2,3})
>>>S2.update({1})
>>>intersect
Set({1,2,3})
```

**d) symmetric_difference** - holds the set of elements which are in one of either set, but not in both
```python
>>>S1 = Set({1,2,3})
>>>S2 = Set({2,3,4})
>>>symm_diff = Observe(S1, method='symmetric_difference', methodParameter=S2)
>>>symm_diff
Set({1,4})
>>>S2.update({1})
>>>symm_diff
Set({4})
```

**e) union** - holds the merger of the two sets
```python
>>>S1 = Set({1,2,3})
>>>S2 = Set({5,7,8})
>>>union = Observe(S1, method='union', methodParameter=S2)
>>>union
Set({1,2,3,5,7,8})
>>>S1.update({0,9})
>>>union
Set({0,1,2,3,5,7,8,9})
```

**f) isdisjoint** - returns **True** if S1 is disjoint with S2, **False** otherwise
```python
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
```

**g) issubset** - returns **True** if S1 is a subset of S2, **False** otherwise
```python
>>>S1 = Set({1,2,3})
>>>S2 = Set({4,5,6})
>>>check = Observe(S1, method='issubset', methodParameter=S2)
>>>check
False
>>>S2.update({1,2,3})
>>>check
True
```

**h) issuperset** - returns **True** if S1 is superset of S2, **False** otherwise
```python
>>>S1 = Set({1,2,3})
>>>S2 = Set({4,5,6})
>>>check = Observe(S1, method='issuperset', methodParameter=S2)
>>>check
False
>>>S1.update({4,5,6})
>>>check
True
```

**i) sum** - holds the sum of all the elements in the Set
```python
>>>a = Set({1, 2, 3, 4})
>>>setSum = Observe(a, method='sum')
>>>setSum
10
>>>a.update({5})
>>>setSum
15
```

**j) max** - holds the element with the maximum value in the Set
```python
>>>a = Set({1, 2, 3, 4})
>>>setMax = Observe(a, method='max')
>>>setMax
4
>>>a.update({5})
>>>setMax
5
```

**k) min** - holds the element with the minimum value in the Set
```python
>>>a = Set({1, 2, 3, 4})
>>>setMin = Observe(a, method='min')
>>>setMin
1
>>>a.update({-1, 5})
>>>setMin
-1
```



Now, it's true that many of the above optional methods could've been made as **Subscribe** operators, but since PyReactive doesn't support parantheses yet, there's no way to ensure the precedence of set operators. To avoid ambiguity (since in this case only one operation can be performed at a time), chaining of set operations can be used to solve complex and intricate set equations.


**Use Case: ByteArray**
```python
>>>a = ByteArray('hello','UTF-8')
>>>b = Observe(a)
>>>b
bytearray(b'hello')
>>>a[0] = 120
>>>b
bytearray(b'xello')
```
Again, the change percolates to cause a change in the Observe object. The optional methods are:

**a) len** - Holds the length of the ByteArray
```python
>>>a = ByteArray('hello', 'UTF-8')
>>>length = Observe(a, method='len')
>>>a.pop()
111
>>>length
4
>>>a
bytearray(b'hell')
```

**b) count** - counts the number of occurrences of the value passed as the methodParameter in the ByteArray
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>count = Observe(a, method='count', methodParameter=b'e')
>>>count
2
>>>a.extend(b'! Evening!')
>>>count
4
```

**c) decode** - holds the decoded ByteArray according to the decoding passed as the methodParameter. There is no default decoding. methodParameter is necessary
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>decoded = Observe(a, method='decode', methodParameter='UTF-8')
>>>decoded
Hi There
>>>a.extend(b"! How are you?")
>>>decoded
Hey There! How are you?
```

**d) endswith** - holds a boolean value. Becomes True if the ByteArray ends with the parameter passed in methodParameter. methodParameter is compulsory
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>endswith = Observe(a, method='endswith', methodParameter=b'e')
>>>endswith
True
>>>a.extend(b'!')
>>>endswith
False
```

**e) find** - holds the first location of the value passed in methodParameter. Holds -1 if value is not found. methodParameter is the search parameter and is compulsory. Currently, only the first location is supported.
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>find = Observe(a, method='find', methodParameter=b'k')
>>>find
-1
>>>a.extend(b' king')
>>>find
9
```

**f) index** - holds the first location of the value passed in methodParameter. Raises ValueError if not found. methodParameter is the search parameter and is compulsory. Currently, only the first location is supported.
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>index = Observe(a, method='index', methodParameter=b'e')
>>>index
5
>>>a.replace(b'H', b'e')
>>>index
0
```

**g) isalnum** - Returns **True** if the ByteArray is **alnum**. **False** otherwise.
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>isalnum = Observe(a, method='isalnum')
>>>isalnum
False
```

**h) isalpha** - Returns **True** if the ByteArray is **alpha**. **False** otherwise.
```python
>>>a = ByteArray("Hi", "UTF-8")
>>>isalpha = Observe(a, method='isalpha')
>>>isalpha
True
```

**i) isdigit** - Returns **True** if the ByteArray is **digit**. **False** otherwise.
```python
>>>a = ByteArray("12345", "UTF-8")
>>>>isdigit = Observe(a, method='isdigit')
>>>isdigit
True
```

**j) islower** - Returns **True** if the ByteArray is **lower**. **False** otherwise.
```python
>>>a = ByteArray("hi there", "UTF-8")
>>>islower = Observe(a, method='islower')
>>>islower
True
```

**k) isupper** - Returns **True** if the ByteArray is **upper**. **False** otherwise.
```python
>>>a = ByteArray("HI THERE", "UTF-8")
>>>isupper = Observe(a, method='isupper')
>>>isupper
True
```

**l) lower** - This holds the ByteArray in its lower case
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>lower = Observe(a, method='lower')
>>>lower
bytearray(b'hi there')
```

**m) upper** - This holds the ByteArray in its upper case
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>upper = Observe(a, method='upper')
>>>upper
bytearray(b'HI THERE)
```

**n) replace** - This holds the ByteArray with the replaced byte passed in the methodParameter. methodParameter is a tuple with the first element being the byte to replace and the second element being the byte that needs to replace.
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>replace = Observe(a, method='replace', methodParameter=(b'e', b'l'))
>>>replace
bytearray(b'Hi Thlrl)
```

**o) reverse** - This holds the reversed ByteArray
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>reverse = Observe(a, method='reverse')
>>>reverse
bytearray(b'erehT iH')
```

**p) slice** - This holds the sliced ByteArray. methodParameter is a tuple and can compose of PyReactive Observe Objects, e.g. methodParameter = (0, 4, 1), or (a, b), where a and b are PyReactive Observe objects. It also takes an optional step as the third argument. This needs to be an integer.
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>a
bytearray(b'Hi There')
>>>sliced = Observe(a, method='slice'. methodParameter=(-3, -1))
>>>sliced
bytearray(b'er')
>>>a.extend(b' Again')
>>>sliced
bytearray(b'ai')
>>>a
bytearray(b'Hi There Again')
>>>b = Observe(2)
>>>c = Observe(5)
>>>sliced = Observe(a, method='slice', methodParameter=(b, c))
>>>sliced
bytearray(b' Th')
>>>c.changeTo(7)
bytearray(b' Ther')
```

**q) startswith** - Returns **True** if the ByteArray starts with the value passed in as the methodParameter. **False** otherwise.
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>startswith = Observe(a, method='startswith', methodParameter=b'H')
>>>startswith
True
```

**r) max** - This holds the maximum value in the ByteArray. Holds an integer.
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>maxBA = Observe(a, method='max')
>>>maxBA
114
```

**s) min** - This holds the minimum value in the ByteArray. Holds an integer.
```python
>>>a = ByteArray("Hi There", "UTF-8")
>>>minBA = Observe(a, method='min')
>>>minBA
32  #The UTF-8 code for blank-space in integer
```

#####Observe class methods
Each Observe object has a few fancy methods too.

**a) modifyMethod** - this method modifies the current method to something different. Also takes in an optional methodParameter that acts in tandem with the method.


```python
>>>a = List([1,3,2,4,9])
>>>b = Observe(a, method='sort')
>>>b
[1,2,3,4,9]
>>>b.modifyMethod(method='firstel')
>>>b
1
```

**b) notify** - This method needs to be overridden if you want something exotic to happen whenever the Observe object changes. Every time that the value of the object changes, the **notify** method is called. An e.g.: Let's say that we want to push the updated value via a WebSocket, all that we have to do is override the **notify** method to push the value via the WebSocket. It takes fewer lines than this description. Seriously.
```python
class ObserveSocket(Observe):
    def notify(self):
        ws.send(self)		#Where ws is the WebSocket object
```
```python
>>>a = List([1,2])
>>>b = ObserveSocket(a)
>>>a.append(9)
#The updated value of b is sent via the WebSocket
>>>
```
**c) changeTo** - this method is used to change the value of the Observe object, in case it observes an immutable data type such as **int**, **str**, etc. Like in all other cases, a change here would trigger a change in all the dependents on this object.

```python
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
```

#####Subscribe Objects

Subscribe objects are similar to Observe objects, but the difference is that they take in multiple operands and operators. Subscribe objects look and behave like mathematical equations. Let's look at the API and a few use cases.

**API:** **Subscribe(expression, name='')**

The expression is written in **INFIX** notation. The operator precedence followed is that of Python's. Once initialized, the expression is stored in the postfix notation, and hence parantheses and unary operators can be used.

If **c** is to subscribe to **a + b**, the API is:
```python
>>>c = Subscribe('a+b')     #This also follows that a and b are the name arguments of the Observe objects a and b. Otherwise, an error is thrown
```

If **result** is to subscribe to **a + b * 5 - c ** 0.87 + d - e/6**, the same API looks like this:
```python
>>>result = Subscribe('a+b*5-c**0.87+d-e/6')
```

As of this moment, the **supported binary operators** are:

1. **+** (Addition),
2. **-** (Subtraction),
3. **/** (Division),
4. __\*__ (Multiplication),
5. __\*\*__ (Exponent),
6. __%__ (Modulus),
7. __//__ (Floor Division),
8. **<<** (Binary Left Shift),
9. **>>** (Binary Right Shift),
10. **&** (Binary/Bitwise AND),
11. **|** (Binary/Bitwise OR),
12. **^** (Binary/Bitwise XOR),
13. **'and'** (Logical AND),
14. **'or'** (Logical OR).

The **supported unary operators** are:

1. **'not'** - Boolean NOT
2. **'~'** - Bitwise NOT
3. **'sin'** - math.sin (Returns the sine of the value)
4. **'cos'** - math.cos (Returns the cosine of the value)
5. **'tan'** - math.tan (Returns the tan of the value)
6. **'round'** - round (Rounds to the nearest integer; does not round to a particular precision as of yet)
7. **'ceil'** - math.ceil (Rounds to the lowest integer greater than the value)
8. **'floor'** - math.floor (Rounds to the greatest integer lower than the value)
9. **'abs'** - math.fabs (Returns the absolute value)


Additionally, one can subscribe to other data types such as ByteArrays, Lists, Dicts, Sets, Observe objects, Subscribe objects.

######Subscribe class methods
Each Subscribe object has a few fancy methods too.

**a) equation** - displays the current expression subscribed to.
```python
>>>c = Subscribe('9<<10')
>>>c
9216
>>>c.equation()
9<<10
```

**b) append** - appends variables and their corresponding operators to the existing expression. The API is same as the one used during initialization.
```python
>>>a = Observe(12, name='a')
>>>b = Observe(16, name='b')
>>>subs = Subscribe('a*b')
>>>subs
192
>>>c = Observe(20, name='c')
>>>subs.append('-c')
>>>subs
172
>>>subs.equation()
a*b-c
```

**c) notify** - Similar to the **notify** method on an **Observe** object, this method too needs to be overridden to do something meaningful. The **notify** method is called every time there's a change in the underlying value of the **Subscribe** object.
```python
>>>a = Observe(10, name='a')
>>>b = Observe(11, name='b')
>>>class SubNotify(Subscribe):
...    def notify(self):
...        if self.value > 23:
...            print("%s hit the upper limit!"%self.name)
>>>c = SubNotify('a+b', name='c')
>>>a.changeTo(11)
>>>b.changeTo(12)
>>>a.changeTo(12)
c hit the upper limit!
>>>
```

######Example Subscribe API

**Simple arithmetic**
```python
>>>a = Observe(5, name='a')
>>>b = Observe(8, name='b')
>>>c = Observe(25, name='c')
>>>sub = Subscribe('a+b*c-c/(a*b)')
>>>sub.value
204.375
>>>c.changeTo(15)
>>>sub.value
124.625
>>>sub.append('-ceil(b/a)+floor(a/b)')
>>>sub.value
122.625
```

**Trigonometric equations**
```python
>>>pi = Observe(math.pi, name='pi')
>>>alpha = Observe(2, name='alpha')
>>>beta = Observe(3, name='beta')
>>>gamma = Observe(4, name='gamma')
>>>sub = Subscribe('sin(pi/alpha) + cos(pi/beta) + tan(pi/gamma)')
>>>sub.value
2.5
>>>gamma.changeTo(6)
>>>sub.value
2.0773502691896257
>>>sub.name = 'sub'
>>>rounded = Subscribe('round(sub)')
>>>rounded.value
2
>>>ceiled = Subscribe('ceil(sub)')
>>>ceiled.value
3
>>>floored = Subscribe('floor(sub)')
>>>floored.value
2
```

#####Known Issues

a)
```python
>>>a = List([1,3,2])
>>>b = Dict({1:a})
>>>c = Observe(b)
>>>b[1].append(9)
>>>a
[1,3,2,9]
>>>b
{1: [1,3,2,9]}
>>>c
{1: [1,3,2,9]}
```
Although **c** works as expected, the change isn't triggered in c because of the change in b. So, overriding notify method of c wouldn't work in this case.
**v0.2.0 has resolved issue a). Support for deep Lists, Dicts, ByteArrays, Sets, Observe objects has been introduced. This issue still persists in all versions <= v0.1.6**

b) If an error occurs when variables are being updated, then they go out of sync. As long as no errors are thrown, the module does what it is told to. A workaround could be to isolate each updation, try to update, and commit the update when there are no errors. Will see to it in the next version.

c) There is no way to delete PyReactive objects as of now. Using **del variableName** might remove the variable from the environment, but it does not remove the dependencies. Will provide an API for deletion in the next update.


######Major Changes

- As of v0.2.3, the notify method has turned silent in case its value does not change. So, it only notifies when there's a tangible change in the value. The below example should help..

```python
>>>l = List([1, 2, 3])
>>>class Trial(Observe):
...     def notify(self):
...         print("Updated %s"%self.value)
>>>a = Trial(l, method='max')
Updated 3
>>>b = Trial(l, method='min')
Updated 1
>>>a
3
>>>b
1
>>>l.append(-1)
Updated -1
>>>b
-1
>>>l.append(4)
Updated 4
>>>a
4
>>>l.append(2.5)
>>>#No update to either a or b
```
In the above example, the notify method on **a** is called only when the **max** value in the List changes. Similarly, the notify method on **b** is called only when the **min** value in the List changes. In versions prior to 0.2.3, the notify method was called irrespective of whether its value changed. This has been altered so that no unnecessary function calls are made.

- As of v0.3.0, the Subscribe API has been altered to make it intuitive. Now accepts infix expressions as strings, parses and stores them as postfix expressions. Hence, unary, binary operators and parantheses can now be used.

######Change log

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


#####Further work:
1. Open up access to other data types and objects such as those of numpy/scipy, etc.
2. Extend this module such that user-defined operators can be included.
3. Write this using asyncio, if needed.
