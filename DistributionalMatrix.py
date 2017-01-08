# Name:       William Edgecomb 
# Email:      wedgeco@brandeis.edu
# Course:     COSI 114
# Assignment: HW5   
# Program:    DistributionalMatrix - this class represents a distributional 
#			  semantic matrix. Contains various methods for semantic analysis
#   	      and for modifying matrix  			  
# Date:       3 April 2016

import numpy, scipy, math
from scipy import spatial

class distribMatrix:

	def __init__(self):

		# will store the co-occurrence/distributional semantic matrix
		self.distribMat = None
		self.unigramCounts = {}
		# each word mapped to a unique numeric ID and vice versa
		self.wordsToIDs = {}
		self.IDsToWords = {}
		self.vocabSize = 0
		# number of features in each word vector. Also the width of the matrix
		self.numFeatures = 0

	# composes pre-trained matrix from doc, information read from data file. 
	def composeMatrixFromDoc(self, doc, numFeatures):
		self.numFeatures = numFeatures
		# each line in doc starts with a word and is f
		docLines = doc.read().split("\n")
		# clears the last line (a non-data line)
		del docLines[len(docLines) - 1]
		
		self.vocabSize = len(docLines)
	
		# preallocates distributional semantic matrix
		self.distribMat = numpy.zeros((self.vocabSize, self.numFeatures))
		
		# populates matrix and word/ID dictionaries
		index = 0
		for line in docLines:
			elements = line.split()
			word = elements[0]
			self.distribMat[index] = elements[1:]
			self.wordsToIDs[word] = index
			self.IDsToWords[index] = word
			index += 1

	# populates matrix and other fields via scanning the corpus
	def composeMatrixFomCorpus(self, corpus):

		sentencesArray = corpus.read().split("\n")
		# the following loop counts instances of unigrams and populates dictionaries
		# wordsToIDs and IDsToWords
		ID = 0
		for sentence in sentencesArray:
			for word in sentence.split():
				if word not in self.wordsToIDs:
					self.wordsToIDs[word] = ID
					self.IDsToWords[ID] = word
					ID += 1
					self.unigramCounts[word] = 1.0
				else:
					self.unigramCounts[word] += 1.0

		self.vocabSize = len(self.unigramCounts)
		self.numFeatures = self.vocabSize 

		# initialize co-occurrence matrix. Matrix is redundant, such that if count of 
		# (w,c)--w,c in either order--is stored in cell [i,j], it is also stored in cell
		# [j,i] 
		self.distribMat = numpy.zeros((self.vocabSize, self.numFeatures))

		# scans corpus and populates co-occurrence matrix
		for sentence in sentencesArray: 
			textIndex = 0
			wordArray = sentence.split()
			while textIndex < len(wordArray) - 1:
				prevWord = wordArray[textIndex]
				nextWord = wordArray[textIndex + 1]
				prevID = self.wordsToIDs[prevWord]
				nextID = self.wordsToIDs[nextWord]
				self.distribMat[prevID][nextID] += 1.0
				if prevID != nextID:
					self.distribMat[nextID][prevID] += 1
				textIndex += 1

	# displays matrix
	def display(self):
		print self.distribMat
	
	# smooths matrix by multiplying each element by multBy and then adding to each addTo.
	# Also adjusts unigram counts accordingly 			
	def simpleSmooth(self, multBy, addTo):

		# Loop calculates average ratio of counts of a word to counts of pairs containing that word. 
		# Will be used to estimate unigram counts from pair counts after smoothing
		unigramToPairRatio = 0
		for ID in self.IDsToWords.keys():
			pairsWithWord = numpy.sum(self.distribMat[ID])
			unigramCount = self.unigramCounts[self.IDsToWords[ID]]
			unigramsToPairs = unigramCount/pairsWithWord
			unigramToPairRatio += unigramsToPairs
		unigramToPairRatio /= self.vocabSize

		# smooths matrix
		self.distribMat = self.distribMat * multBy + addTo

		# refactors unigram counts according to unigramToPairRatio
		for ID in self.IDsToWords.keys():
			pairsWithWord = numpy.sum(self.distribMat[ID])
			self.unigramCounts[self.IDsToWords[ID]] = pairsWithWord * unigramToPairRatio

	# calculates positive pointwise mutual information matrix (PPMI)		
	def PPMIfromCountsMatrix(self):
		
		# counts total tokens
		totalTokens = 0
		for unigram in self.unigramCounts:
			totalTokens += self.unigramCounts[unigram]

		# counts total pairs (excludes redundant cells, i.e. does not count cell[i,j] and cell[j,i] separately)
		totalPairs = 0.0
		for index1 in range(self.vocabSize):
			for index2 in range(index1, self.numFeatures):
				totalPairs += self.distribMat[index1][index2]

		# initializes PPMI matrix
 		PPMI = numpy.zeros((self.vocabSize, self.numFeatures))
 		# populates PPMI matrix by calculatig PPMI for each cell
		for contextID in range(self.vocabSize):
			for wordID in range(self.numFeatures):
				context = self.IDsToWords[contextID]
				word = self.IDsToWords[wordID]
				probPair = self.distribMat[contextID][wordID] / totalPairs
				probContext = self.unigramCounts[context] / totalTokens
				probWord = self.unigramCounts[word] / totalTokens
				PPMI[contextID][wordID] = max(math.log(probPair / (probContext * probWord), 2), 0)

		return PPMI

	# reweights matrix by multiplying matrix elementwise by corresponding PPMI matrix
	def distribMatToReweightedPPMI(self, PPMImatrix):
		reweightedPPMI = numpy.multiply(self.distribMat, PPMImatrix)
		self.distribMat = reweightedPPMI 
		return reweightedPPMI

	# returns a 2-element list of the feature vectors for the inputted words	
	def calcFeatureVecs(self, word1, word2):
		#if word1 not in self.wordsToIDs.keys() or word2 not in self.wordsToIDs.keys():
		#	return None

		wordID1 = self.wordsToIDs[word1]
		wordID2 = self.wordsToIDs[word2]
		featureVec1 = self.distribMat[wordID1]
		featureVec2 = self.distribMat[wordID2]
		return [featureVec1, featureVec2]

	# calculates the euclidean distance of the vectors corresponding to the inputted words
	def getEuclidDstnc(self, word1, word2):
		
		featureVecs = self.calcFeatureVecs(word1, word2)

		# returned if either word not in vocabulary
		#if featureVecs == None:
			#return float("Inf")

		featureVec1 = featureVecs[0]
		featureVec2 = featureVecs[1]

		# calculates and returns euclidean distance
		euclidDistncSqr = 0.
		for j in range(self.numFeatures):
			euclidDistncSqr += numpy.power((featureVec2.item(j) - featureVec1.item(j)), 2)
		return numpy.sqrt(euclidDistncSqr)

	# calculates the cosine similarity of the vectors corresponding to the inputted words
	def getCosSimilarity(self, word1, word2):
		featureVecs = self.calcFeatureVecs(word1, word2)

		# returned if either word not in vocabulary
		if featureVecs == None:
			return float("Inf")

		featureVec1 = featureVecs[0]
		featureVec2 = featureVecs[1]

		return 1. - scipy.spatial.distance.cosine(featureVec1, featureVec2)

	# reduces matrix's number of features to newDimensions number of dimensions, using SVD 
	def reduceMatrix(self, newDimensions):
		# reduces matrix to components using SVD
		U, E, V = scipy.linalg.svd(self.distribMat, full_matrices = False)
		E = numpy.matrix(numpy.diag(E))
		V = numpy.matrix(V)
		U = numpy.matrix(U)
		
		print "\nVerify original matrix recoverable:" 
		recoveredMat = (U * E * V)
		print "Recovered matrix (U * E * V), rounded to nearest integer:"
		print numpy.matrix.round(recoveredMat)

		# reduce matrix dimensions to newDimensions 
		reducedMat = self.distribMat * V[:,0:newDimensions]
		self.numFeatures = newDimensions
		self.distribMat = reducedMat 
		return reducedMat 