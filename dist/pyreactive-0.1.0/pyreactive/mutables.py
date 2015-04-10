"""Module that consists of overridden default mutable datatypes"""

class List(list):

	"""List() -> new empty list
   	   List(iterable) -> new list initialized from iterable's items"""

	def append(self, value):
		"""L.append(object) -> None -- append object to end"""
		super(List, self).append(value)
		self.onchange()

	def clear(self):
		""" L.clear() -> None -- remove all items from L"""
		#When a list is cleared, check for all its dependencies, and clear it only if there are no corresponding Observables and Subscriptions. Otherwise, throw an Exception
		super(List, self).clear()
		self.onchange()

	#Copy isn't required

	#**************************************************************************************************
	#Count isn't required, because this will be an Observable
	#**************************************************************************************************

	def extend(self, value):
		"""L.extend(iterable) -> None -- extend list by appending elements from the iterable"""
		super(List, self).extend(value)
		self.onchange()

	#Index isn't required

	def insert(self, index, value):
		"""L.insert(index, object) -- insert object before index"""
		super(List, self).insert(index, value)
		self.onchange()

	def pop(self, location=-1):
		"""L.pop([index]) -> item -- remove and return item at index (default last)
			Raises IndexError if list is empty or index is out of range."""
		print(super(List, self).pop(location))
		self.onchange()

	def remove(self, value):
		""" L.remove(value) -> None -- remove first occurrence of value.
			Raises ValueError if the value is not present."""
		super(List, self).remove(value)
		self.onchange()

	def reverse(self):
		"""L.reverse() -- reverse *IN PLACE*"""
		super(List, self).reverse()
		self.onchange()

	def __setitem__(self, key, value):
		"""Set self[key] to value."""
		##print("Set key:%s and value:%s"%(key,value))
		super(List, self).__setitem__(key, value)
		self.onchange()

	def __delitem__(self, key):
		"""Delete self[key]."""
		##print("Deleted key:%s"%key)
		super(List, self).__delitem__(key)
		self.onchange()

	def onchange(self):
		"""Internal method that is always called when there's a change in the data type"""
		pass

	#**************************************************************************************************
	#Reverse will also be an Observable
	#**************************************************************************************************

	#**************************************************************************************************
	#Sort isn't required, because this will be an Observable
	#**************************************************************************************************

class Set(set):
	"""Set() -> new empty set object
 	   Set(iterable) -> new set object
 	   Build an unordered collection of unique elements."""

	def add(self, value):
		"""Add an element to a set.
		   This has no effect if the element is already present."""
		super(Set, self).add(value)
		self.onchange()

	def clear(self):
		"""Remove all elements from this set."""
		super(Set, self).clear()
		self.onchange()

	def difference_update(self, *value):
		"""Remove all elements of another set from this set."""
		for val in value:
			super(Set, self).difference_update(val)
		self.onchange()

	def discard(self, value):
		"""Remove an element from a set if it is a member.
		   If the element is not a member, do nothing."""
		super(Set, self).discard(value)
		self.onchange()

	def intersection_update(self, *value):
		"""Update a set with the intersection of itself and another."""
		for val in value:
			super(Set, self).intersection_update(val)
		self.onchange()

	def pop(self):
		"""Remove and return an arbitrary set element.
		   Raises KeyError if the set is empty."""
		print(super(Set, self).pop())
		self.onchange()

	def remove(self, value):
		"""Remove an element from a set; it must be a member.
		   If the element is not a member, raise a KeyError."""
		super(Set, self).remove(value)
		self.onchange()

	def symmetric_difference_update(self, *value):
		"""Update a set with the symmetric difference of itself and another."""
		for val in value:
			super(Set, self).symmetric_difference_update(val)
		self.onchange()

	def update(self, value):
		"""Update a set with the union of itself and others."""
		super(Set, self).update(value)
		self.onchange()


	def onchange(self):
		"""Internal method that is always called when there's a change in the data type"""
		pass

	#**************************************************************************************************
	#The remaining functions such as difference, union, intersection and their variants are supposed to be Observables
	#difference, difference_update, intersection, intersection_update, symmetric_difference, symmetric_difference_update, union are the Observables
	#**************************************************************************************************

class Tuple(tuple):
	pass
		#Comment this data type
	#**************************************************************************************************
	#Count again is an Observable here
	#**************************************************************************************************

class Int(int):
	#Can't subclass int, and int objects are immutable. Similar will be the case with strings and tuples
	pass
	#def modify(self, value):
		#value = Int(value)


	#	self = Int(value)
	#	self.__new__(Int, self)
		##print(self)
		##print("self is "%self)

	#	#print("Self is %s"%self)

	#	return(super(Int, self).__new__(Int ,value-self))
		#super(Int, self).__new__(self, value)

	#def __new__(cls, *args, **kwargs):
		##print("cls is %s args is %s"%(cls, args))
	#	#print(super(Int, cls).__new__(cls, *args))
	#def __init__(self, value):
	#	super(Int, self).__init__(value)

class Dict(dict):
	"""Dict() -> new empty dictionary
 	   Dict(mapping) -> new dictionary initialized from a mapping object's
        (key, value) pairs
 	   Dict(iterable) -> new dictionary initialized as if via:
 	      d = Dict()
 	      for k, v in iterable:
 	          d[k] = v
 	  Dict(**kwargs) -> new dictionary initialized with the name=value pairs
 	      in the keyword argument list.  For example:  Dict(one=1, two=2)"""

	def clear(self):
		"""D.clear() -> None.  Remove all items from D."""
		super(Dict, self).clear()
		self.onchange()



	def pop(self, key):
		""" D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
 		      If key is not found, d is returned if given, otherwise KeyError is raised."""
		print(super(Dict, self).pop(key))
		self.onchange()


	def popitem(self):
		"""D.popitem() -> (k, v), remove and return some (key, value) pair as a
 		      2-tuple; but raise KeyError if D is empty."""
		print(super(Dict, self).popitem())
		self.onchange()

	def update(self, anotherDict):
		"""D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
 	      If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
 	      If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
 	      In either case, this is followed by: for k in F:  D[k] = F[k]"""
		super(Dict, self).update(anotherDict)
		self.onchange()


	def __setitem__(self, key, value):
		"""Set self[key] to value."""
		##print("Set key:%s and value:%s"%(key,value))
		super(Dict, self).__setitem__(key, value)
		self.onchange()

	def __delitem__(self, key):
		"""Delete self[key]."""
		##print("Deleted key:%s"%key)
		super(Dict, self).__delitem__(key)
		self.onchange()

	def onchange(self):
		"""Internal method that is always called when there's a change in the data type"""
		pass


	#Override [] for dictionary and bytearray


######Need to add methods for bytearray here

class ByteArray(bytearray):
	"""ByteArray(iterable_of_ints) -> ByteArray
 		  ByteArray(string, encoding[, errors]) -> ByteArray
 	  	ByteArray(bytes_or_buffer) -> mutable copy of bytes_or_buffer
 	  	ByteArray(int) -> bytes array of size given by the parameter initialized with null bytes
 	  	ByteArray() -> empty bytes array

 	  	Construct an mutable bytearray object from:
 	    	- an iterable yielding integers in range(256)
 	    	- a text string encoded using the specified encoding
 	    	- a bytes or a buffer object
 	    	- any object implementing the buffer API.
 	    	- an integer"""

	def __delitem__(self, key):
		"""Delete self[key]."""
		super(ByteArray, self).__delitem__(key)
		self.onchange()

	def __setitem__(self, key, value):
		"""Set self[key] to value."""
		super(ByteArray, self).__setitem__(key, value)
		self.onchange()

	def append(self, value):
		"""B.append(int) -> None

 	      	Append a single item to the end of B."""
		super(ByteArray, self).append(value)
		self.onchange()

	def clear(self):
		"""B.clear() -> None

 		    Remove all items from B."""
		super(ByteArray, self).clear()
		self.onchange()

	#**************************************************************************************************
	#Count again is an Observable here, Decode, Reverse too. Have reverse as a method as well as an observable parameter
	#**************************************************************************************************

	def extend(self, itr):
		"""B.extend(iterable_of_ints) -> None

 	      Append all the elements from the iterator or sequence to the
 	      end of B."""
		super(ByteArray, self).extend(itr)
		self.onchange()

	def insert(self, index, value):
		"""B.insert(index, int) -> None

 	      Insert a single item into the bytearray before the given index."""
		super(ByteArray, self).insert(index, value)
		self.onchange()

	def pop(self, location=-1):
		"""B.pop([index]) -> int

 	      Remove and return a single item from B. If no index
 	      argument is given, will pop the last value."""
		print(super(ByteArray, self).pop(location))
		self.onchange()

	def remove(self, value):
		"""B.remove(int) -> None

 	      Remove the first occurrence of a value in B."""
		super(ByteArray, self).remove(value)
		self.onchange()

	def reverse(self):
		"""B.reverse() -> None

 	      Reverse the order of the values in B in place."""
		super(ByteArray, self).reverse()
		self.onchange()


	def onchange(self):
		"""Internal method that is always called when there's a change in the data type"""
		pass
