import uuid
import math
from .mutables import *

dependencyGraph = {}						#Define a central dependency graph that holds all relations between mutables
idVariableDict = {}							#Define a dictionary that maps uuids to the relevant object eg: idVariableDict[self.id] = self
immutableList = []							#Define a list that holds all the immutables, and the changeTo() method is available on items that are present in this list. This ensures that the changeTo() method can be limited to immutables only.

##################################################################################################################################################################################
#Override certain methods of data types imported from mutables

class List(List):
    def __init__(self, args):
        self.id = uuid.uuid4()
        dependencyGraph[self.id] = []
        idVariableDict[self.id] = self
        ##print(args)



        self.subLevelList = args[:]		#List that consists of all elements one level below the current level
        self.allDependencies = []		#List that holds all the dependencies
        #for i in args:
        while self.subLevelList:
            #Need to recursively resolve dependencies
            #Try: i.id --> if it passes, i is a PyReactive Object. If it throws an error, i is a normal data type

            #print("self.subLevelList is %s"%self.subLevelList)

            if isinstance(self.subLevelList[0], (ByteArray, Dict, List, Set)):
                #print("Object is BDLS")
                #This has id, but no .value attribute
                #Open this node and search if it depends on other lists
                self.allDependencies.append(self.subLevelList[0].id)
                for element in self.subLevelList[0]:
                    if isinstance(element, (ByteArray, Dict, List, Set, Observe, Subscribe)):
                        self.allDependencies.append(element.id)
                        self.subLevelList.append(element)

                self.subLevelList.pop(0)

            elif isinstance(self.subLevelList[0], (Observe, Subscribe)):
                #print("Object is Observe/Subscribe")
                #This has id and .value attribute
                #This needs to be pondered over. Would there be cases where there are nested Observe/Subscribe objects?
                self.allDependencies.append(self.subLevelList[0].id)
                self.subLevelList.pop(0)

            else:
                #This is a normal object. Discard it from the list
                #Need to dig deeper here. If the object is a list, which consists of BDSL, can't drop it. Need to change this behavior

                if isinstance(self.subLevelList[0], (list, dict, bytearray, set)):
                    #THere's a chance that an element inside this object could be of BDLS. Hence, open this object and tack them to the end of self.subLevelList so that when they appear as fundamental python datatypes, they can be ignored right in this else block.
                    for element in self.subLevelList[0]:
                        #print("element in ELSE is %s"%element)
                        self.subLevelList.append(element)

                #print("Python Object. Discarding it")
                self.subLevelList.pop(0)
                #pass


            #try:
                #Check if i is a PyReactive object. Use the isinstance method instead of a try catch.
            #	if self.subLevelList[0].id in dependencyGraph:
                    #This is a PyReactive Object. Recursively, resolve its dependencies
            #		#print("PyReactive Object")

                    #Open the node and search it for other PyReactive Objects.

                    #Here, check if self.subLevelList[0] is BDSL or an Observe object or a Subscribe object
            #except:
                #The element is neither BDLS nor Observe/Subscribe. Hence, discard it
            #	self.subLevelList.pop(0)
            ##print(i)
        #dependencyGraph[self.id] = self.allDependencies[:]

        for i in self.allDependencies:
            dependencyGraph[i].append(self.id)

        super(List, self).__init__(args)
        #At __init__, set up an entry in the dependencyGraph

        ##print(dependencyGraph)
        ###print("List initialised")

    def onchange(self):
        ##print("List object has changed --> onchange method called")
        for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
            try:
                #When element is Observe/Subscribe
                idVariableDict[element].update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
            except:
                #When element is BDLS
                idVariableDict[element].onchange()


class Dict(Dict):
    def __init__(self, args):

        #At __init__, set up an entry in the dependencyGraph
        self.id = uuid.uuid4()
        dependencyGraph[self.id] = []
        idVariableDict[self.id] = self


        #####################################
        #In dicts, keys cannot be set/list/dict/bytearray. Store all the values in self.subLevelList. Then run the search, because it would then be similar to a search on a List.
        #####################################

        ##print("args are %s"%args)

        self.subLevelList = []

        for key in args:
            self.subLevelList.append(args[key])
            #Push all the values in a key:value pair to a list.

        #self.subLevelList = dict(args)		#List that consists of all elements one level below the current level
        self.allDependencies = []		#List that holds all the dependencies
        #for i in args:
        while self.subLevelList:
            #Need to recursively resolve dependencies
            #Try: i.id --> if it passes, i is a PyReactive Object. If it throws an error, i is a normal data type

            #print("self.subLevelList is %s"%self.subLevelList)

            if isinstance(self.subLevelList[0], (ByteArray, Dict, List, Set)):
                #print("Object is BDLS")
                #This has id, but no .value attribute
                #Open this node and search if it depends on other lists
                self.allDependencies.append(self.subLevelList[0].id)
                for element in self.subLevelList[0]:
                    if isinstance(element, (ByteArray, Dict, List, Set, Observe, Subscribe)):
                        self.allDependencies.append(element.id)
                        self.subLevelList.append(element)

                self.subLevelList.pop(0)

            elif isinstance(self.subLevelList[0], (Observe, Subscribe)):
                #print("Object is Observe/Subscribe")
                #This has id and .value attribute
                #This needs to be pondered over. Would there be cases where there are nested Observe/Subscribe objects?
                self.allDependencies.append(self.subLevelList[0].id)
                self.subLevelList.pop(0)

            else:
                #This is a normal object. Discard it from the list
                #Need to dig deeper here. If the object is a list, which consists of BDSL, can't drop it. Need to change this behavior

                if isinstance(self.subLevelList[0], (list, dict, bytearray, set)):
                    #THere's a chance that an element inside this object could be of BDLS. Hence, open this object and tack them to the end of self.subLevelList so that when they appear as fundamental python datatypes, they can be ignored right in this else block.
                    for element in self.subLevelList[0]:
                        #print("element in ELSE is %s"%element)
                        self.subLevelList.append(element)

                #print("Python Object. Discarding it")
                self.subLevelList.pop(0)

        for i in self.allDependencies:
            dependencyGraph[i].append(self.id)

        super(Dict, self).__init__(args)

    def onchange(self):
        ##print("List object has changed --> onchange method called")
        for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
            try:
                #When element is Observe/Subscribe
                idVariableDict[element].update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
            except:
                #When element is BDLS
                idVariableDict[element].onchange()


class Set(Set):
    def __init__(self, args):
        super(Set, self).__init__(args)
        #At __init__, set up an entry in the dependencyGraph
        self.id = uuid.uuid4()
        dependencyGraph[self.id] = []
        idVariableDict[self.id] = self

    def onchange(self):
        for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
            try:
                idVariableDict[element].update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
            except:
                #When element is BDLS
                idVariableDict[element].onchange()


class ByteArray(ByteArray):
    def __init__(self, *args):
        super(ByteArray, self).__init__(*args)
        #At __init__, set up an entry in the dependencyGraph
        self.id = uuid.uuid4()
        dependencyGraph[self.id] = []
        idVariableDict[self.id] = self


    def onchange(self):
        ##print("List object has changed --> onchange method called")
        for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
            try:
                #When element is Observe/Subscribe
                idVariableDict[element].update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
            except:
                #When element is BDLS
                idVariableDict[element].onchange()

##################################################################################################################################################################################

class InvalidSubscriptionError(Exception):
    """Special Exception that inherits from Base Exception class. Does nothing but raise a relevant exception"""
    pass

class Observe:
    """Deals with all observables
        Takes the dependency, an optional name for the object, an optional method, and an optional method parameter.
        The optional methods are:

        1. In case of List

            For all the examples below, the common List that is used is as follows:

            >>>a = List([1, 2, 3, 4])	#This is the standard data structure that's assumed to be in memory before every individual operation. All the examples below are independent of each other (for this example)

            a) count - holds the count of the element passed as the methodParameter

                >>>a
                [1, 2, 3, 4]
                >>>count = Observe(a, method='count', methodParameter=1)
                >>>count
                1
                >>>a.append(1)
                >>>count
                2

            b) reverse - holds the reverse of the List. methodParameter is not applicable

                >>>a
                [1, 2, 3, 4]
                >>>reverseList = Observe(a, method='reverse')
                >>>reverseList
                [4, 3, 2, 1]
                >>>a.extend([7])
                >>>reverseList
                [7, 4, 3, 2, 1]

            c) lastel - always holds the last element of the List. methodParameter is not applicable

                >>>a
                [1, 2, 3, 4]
                >>>lastelement = Observe(a, method='lastel')
                >>>lastelement
                4
                >>>a.append()

            d) firstel - always holds the first element of the list. methodParameter is not applicable

                >>>a
                [1, 2, 3, 4]
                >>>firstelement = Observe(a, method='firstel')
                >>>firstelement
                1

            e) sort - always holds the sorted List. methodParameter could be the sort key

                >>>a
                [1, 2, 3, 4,]
                >>>sortedList = Observe(a, method='sort')
                >>>sortedList
                [1, 2, 3, 4]
                >>>a. extend([-1, -5, 8, 10, -20])
                >>>sortedList
                [-20, -5, -1, 1, 2, 3, 4, 8, 10]

            f) slice - always holds the sliced part of the List. methodParameter is a tuple and can compose of PyReactive Observe Objects, e.g. methodParameter = (0, 4, 1), or (a, b), where a and b are PyReactive Observe objects. It also takes in an optional step as the third argument. This needs to be an integer.

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

            g) set - always holds the unique elements in the List. methodParameter is not applicable

                >>>a
                [1, 2, 3, 4]
                >>>makeSet = Observe(a, method='set')
                >>>makeSet
                {1, 2, 3, 4}
                >>>a.extend([1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4])
                >>>makeSet
                {1, 2, 3, 4}

            h) len - always holds the length of the List. methodParameter is not applicable

                >>>a
                [1, 2, 3, 4]
                >>>listLength = Observe(a, method='len')
                >>>listLength
                4
                >>>a.extend([4, 5, 6, 7])
                >>>listLength
                8

            i) sum - always holds the sum of the elements in the List. methodParameter is not applicable

                >>>a
                [1, 2, 3, 4]
                >>>listSum = Observe(a, method='sum')
                >>>listSum
                10
                >>>a.extend([5, 6, 7])
                >>>listSum
                28

            j) max - always holds the maximum value of the List. methodParameter is not applicable

                >>>a
                [1, 2, 3, 4]
                >>>listMax = Observe(a, method='max')
                >>>listMax
                4
                >>>a.extend([5, -1, 5, 7])
                >>>listMax
                7

            k) min - always holds the minimum value of the List. methodParameter is not applicable

                >>>a
                [1, 2, 3, 4]
                >>>listMin = Observe(a, method='min')
                >>>listMin
                1
                >>>a.extend([-1, -2, 5, 9, -5])
                >>>listMin
                -5

        2. In case of Set

            For all the examples below, the common Set that is used is as follows:

            >>>a = Set({1, 2, 3, 4})

            a) len - always holds the current length of the Set. methodParameter is not applicable

                >>>a
                {1, 2, 3, 4}
                >>>setLength = Observe(a, method='len')
                >>>setLength
                4
                >>>a.update({5})
                >>>setLength
                5

            b) difference - always holds the difference between two Sets. methodParameter is the Set with which the difference needs to be calculated

                >>>set1 = Set({1, 2, 3, 4})
                >>>set2 = Set({4, 5, 6, 7})
                >>>diff = Observe(set1, method='difference', methodParameter=set2)
                >>>diff
                Set({1, 2, 3})
                >>>set1.update({8})
                >>>diff
                Set({1, 2, 3, 4, 8})

            c) intersection - always holds the intersection of two Sets. methodParameter is the Set with which the intersection needs to be calculated

                >>>set1 = Set({1, 2, 3, 4})
                >>>set2 = Set({4, 5, 6, 7})
                >>>intersection = Observe(set1, method='intersection', methodParameter=set2)
                >>>intersection
                Set({4})
                >>>set1.update({5})
                >>>intersection
                Set({4, 5})

            d) isdisjoint - boolean value which denotes if the two sets are disjoint. methodParameter is the Set with which the boolean value needs to be calculated

                >>>set1 = Set({1, 2, 3, 4})
                >>>set2 = Set({4, 5, 6, 7})
                >>>isdisjoint = Observe(set1, method='isdisjoint', methodParameter=set2)
                >>>isdisjoint
                False
                >>>set1.remove(4)
                >>>isdisjoint
                True

            e) issubset - boolean value which denotes if one Set is subset of the other. methodParameter is the Set with which the boolean value needs to be calculated

                >>>set1 = Set({1, 2, 3, 4})
                >>>set2 = Set({1, 2, 3, 4, 5, 6, 7})
                >>>issubset = Observe(set1, method='issubset', methodParameter=set2)
                >>>issubset
                True

            f) issuperset - boolean value which denotes which one Set is superset of the other. methodParameter is the Set with which the boolean value needs to be calculated

                >>>set1 = Set({1, 2, 3, 4})
                >>>set2 = Set({1, 2, 3, 4, 5, 6, 7})
                >>>issuperset = Observe(set1, method='issuperset', methodParameter=set2)
                >>>issuperset
                False

            g) symmetric_difference - always holds the symmetric difference of the two Sets. methodParameter is the Set with which the symmetric difference needs to be calculated

                >>>set1 = Set({1, 2, 3, 4})
                >>>set2 = Set({1, 2, 3, 4, 5, 6, 7})
                >>>symm_diff = Observe(set1, method='symmetric_difference', methodParameter=set2)
                >>>symm_diff
                Set({5, 6, 7})

            h) union - always holds the union of the two Sets. methodParameter is the Set with which the union needs to be calculated

                >>>set1 = Set({1, 2, 3, 4})
                >>>set2 = Set({1, 2, 3, 4, 5, 6, 7})
                >>>union = Observe(set1, method='union', methodParameter=set2)
                >>>union
                Set({1, 2, 3, 4, 5, 6, 7})
                >>>set2. remove(6)
                >>>union
                Set({1, 2, 3, 4, 5, 7})

            i) sum - holds the sum of all elements in the Set. methodParameter is not applicable

                >>>a = Set({1, 2, 3, 4})
                >>>setSum = Observe(a, method='sum')
                >>>setSum
                10
                >>>a.update({5})
                >>>setSum
                15

            j) max - holds the element with the maximum value in the Set. methodParameter is not applicable

                >>>a = Set({1, 2, 3, 4})
                >>>setMax = Observe(a, method='max')
                >>>setMax
                4
                >>>a.update({5})
                >>>setMax
                5

            k) min - holds the element with the minimum value in the Set. methodParameter is not applicable

                >>>a = Set({1, 2, 3, 4})
                >>>setMin = Observe(a, method='min')
                >>>setMin
                1
                >>>a.update({-1, 5})
                >>>setMin
                -1

        3. In case of Dict

            For all the examples below, the common Dict that is used is as follows:

            >>>a = Dict({1: 2, 2: List([3, 4, 5])})

            a) key - holds the current value of the key. methodParameter is one of the keys of the Dict

                >>>a = Dict({1: 2, 2: List([3, 4, 5])})
                >>>a
                {1: 2, 2: [3, 4, 5]}
                >>>key = Observe(a, method='key', methodParameter=2)
                >>>key
                [3, 4, 5]
                >>>a[2].append(9)
                >>>key
                [3, 4, 5, 9]

            b) len - holds the current length of the Dict. methodParameter is not applicable

                >>>a = Dict({1: 2, 2: List([3, 4, 5])})
                >>>a
                {1: 2, 2: [3, 4, 5]}
                >>>dictLength = Observe(a, method='len')
                >>>dictLength
                2
                >>>a[3] = {4, 5, 6, 7}
                >>>dictLength
                3

            c) sum - holds the sum of all the keys in the Dict. methodParameter is not applicable

                >>>a = Dict({1: 2, 2: List([3, 4, 5])})
                >>>a
                {1: 2, 2: [3, 4, 5]}
                >>>dictSum = Observe(a, method='sum')
                >>>dictSum
                3
                >>>a[4] = {4, 5, 6, 7}
                >>>dictSum
                7   # 1 + 2 + 4

            d) max - holds the max of all the keys in the Dict. methodParameter is not applicable

                >>>a = Dict({1: 2, 2: List([3, 4, 5])})
                >>>a
                {1: 2, 2: [3, 4, 5]}
                >>>maxDict = Observe(a, method='max')
                >>>maxDict
                2
                >>>a[3] = [4, 5, 6, 7]
                >>>maxDict
                3

            e) min - holds the min of all the keys in the Dict. methodParameter is not applicable

                >>>a = Dict({1: 2, 2: List([3, 4, 5])})
                >>>a
                {1: 2, 2: [3, 4, 5]}
                >>>minDict = Observe(a, method='min')
                >>>minDict
                1
                >>>a[-1] = {1, 2}
                >>>minDict
                -1

        4. In case of ByteArray

            For all the examples below, the common ByteArray that is used is as follows:

            >>>a = ByteArray("Hi There", "UTF-8")

            a) len - holds the current length of the ByteArray. methodParameter is not applicable

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>lenBA = Observe(a, method='len')
                >>>lenBA
                8
                >>>a.extend(b" again")
                >>>lenBA
                14

            b) count - counts the number of occurrences of the value passed as the methodParameter in the ByteArray

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>count = Observe(a, method='count', methodParameter=b'e')
                >>>count
                2
                >>>a.extend(b'! Evening!')
                >>>count
                4

            c) decode - holds the decoded ByteArray according to the decoding passed as the methodParameter. There is no default decoding. methodParameter is necessary

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>decoded = Observe(a, method='decode', methodParameter='UTF-8')
                >>>decoded
                Hi There
                >>>a.extend(b"! How are you?")
                >>>decoded
                Hey There! How are you?

            d) endswith - holds a boolean value. Becomes True if the ByteArray ends with the parameter passed in methodParameter. methodParameter is compulsory

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>endswith = Observe(a, method='endswith', methodParameter=b'e')
                >>>endswith
                True
                >>>a.extend(b'!')
                >>>endswith
                False

            e) find - holds the first location of the value passed in methodParameter. Holds -1 if value is not found. methodParameter is the search parameter and is compulsory. Currently, only the first location is supported.

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>find = Observe(a, method='find', methodParameter=b'k')
                >>>find
                -1
                >>>a.extend(b' king')
                >>>find
                9

            f) index - holds the first location of the value passed in methodParameter. Raises ValueError if not found. methodParameter is the search parameter and is compulsory. Currently, only the first location is supported.

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>index = Observe(a, method='index', methodParameter=b'e')
                >>>index
                5
                >>>a.replace(b'H', b'e')
                >>>index
                0

            g) isalnum - This holds a boolean value. Is True if the ByteArray is alnum. Otherwise, is False. methodParameter is not applicable

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>isalnum = Observe(a, method='isalnum')
                >>>isalnum
                False

            h) isalpha - This holds a boolean value. Is True if the ByteArray is alpha. Otherwise, is False. methodParameter is not applicable

                >>>a = ByteArray("Hi", "UTF-8")
                >>>a
                bytearray(b'Hi')
                >>>isalpha = Observe(a, method='isalpha')
                >>>isalpha
                True

            i) isdigit - This holds a boolean value. Is True if the ByteArray is digit. Otherwise, is False. methodParameter is not applicable

                >>>a = ByteArray("12345", "UTF-8")
                >>>a
                bytearray(b'12345')
                >>>>isdigit = Observe(a, method='isdigit')
                >>>isdigit
                True

            j) islower - This holds a boolean value. Is True if the ByteArray is lower. Otherwise, is False. methodParameter is not applicable

                >>>a = ByteArray("hi there", "UTF-8")
                >>>a
                bytearray(b'hi there')
                >>>islower = Observe(a, method='islower')
                >>>islower
                True

            k) isupper - This holds a boolean value. Is True if the ByteArray is upper. Otherwise, is False. methodParameter is not applicable

                >>>a = ByteArray("HI THERE", "UTF-8")
                >>>a
                bytearray(b'HI THERE')
                >>>isupper = Observe(a, method='isupper')
                >>>isupper
                True

            l) lower - This holds the ByteArray in its lower case. methodParameter is not applicable

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>lower = Observe(a, method='lower')
                >>>lower
                bytearray(b'hi there')

            m) upper - This holds the ByteArray in its upper case. methodParameter is not applicable

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>upper = Observe(a, method='upper')
                >>>upper
                bytearray(b'HI THERE)

            n) replace - This holds the ByteArray with the replaced byte passed in the methodParameter. methodParameter is a tuple with the first element being the byte to replace and the second element being the byte that needs to replace.

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>replace = Observe(a, method='replace', methodParameter=(b'e', b'l'))
                >>>replace
                bytearray(b'Hi Thlrl)

            o) reverse - This holds the reversed ByteArray. methodParameter is not applicable

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>reverse = Observe(a, method='reverse')
                >>>reverse
                bytearray(b'erehT iH')

            p) slice - This holds the sliced ByteArray. methodParameter is a tuple and can compose of PyReactive Observe Objects, e.g. methodParameter = (0, 4, 1), or (a, b), where a and b are PyReactive Observe objects. It also takes in an optional step as the third argument. This needs to be an integer.

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

            q) startswith - This holds a boolean value. Is True if the ByteArray starts with the value passed in as the methodParameter. Otherwise, is False. methodParameter is compulsory

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>startswith = Observe(a, method='startswith', methodParameter=b'H')
                >>>startswith
                True

            r) max - This holds the maximum value in the ByteArray. Holds an integer. methodParameter is not applicable

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>maxBA = Observe(a, method='max')
                >>>maxBA
                114

            s) min - This holds the minimum value in the ByteArray. Holds an integer. methodParameter is not applicable

                >>>a = ByteArray("Hi There", "UTF-8")
                >>>a
                bytearray(b'Hi There')
                >>>minBA = Observe(a, method='min')
                >>>minBA
                32  #The UTF-8 code for blank-space in integer


            """
    def __init__(self, dependency, name='', method='', methodParameter=None):
        self.id = uuid.uuid4()									#Using ids because without them, in case of unhashable data types such as Lists, we cannot create the dependencyGraph. Hence, uuids to the rescue
        self.name = name
        self.methodParameter = methodParameter
        idVariableDict[self.id] = self
        self.dependency = dependency 					#Setting up the dependency of the Observable to the passed variable
        self.underlyingValue = dependency

        self.initialCalc = True			#Boolean flag that denotes if this is the first time that the value is being calculated

        #if isinstance(self.underlyingValue, (Observe, Subscribe)):
        #	self.underlyingValue = self.dependency.value

        #This following block can be rewritten to save on redundant conditions
        ############################################################
        try:
            if dependency.id in idVariableDict:					#This means that value is a mutable data type belonging to List, Dict, Set, ByteArray. There is no else case here since there's no chance that a List/Set/ByteArray/Dict (BDLS) can be declared without having an entry in idVariableDict
                #Corresponding code

                self.method = method
                #self.value = self.dependency			#This dependency can be taken up to the first "try" case itself and this update method can be entirely removed.
                ##print("Setting dependencyGraph attribute")
                dependencyGraph[dependency.id].append(self.id)				################################### Key assignment. This is where the actual dependency is stated.
                dependencyGraph[self.id] = []
                self.update()									#This sets self.value in the update method


        except:
            #Case where value is a native mutable/immutable data type. If it is a mutable data type, ignore it and raise an exception. Don't allow mutable data types. This is only for immutable data types.
            #self.dependency = None
            self.value = self.dependency
            #if method is 'not' or method is '~' or method is 'len' :
                ##print("method is not")
            #	pass
            #elif method is not '':
            #	raise InvalidSubscriptionError("The method %s is not applicable on native data types"%method)
            self.method = method
            dependencyGraph[self.id] = []
            immutableList.append(self)		#Append to immutableList
            self.update()

            #if isinstance(dependency, (int, str, tuple, bool, bytes, float, complex, frozenset)):
                #This is acceptable
            #	self.dependency = dependency
            #	self.value = dependency 						#Here, the value can directly be assigned as the dependency, since the dependency is an immutable
            #elif isinstance(dependency, (list, dict, bytearray, set)):
                #This is acceptable too, but try to ouput a message that the underlying values will now be frozen since they cannot be updated.
            #	self.dependency = dependency
            #	self.value = dependency 						#Again, the value can directly be assigned as the dependency, since the dependency is mutable, but frozen --> effectively, it behaves like an immutable. It acts as a beefed up Observable that has lost all its progenitors' superpowers.
            #elif isinstance(dependency, (Observable, Subscribe)):
                #Write code to set self.value when the dependency is an observable or a subscription. As it turns out, this case can be completely eliminated, since an Observable or a Subscription can't be absent in the idVariableDict in the first place.
            #	pass
        ############################################################

    #def __index__(self):
    #    return self.value



    def update(self):
        """Sets the value of the Observable every time this is called. It is called at __init__ and at every time that the underlying dependency changes. If the underlying dependency is a native mutable or a native immutable, this method won't be called. This is only called when the dependency belongs to BDLS"""
        #Update method cannot be removed, since it would also deal with Observable methods suchs as sort, remove etc.



        if isinstance(self.underlyingValue, Observe):			#This is the case when there's an Observable, and it needs to be distilled down to either
            ##print("isinstance Observe true. Hence changing underlyingValue to dependency.value")
            self.underlyingValue = self.dependency.value 		#This is done so as to assign the underlyingValue to dependency.value --> this would mean that currently, the underlyingValue is modified to be a List object rather than an Observe object. For further clarification, in the interpreter, check the values of type(self.underlyingValue) and type(self.dependency.value). The former yields an Observe and the latter yields a BDLS. This is so that the further actions can be operated on BDLS, rather than on the Observable, since an Observable does not have the necessary methods that a BDLS has.


        ########################## WRITE CODE FOR HANDLING METHOD ATTRIBUTE HERE

        if isinstance(self.underlyingValue, (str, tuple, frozenset)):
            ##print("isinstance immutables true, hence entered this if-block")
            if self.method in ['len']:		#First check to sift away all methods that don't belong to the object
                if self.method is 'len':	#Second check to iterate through each of the possibilities. It doesn't make sense here, but refer to the List section underneath. Doing this so as to ensure a unified coding pattern
                    self.value = len(self.underlyingValue)
            elif self.method is '':			#If there is no method mentioned
                self.value = self.dependency
            elif self.method is not '':		#If the mentioned method does not belong to the object, raise an exception.
                raise InvalidSubscriptionError("%s method on this object isn't applicable"%self.method)

        elif isinstance(self.underlyingValue, (int, float, bool)):
            if self.method in ['not', '~']:
                if self.method is 'not':
                    ##print("Entered not case of int, float, bool")
                    try:
                        self.value = not(self.dependency.value)
                    except:
                        raise InvalidSubscriptionError("Can't have a not method on a first-level Observe object") #self.dependency is used instead of self.dependency.value, since there is no value attribute to self.dependency, since self.dependency itself is either an int, float, or bool
                if self.method is '~':
                    try:
                        self.value = ~self.dependency.value
                    except:
                        raise InvalidSubscriptionError("Can't have ~ on a first-level Observe object")

            elif self.method is '':
                ##print("entered case where method is null")
                self.value = self.dependency
            elif self.method is not '':
                raise InvalidSubscriptionError("%s method on this object isn't applicable"%self.method)

        elif isinstance(self.underlyingValue, List):
            ##print("isinstance List true, hence entered this if-block")
            #Handle the methods of List
            if self.method in ['count', 'reverse', 'sort', 'lastel', 'firstel', 'slice', 'set', 'len', 'sum', 'max', 'min']:
                #Found self.method in the defined additional method for List
                if self.method is 'count':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't count None. 'methodParameter' was not declared")
                    else:
                        self.value = self.underlyingValue.count(self.methodParameter)	#Count the occurrences of self.methodParameter in the underlyingValue
                elif self.method is 'reverse':
                    temp = self.underlyingValue[:]
                    temp.reverse()
                    self.value = List(temp[:])
                    del temp
                elif self.method is 'sort':
                    temp = self.underlyingValue[:]						#Could also use the builtin sorted method
                    temp.sort(key=self.methodParameter)					#Next update, take a key for sort too
                    self.value = List(temp[:])
                    del temp
                elif self.method is 'lastel':
                    ##print("self.underlyingValue is %s"%self.underlyingValue)
                    try:
                        temp = self.underlyingValue[-1]
                    except:
                        temp = None
                    self.value = temp
                    del temp

                elif self.method is 'firstel':
                    ##print("self.underlyingValue is %s"%self.underlyingValue)
                    try:
                        temp = self.underlyingValue[0]
                    except:
                        temp = None
                    self.value = temp
                    del temp
                elif self.method is 'set':
                    ##print("self.underlyingValue is %s"%self.underlyingValue)
                    temp = self.underlyingValue[:]
                    temp = set(temp)
                    self.value = temp.copy()
                    del temp

                elif self.method is 'slice':
                    ##print("self.underlyingValue is %s"%self.underlyingValue)		#Case when self.method is sliced

                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't slice None. 'methodParameter' was not declared")

                    if isinstance(self.methodParameter, slice):
                        raise InvalidSubscriptionError("Using slice is deprecated. The new API takes methodParameter as a tuple")

                    try:
                        startSlice = self.methodParameter[0]
                        stopSlice = self.methodParameter[1]
                    except:
                        raise InvalidSubscriptionError("Need methodParameter as a tuple. The first element should be the start of the slice and the second element should be the stop of the slice. An optional step is the third element of the tuple")
                    try:
                        stepSlice = self.methodParameter[2]
                    except:
                        stepSlice = None

                    #Check if startSlice/stopSlice/stepSlice are Observe/Subscribe
                    if isinstance(startSlice, (Observe, Subscribe)):
                        if self.id not in dependencyGraph[startSlice.id]:
                            dependencyGraph[startSlice.id].append(self.id)


                        startSlice = startSlice.value

                    if isinstance(stopSlice, (Observe, Subscribe)):
                        if self.id not in dependencyGraph[stopSlice.id]:
                            dependencyGraph[stopSlice.id].append(self.id)
                        stopSlice = stopSlice.value
                    if isinstance(stepSlice, (Observe, Subscribe, ByteArray, List, Dict, Set)):
                        raise InvalidSubscriptionError("Step in a slice needs to be an integer. You gave %s"%stepSlice)

                    self.value = self.underlyingValue[startSlice : stopSlice : stepSlice]

                elif self.method is 'sum':
                    self.value = sum(self.underlyingValue)

                elif self.method is 'len':
                    self.value = len(self.underlyingValue)
                elif self.method is 'max':
                    self.value = max(self.underlyingValue)
                elif self.method is 'min':
                    self.value = min(self.underlyingValue)
                       ########################################################################################################################################
            elif self.method is '':
                self.value = self.dependency

            elif self.method is not '':			#Case when self.method is sent, but the relevant parameter isn't defined in the code
                raise InvalidSubscriptionError("List object doesn't have %s as the method parameter"%self.method)

        elif isinstance(self.underlyingValue, Set):
            ##print("There's nothing to Observe in a Set")
            #if self.method in ['issubset', 'issuperset', 'isdisjoint']:
            #	if self.method is 'issubset':

            #	elif self.method is 'issuperset':

            #	elif self.method is 'isdisjoint':

            if self.method in ['len', 'difference', 'intersection', 'isdisjoint', 'issubset', 'issuperset', 'symmetric_difference', 'union', 'sum', 'max', 'min']:
                if self.method is 'len':
                    self.value = len(self.underlyingValue)
                elif self.method is 'sum':
                    self.value = sum(self.underlyingValue)

                elif self.method is 'max':
                    self.value = max(self.underlyingValue)
                elif self.method is 'min':
                    self.value = min(self.underlyingValue)

                elif self.method in ['difference', 'intersection', 'isdisjoint', 'issubset', 'issuperset', 'symmetric_difference', 'union']:

                    try:
                        if self.id not in dependencyGraph[self.methodParameter.id]:
                            dependencyGraph[self.methodParameter.id].append(self.id)
                    except:
                        raise InvalidSubscriptionError("methodParameter passed is not in the right format. Check again.")

                    try:	#Process where self.method is applied
                        if self.method is 'difference':
                            self.value = Set(self.dependency.difference(self.methodParameter))
                        elif self.method is 'intersection':
                            self.value = Set(self.dependency.intersection(self.methodParameter))
                        elif self.method is 'isdisjoint':
                            self.value = self.dependency.isdisjoint(self.methodParameter)
                            ##print("isdisjoint checked")
                        elif self.method is 'issubset':
                            self.value = self.dependency.issubset(self.methodParameter)
                        elif self.method is 'issuperset':
                            self.value = self.dependency.issuperset(self.methodParameter)
                            ##print('issuperset checked')
                        elif self.method is 'symmetric_difference':
                            self.value = Set(self.dependency.symmetric_difference(self.methodParameter))
                        elif self.method is 'union':
                            self.value = Set(self.dependency.union(self.methodParameter))



                    except:		#Case where the methodParameter isn't set
                        raise InvalidSubscriptionError("methodParameter not set")

            elif self.method is '':
                self.value = self.dependency
            elif self.method is not '':	#Case when self.method is sent, but it is illegal/not defined
                raise InvalidSubscriptionError("Set object doesn't have %s as the method parameter"%self.method)

        elif isinstance(self.underlyingValue, Dict):
            ##print("isinstance Dict is true, hence entered the Corresponding if-block")
            if self.method in ['key', 'len', 'sum', 'max', 'min']:				#Keep this so that it can be extended easily to acoomodate other methods in the future
                if self.method is 'key':
                    if self.methodParameter is None:
                        raise InvalidSubscriptionError("Can't observe a Dict with key as None")
                    else:		#Case when self.methodParameter is not None
                        self.value = self.underlyingValue[self.methodParameter]
                        #In case self.methodParameter is not a valid key, Python will automatically throw the relevant KeyError. We don't need to handle.
                elif self.method is 'len':
                    self.value = len(self.underlyingValue)
                elif self.method is 'sum':
                    self.value = sum(self.underlyingValue)
                elif self.method is 'max':
                    self.value = max(self.underlyingValue)
                elif self.method is 'min':
                    self.value = min(self.underlyingValue)
            elif self.method is '':
                self.value = self.dependency
            elif self.method is not '':
                raise InvalidSubscriptionError("Dict object doesn't have %s as the method parameter"%self.method)

        elif isinstance(self.underlyingValue, ByteArray):
            if self.method in ['len', 'count', 'decode', 'endswith', 'find', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isupper', 'lower', 'max', 'min', 'replace', 'reverse', 'slice', 'startswith', 'upper']:
                if self.method is 'len':
                    self.value = len(self.underlyingValue)



                elif self.method is 'count':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't count None. 'methodParameter' was not declared")
                    else:
                        self.value = self.underlyingValue.count(self.methodParameter)	#Count the




                elif self.method is 'decode':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't decode without decoding type. 'methodParameter' was not declared")
                    else:
                        self.value = self.underlyingValue.decode(self.methodParameter)




                elif self.method is 'endswith':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("endswith needs a methodParameter. 'methodParameter' was not declared")
                    else:
                        self.value = self.underlyingValue.endswith(self.methodParameter)


                elif self.method is 'find':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't find None. 'methodParameter' was not declared")
                    else:
                        self.value = self.underlyingValue.find(self.methodParameter)


                elif self.method is 'index':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't index None. 'methodParameter' was not declared")
                    else:
                        self.value = self.underlyingValue.index(self.methodParameter)


                elif self.method is 'isalnum':
                    self.value = self.underlyingValue.isalnum()
                elif self.method is 'isalpha':
                    self.value = self.underlyingValue.isalpha()
                elif self.method is 'isdigit':
                    self.value = self.underlyingValue.isdigit()
                elif self.method is 'islower':
                    self.value = self.underlyingValue.islower()
                elif self.method is 'isupper':
                    self.value = self.underlyingValue.isupper()
                elif self.method is 'lower':
                    self.value = self.underlyingValue.lower()
                elif self.method is 'max':
                    self.value = max(self.underlyingValue)
                elif self.method is 'min':
                    self.value = min(self.underlyingValue)



                elif self.method is 'replace':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't replace None. 'methodParameter' was not declared")
                    else:
                        self.value = self.underlyingValue.replace(self.methodParameter[0], self.methodParameter[1])


                elif self.method is 'reverse':
                    self.temp = self.underlyingValue[:]
                    self.temp.reverse()
                    self.value = self.temp[:]
                    del self.temp

                elif self.method is 'slice':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't slice None. 'methodParameter' was not declared")

                    if isinstance(self.methodParameter, slice):
                        raise InvalidSubscriptionError("Using slice is deprecated. The new API takes methodParameter as a tuple")

                    try:
                        startSlice = self.methodParameter[0]
                        stopSlice = self.methodParameter[1]
                    except:
                        raise InvalidSubscriptionError("Need methodParameter as a tuple. The first element should be the start of the slice and the second element should be the stop of the slice. An optional step is the third element of the tuple")
                    try:
                        stepSlice = self.methodParameter[2]
                    except:
                        stepSlice = None

                    #Check if startSlice/stopSlice/stepSlice are Observe/Subscribe
                    if isinstance(startSlice, (Observe, Subscribe)):
                        if self.id not in dependencyGraph[startSlice.id]:
                            dependencyGraph[startSlice.id].append(self.id)


                        startSlice = startSlice.value

                    if isinstance(stopSlice, (Observe, Subscribe)):
                        if self.id not in dependencyGraph[stopSlice.id]:
                            dependencyGraph[stopSlice.id].append(self.id)
                        stopSlice = stopSlice.value
                    if isinstance(stepSlice, (Observe, Subscribe, ByteArray, List, Dict, Set)):
                        raise InvalidSubscriptionError("Step in a slice needs to be an integer. You gave %s"%stepSlice)

                    self.value = self.underlyingValue[startSlice : stopSlice : stepSlice]

                elif self.method is 'startswith':
                    if self.methodParameter is None:	#When self.methodParameter isn't declared at __init__
                        raise InvalidSubscriptionError("Can't check. 'methodParameter' was not declared")
                    else:
                        self.value = self.underlyingValue.startswith(self.methodParameter)

                elif self.method is 'upper':
                    self.value = self.underlyingValue.upper()
            elif self.method is '':
                self.value = self.dependency
            elif self.method is not '':
                raise InvalidSubscriptionError("ByteArray object doesn't have %s as the method parameter"%self.method)

        ##########################



        #while isinstance(localValue, (ByteArray, Dict, List, Set)):			#Case where the underlying dependency belongs to BDLS
        #	localValue = localValue
        ##print("Calling update method of Observable")

        ################ Check for type(self.dependency) here. If the type is List, then the methods are different, and if the type is Set, the methods are different. If the declared method isn't associated with the object, raise an Exception


        for element in dependencyGraph[self.id]:
            idVariableDict[element].update()

        self.underlyingValue = self.dependency 			#Restore self.underlyingValue from BDLS to Observe class. self.dependency is an Observable, while in the above declaration at the beginning of the update, we've changed it to a BDLS so that further calculations are possible.

        if self.initialCalc:
            #This is the first time that it has been calculated. Hence, call notify.
            self.oldValue = self.value		#Assign the calculated value to self.oldValue. This variable keeps track of the changes in the value.
            self.initialCalc = False	#Set initialCalc to False since this isn't needed after init
            self.notify()

        else:	#Case after initialCalc
            if self.oldValue == self.value:
                #Do not notify
                pass
            else:
                #Call the notify method and assign the new value to oldValue
                self.oldValue = self.value
                self.notify()
        #self.notify()

    def notify(self):				#Make this the method that is called every time there's a change in the underlying dependency, as the update method is no longer needed.
        """This method is supposed to be overridden to perform anything of value whenever a change occurs"""
        pass
        ##print("Observable changed and value is %s"%self.value)

    def __repr__(self):			#This is the killer method! Without this, my life and architecture would've been ludicrously tough. Is this the golden bullet?
        return("%s"%self.value)

    def modifyMethod(self, method='', methodParameter=None):
        """This method takes a method name and an optional methodParameter so as to modify the Observe object to observe a variant of that particular data type. For e.g., an Observe object could initially be defined over a List object with method = 'sort'. Later, it can be modified to method='reverse' using this method."""
        if method is '':
            self.method = self.method
            #self.methodParameter =
        else:
            self.method = method
        self.methodParameter = methodParameter
        self.update()

    def changeTo(self, value):
        """This method is applicable only on observe objects that observe immutable data types. Throws an exception if it is tried on mutables. Changes the underlying immutable value to the new specified value. Also, throws an exception if an Observe object, which is defined over another Observe object since an Observe object is a mutable."""
        if self in immutableList:
            if len(dependencyGraph[self.id]) is 0:
                self.dependency = None
                self.value = value
            else:
                self.dependency = value
                self.value = self.dependency
            for element in dependencyGraph[self.id]:
                idVariableDict[element].update()
        else:
            raise InvalidSubscriptionError("changeTo method not permitted on mutables, or when the an Observe object is created over another Observe object")


class Subscribe:
    """Deals with subscriptions of observables/mutables"""

    def __init__(self, name='', **args):
        """Initialize the object with an optional name and variables and corresponding operators. e.g., Subscribe(var=(a,b), op=('+',)). Need a minimum of 2 operands and 1 operator. Unary operators are handled in the case of Observe objects."""
        try:
            self.variablesSubscribedTo = list(args['var'])
            self.operatorsList = list(args['op'])
        except:
            raise InvalidSubscriptionError("Can't initialize a subscription with no observables")


        for var in self.variablesSubscribedTo:
            try:
                if var.id not in idVariableDict:		#if var.id is available but it is not in the dependencyGraph..this is the case when a foreign object might have a parameter called 'id'
                    raise InvalidSubscriptionError("Can't subscribe to a foreign object. Subscribe only supports ByteArray, List, Dict, Set, and other Observe objects as of yet.")
            except:					#This is the case when var.id in the try segment fails. That is, the object has not 'id' parameter
                raise InvalidSubscriptionError("Can't subscribe to object %s. Not supported yet."%var)


            #All variables now can be safely assumed to have a presence in the dependencyGraph

        if len(self.variablesSubscribedTo) - 1 != len(self.operatorsList):		#Case when the required number of operators mismatches the number of operands
            raise InvalidSubscriptionError("The number of operators can only be 1 less than the number of operands. Subscription aborted.")

            #The scrubbing/sanitization of variables passed is now complete.


        try:
            self.rformat = list(args['rformat'])
            if len(self.rformat) < len(self.operatorsList):
                #Since the length is shorter, i.e., rformat isn't mentioned for every operation, pad the list with None until its becomes the same size as that of the operatorsList.
                self.tempLenDiff = len(self.operatorsList) - len(self.rformat)
                self.rformat.extend([None]*self.tempLenDiff)
                del self.tempLenDiff
                print("self.rformat in try at init is %s"%self.rformat)
        except:
            self.rformat = [None]*len(self.operatorsList)

        #At this point, self.rformat becomes available and is of the same length as self.operatorsList
        #print("self.rformat is %s"%self.rformat)

        self.id = uuid.uuid4()
        dependencyGraph[self.id] = []
        idVariableDict[self.id] = self
        self.name = name

        for var in self.variablesSubscribedTo:
            dependencyGraph[var.id].append(self.id)			#Declare the dependency of the Subsciption object on each of the variablesSubscribedTo.

        self.update()		#Call the update method to calculate the value

    #def __index__(self):
    #    return self.value


    """
    or

    **API:** **SubscribeObject = Subscribe(var=(var1, var2,...), op=('+','-',....), rformat=('fabs', 'ceil', 'floor'))**

    A Subscribe object also takes an optional **rformat** which accepts either **ceil**, **floor**, **fabs**. These are similar to the methods available in the standard **math** module. **ceil** would compute the ceil value of the two operands, **fabs** would compute the absolute value of the two operands, and **floor** would compute the floor value of the two operands. **rformat** is a tuple with its order similar to that of **op**. If no return format needs to be specified, it also accepts **None** or **''**.

    If the equation is 2 + floor(5/4) x ceil(20/3) + abs(-4/2), then the Subscribe object is:
```python
>>>op1 = Observe(2)
>>>op2 = Observe(5)
>>>op3 = Observe(4)
>>>op4 = Observe(20)
>>>op5 = Observe(3)
>>>op6 = Observe(-4)
>>>op7 = Observe(2)
>>>eqn = Subscribe(var=(op1, op2, op3, op4, op5, op6, op7), op=('+', '/','*','/', '+', '/'), rformat=(None, 'floor', None, 'ceil', None, 'fabs'))
```
    """

    def update(self):
        operatorsSet = createSetInPrecedence(self.operatorsList)
        operatorsListCopy = self.operatorsList[:]
        rformatCopy = self.rformat[:]
        tempVariablesSubscribedTo = self.variablesSubscribedTo[:]
        tempVariablesSubscribedTo2 = []
        for var in tempVariablesSubscribedTo:
            if isinstance(var, (Observe, Subscribe)):
                tempVariablesSubscribedTo2.append(var.value)	#In case var is an Observe/Subscribe object
            else:
                tempVariablesSubscribedTo2.append(var)		#In case var is a simple BDLS
            #tempVariablesSubscribedTo2 is now the list of all variables with the corresponding values. This aids in calculations

        for operator in operatorsSet:
            (tempVariablesSubscribedTo2, rformatCopy) = evaluateEquation(tempVariablesSubscribedTo2, operator, operatorsListCopy, rformatCopy)

        self.value = tempVariablesSubscribedTo2[0]

        for element in dependencyGraph[self.id]:
            idVariableDict[element].update()


            #Set self.value somewhere here
        self.notify()

    def notify(self):
        pass

    def append(self, **args):
        """Append operands and operators to the existing object. Format is similar to __init__"""
        try:
            variablesSubscribedTo = list(args['var'])
            operatorsList = list(args['op'])
        except:
            raise InvalidSubscriptionError("Can't initialize a subscription with no observables")

        for var in variablesSubscribedTo:
            try:
                if var.id not in idVariableDict:		#if var.id is available but it is not in the dependencyGraph..this is the case when a foreign object might have a parameter called 'id'
                    raise InvalidSubscriptionError("Can't subscribe to a foreign object. Subscribe only supports ByteArray, List, Dict, Set, and other Observe objects as of yet.")
            except:					#This is the case when var.id in the try segment fails. That is, the object has not 'id' parameter
                raise InvalidSubscriptionError("Can't subscribe to object %s. Not supported yet."%var)


            #All variables now can be safely assumed to have a presence in the dependencyGraph

        self.variablesSubscribedTo += variablesSubscribedTo 	#Update the object variables
        self.operatorsList += operatorsList

        if len(self.variablesSubscribedTo) - 1 != len(self.operatorsList):		#Case when the required number of operators mismatches the number of operands
            raise InvalidSubscriptionError("The number of operators can only be 1 less than the number of operands. Subscription aborted.")

        self.update()

    def equation(self):
        """Returns the current equation of the subscription"""
        equationString = ''
        if self.name != '':
            equationString = self.name + ' ='
        for i in range(len(self.variablesSubscribedTo)):
            if i < len(self.operatorsList):
                operatorEqn = self.operatorsList[i]
            else:
                operatorEqn = ''
            try:
                if self.variablesSubscribedTo[i].name == '':		#Case when name hasn't been defined
                    nameOfVariable = str(self.variablesSubscribedTo[i])
                else:
                    nameOfVariable = self.variablesSubscribedTo[i].name
            except:
                nameOfVariable = str(self.variablesSubscribedTo[i])

            equationString += ' ' + nameOfVariable + ' ' + operatorEqn		#Instead of using .get(), use self.variablesSubscribedTo.variableName here. Store variableName as an Observe class parameter and declare it at __init__ itself.
        self.equationString = equationString
        return self.equationString




    def __repr__(self):
        return("%s"%self.value)

def createSetInPrecedence(operatorsList):
    newOperatorList = []
    #Check for all operators here. In future, this can accomodate more operators
    if '**' in operatorsList:
        newOperatorList.append('**')
        ####print("newOperatorList is %s"%newOperatorList)
    #if '~' in operatorsList:	#This is a unary operand. Should be on the observe object
    #	newOperatorList.append('~')


    if '*' in operatorsList:
        newOperatorList.append('*')
        ####print("newOperatorList is %s"%newOperatorList)
    if '/' in operatorsList:
        newOperatorList.append('/')
        ###print("newOperatorList is %s"%newOperatorList)
    if '%' in operatorsList:
        newOperatorList.append('%')
        ###print("newOperatorList is %s"%newOperatorList)
    if '//' in operatorsList:
        newOperatorList.append('//')
        ###print("newOperatorList is %s"%newOperatorList)
    if '+' in operatorsList:
        newOperatorList.append('+')
        ###print("newOperatorList is %s"%newOperatorList)
    if '-' in operatorsList:
        newOperatorList.append('-')
        ###print("newOperatorList is %s"%newOperatorList)

    if '>>' in operatorsList:
        newOperatorList.append('>>')
    if '<<' in operatorsList:
        newOperatorList.append('<<')
    if '&' in operatorsList:
        newOperatorList.append('&')
    if '^' in operatorsList:
        newOperatorList.append('^')
    if '|' in operatorsList:
        newOperatorList.append('|')
    if 'or' in operatorsList:
        newOperatorList.append('or')
    if 'and' in operatorsList:
        newOperatorList.append('and')
    return(newOperatorList)				#Returns the set of operators in the order of precedence

def evaluateEquation(alteredList, operator, OperatorsList, rFormatList):
    count = OperatorsList.count(operator)
    locOperator = 0
    for i in range(count):
        ##print("Count value is %s"%i)
        ##print("locOperator is %s"%locOperator)
        ##print("OperatorsList is %s"%OperatorsList)
        locOperator = OperatorsList.index(operator, locOperator)
        #Found the index of the operator. Now, find the corresponding 2 variables in variablesToObserve and perform the operation
        #Perform the evaluation of variablesToObserve[locOperator]-'operator'-variablesToObserve[locOperator+1] here, and replace the two variables with the evaluated result at the location - 'locOperator'

        try:
            firstOperand = alteredList[locOperator].value				#Pick the first operand
        except:
            firstOperand = alteredList[locOperator]
        try:
            secondOperand = alteredList[locOperator + 1].value			#Pick the second operand
        except:
            secondOperand = alteredList[locOperator + 1]

        localRFormat = rFormatList[locOperator]
        #print("localRFormat in evaluateEquation is %s"%localRFormat)
        resultant = evaluateExpression(firstOperand, secondOperand, operator, localRFormat)		#Send the expression to another function, and the result will be replaced in the original variablesToObserve, along with the removal of the operator at that location from OperatorsList

        #print("resultant in evaluateEquation is %s"%resultant)

        alteredList.pop(locOperator)		#Pop the two operands, and replace them with the resultant
        alteredList.pop(locOperator)
        rFormatList.pop(locOperator)
        alteredList.insert(locOperator, resultant)		#Insert the resultant at the location where the two operands have been removed
        OperatorsList.remove(operator)					#Also remove the operator, since it has been evaluated

        ###print("AlteredList has become %s and OperatorsList has become %s"%(alteredList, OperatorsList))
        #locOperator += 1		#Increase the location index so as to find the next location of the current operator
    return (alteredList, rFormatList)

def evaluateExpression(firstOperand, secondOperand, operator, localRFormat):
    #Check for the apposite operator, perform the operation nad return the result
    ###print("Operator received in evaluateExpression is %s and type of operator is %s"%(operator,type(operator)))

    if len(operator) >= 2:		#In case the operand consists of 2 characters. e.g., **,//, and other set operations. Greater than is used so as to leave a vacancy to extend future user-defined operators
        operator = operator[:]

    try:
        if '**' in operator:
            result = firstOperand**secondOperand
        elif operator is '-':
            result = firstOperand - secondOperand
        elif operator is '/':
            result = firstOperand/secondOperand
        elif operator is '*':
            result = firstOperand*secondOperand
        elif '//' in operator:
            result = firstOperand//secondOperand
        elif operator is '+':
            result = firstOperand + secondOperand
        elif operator is '%':
            result = firstOperand%secondOperand
        elif '<<' in operator:
            result = firstOperand<<secondOperand
        elif '>>' in operator:
            result = firstOperand>>secondOperand
        elif operator is '&':
            result = firstOperand & secondOperand
        elif operator is '|':
            result = firstOperand | secondOperand
        #elif operator is '~':
        #	result = firstOperand ~ secondOperand
        elif operator is '^':
            result = firstOperand ^ secondOperand
        elif operator is 'and':
            result = firstOperand and secondOperand
        elif operator is 'or':
            result = firstOperand or secondOperand
        else:
            raise TypeError("No %s operator found"%operator)
    finally:

        ###print("Result in evaluateExpression is %s"%result)

        #Formats are ceil, fabs, floor
        #print("localRFormat in evaluateExpression is %s"%localRFormat)
        if localRFormat is None or localRFormat == '':
            return result
        elif localRFormat in 'ceil':
            return math.ceil(result)
        elif localRFormat in 'fabs':
            return math.fabs(result)
        elif localRFormat in 'floor':
            #print("in floor if-else case")
            return math.floor(result)
        #return result
