import tokenize
import math
import sys

if sys.version_info[0] == 2:
    #print("Running on Python 2")
    from StringIO import StringIO
    version = 2
else:
    #print("Running on Python 3")
    from io import BytesIO
    version = 3

class ReversePolish:

    def __init__(self, expression):
        #Accepts the expression and makes it an attribute
        self.expression = expression
        #Define the weights of each operator in a dict
        self.operator_weight = {
                                    'or' : 1,   #Boolean OR
                                    'and' : 2,  #Boolean AND
                                    'not' : 3,  #Boolean NOT
                                    '|' : 4,    #Bitwise OR
                                    '^' : 5,    #Bitwise XOR
                                    '&' : 6,    #Bitwise AND
                                    '<<' : 7, '>>' : 7,     #Bitwise Shifts
                                    '+' : 8, '-' : 8,       #Addition and Subtraction
                                    '*' : 9, '/' : 9, '//' : 9, '%' : 9,    #Multiplication, Division, Remainder
                                    '~' : 10,   #Bitwise NOT
                                    '**' : 11,  #Exponentiation
                                    'sin' : 12, 'cos' : 12, 'tan' : 12, 'round' : 12, 'ceil' : 12, 'floor' : 12, 'abs' : 12,  #Mathematical functions
                                    '(' : 13, ')' : 13, '{' : 13, '}' : 13, '[' : 13, ']' : 13  #Parantheses
                                }
        #Hold the list of applicable operators in a separate list
        self.applicable_operators = list(self.operator_weight.keys())
        #Hold binary operators in a list
        self.binary_operators = ['or', 'and', '|', '^', '&', '<<', '>>', '+', '-', '*', '/', '//', '%', '**']
        #Hold unary operators in a list
        self.unary_operators = ['sin', 'cos', 'tan', 'round', 'ceil', 'floor', 'abs', 'not', '~']
        #Hold the matching brackets in another list
        self.matching_brackets = {
                                    '}' : '{',
                                    ')' : '(',
                                    ']' : '['
                                }
        #Now tokenize the expression
        self.tokenize()
        #Convert from infix to postfix notation
        self.postfix()


    def __repr__(self):
        return self.expression

    def tokenize(self):
        #The logic for the tokenizer
        #At init, the expression is assigned to self.expression. Hence, expression becomes an attribute

        self.tokenized_list = []
        if version == 3:    #Code for Python 3
            tokens = tokenize.tokenize(BytesIO(self.expression.encode("UTF-8")).readline)
            for token in tokens:
                try:
                    #For >v3.1, where token is a namedtuple
                    self.tokenized_list.append(token.string)
                except:
                    #For v3.0, where token isn't a namedtuple
                    #String is the second element of the tuple
                    self.tokenized_list.append(token[1])
            self.tokenized_list.pop()   #Pop the last element which is the ENDMARKER
            self.tokenized_list.pop(0)  #Pop the first element which is the ENCODING

        else:               #Code for Python 2
            tokens = tokenize.generate_tokens(StringIO(self.expression.encode("UTF-8")).readline)
            #print("tokens in python2 is %r"%tokens)
            for token in tokens:
                self.tokenized_list.append(token[1])    #String is the second element of the tuple
            self.tokenized_list.pop()   #Pop the last element which is the ENDMARKER

    def postfix(self):
        #Initialize an empty operator stack and an empty postfix stack
        #Loop through each token in the tokenized_list and keep pushing elements on to appropriate stacks
        self.operator_stack = []    #A temporary stack to hold the operators
        self.postfix_stack = []     #Holds the postfix string as a list
        for token in self.tokenized_list:
            #print("Token in for loop beginning is %s"%token)
            if token in self.applicable_operators:
                #Token is an operator

                if len(self.operator_stack) == 0:
                    #Stack is empty. Hence, push the operator
                    #print("Stack is empty and token is %s"%token)
                    self.operator_stack.append(token)

                elif token == '(' or token == '{' or token == '[':
                    #Token is an open parantheses. Push it to the operator_stack
                    #print("Opening bracket found")
                    self.operator_stack.append(token)

                elif token == ')' or token == '}' or token == ']':
                    #Token is a close parantheses. Find the matching opening parantheses and pop all the elements in the stack until the opening parantheses.
                    #print("postfix_stack is %s"%self.postfix_stack)

                    while self.operator_stack[-1] is not self.matching_brackets[token]:
                        #Keep popping the stack until the matching closing parantheses is found. When the loop exits, pop the opening parantheses too.
                        lastel = self.operator_stack.pop()
                        #print("lastel is %s"%lastel)
                        self.postfix_stack.append(lastel)

                    #At this point, the last element of the operator_stack is '(' or '{' or '['. Pop that element too
                    self.operator_stack.pop()

                else:
                    #The stack is not empty. Need to check operator weight before further processing
                    #Retrieve the last element of the stack and check its weight. If its weight is higher, then pop that element and append it to the postfix_stack, and append this new operator to the operator_stack.
                    try:
                        #Greater than or equal to used because the same logic is followed in both the cases (when there's a left to right associativity)
                        while self.operator_weight[self.operator_stack[-1]] >= self.operator_weight[token] and self.operator_stack[-1] not in self.matching_brackets.values():
                            #The weight of the last operator on the stack is higher than the current token. Hence, pop the operator with the higher weight and append it to postfix_stack.
                            previous_operator_in_stack = self.operator_stack.pop()
                            self.postfix_stack.append(previous_operator_in_stack)
                    except:
                        pass

                    self.operator_stack.append(token)

            else:
                #Token is an operand. Push it to postfix_stack
                self.postfix_stack.append(token)

        #After iterating through all the operands, append the ones present in the operator_stack to the postfix_stack in the reverse order
        while self.operator_stack:
            operator = self.operator_stack.pop()
            self.postfix_stack.append(operator)

    def display_rpn(self):
        print((" ").join(self.postfix_stack))

    def evaluate(self, postfix_expression):
        #Evaluate postfix expression and return the value.
        self.postfix_expression = postfix_expression
        localStack = []
        for token in self.postfix_expression:
            if token in self.applicable_operators:
                #Token is an operator
                #print("Token is in applicable_operators and its value is %s"%token)
                if token in self.binary_operators:
                    #Pop the last two elements of the stack and perform the operation
                    try:
                        #First pop is the second operand
                        second_operand = localStack.pop()
                        #Second pop is the first operand
                        first_operand = localStack.pop()
                    except:
                        raise SyntaxError("Seems like there's something wrong with the syntax. Probable cause: Too many operands/operators")

                    if isinstance(first_operand, str):
                        #Convert only if the operands are strings
                        first_operand = convert(first_operand)
                    if isinstance(second_operand, str):
                        #Convert only if the operands are strings
                        second_operand = convert(second_operand)

                    #print("TYPE OF first_operand is %s"%type(first_operand))
                    #print("TYPE OF second_operand is %s"%type(second_operand))

                    if token == 'or':
                        result = first_operand or second_operand
                    elif token == 'and':
                        result = first_operand and second_operand
                    elif token == '|':
                        result = first_operand | second_operand
                    elif token == '^':
                        result = first_operand ^ second_operand
                    elif token == '&':
                        result = first_operand & second_operand
                    elif token == '<<':
                        result = first_operand << second_operand
                    elif token == '>>':
                        result = first_operand >> second_operand
                    elif token == '+':
                        result = first_operand + second_operand
                    elif token == '-':
                        result = first_operand - second_operand
                    elif token == '*':
                        result = first_operand * second_operand
                    elif token == '/':
                        if second_operand == 0:
                            raise ZeroDivisionError("integer division or modulo by zero")
                        else:
                            result = first_operand / second_operand
                    elif token == '//':
                        if second_operand == 0:
                            raise ZeroDivisionError("integer division or modulo by zero")
                        else:
                            result = first_operand // second_operand
                    elif token == '%':
                        if second_operand == 0:
                            raise ZeroDivisionError("integer division or modulo by zero")
                        else:
                            result = first_operand % second_operand
                    elif token == '**':
                        result = first_operand ** second_operand
                    #Append the result to localStack
                    localStack.append(result)

                elif token in self.unary_operators:
                    try:
                        unary_operand = localStack.pop()
                    except:
                        raise SyntaxError("Seems like there's something wrong with the syntax. Probable cause: Too many operands/operators")

                    if isinstance(unary_operand, str):
                        #Convert only if the operands are strings
                        unary_operand = convert(unary_operand)

                    #Perform the operation on the last element of the stack
                    if token == 'sin':
                        result = math.sin(unary_operand)
                    elif token == 'cos':
                        result = math.cos(unary_operand)
                    elif token == 'tan':
                        result = math.tan(unary_operand)
                    elif token == 'round':
                        result = round(unary_operand)
                    elif token == 'ceil':
                        result = math.ceil(unary_operand)
                    elif token == 'floor':
                        result = math.floor(unary_operand)
                    elif token == 'abs':
                        result = math.fabs(unary_operand)
                    elif token == 'not':
                        result = not unary_operand
                    elif token == '~':
                        result = ~unary_operand
                    localStack.append(result)
            else:
                #Token is not an operand. Should be an identifier. Hence, append it to the stack
                localStack.append(token)
        #The loop has exited. At this point, there should only be 1 element in the stack. Otherwise, this is an error.
        if len(localStack) != 1:
            raise SyntaxError("Couldn't consume stack. Too many operators.")
        else:
            final_result = localStack.pop()
        return final_result

def convert(operand):
    #Function that converts string to either Integer or Float, depending on its nature
    #print("Operand received in convert is %s"%operand)
    try:
        if operand.isnumeric():
            #This is an integer. Convert it to int
            #print("Operand is numeric")
            operand = int(operand)
        else:
            #This could either be a float or an identifier. Although, if properly designed, it won't be an identifier.
            #if int(float(operand)) == float(operand):
                #This is a float. Perform a floating point conversion
            #print("Operand is float")
            operand = float(operand)
    except FloatingPointError:
        print("Couldn't convert to floating point")
    return operand
