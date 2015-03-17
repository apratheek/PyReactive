#Create classes Observable and Subscribe 
#Observable applies on any property that needs to be observed
#Subscribe applies on cases where a variable depends on the subscribed values. A variable could Subscribe to one or more Observables, with an operand in case there's more than one observables. The operation is evaluated according to Infix notation.
#Create a global dictionary that is initialized when the module is imported. Hold the variable ids against the name of the variables. Whenever a Subscription comes in, check for its dependencies, create a dependency graph, and mention this in a list called VariablesThatDepend.


#UUID is the basis on which each variable is identified. In other words, the variable in a program is uniquely mapped to a UUID, which serves as the placeholder for the variable.
import uuid

_observable = {}
_depends_on = {}
cascadeEffect = {}
observerMethodAvailability = {list: ['sort','max','min','count','set'], str: ['split','set','list'] }	#Add other methods here as needed

subscribeMethodAvailability = {set: ['union','intersection','difference','symmetric_difference','list']}

class InvalidSubscriptionError(Exception):
	"""Special Exception that inherits from Base Exception class. Does nothing but raise a relevant exception"""
	pass

class Observe:
	"""Deals with all observables/properties."""
	
	global _observable, _depends_on, cascadeEffect
	def __init__(self, value, name='', method=''):		#Need to alter the list of parameters to include the argument for methods such as count, split, etc. 
		"""Initializes the observable. Also assigns a UUID"""
		self.id = uuid.uuid4()
		self.value = value
		self.method = method		#Declare a blank initially, so that after the first get(), we'll get to know about the typeOfGet, after which we'll know if the method argument can be performed on the data type. Otherwise, we'll raise an exception
		self.typeOfGet = ''
		localGet = self.get()
		self.typeOfGet = type(localGet)
		#Handle type check here, which means, check if self is a list, set, dict, tuple, or any other data type and check for the availability of the corresponding method
		if method is not '':
			if self.typeOfGet is list:
				if method in observerMethodAvailability[self.typeOfGet]:
					self.method = method
				else:
					raise AttributeError("'%s' object has no attribute '%s'"%(self.typeOfGet, method))
			elif self.typeOfGet is str:
				if method in observerMethodAvailability[typeOfGet]:
					self.method = method
				else:
					raise AttributeError("'%s' object has no attribute '%s'"%(self.typeOfGet, method))
			#elif typeOfGet is set:
			#	if method in observerMethodAvailability[typeOfGet]:
			#		self.method = method
			#	else:
			#		raise AttributeError("'%s' object has no attribute '%s'"%(typeOfGet, method))

		#This else block is pretty much redundant
		else:
			self.method = method 		#The assigned method would be a blank string

		#print("Value is %s"%self.value)
		_observable[self] = self.id
		cascadeEffect[self] = []
		if type(name) is str:
			self.name = name
		else:
			raise TypeError("Name has to be a string.")
		#print("%s"%_observable)

	def get(self):
		"""Returns the current value of the variable"""
		temp = self.value
		
		if type(temp) is Observe:
			while type(temp) is Observe:
				temp = temp.value
				continue
		if type(temp) is Subscribe:
			#Write the code for observing a Subscription.
			while type(temp) is Subscribe:
				temp = temp.value
				continue
		
		#Perform the method application at this level, so that the resultant value will always be in sync with the associated method
		#To remove the computation during the initialization, since the get() method is being called even during __init__, we could use a counter variable that counts the number of times the get() method is called. In other words, if the counter variable's value is 1, do not call the following block of statements, and if it's greater than 1, call the block. This reduced the __init__ time.
		if self.typeOfGet is list:
			#The self.method is not '' if statement is redundant, but is being used because more often than not, if there's no method initialised, the program would need to parse the entire if-else block to realise the case for when there's no method defined. A workaround for this is by placing the if case for the condition where there's no method right up as the first check, and the remaining would be overlooked. This might turn out to be efficient
			if self.method is not '':
				if self.method is 'sort':
					temp = sorted(temp)
				elif self.method is 'max':
					temp = max(temp)
				elif self.method is 'min':
					temp = min(temp)
				elif self.method is 'count':
					pass
					#Need to receive an additional parameter while initialising in case the count method is used
				elif self.method is 'set':
					temp = set(temp)

		elif self.typeOfGet is str:
			if self.method is not '':
				if self.method is 'split':
					pass
					#Need additional parameters while initialising
				elif self.method is 'set':
					temp = set(temp)
				elif self.method is 'list':
					temp = list(temp)

		#elif self.typeOfGet is set:

		return temp
	
	def update(self, value):
		"""Updates the value of the variable"""
		self.value = value
		#Whenever an update of a variable occurs, this update needs to cascade into an updation of the value of the subscripted variable that depends on it. And this could be done by maintaining a cascadeList.
		#Cascade the effect on to the subscription.
		if len(cascadeEffect[self]) != 0:
			for i in cascadeEffect[self]:
				Subscribe.update(i)


class Subscribe:
	"""Deals with the subscription of observables/properties."""

	global _observable, _depends_on, cascadeEffect
	def __init__(self, name = '', **args):
		"""Initializes the subscription. Compulsory arguments are var and op, where var is a tuple of variables that need to be subscribed to and op is the tuple of operands that operate upon the variables. v0.0.1 would only work for binary operators."""
		#print("args are %s"%args)
		try:
			self.variablesToObserve = list(args['var'])

			self.OperatorsList = list(args['op'])
			#_depends_on[self] = {}
			secondOperatorsList = self.OperatorsList[:]
		except:
			raise InvalidSubscriptionError("Can't initialize a subscription with no observables")
		#if len(args) is 0 or len(args['var']) is 0 or len(args['op'] is 0:
		#	raise InvalidSubscriptionError("Can't initialize a subscription with no observables")
		#Not handling unary operators here. Need to handle '++', '--', '- (negation)', byte shift. Also check for other unary operands
		

		
		for var in self.variablesToObserve:
			#Checking if the received variable is a predefined observable
			try:
				#variableId = var.id
				#if variableId not in _observable:
					#Case when the variable is an observable, except that it hasn't been declared in the local scope
				#	raise InvalidSubscriptionError("Not a local observable. Initialize the observable first")
				varId = _observable[var]
				#print("Variable UUID is %s"%varId)
			except:
				#Case when the variable passed isn't an observable
				raise InvalidSubscriptionError("Variable not an observable. Declare the variable as an observable before subscribing to it")

		if len(self.variablesToObserve) - 1 != len(self.OperatorsList):
			raise InvalidSubscriptionError("Can't initialize subscription. The number of variables should always be 1 more than the number of operands")
		#else:
		#	print(args)

		self.id = uuid.uuid4()
		cascadeEffect[self] = []

		_observable[self] = self.id
		self.name = name
		for i in self.variablesToObserve:
			cascadeEffect[i].append(self)
		self.update()
		#_depends_on[]

		#The procedure from here could be done using asyncio. The above process can't, because it would be too risky, as the variables passed might not be Observables. But at this point, all variables are checked for their nature, and only if they're Observables, can we reach this point of execution. Hence, it is safe to execute further code asynchronously.

		#BEGIN THE EVALUATION HERE
		#THE EVALUATION PRECEDENCE IS AS FOLLOWS:
		#1. ** OPERATOR GETS THE HIGHEST PREFERENCE
		#2. *, /, //, % GET THE NEXT PREFERENCE
		#3. + and - GET THE NEXT PREFERENCE
		#4. Also, in case of a tie, the L-to-R operator precedence is followed. This is because the first occurrence of the operator is found, evaluated, then the evaluation moves on to the second occurrence. 
		#BRACKETS AREN'T SUPPORTED YET, SO A WORKAROUND IS TO SUBSCRIBE A RESULTANT ON THE OBSERVABLES, AND THEN FURTHER PASS THIS VALUE TO THE NEW SUBSCRIPTION

		#CASE list(1: CHECK FOR THE PRESENCE OF ** IN OperatorsList, NOTE ITS LOCATION, POP THE RELEVANT OPERANDS FROM THE VARIABLESTOOBSERVE LIST, PERFORM THE OPERATION, ASSIGN IT TO A TEMP VARIABLE)
		#ALSO, COUNT THE NUMBER OF TIMES THE CORRESPONDING OPERATOR IS PRESENT. ITERATE THESE MANY TIMES, PICK UP THE CORRESPONDING ELEMENTS, PERFORM THE OPERATIONS, REPLACE THE CORRESPONDIlist(NG ELEMENTS WITH THE RESULT, THEN CONTINUE WITH OTHER OPERATIONS)

		#REWORK: CREATE A SET OF ALL OPERATORS AND LOOP THROUGH EACH OPERATOR. FOR EVERY OPERATOR, COUNT THE NUMBER OF TIMES OF OCCURRENCE, AND EVALUATE THE APPROPRIATE OPERANDS

	def update(self):
		"""This method needs to be hidden. Can only be called by Observables when there's an update in their values."""

		OperatorsSet = createSetInPrecedence(self.OperatorsList)		#Generates the set of all operators, and hence, this is unique. Also, the set has the operators according to their order of precedence, that is, the operator with the highest order of precedence will have a lower index.
		OperatorsListCopy = self.OperatorsList[:]
		#print("The operators set in order of precedence is %s"%OperatorsSet)
		#Here, instead of simply shallow copying the variablesToObserve list, copy the return values of every item with the .get() method. This would mean that only the latest values of the observables are used, and also, further calculation would be easier.
		alteredListCopy = self.variablesToObserve[:]
		alteredList = []
		for element in alteredListCopy:
			alteredList.append(element.get())

		for operator in OperatorsSet:
			#Send the list of variables, current operator and OperatorsList to a calculatingFunction that evaluates
			#print("The operator in __init__ is %s"%operator)
			alteredList = evaluateEquation(alteredList, operator, OperatorsListCopy)
			#print("The alteredList is %s"%alteredList)

		self.value = alteredList[0]		#Assign the last remaining value as the value of the expression
		#print(self.value)

		if len(cascadeEffect[self]) != 0:
			for i in cascadeEffect[self]:
				Subscribe.update(i)

		self.onchange()

	def onchange(self):
		pass


	def equation(self):
		"""Returns the current equation of the subscription"""
		equationString = ''
		if self.name != '':
			equationString = self.name + ' ='
		for i in range(len(self.variablesToObserve)):
			if i < len(self.OperatorsList):
				operatorEqn = self.OperatorsList[i]
			else:
				operatorEqn = ''
			if self.variablesToObserve[i].name == '':		#Case when name hasn't been defined
				nameOfVariable = str(self.variablesToObserve[i].get())
			else:
				nameOfVariable = self.variablesToObserve[i].name

			equationString += ' ' + nameOfVariable + ' ' + operatorEqn		#Instead of using .get(), use self.variablesToObserve.variableName here. Store variableName as an Observe class parameter and declare it at __init__ itself.
		self.equationString = equationString
		return self.equationString

	def get(self):
		"""Retrieve the latest value of the subscription"""
		return self.value


def createSetInPrecedence(OperatorsList):
	newOperatorList = []
	#Check for all operators here. In future, this can accomodate more operators
	if '**' in OperatorsList:
		newOperatorList.append('**')
		#print("newOperatorList is %s"%newOperatorList)
	if '*' in OperatorsList:
		newOperatorList.append('*')
		#print("newOperatorList is %s"%newOperatorList)
	if '/' in OperatorsList:
		newOperatorList.append('/')
		#print("newOperatorList is %s"%newOperatorList)
	if '%' in OperatorsList:
		newOperatorList.append('%')
		#print("newOperatorList is %s"%newOperatorList)
	if '//' in OperatorsList:
		newOperatorList.append('//')
		#print("newOperatorList is %s"%newOperatorList)
	if '+' in OperatorsList:
		newOperatorList.append('+')
		#print("newOperatorList is %s"%newOperatorList)
	if '-' in OperatorsList:
		newOperatorList.append('-')
		#print("newOperatorList is %s"%newOperatorList)
	return(newOperatorList)				#Returns the set of operators in the order of precedence


def evaluateEquation(alteredList, operator, OperatorsList):
	count = OperatorsList.count(operator)
	locOperator = 0
	for i in range(count):
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

		#print("AlteredList has become %s and OperatorsList has become %s"%(alteredList, OperatorsList))
		locOperator += 1		#Increase the location index so as to find the next location of the current operator
	return alteredList



def evaluateExpression(firstOperand, secondOperand, operator):
	#Check for the apposite operator, perform the operation nad return the result
	#print("Operator received in evaluateExpression is %s and type of operator is %s"%(operator,type(operator)))
	
	if len(operator) == 2:
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
		else:
			raise TypeError("No %s operator found"%operator)
	finally:

		#print("Result in evaluateExpression is %s"%result)
		return result

"""To Do: 
			Check		1. On subscription success, i.e., after all the variables are vetted, add an entry to the dictionary with the key being the UUID of the subscribing variable and the values being the UUIDs of the subscibed variables. TL; DR: Update the _depends_on dict
			Check		2. When an observable is UPDATED, issue a cascade effect that translates into the updation of all the Subscibing variables. The code for this needs to be written in the update() method of the Observe class 
			Check		3. Complete writing code for the method evaluateEquation looking at the comments
			Check 		4. Write code for Observing a Subscription
			Check 		5. Write a get() method inside the Subscribe class
			Check 		6. Modify the alteredList to hold the .get() values instead of a shallow copy of the variablesToObserve list. This also implies that every variable inside the list has a .get() method"""
