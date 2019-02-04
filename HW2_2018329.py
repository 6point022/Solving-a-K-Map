# CSE 101 - IP HW2
# K-Map Minimization 
# Name: Anmol Gupta
# Roll Number: 2018329
# Section: B
# Group: 2
# Date: 19/10/18

def binary_to_decimal(numVar, num):
	'''This function converts a decimal number to its binary representation.
	It takes the number of bits and the decimal representation of the number as the input.
	It returns the binary representation.'''
	bin = []
	while True:
		bin.append(num % 2)
		num //= 2
		if num == 0:
			break

	bin = bin[::-1]

	while len(bin) < numVar:
		bin.insert(0, 0)

	return bin

def extract_terms(numVar, s):
	'''This function extracts the minterms from the input string
	and returns their binary and decimal representation.
	It takes the number of variables and the minterm string as the input.'''
	term = []
	bin_term = []
	dontcare_term = []
	comma1_index = flag = 0

	index_dontcare = s.find('d (')

	if s.find(')') - s.find('(') == 1:
		return [], [], [] #if no minterm is sent, we return an empty list

	if index_dontcare == -1:
		while True:
			comma2_index = s.find(',', comma1_index + 1)

			if comma2_index == -1:
				comma2_index = s.find(')', comma1_index + 1)
				flag = 1

			term.append(int(s[comma1_index + 1:comma2_index]))

			if flag == 1:
				break

			comma1_index = comma2_index

	else:
		s1 = s[:index_dontcare - 1]
		s2 = s[index_dontcare + 2:]

		while True:
			comma2_index = s1.find(',', comma1_index + 1)

			if comma2_index == -1:
				comma2_index = s1.find(')', comma1_index + 1)
				flag = 1

			term.append(int(s1[comma1_index + 1:comma2_index]))

			if flag == 1:
				break

			comma1_index = comma2_index

		comma1_index = flag = 0

		while True:
			comma2_index = s2.find(',', comma1_index + 1)

			if comma2_index == -1:
				comma2_index = s2.find(')', comma1_index + 1)
				flag = 1

			dontcare_term.append(int(s2[comma1_index + 1:comma2_index]))

			if flag == 1:
				break

			comma1_index = comma2_index

	term_including_dontcare = term + dontcare_term
	term_including_dontcare.sort()

	for t in term_including_dontcare:
		bin_term.append(binary_to_decimal(numVar, t))

	return bin_term, term, dontcare_term

def common_bit(l, numVar):
	'''This function takes a list of binary representations and the number of variables as input.
	It returns a new list of binary numbers with a difference of only one bit and the input list
	with the upgraded entries deleted. We eventually get a list of prime implicants using this function.'''
	combined_terms = []
	c_unchecked = []
	c_unchecked_no_dupli = []
	temp_list = [0]

	for i in range(len(l)):
		flag = 0
		for j in range(len(l)):
			count_different = 0
			for k in range(numVar):
				if l[i][k] != l[j][k]:
					count_different += 1
					different_bit = k
			if count_different == 1:
				flag = 1
				temp_list[0] = l[i].copy()
				temp_list[0][different_bit] = '-'
				combined_terms.append(temp_list[0])

		if flag == 0:
			c_unchecked.append(l[i])

	for i in c_unchecked:
		if i not in c_unchecked_no_dupli:
			c_unchecked_no_dupli.append(i)

	return combined_terms, c_unchecked_no_dupli

def isSubstring(s1, s2):
	'''This function takes two strings, s1 and s2, as input and returns True if s1 is a substring of s2.'''
	flag = 0
	if len(s1) < len(s2):
		for char in s1:
			if char not in s2:
				flag = 1
				break

	else:
		return False

	if flag == 0:
		return True

	else:
		return False

def make_it_lexicographic(s):
	'''It takes the final string as input and returns the string
	sorted into lexicographic order.'''
	l1 = s.split(" OR ")
	l3 = []

	for t in l1:
		l2 = t.split("+")
		l2.sort(key=lambda k: k.replace('\'', ''))
		l3.append('+'.join(l2))

	l3.sort(key=lambda k: k.replace('\'', ''))

	return " OR ".join(l3)

def minFunc(numVar, stringIn):
	"""
        This python function takes function of maximum of 4 variables
        as input and gives the corresponding minimized function(s)
        as the output (minimized using the K-Map methodology),
        considering the case of Don’t Care conditions.

	Input is a string of the format (a0,a1,a2, ...,an) d(d0,d1, ...,dm)
	Output is a string representing the simplified Boolean Expression in
	SOP form.

        No need for checking of invalid inputs.
        
	Do not include any print statements in the function.
	"""
	c3 = []
	c4 = []

	c1, decimal_term, dontcare_term = extract_terms(numVar, stringIn)

	if len(decimal_term) == 0:
		return "0"

	decimal_term += dontcare_term
	decimal_term.sort()

	if len(decimal_term) == 2 ** numVar:
		return "1"

	if numVar == 1:
		if 0 in decimal_term:
			return "w'"
		else:
			return "w"

	c2, c1 = common_bit(c1, numVar)

	c3_temp, c2 = common_bit(c2, numVar)

	for i in c3_temp:
		if i not in c3:
			c3.append(i)

	if len(c3) != 0:
		c4_temp, c3 = common_bit(c3, numVar)
		for i in c4_temp:
			if i not in c4:
				c4.append(i)

	prime_implicants = c1 + c2 + c3 + c4

	decimal_values = []
	essential_primes = []

	for prime_implicant in prime_implicants:

		value = []
		v1 = v2 = v2a = v3 = v3a = v3b = v3c = v4 = 0

		count_hyphens = prime_implicant.count('-')

		if count_hyphens == 0:
			for i in range(0, numVar):
				v1 += prime_implicant[i] * 2 ** (numVar - 1 - i)
			value.append(v1)

		elif count_hyphens == 1:
			for i in range(0, numVar):
				if prime_implicant[i] == 1:
					v2 += 2 ** (numVar - 1 - i)
				elif prime_implicant[i] == '-':
					v2a += 2 ** (numVar - 1 - i)
			v2a += v2
			value.append(v2)
			value.append(v2a)

		elif count_hyphens == 2:
			for i in range(0, numVar):
				if prime_implicant[i] == 1:
					v3 += 2 ** (numVar - 1 - i)
				
			i1 = prime_implicant.index('-')
			i2 = prime_implicant.index('-', i1 + 1)

			v3a += v3 + 2 ** (numVar - 1 - i1)
			v3b += v3 + 2 ** (numVar - 1 - i2)
			v3c += v3a + v3b - v3

			value.append(v3) #when all hyphens are 0
			value.append(v3b) #when first hyphen is 1
			value.append(v3a) #when second hyphen is 1
			value.append(v3c) #when both the hyphens are 1

		elif count_hyphens == 3:
			for i in range(0, numVar):
				if prime_implicant[i] == 1:
					v1 += 2 ** (numVar - 1 - i)

			i1 = prime_implicant.index('-')
			i2 = prime_implicant.index('-', i1 + 1)
			i3 = prime_implicant.index('-', i2 + 1)

			v2 += v1 + 2 ** (numVar - 1 - i1)
			v2a += v1 + 2 ** (numVar - 1 - i2)
			v3 += v1 + 2 ** (numVar - 1 - i3)
			v3a += v3 + v2a - v1
			v3b += v3 + v2 - v1
			v3c += v2 + v2a - v1
			v4 += v3 + v2a + v2 - v1 - v1

			value.append(v1) #when all hyphens are 0
			value.append(v3) #when third hyphen is 1
			value.append(v2a) #when second hyphen is 1
			value.append(v3a) #when second and third hyphens are 1
			value.append(v2) #when first hyphen is 1
			value.append(v3b) #when first and third hyphens are 1
			value.append(v3c) #when first and second hyphens are 1
			value.append(v4) #when all hyphens are 1

		decimal_values.append(value)

	dictionary_prime_implicants = {}

	for p in range(len(decimal_values)):
		dictionary_prime_implicants[chr(65 + p)] = decimal_values[p]

	decimal_term = list(set(decimal_term) - set(dontcare_term))

	s = ''

	for minterm in decimal_term:
		s += "("
		for prime in dictionary_prime_implicants:
			if minterm in dictionary_prime_implicants[prime]:
				s += prime + '+'
		s += ")"		

	s = s.replace("+)", ")")

	l5 = []

	if s.count('(') == 1:
		for ch in dictionary_prime_implicants:
			l5.append(ch)

	for o in range(s.count("(") - 1):
		s = s.replace("+)", ")")

		i1 = s.find("(")
		i2 = s.find(")")

		term1 = s[i1 + 1:i2]

		i3 = s.find("(", i2 + 1)
		i4 = s.find(")", i2 + 1)

		term2 = s[i3 + 1:i4]

		s = s[i4 + 1:]

		m = n = 0
		l1 = []

		while True:
			m = term1.find('+', n)
			if m == -1:
				l1.append(term1[n:])
				break
			l1.append(term1[n:m])
			n = m + 1

		m = n = 0
		l2 = []

		while True:
			m = term2.find('+', n)
			if m == -1:
				l2.append(term2[n:])
				break
			l2.append(term2[n:m])
			n = m + 1

		l3 = []

		for a in l1:
			for b in l2:
				if a in b or b in a:
					if len(a) > len(b):
						l3.append(a)
					else:
						l3.append(b)
				else:
					l3.append(a + b)

		l3 = list(set(l3))

		l4 = l3.copy()

		for i in range(len(l4)):
			for j in range(len(l4)):
				if i != j:
					if isSubstring(l4[i], l4[j]) and l4[j] in l3:
						l3[j] = 0

		for i in range(l3.count(0)):
			l3.remove(0)

		min_len = len(l3[0])

		for t in l3:
			if len(t) < min_len:
				min_len = len(t)

		l5 = []

		for t in l3:
			if len(t) == min_len:
				l5.append(t)

		s2 = "("

		for t in l3:
			s2 += t
			s2 += "+"

		s2 += ")"

		s = s2 + s

	stringOut = ''

	for one_solution in l5:

		final_terms = []

		for ch in one_solution:
			index_prime = decimal_values.index(dictionary_prime_implicants[ch])
			j = 0
			w = ''
			for i in prime_implicants[index_prime]: # converting the numerical binary representations into alphabetical representation
				if i == 1:
					if numVar - 1 - j == 3:
						w += 'w'
					elif numVar - 1 - j == 2:
						w += 'x'
					elif numVar - 1 - j == 1:
						w += 'y'
					elif numVar - 1 - j == 0:
						w += 'z'
				if i == 0:
					if numVar - 1 - j == 3:
						w += 'w\''
					elif numVar - 1 - j == 2:
						w += 'x\''
					elif numVar - 1 - j == 1:
						w += 'y\''
					elif numVar - 1 - j == 0:
						w += 'z\''
				j += 1

			final_terms.append(w)

		final_string = ''

		for x in final_terms:
			final_string += x + '+'

		stringOut += final_string[:-1]
		stringOut += " OR "

	last_OR_index = stringOut.rfind(" OR ")
	stringOut = stringOut[:last_OR_index]

	if numVar == 3:
		stringOut = stringOut.replace('x', 'w')
		stringOut = stringOut.replace('y', 'x')
		stringOut = stringOut.replace('z', 'y')

	elif numVar == 2:
		stringOut = stringOut.replace('y', 'w')
		stringOut = stringOut.replace('z', 'x')

	stringOut = make_it_lexicographic(stringOut)

	return stringOut

# print(minFunc(3, "(0,1,2,4,5) d (6)"))
# print(minFunc(4, "(1,3,7,11,15) d (0,2,5)"))
#print(minFunc(4, "(0,2,3,4,5,6,7,8,9,10,11,12,13) d -"))
#print(minFunc(4, "(0,2,5,6,7,8,10,12,13,14,15) d -"))
print(1, minFunc(2, "(1) d (0,3)") )
print(2, minFunc(2, "(1,2) d -") )
print(3, minFunc(3, "(3,4,7) d (1,2,5,6)") )
print(4, minFunc(3, "(0,1,2,5,6,7) d -") )
print(5, minFunc(4, "(3,9,12,15) d (0,1,4,7,8,10,11,14)") )
print(6, minFunc(4, "(0,1,4,5,7,9,10,11,13,15) d -") )
print(7, minFunc(4, "(0,1,2,3,4,5,6) d (7,8,9,10,11,12,13,14,15)") )
