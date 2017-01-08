# Name:       William Edgecomb 
# Email:      wedgeco@brandeis.edu
# Course:     COSI 114
# Assignment: HW5   
# Program:    Part2_TakeSynTest	- this script uses pre-trained distributional 
#  			  semantic matrics (read in from file) to take a multiple choice 
#		      synonym test, which is stored in a formatted text document. Each 
#			  matrix is used to take the test according to two different strategies,
#			  one utilizing euclidean distance and the other utilizing cosine similarity  		  
# Date:       3 May 2016

from DistributionalMatrix import distribMatrix

# reads in matrix data into instances of class distribMatrix
googleDoc = open("GoogleNews-vectors-rcv_vocab.txt")
googleMat = distribMatrix()
googleMat.composeMatrixFromDoc(googleDoc, 300)
composesDoc = open("EN-wform.w.2.ppmi.svd.500.rcv_vocab.txt")
composesMat = distribMatrix()
composesMat.composeMatrixFromDoc(composesDoc, 500)

# takes test. questions is the list of lines in the test. oovWords is the set of words on
# the test that are not in distribMat's vocabulary. Returns array of performance statistics 
def takeSynTest(distribMat, questions, oovWords, strategy):

	# calculates metric for relation between the test word and a candidate answer. Low values considered best
	def calcMetric(testWord, choiceWord):
		if choiceWord in oovWords:
			return float("Inf")
		elif strategy == "euclid":  
			return distribMat.getEuclidDstnc(testWord, choiceWord)
		elif strategy == "cosine":
			# note that here we return negation of cosine similarity, since low values are considered best
			return distribMat.getCosSimilarity(testWord, choiceWord) * -1.

	numTrue = 0
	numExcluded = 0

	# for each iteration program attempts to answer one question
	for q in questions:
		elements = q.split()
		testWord = elements[0]
		if testWord in oovWords:
			numExcluded += 1
			continue
		# first choice set as default best choice	
		answer = elements[1]
		choiceWord = elements[2]
		bestMetric = calcMetric(testWord, choiceWord)
		bestChoice = choiceWord
		# iterates through remaining answer choices and updates bestMetric and bestChoice
		for i in range(3,7):
			choiceWord = elements[i]
			metric = calcMetric(testWord, choiceWord)
			if metric < bestMetric:
				bestMetric = metric
				bestChoice = choiceWord
		# increments numtrue if correct answer selected
		if bestChoice == answer:
			numTrue += 1
	stats = [numTrue, numExcluded]
	return stats


synTest = open("synQuestions.txt")
questions = synTest.read().split("\n")
synTest.close()
# deletes blank line at end of doc
del questions[len(questions) - 1]

# populates set of vocab words
synVocab = set()
for q in questions:
	for word in q.split():
		synVocab.add(word)
		synVocab.add(word[0].upper() + word[1:])

# computes sets of words in synonym test not in model's vocabularies  
googleOOVwords = synVocab - set(googleMat.wordsToIDs.keys())
composesOOVwords = synVocab - set(composesMat.wordsToIDs.keys())

# takes test
statsGoogleEuclid = takeSynTest(googleMat, questions, googleOOVwords, "euclid")
statsComposesEuclid = takeSynTest(composesMat, questions, composesOOVwords, "euclid")
statsGoogleCosine = takeSynTest(googleMat, questions, googleOOVwords, "cosine")
statsComposesCosine = takeSynTest(composesMat, questions, composesOOVwords, "cosine")

print "Google Euclidean Method:" 
print "Number true: " + str(statsGoogleEuclid[0])
print "Number excluded: " + str(statsGoogleEuclid[1])

print "Composes Euclidean Method:" 
print "Number true: " + str(statsComposesEuclid[0])
print "Number excluded: " + str(statsComposesEuclid[1])

print "Google Cosine Method:" 
print "Number true : " + str(statsGoogleCosine[0])
print "Number excluded: " + str(statsGoogleCosine[1])

print "Composes Cosine Method:" 
print "Number true : " + str(statsComposesCosine[0])
print "Number excluded: " + str(statsComposesCosine[1])

