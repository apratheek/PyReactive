import uuid
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
		super(List, self).__init__(args)
		#At __init__, set up an entry in the dependencyGraph

		#print(dependencyGraph)
		##print("List initialised")

	def onchange(self):
		#print("List object has changed --> onchange method called")
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
	"""Deals with all observables
		Takes the dependency, an optional name for the object, an optional method, and an optional method parameter.
		The optional methods are:

		1. In case of List
			a) count - holds the count of the element passed as the methodParameter
			b) reverse - holds the reverse of the List. methodParameter is invalid
			c) lastel - always holds the last element of the List. methodParameter is invalid
			d) firstel - always holds the first element of the list. methodParameter is invalid
			e) sort - always holds the sorted List. methodParameter could be the sort key
			f) slice - always holds the sliced part of the List. methodParamter is only a slice object, e.g. methodParameter = slice(0, x, y)
			g) set - always holds the unique elements in the List. methodParameter is invalid

		2. In case of Set
			As of this version, there's nothing to Observe. Could be used for future expansion

		3. In case of Dict
			a) key - holds the current value of the key. methodParameter is one of the keys of the Dict

		4. In case of ByteArray
			Need to add documentation for this
			"""
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
				#print("Setting dependencyGraph attribute")
				dependencyGraph[dependency.id].append(self.id)				################################### Key assignment. This is where the actual dependency is stated.
				dependencyGraph[self.id] = []
				self.update()									#This sets self.value in the update method


		except:
			#Case where value is a native mutable/immutable data type. If it is a mutable data type, ignore it and raise an exception. Don't allow mutable data types. This is only for immutable data types.
			#self.dependency = None
			self.value = self.dependency
			#if method is 'not' or method is '~' or method is 'len' :
				#print("method is not")
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





	def update(self):
		"""Sets the value of the Observable every time this is called. It is called at __init__ and at every time that the underlying dependency changes. If the underlying dependency is a native mutable or a native immutable, this method won't be called. This is only called when the dependency belongs to BDLS"""
		#Update method cannot be removed, since it would also deal with Observable methods suchs as sort, remove etc.



		if isinstance(self.underlyingValue, Observe):			#This is the case when there's an Observable, and it needs to be distilled down to either
			#print("isinstance Observe true. Hence changing underlyingValue to dependency.value")
			self.underlyingValue = self.dependency.value 		#This is done so as to assign the underlyingValue to dependency.value --> this would mean that currently, the underlyingValue is modified to be a List object rather than an Observe object. For further clarification, in the interpreter, check the values of type(self.underlyingValue) and type(self.dependency.value). The former yields an Observe and the latter yields a BDLS. This is so that the further actions can be operated on BDLS, rather than on the Observable, since an Observable does not have the necessary methods that a BDLS has.


		########################## WRITE CODE FOR HANDLING METHOD ATTRIBUTE HERE

		if isinstance(self.underlyingValue, (str, tuple, frozenset)):
			#print("isinstance immutables true, hence entered this if-block")
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
					#print("Entered not case of int, float, bool")
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
				#print("entered case where method is null")
				self.value = self.dependency
			elif self.method is not '':
				raise InvalidSubscriptionError("%s method on this object isn't applicable"%self.method)

		elif isinstance(self.underlyingValue, List):
			#print("isinstance List true, hence entered this if-block")
			#Handle the methods of List
			if self.method in ['count', 'reverse', 'sort', 'lastel', 'firstel', 'slice', 'set', 'len', 'sum']:
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
					#print("self.underlyingValue is %s"%self.underlyingValue)
					try:
						temp = self.underlyingValue[-1]
					except:
						temp = None
					self.value = temp
					del temp

				elif self.method is 'firstel':
					#print("self.underlyingValue is %s"%self.underlyingValue)
					try:
						temp = self.underlyingValue[0]
					except:
						self.value = temp
					del temp
				elif self.method is 'set':
					#print("self.underlyingValue is %s"%self.underlyingValue)
					temp = self.underlyingValue[:]
					temp = set(temp)
					self.value = temp
					del temp

				elif self.method is 'slice':
					#print("self.underlyingValue is %s"%self.underlyingValue)		#Case when self.method is sliced
					self.value = self.underlyingValue[self.methodParameter]

				elif self.method is 'sum':
					self.value = sum(self.underlyingValue)

				elif self.method is 'len':
					self.value = len(self.underlyingValue)
					   ########################################################################################################################################
			elif self.method is '':
				self.value = self.dependency

			elif self.method is not '':			#Case when self.method is sent, but the relevant parameter isn't defined in the code
				raise InvalidSubscriptionError("List object doesn't have %s as the method parameter"%self.method)

		elif isinstance(self.underlyingValue, Set):
			#print("There's nothing to Observe in a Set")
			#if self.method in ['issubset', 'issuperset', 'isdisjoint']:
			#	if self.method is 'issubset':

			#	elif self.method is 'issuperset':

			#	elif self.method is 'isdisjoint':

			if self.method in ['len', 'difference', 'intersection', 'isdisjoint', 'issubset', 'issuperset', 'symmetric_difference', 'union', 'sum']:
				if self.method is 'len':
					self.value = len(self.underlyingValue)
				elif self.method is 'sum':
					self.value = sum(self.underlyingValue)
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
							#print("isdisjoint checked")
						elif self.method is 'issubset':
							self.value = self.dependency.issubset(self.methodParameter)
						elif self.method is 'issuperset':
							self.value = self.dependency.issuperset(self.methodParameter)
							#print('issuperset checked')
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
			#print("isinstance Dict is true, hence entered the Corresponding if-block")
			if self.method in ['key', 'len', 'sum']:				#Keep this so that it can be extended easily to acoomodate other methods in the future
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
			elif self.method is '':
				self.value = self.dependency
			elif self.method is not '':
				raise InvalidSubscriptionError("Dict object doesn't have %s as the method parameter"%self.method)

		elif isinstance(self.underlyingValue, ByteArray):
			if self.method in ['len']:
				if self.method is 'len':
					self.value = len(self.underlyingValue)
			elif self.method is '':
				self.value = self.dependency
			elif self.method is not '':
				raise InvalidSubscriptionError("ByteArray object doesn't have %s as the method parameter"%self.method)

		##########################



		#while isinstance(localValue, (ByteArray, Dict, List, Set)):			#Case where the underlying dependency belongs to BDLS
		#	localValue = localValue
		#print("Calling update method of Observable")

		################ Check for type(self.dependency) here. If the type is List, then the methods are different, and if the type is Set, the methods are different. If the declared method isn't associated with the object, raise an Exception


		for element in dependencyGraph[self.id]:
			idVariableDict[element].update()

		self.underlyingValue = self.dependency 			#Restore self.underlyingValue from BDLS to Observe class. self.dependency is an Observable, while in the above declaration at the beginning of the update, we've changed it to a BDLS so that further calculations are possible.
		self.notify()

	def notify(self):				#Make this the method that is called every time there's a change in the underlying dependency, as the update method is no longer needed.
		"""This method is supposed to be overridden to perform anything of value whenever a change occurs"""
		pass
		#print("Observable changed and value is %s"%self.value)

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

		self.id = uuid.uuid4()
		dependencyGraph[self.id] = []
		idVariableDict[self.id] = self
		self.name = name

		for var in self.variablesSubscribedTo:
			dependencyGraph[var.id].append(self.id)			#Declare the dependency of the Subsciption object on each of the variablesSubscribedTo.

		self.update()		#Call the update method to calculate the value


	def update(self):
		operatorsSet = createSetInPrecedence(self.operatorsList)
		operatorsListCopy = self.operatorsList[:]
		tempVariablesSubscribedTo = self.variablesSubscribedTo[:]
		tempVariablesSubscribedTo2 = []
		for var in tempVariablesSubscribedTo:
			if isinstance(var, (Observe, Subscribe)):
				tempVariablesSubscribedTo2.append(var.value)	#In case var is an Observe/Subscribe object
			else:
				tempVariablesSubscribedTo2.append(var)		#In case var is a simple BDLS
			#tempVariablesSubscribedTo2 is now the list of all variables with the corresponding values. This aids in calculations

		for operator in operatorsSet:
			tempVariablesSubscribedTo2 = evaluateEquation(tempVariablesSubscribedTo2, operator, operatorsListCopy)

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
		##print("newOperatorList is %s"%newOperatorList)
	#if '~' in operatorsList:	#This is a unary operand. Should be on the observe object
	#	newOperatorList.append('~')


	if '*' in operatorsList:
		newOperatorList.append('*')
		##print("newOperatorList is %s"%newOperatorList)
	if '/' in operatorsList:
		newOperatorList.append('/')
		##print("newOperatorList is %s"%newOperatorList)
	if '%' in operatorsList:
		newOperatorList.append('%')
		##print("newOperatorList is %s"%newOperatorList)
	if '//' in operatorsList:
		newOperatorList.append('//')
		##print("newOperatorList is %s"%newOperatorList)
	if '+' in operatorsList:
		newOperatorList.append('+')
		##print("newOperatorList is %s"%newOperatorList)
	if '-' in operatorsList:
		newOperatorList.append('-')
		##print("newOperatorList is %s"%newOperatorList)

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

def evaluateEquation(alteredList, operator, OperatorsList):
	count = OperatorsList.count(operator)
	locOperator = 0
	for i in range(count):
		#print("Count value is %s"%i)
		#print("locOperator is %s"%locOperator)
		#print("OperatorsList is %s"%OperatorsList)
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

		resultant = evaluateExpression(firstOperand, secondOperand, operator)		#Send the expression to another function, and the result will be replaced in the original variablesToObserve, along with the removal of the operator at that location from OperatorsList

		alteredList.pop(locOperator)		#Pop the two operands, and replace them with the resultant
		alteredList.pop(locOperator)

		alteredList.insert(locOperator, resultant)		#Insert the resultant at the location where the two operands have been removed
		OperatorsList.remove(operator)					#Also remove the operator, since it has been evaluated

		##print("AlteredList has become %s and OperatorsList has become %s"%(alteredList, OperatorsList))
		#locOperator += 1		#Increase the location index so as to find the next location of the current operator
	return alteredList

def evaluateExpression(firstOperand, secondOperand, operator):
	#Check for the apposite operator, perform the operation nad return the result
	##print("Operator received in evaluateExpression is %s and type of operator is %s"%(operator,type(operator)))

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

		##print("Result in evaluateExpression is %s"%result)
		return result
