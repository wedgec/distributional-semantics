# Name:       William Edgecomb 
# Email:      wedgeco@brandeis.edu
# Course:     COSI 114
# Assignment: HW5   
# Program:    Part2_MakeSynTest - This script takes the synonym file and creates
#			  a text file that represents a multiple choice synonym detection test.
#			  Outputted test will have 1000 questions  			  
# Date:       3 April 2016

import random

# opens take containing synonyms
doc = open("EN_syn_verb.txt")
synPairs = doc.read().split("\n")

# deletes non-data elements
del synPairs[0]
del synPairs[len(synPairs) - 1]

# maps input word verbs to sets of synonyms, 
# and populates set of all answer words
synsDict = {}
allAnswers = set()
index = 0
for pair in synPairs:
	pair = pair.split()
	inputWord = pair[0]
	syn = pair[1]
	# skips input words with 0 listed as synonym 
	if syn == "0":
		continue	
	allAnswers.add(syn)
	if inputWord in synsDict.keys():
		synSet = synsDict[inputWord]
		synSet.add(syn)
	else:
		synSet = {syn}
		synsDict[inputWord] = synSet

# to write test to new file
outputWriter = open("snynonymTest.txt", "w")

# structure of file is as follows: each line represents a question. Each line
# has 7 words, separated by spaces. First word is the question word, to be matched with
# correct synonym. Second word represents the correct answer. The subsequent five words represent
# the answer choices

# writes one line, a single question
def writeSynQuestion(outputWriter, inputWord, synsDict, allAnswers):
	# writes input word word less beginning substring "to_". This deletion will be made
	# for all words
	outputWriter.write(inputWord[3:] + " ")
	# randomly selects correct answer and writes it to file
	synSet = synsDict[inputWord]
	randomSyn = random.sample(synSet, 1)
	outputWriter.write(randomSyn[0][3:])
	nonSynSet = allAnswers^synSet
	# randomly selects 4 unique wrong answers
	wrongAnswers = set(random.sample(nonSynSet, 4))
	# puts all five choices together in a set
	fiveChoices = wrongAnswers|set(randomSyn)
	# writes five choices in whatever order python iterates through sets of strings. 
	# Correct answer will end up in different positions for different questions, so it at
	# leat seems random
	for choice in fiveChoices:
		outputWriter.write(" " + choice[3:])

# writes ten questions per input word, takes us to 990 questions
for inputWord in synsDict.keys():
	for i in range(10):
		# writes individual question for input word
		writeSynQuestion(outputWriter, inputWord, synsDict, allAnswers)
		outputWriter.write("\n")

# writes ten more questions with randomly selected input words. Completes
# the 1000 questions
for i in range(10):
	inputWord = random.sample(synsDict.keys(), 1)[0]
	writeSynQuestion(outputWriter, inputWord, synsDict, allAnswers)
	outputWriter.write("\n")
	
outputWriter.close()
