class List(list):
	
	"""List() -> new empty list
   	   List(iterable) -> new list initialized from iterable's items"""
	
	def append(self, value):
		"""L.append(object) -> None -- append object to end"""
		super(List, self).append(value)

	def clear(self):
		""" L.clear() -> None -- remove all items from L"""
		#When a list is cleared, check for all its dependencies, and clear it only if there are no corresponding Observables and Subscriptions. Otherwise, throw an Exception
		super(List, self).clear()

	#Copy isn't required

	#**************************************************************************************************
	#Count isn't required, because this will be an Observable
	#**************************************************************************************************

	def extend(self, value):
		"""L.extend(iterable) -> None -- extend list by appending elements from the iterable"""
		super(List, self).extend(value)

	#Index isn't required

	def insert(self, index, value):
		"""L.insert(index, object) -- insert object before index"""
		super(List, self).insert(index, value)

	def pop(self, location=-1):
		"""L.pop([index]) -> item -- remove and return item at index (default last)
			Raises IndexError if list is empty or index is out of range."""
		return(super(List, self).pop(location))

	def remove(self, value):
		""" L.remove(value) -> None -- remove first occurrence of value.
			Raises ValueError if the value is not present."""
		super(List, self).remove(value)

	def __setitem__(self, key, value):
		#print("Set key:%s and value:%s"%(key,value))
		super(List, self).__setitem__(key, value)

	def __delitem__(self, key):
		#print("Deleted key:%s"%key)
		super(List, self).__delitem__(key)

	#**************************************************************************************************
	#Reverse isn't required, because this will be an Observable
	#**************************************************************************************************

	#**************************************************************************************************
	#Sort isn't required, because this will be an Observable
	#**************************************************************************************************

class Set(set):
	"""set() -> new empty set object
 	   set(iterable) -> new set object
 	   Build an unordered collection of unique elements."""

	def add(self, value):
		"""Add an element to a set.
		   This has no effect if the element is already present."""
		super(Set, self).add(value)

	def clear(self):
		"""Remove all elements from this set."""
		super(Set, self).clear()

	def discard(self, value):
		"""Remove an element from a set if it is a member.
		   If the element is not a member, do nothing."""
		super(Set, self).discard(value)

	def pop(self, location=-1):
		"""Remove and return an arbitrary set element.
		   Raises KeyError if the set is empty."""
		return(super(Set, self).pop(location))

	def remove(self, value):
		"""Remove an element from a set; it must be a member.
		   If the element is not a member, raise a KeyError."""
		super(Set, self).remove(value)

	def update(self, value):
		"""Update a set with the union of itself and others."""
		super(Set, self).update(value)

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
	#pass
	def modify(self, value):
		#value = Int(value)
		
		
		self = Int(value)
		self.__new__(Int, self)
		#print(self)
		#print("self is "%self)
		
	#	print("Self is %s"%self)
		
	#	return(super(Int, self).__new__(Int ,value-self))
		#super(Int, self).__new__(self, value)
	
	def __new__(cls, *args, **kwargs):
		#print("cls is %s args is %s"%(cls, args))
		return super(Int, cls).__new__(cls, *args)
	#def __init__(self, value):
	#	super(Int, self).__init__(value)

class Dict(dict):
	def clear(self):
		super(Dict, self).clear()
		


	def pop(self, key):
		return super(Dict, self).pop(key)
		

	def popitem(self):
		return super(Dict, self).popitem()

	def update(self, anotherDict):
		super(Dict, self).update(anotherDict)
		

	def __setitem__(self, key, value):
		print("Set key:%s and value:%s"%(key,value))
		super(Dict, self).__setitem__(key, value)

	def __delitem__(self, key):
		print("Deleted key:%s"%key)
		super(Dict, self).__delitem__(key)


	#Override [] for dictionary and bytearray