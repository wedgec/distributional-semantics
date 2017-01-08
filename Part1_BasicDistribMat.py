# Name:       William Edgecomb 
# Email:      wedgeco@brandeis.edu
# Course:     COSI 114
# Assignment: HW5   
# Program:    Part1 - Script for Part 1 of HW 5. Creates a distributional
#			  co-occurrence matrix from a corpus, smooths it, reweights it
#			  against a PPMI matrix, and then reduces its dimensions using SVD   			  
# Date:       3 May 2016

import numpy
from DistributionalMatrix import distribMatrix

print "\nDistributional Semantics, Part 1\n"

# object that represents a distributional semantic matrix
distribMat = distribMatrix()

# populates the matrix by scanning corpus and counting co-occorrences
corpus = open("dist_sim_data.txt", "r")
distribMat.composeMatrixFomCorpus(corpus)
corpus.close()

print "Word IDs (counts for word found in row and column of ID):"
print distribMat.IDsToWords

print "\nMatrix with raw counts:"
distribMat.display()

# smooths matrix by multiplying by 10 and adding 1 to each element
distribMat.simpleSmooth(10., 1.)
print "\nMatrix with smoothed counts (counts*10+1):"
distribMat.display()

# calculates PPMI matrix
PPMImatrix = distribMat.PPMIfromCountsMatrix()
print "\nPPMI matrix, rounded to 3 decimal places:"
print numpy.matrix.round(PPMImatrix, 3)
 
# reweights smoothed matrix by multiplying it elementwise by
# PPMI matrix
reweightedMatrix = distribMat.distribMatToReweightedPPMI(PPMImatrix)
print "\nMatrix reweighted by PPMI, rounded to three decimal places:"
print numpy.matrix.round(reweightedMatrix, 3)

print "\nEuclidean Distances, full feature set:"

def printDistnc(word1, word2):
	distnce = distribMat.getEuclidDstnc(word1, word2)
	print word1 + ' & ' + word2 + ': ' + str(distnce)

printDistnc("women", "men")
printDistnc("women", "dogs")
printDistnc("men", "dogs")
printDistnc("feed", "like")
printDistnc("feed", "bite")
printDistnc("like", "bite")

# reduces matrix to three features using SVD
reducedMatrix = distribMat.reduceMatrix(3)
print "\nReduced features matrix, rounded to three decimal places:"
print numpy.matrix.round(reducedMatrix, 3)

print "\nEuclidean Distances, reduced feature set:"

printDistnc("women", "men")
printDistnc("women", "dogs")
printDistnc("men", "dogs")
printDistnc("feed", "like")
printDistnc("feed", "bite")
printDistnc("like", "bite")