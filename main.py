import uuid
from mutables import *

dependencyGraph = {}						#Define a central dependency graph that holds all relations between mutables
idVariableDict = {}							#Define a dictionary that maps uuids to the relevant object eg: idVariableDict[self.id] = self

##################################################################################################################################################################################
#Override certain methods of data types imported from mutables

class List(List):
	def __init__(self, args):
		super(List, self).__init__(args)
		#At __init__, set up an entry in the dependencyGraph
		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self
		print(dependencyGraph)
		#print("List initialised")

	def onchange(self):
		print("List object has changed --> onchange method called")
		for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
			element.update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions


class Dict(Dict):
	def __init__(self, args):
		super(Dict, self).__init__(args)
		#At __init__, set up an entry in the dependencyGraph
		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self

	def onchange(self):
		for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
			element.update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
		

class Set(Set):
	def __init__(self, args):
		super(Set, self).__init__(args)
		#At __init__, set up an entry in the dependencyGraph
		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self

	def onchange(self):
		for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
			element.update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
		

class ByteArray(ByteArray):
	def __init__(self, *args):
		super(ByteArray, self).__init__(*args)
		#At __init__, set up an entry in the dependencyGraph
		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self

	def onchange(self):
		for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
			element.update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
		
##################################################################################################################################################################################

class InvalidSubscriptionError(Exception):
	"""Special Exception that inherits from Base Exception class. Does nothing but raise a relevant exception"""
	pass

class Observable:
	"""Deals with all observables"""
	def __init__(self, dependency, name='', method=''):
		self.id = uuid.uuid4()
		self.name = name
		self.method = method
		idVariableDict[self.id] = self
		

		#This following block can be rewritten to save on redundant conditions
		############################################################
		try:
			if dependency.id in idVariableDict:					#This means that value is a mutable data type belonging to List, Dict, Set, ByteArray. There is no else case here since there's no chance that a List/Set/ByteArray/Dict (BDLS) can be declared without having an entry in idVariableDict
				#Corresponding code
				self.dependency = dependency 					#Setting up the dependency of the Observable to the passed variable
				self.update()									#This sets self.value in the update method
				
		except:
			#Case where value is a native mutable/immutable data type. If it is a mutable data type, ignore it and raise an exception. Don't allow mutable data types. This is only for immutable data types.
			
			if isinstance(dependency, (int, str, tuple, bool, bytes, float, complex, frozenset)):
				#This is acceptable
				self.value = dependency 						#Here, the value can directly be assigned as the dependency, since the dependency is an immutable
			elif isinstance(dependency, (list, dict, bytearray, set)):
				#This is acceptable too, but try to ouput a message that the underlying values will now be frozen since they cannot be updated.
				self.value = dependency 						#Again, the value can directly be assigned as the dependency, since the dependency is mutable, but frozen --> effectively, it behaves like an immutable. It acts as a beefed up Observable that has lost all its progenitors' superpowers.
			elif isinstance(dependency, (Observable, Subscribe)):
				#Write code to set self.value when the dependency is an observable or a subscription
				pass
		############################################################



		dependencyGraph[dependency.id].append(self)				################################### Key assignment. This is where the actual dependency is stated.
		dependencyGraph[self.id] = []

	def update(self):
		"""Sets the value of the Observable every time this is called. It is called at __init__ and at every time that the underlying dependency changes. If the underlying dependency is a native mutable or a native immutable, this method won't be called. This is only called when the dependency belongs to BDLS"""
		self.value = self.dependency
		#while isinstance(localValue, (ByteArray, Dict, List, Set)):			#Case where the underlying dependency belongs to BDLS
		#	localValue = localValue
		print("Calling update method of Observable")
		
		################ Check for type(self.dependency) here. If the type is List, then the methods are different, and if the type is Set, the methods are different. If the declared method isn't associated with the object, raise an Exception


		self.onchange()
		for element in dependencyGraph[self.id]:
			element.update()

	def onchange(self):
		print("Observable changed and value is %s"%self.value)

	def __repr__(self):
		return("%s"%self.value)

class Subscribe:
	pass