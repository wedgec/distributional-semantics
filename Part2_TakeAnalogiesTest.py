# Name:       William Edgecomb 
# Email:      wedgeco@brandeis.edu
# Course:     COSI 114
# Assignment: HW5   
# Program:    Part2_TakeTestSAT	- this script uses pre-trained distributional 
#  			  semantic matrics (read in from file) to take a multiple choice 
#		      analogy test, which is stored in a formatted text document. Each 
#			  matrix is used to take the test according to two different strategies,
#			  one utilizing vector concatenation and the other utilizing vector 
#		      subtraction	
# Date:       3 May 2016

import numpy, scipy
from scipy import spatial
from DistributionalMatrix import distribMatrix

# reads in matrix data into instances of class distribMatrix
google = open("GoogleNews-vectors-rcv_vocab.txt")
googleMat = distribMatrix()
googleMat.composeMatrixFromDoc(google, 300)
composesDoc = open("EN-wform.w.2.ppmi.svd.500.rcv_vocab.txt")
composesMat = distribMatrix()
composesMat.composeMatrixFromDoc(composesDoc, 500)

# calculates metric for analogy word pair dependant on strategy. Low scores are considered better
def calcChoiceMetric(strategy, distribMat, input1, input2, choiceWord1, choiceWord2, OOVwords):
	# return Inf for any oov words
	if choiceWord1 in OOVwords or choiceWord2 in OOVwords:
		return float("Inf")
	
	# strategy1 is vector concatenation with cosine similarity	
	if strategy == "strategy1":
		inputVecs = distribMat.calcFeatureVecs(input1, input2)
		inputVecsConcat = numpy.concatenate((inputVecs[0], inputVecs[1]))
		choiceVecs = distribMat.calcFeatureVecs(choiceWord1, choiceWord2)
		if choiceVecs == None:
			return float("Inf")
		choiceVecsConcat = numpy.concatenate((choiceVecs[0], choiceVecs[1]))
		# note, cosine similarity multiplied by -1 since low scores are considered best
		choiceMetric = (1. - scipy.spatial.distance.cosine(inputVecsConcat, choiceVecsConcat)) * -1
	
	# strategy2	is vector subtraction with Euclidean distance
	elif strategy == "strategy2":
		choiceVecs = distribMat.calcFeatureVecs(choiceWord1, choiceWord2)
		if choiceVecs == None:
			return float("Inf")
		inputVecs = distribMat.calcFeatureVecs(input1, input2)
		diffVecInput = numpy.subtract(inputVecs[0], inputVecs[1])
		diffVecChoice = numpy.subtract(choiceVecs[0], choiceVecs[1]) 
		choiceMetric = scipy.spatial.distance.euclidean(diffVecInput, diffVecChoice)
	return choiceMetric

# takes the analogy SAT test and returns array of performance stats
def takeAnalogyTest(strategy, distribMat, OOVwords):
	analogiesTest = open("SAT-package-V3.txt")
	for i in range(42):
		analogiesTest.readline()

	# each iteration of loop, program attempts to answer one question	
	numTrue = 0
	numExcluded = 0
	while analogiesTest.readline() != "":
		inputs = analogiesTest.readline().split()
		input1 = inputs[0]
		input2 = inputs[1]
		if input1 in OOVwords or input2 in OOVwords:
			numExcluded += 1
			# skips to next question
			for i in range(7):
				analogiesTest.readline()
			continue
		# first candidate answer default best choice	
		choiceWords = analogiesTest.readline().split()
		choiceMetric = calcChoiceMetric(strategy, distribMat, input1, input2, choiceWords[0], choiceWords[1], OOVwords)
		bestVal = choiceMetric
		bestAnswer = "a"

		# evaluates remaining choices
		for letter in ["b", "c", "d", "e"]:
			choiceWords = analogiesTest.readline().split()
			choiceMetric = calcChoiceMetric(strategy, distribMat, input1, input2, choiceWords[0], choiceWords[1], OOVwords)
			if choiceMetric < bestVal:
				bestVal = choiceMetric
				bestAnswer = letter
		answer = analogiesTest.readline().split()[0]
		# increments numTrue if correct answer selected
		if bestAnswer == answer:
			numTrue += 1
		analogiesTest.readline()
	stats = [numTrue, numExcluded]
	analogiesTest.close()
	return stats

# populates set of vocab words
analogiesVocab = set()
analogiesTest = open("SAT-package-V3.txt")
# skips intro
for i in range(42):
	analogiesTest.readline()
while analogiesTest.readline() != "":
	for i in range(6):
		words = analogiesTest.readline().split()
		analogiesVocab.add(words[0])
		analogiesVocab.add(words[1])
	analogiesTest.readline()
	analogiesTest.readline()	

analogiesTest.close()

# computes sets of words in synonym test not in model's vocabularies  
googleOOVwords = analogiesVocab - set(googleMat.wordsToIDs.keys())
composesOOVwords = analogiesVocab - set(composesMat.wordsToIDs.keys())

# takes test
statsGoogleStrat1 = takeAnalogyTest("strategy1", googleMat, googleOOVwords)
statsComposesStrat1 = takeAnalogyTest("strategy1", composesMat, composesOOVwords)
statsGoogleStrat2 = takeAnalogyTest("strategy2", googleMat, googleOOVwords)
statsComposesStrat2 = takeAnalogyTest("strategy2", composesMat, composesOOVwords)

print "Google Concatenate Method:" 
print "Number true: " + str(statsGoogleStrat1[0])
print "Number excluded: " + str(statsGoogleStrat1[1])

print "Composes Concatenate Method:" 
print "Number true: " + str(statsComposesStrat1[0])
print "Number excluded: " + str(statsComposesStrat1[1])

print "Google Vector Subtratction Euclidean Method:" 
print "Number true : " + str(statsGoogleStrat2[0])
print "Number excluded: " + str(statsGoogleStrat2[1])

print "Composes Vector Subtraction Euclidean Method:" 
print "Number true : " + str(statsComposesStrat2[0])
print "Number excluded: " + str(statsComposesStrat2[1])