#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Libraries
import sys
import time
import logging
import platform
import os
import random

# Modules
import core.log
from core.data.wordlist import *
from core.data.crossword import *
from core.data.constants import *
from core.helpers.parse import *
from core.implements.basic_backtracking import *
from core.implements.fc_backtracking import *
from core.implements.live_backtracking import *
from cli.arguments.parsers import DEFAULT_PARSER
from cli.arguments.constants import *
from cli.printers.crossword import *
from renderer.cwboard import CrosswordBoard

# Constants
LOGGER = logging.getLogger(__name__)

# Functions
"""
Takes the system arguments vector and tries to parse the arguments in it given
the argument parser specified and returns the namespace generated

@param 	parser 	the ArgumentParser objects to use to parse the arguments
"""
def parseArguments(parser):
	return parser.parse_args()

"""
Given the origin of the data for the wordlist, loads the wordlist and returns
it, while giving some information about it if it's required

@param 	origin		the source to load the wordlist from
@param 	isThesaurus	the source is an Hunspell thesaurus
@return wordlist valid object (or None if couldn't load)
"""
def loadWordlist(origin, isThesaurus=False):
	LOGGER.info("-> Loading wordlist (from %s)",origin)
	wordlist = WordList(origin, isThesaurus)
	if args.timers > 1: 	time_load_wordlist_start = time.time()
	wordlist.read()
	if args.timers > 2:
		LOGGER.info("--> Read   in %f seconds",time.time()-\
		time_load_wordlist_start)
		time_load_wordlist_start_parse = time.time()
	wordlist.parse()
	if args.timers > 2:
		LOGGER.info("--> Parsed in %f seconds",time.time()-\
		time_load_wordlist_start_parse)
	if args.timers > 1:
		LOGGER.info("--> Loaded in %f seconds",time.time()-\
		time_load_wordlist_start)
	if args.show_wordlist:
		LOGGER.info(wordlist)
	return wordlist

"""
Given the origin of the data for the crossword, loads the crossword and returns
it, while giving some information about it if it's required

@param 	origin 	the source to load the wordlist from
@return crossword valid object (or None if couldn't load)
"""
def loadCrossword(origin):
	crossword = Crossword(origin)
	LOGGER.info("-> Loading crossword (from %s)",origin)
	if args.timers > 1:		time_load_crossword_start = time.time()
	crossword.read().parse()
	if args.timers > 1:
		LOGGER.info("--> Loaded in %f seconds",time.time()-\
		time_load_crossword_start)
	if args.show_crossword:
		LOGGER.info(crossword)
	return crossword

"""
Retrieves the algorithm object to use depending on the arguments

@return algorithm callable object
"""
def selectAlgorithm():
	alg = None
	LOGGER.info("Chose %s algorithm"%args.algorithm)
	if args.algorithm == ALG_BACKTRACKING_SIMPLE:
		alg = CrosswordBasicBacktracking(wordlist.getList(),
			crossword.getConstraints())
	elif args.algorithm == ALG_BACKTRACKING_FC:
		alg = CrosswordForwardCheckingBacktracking(wordlist.getList(),
			crossword.getConstraints())
	elif args.algorithm == ALG_BACKTRACKING_LIVE:
		crossword_printer = CrosswordPrinter(crossword,args.frames)
		crossword_printer.setStyle(args.style)
		alg = CrosswordLiveBacktracking(wordlist.getList(),
			crossword.getConstraints(),crossword_printer)
	return alg

"""
Given the solution returned from the crossword, searches the thesaurus (if any)
for the definitions of the words appearing in the solution and shows the user
the definitions so they can solve the crossword theyreselves.

If no thesaurus is provided, then goes on line to search in Wiktionary:
- https://www.wiktionary.org/
(only on line search for Catalan language is supported)

The crossword board, solution and its word definitions are then rendered
in an HTML file.

@param 	solution 	solution to show hints
"""
def playGame(solution):
	LOGGER.info("---- GAME MODE ----")
	LOGGER.info("I want to play a game...")
	#game_board = CrosswordBoard(crossword.getLists())
	game_board = CrosswordBoard(crossword.getOrigin())
	game_board.setSolution(crossword.getVariables(), solution)
	if wordlist._thes is None:
		# searches over the internet for the definitions
		from bs4 import BeautifulSoup
		import mwapi
		session = mwapi.Session('https://ca.wiktionary.org')
		for word_i in range(len(solution)):
			word = "".join(list(map(chr,solution[word_i]))).lower()
			var = crossword.getVariableString(word_i)
			resp = session.get(action='query',prop='extracts',titles=word)\
			["query"]["pages"]
			pages = list(resp.keys())
			try:
				extract = resp[pages[0]]["extract"]
			except:
				extract = None
			parser = None
			if extract:
				parser = BeautifulSoup(extract,"html.parser").findAll("li")
			definition = ""
			if parser != None:
				valid_defs = []
				for info in parser:
					text = info.getText()
					if "Pronúncia" in text \
					or "Exemples" in text \
					or "Etimologia" in text \
					or "Per a més informació vegeu" in text\
					or len(text.split()) < 4:
						continue
					else:
						valid_defs.append(text)
				if len(valid_defs):
					definition = random.choice(valid_defs)
			if definition == "":
				definition = word + " (no hem trobat cap definició)"
			LOGGER.info("%s: %s",var,definition)
			game_board.updateClues(crossword.get2DVariable(word_i), definition)
	else:
		# searches the thesaurus
		for word_i in range(len(solution)):
			word = "".join(list(map(chr,solution[word_i]))).lower()
			var = crossword.getVariableString(word_i)
			valid_defs = wordlist._thes.lookup(word)
			definition = ""
			if valid_defs is not None:
				meanings = [mean.main for mean in valid_defs.mean_tuple]
				definition = random.choice(meanings)
			if definition == "":
				definition = word + " (no hem trobat cap definició)"
			LOGGER.info("%s: %s",var,definition)
			game_board.updateClues(crossword.get2DVariable(word_i), definition)
	html_file_name = game_board.render()
	LOGGER.info("Built HTML file in '{}'".format(html_file_name))

"""
Given a solution from the crossword, tries to print it over the screen, or logs
that no solution was found if necessary

@param 	solution 	solution to print
"""
def showSolution(solution):
	if solution == None:
		LOGGER.info("The algorithm hasn't found any valid solution :(")
	else:
		printer = CrosswordPrinter(crossword)
		printer.setStyle(args.style)
		if args.solution:
			if args.play:
				print(printer)
				playGame(solution)
			elif args.algorithm != ALG_BACKTRACKING_LIVE:
				printer.printSolution(solution)
		else:
			LOGGER.info("The algorithm has found a valid solution :)")

if __name__ == "__main__":
	# Prepare coding
	if platform.system() == "Windows":
		os.system("chcp 65001")

	# Parse arguments
	args = parseArguments(DEFAULT_PARSER)

	# Set default tablesets
	args.style = CHAR_TABLESETS[args.style]

	# Welcome
	LOGGER.info("Welcome to Crossword solver")
	# Load data
	LOGGER.info("Loading crossword and wordlist")
	if args.timers > 0:		time_load_start = time.time()

	# Datasets
	if args.wordlist == None:
		args.wordlist = ITEMSET_BYNAME[args.itemset]["wordlist"]
	if args.crossword == None:
		args.crossword = ITEMSET_BYNAME[args.itemset]["crossword"]

	# Wordlist
	wordlist = loadWordlist(args.wordlist, args.use_thesaurus)

	# Crossword
	crossword = loadCrossword(args.crossword)

	# Loading ended
	if args.timers > 0:
		time_load_end = time.time()
		LOGGER.info("Loaded all in %f seconds",
		time_load_end-time_load_start)
	else:
		LOGGER.info("Loaded all data succesfully")

	# Choose algorithm
	alg = selectAlgorithm()

	# Solve the problem
	LOGGER.info("Started backtracking algorithm")
	if args.timers > 0: 	time_alg_start = time.time()
	solution = alg(crossword.getVariables())
	if args.timers > 0:
		time_alg_end = time.time()
		LOGGER.info("Ended alg. in %f seconds",
		time_alg_end-time_alg_start)
	else:
		LOGGER.info("Ended backtracking algorithm")

	# Solution
	if args.timers > 0:
		LOGGER.info("TOTAL TIME:   %f seconds",time_alg_end-time_load_start)
	showSolution(solution)
	LOGGER.info("Thanks for trusting our app ;)")
