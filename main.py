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
	def __init__(self, value, name='', method=''):
		self.id = uuid.uuid4()
		idVariableDict[self.id] = self
		try:
			if value.id in idVariableDict:					#This means that value is a mutable data type belonging to List, Dict, Set, ByteArray. There is no else case here since there's no chance that a List/Set/ByteArray/Dict (BDLS) can be declared without having an entry in idVariableDict
				#Corresponding code
				pass
		except:
			#Case where value is a native mutable/immutable data type. If it is a mutable data type, ignore it and raise an exception. Don't allow mutable data types. This is only for immutable data types.
			pass

			
