import uuid
from mutables import *

dependencyGraph = {}						#Define a central dependency graph that holds all relations between mutables
idVariableDict = {}							#Define a dictionary that maps uuids to the relevant object eg: idVariableDict[self.id] = self

##################################################################################################################################################################################
#Override certain methods of data types imported from mutables

class List(List):
	def __init__(self, args):
		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self
		super(List, self).__init__(args)
		#At __init__, set up an entry in the dependencyGraph
		
		print(dependencyGraph)
		#print("List initialised")

	def onchange(self):
		print("List object has changed --> onchange method called")
		for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
			idVariableDict[element].update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions


class Dict(Dict):
	def __init__(self, args):
		super(Dict, self).__init__(args)
		#At __init__, set up an entry in the dependencyGraph
		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self

	def onchange(self):
		for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
			idVariableDict[element].update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
		

class Set(Set):
	def __init__(self, args):
		super(Set, self).__init__(args)
		#At __init__, set up an entry in the dependencyGraph
		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self

	def onchange(self):
		for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
			idVariableDict[element].update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
		

class ByteArray(ByteArray):
	def __init__(self, *args):
		super(ByteArray, self).__init__(*args)
		#At __init__, set up an entry in the dependencyGraph
		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self

	def onchange(self):
		for element in dependencyGraph[self.id]:			#Retrieves the list of all elements that will change because of a change in this variable
			idVariableDict[element].update()								#Calls the update method on every Observable as well as Subscriptions; additionally, this won't crash, because a generic data type cannot depend on another generic data type. This privilege is only enjoyed by Observables and Subscriptions
		
##################################################################################################################################################################################

class InvalidSubscriptionError(Exception):
	"""Special Exception that inherits from Base Exception class. Does nothing but raise a relevant exception"""
	pass

class Observe:
	"""Deals with all observables"""
	def __init__(self, dependency, name='', method='', methodParameter=None):
		self.id = uuid.uuid4()									#Using ids because without them, in case of unhashable data types such as Lists, we cannot create the dependencyGraph. Hence, uuids to the rescue
		self.name = name
		self.methodParameter = methodParameter
		idVariableDict[self.id] = self
		self.dependency = dependency 					#Setting up the dependency of the Observable to the passed variable
		self.underlyingValue = dependency
		#if isinstance(self.underlyingValue, (Observe, Subscribe)):
		#	self.underlyingValue = self.dependency.value

		#This following block can be rewritten to save on redundant conditions
		############################################################
		try:
			if dependency.id in idVariableDict:					#This means that value is a mutable data type belonging to List, Dict, Set, ByteArray. There is no else case here since there's no chance that a List/Set/ByteArray/Dict (BDLS) can be declared without having an entry in idVariableDict
				#Corresponding code
				
				self.method = method
				#self.value = self.dependency			#This dependency can be taken up to the first "try" case itself and this update method can be entirely removed.
				print("Setting dependencyGraph attribute")
				dependencyGraph[dependency.id].append(self.id)				################################### Key assignment. This is where the actual dependency is stated.
				dependencyGraph[self.id] = []
				self.update()									#This sets self.value in the update method
				
				
		except:
			#Case where value is a native mutable/immutable data type. If it is a mutable data type, ignore it and raise an exception. Don't allow mutable data types. This is only for immutable data types.
			self.dependency = dependency
			self.value = self.dependency
			if method is not '':
				raise InvalidSubscriptionError("Can't have method parameter set for native data types")
			

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



		

	def update(self):
		"""Sets the value of the Observable every time this is called. It is called at __init__ and at every time that the underlying dependency changes. If the underlying dependency is a native mutable or a native immutable, this method won't be called. This is only called when the dependency belongs to BDLS"""
		#Update method cannot be removed, since it would also deal with Observable methods suchs as sort, remove etc. 

		
		
		if isinstance(self.underlyingValue, Observe):			#This is the case when there's an Observable, and it needs to be distilled down to either 
			print("isinstance Observe true. Hence changing underlyingValue to dependency.value")
			self.underlyingValue = self.dependency.value 		#This is done so as to assign the underlyingValue to dependency.value --> this would mean that currently, the underlyingValue is modified to be a List object rather than an Observe object. For further clarification, in the interpreter, check the values of type(self.underlyingValue) and type(self.dependency.value). The former yields an Observe and the latter yields a BDLS. This is so that the further actions can be operated on BDLS, rather than on the Observable, since an Observable does not have the necessary methods that a BDLS has.

		########################## WRITE CODE FOR HANDLING METHOD ATTRIBUTE HERE

		if isinstance(self.underlyingValue, List):
			print("isinstance List true, hence entered this if-block")
			#Handle the methods of List
			if self.method in ['count', 'reverse', 'sort', 'lastel', 'firstel', 'sliced']:
				#Found self.method in the defined additional method for List
				if self.method is 'count':
					self.value = self.underlyingValue.count(self.methodParameter)	#Count the occurrences of self.methodParameter in the underlyingValue
				elif self.method is 'reverse':
					temp = self.underlyingValue[:]
					temp.reverse()
					self.value = List(temp[:])
					del temp
				elif self.method is 'sort':
					temp = self.underlyingValue[:]
					temp.sort()					#Next update, take a key for sort too
					self.value = List(temp[:])
					del temp
				elif self.method is 'lastel':
					print("self.underlyingValue is %s"%self.underlyingValue)
					temp = self.underlyingValue[-1]
					self.value = temp
					del temp

				elif self.method is 'firstel':
					print("self.underlyingValue is %s"%self.underlyingValue)
					temp = self.underlyingValue[0]
					self.value = temp
					del temp
				else:		#Case when self.method is sliced
					pass   ########################################################################################################################################
			elif self.method is '':
				self.value = self.dependency

			elif self.method is not '':			#Case when self.method is sent, but the relevant parameter isn't defined in the code 
				raise InvalidSubscriptionError("List object doesn't have %s as the method parameter"%self.method)

		elif isinstance(self.underlyingValue, Set):
			pass

		elif isinstance(self.underlyingValue, Dict):
			pass
		elif isinstance(self.underlyingValue, ByteArray):
			pass
		##########################



		#while isinstance(localValue, (ByteArray, Dict, List, Set)):			#Case where the underlying dependency belongs to BDLS
		#	localValue = localValue
		print("Calling update method of Observable")
		
		################ Check for type(self.dependency) here. If the type is List, then the methods are different, and if the type is Set, the methods are different. If the declared method isn't associated with the object, raise an Exception


		self.onchange()
		
		for element in dependencyGraph[self.id]:
			idVariableDict[element].update()
		self.underlyingValue = self.dependency 			#Restore self.underlyingValue from BDLS to Observe class. self.dependency is an Observable, while in the above declaration at the beginning of the update, we've changed it to a BDLS so that further calculations are possible.

	def onchange(self):				#Make this the method that is called every time there's a change in the underlying dependency, as the update method is no longer needed.
		print("Observable changed and value is %s"%self.value)

	def __repr__(self):			#This is the killer method! Without this, my life and architecture would've been ludicrously tough. Is this the golden bullet?
		return("%s"%self.value)

	def modifyMethod(self, method=''):
		if method is '':
			self.method = self.method
		else:
			self.method = method
		self.update()

class Subscribe:
	pass
