#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import getpass

C_YN = ['y','Y','n','N']

def promptSimple(question,default = ''):
	"""
		The ``promptSimple`` function
		=============================
		
		Use it for a text required input from stdin
		
		:param question: Text displayed before text input
		:type question: string

		:return: user typed text
		:rtype: string

		:Example:

		>>> from Prompt import *
		>>> promptSimple('What is the answer to life, the universe, and everything?')
		What is the answer to life, the universe, and everything?
		0 = Exit
		42
		'42'
		
	"""
	str_default = ''
	if default != '':
		str_default = ' [' + str(default) + ']'
	reponse = raw_input(question + str_default + "\n0 : Exit\n")
	if reponse == '':
		reponse = str(default)
	elif reponse == "0":
		sys.exit()
	return reponse

def promptPass(question):
	"""
		The ``promptPass`` function
		=============================
		
		Use it for a password required input from stdin
		User input will not been shown during typing
		
		:param question: Text displayed before password input
		:type question: string

		:return: user typed text
		:rtype: string

		:Example:

		>>> from Prompt import *
		>>> promptPass('Okay. Whats the password?')
		Okay. Whats the password?
		0 = Exit

		'You got it'
		
	"""
	reponse = getpass.getpass(question + "\n0 : Exit\n")
	if reponse == "0":
		sys.exit()
	return reponse

def promptChoice(question,choix,default = 0):
	"""
		The ``promptChoice`` function
		=============================
		
		Use it for let user select a choice in a restricted choices list
		
		:param question: Text displayed before choice list
		:type question: string
		
		:param choix: List of choices. Choices are list of number and choice label
		:type choix: list

		:param default: Index of the default choice (0 by default, ie. the first choice)
		:type choix: Integer

		:return: Index of the choice
		:rtype: Integer

		:Example:

		>>> from Prompt import *
		>>> promptChoice("What do you prefer?",[[12,'Duck'],[34,'Rabbit'],[56,'Snail']],2)
		What do you prefer? [3 by default]
		1 : Duck
		2 : Rabbit
		3 : Snail
		0 : Exit
		2
		34
		
	"""
	while True:	
		possible = []
		print(question + " [" + str(default+1) + " by default]")
		for i,val in enumerate(choix):
			possible.append(str(val[0]))
			print(str(i+1) + " : " + val[1])
		reponse = raw_input("0 : Exit\n")

		if reponse == "0":
			sys.exit()

		reponse = str(choix[default][0]) if reponse == '' else reponse

		if int(reponse) < len(choix)+1 and int(reponse) > 0:
			return choix[int(reponse)-1][0]
		else:
			print('incorrect choice')
	
def promptYN(question,default = C_YN[0]):
	"""
		The ``promptYN`` function
		=========================
		
		Use it for let user select between Yes or No
		
		:param question: Text displayed before choice
		:type question: string

		:param default: Default answer ('Y' by default)
		:type choix: Character

		:return: answer
		:rtype: Boolean

		:Example:

		>>> from Prompt import *
		>>> promptYN("Luke, I'm your father",'N')
		Luke, I'm your father [y/N] n
		False
		
	"""
	while True:
		if default not in C_YN:
			default = C_YN[0]
		str_y = C_YN[1] if default.lower() == C_YN[0] else C_YN[0] 
		str_n = C_YN[3] if default.lower() == C_YN[2] else C_YN[2] 
		reponse = raw_input(question + " [" + str(str_y) + "/" + str(str_n) + "] ")

		reponse = str(default) if reponse == '' else reponse

		if reponse in C_YN[0:2]:
			return True
		elif reponse in C_YN[2:4]:
			return False
		else:
			print('incorrect choice')

