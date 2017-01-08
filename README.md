# distributional-semantics
###Solution to Computational Linguistics Assignment

SCHOOL: Brandeis University  
COURSE: COSI 114B: Fundamentals of Computational Linguistics  
PROFESSOR: Marie Meteer
HEAD TA: Nikhil Krishnaswamy
SEMESTER: Spring 2016

**DESCRIPTION**: The purpose of the assignmet is to explore distribuational semantic matrices and associated techniques. For Part 1 of the assignment we were to construct a distributional semantic matrix from a small corpus, performing along the way smoothing, reweighting by positive pointwise mutual information (PPMI), and dimension reduction by singular value decomposition. For Part 2 our task was to use third-party distributional semantic matrices in conjunction with linear algbraic techniques in order to take multiple choice tests, one test for synonym identification and other for analogy completion. Complete assignment instructions are available as a PDFs.

**Files**:  
+ *DistributionalMatrix.py* -- object representing distributional semantic matrix. Performing associated computations, and is used throughout the assignment
+ *Part1_BasicDistribMat.py* -- script for accomplishing Part 1  
+ *Part2_MakeSynonymTest.py* -- composes synonyms test  
+ *synonyms.txt* -- file of synonym pairings used to create test  
+ *snynonymTest* -- represents multiple choice synonym identification test, output of Part2_MakeSynonymTest.py  
+ *Part2_TakeSynonymTest.py* -- script for taking synonym identification test, using different techniques  
+ *Part2_TakeAnalogiesTest.py* -- script for taking analogy completion test, using different techniques  
+ *GoogleNews-vectors-rcv_vocab.txt* (NOT IN REPO) -- data file for reconstituting distributional semantic matrix from Google  
+ *GEN-wform.w.2.ppmi.svd.500.rcv_vocab.txt* (NOT IN REPO) -- data file for reconstituting distributional semantic matrix built using COMPOSES toolkit  
+ *SAT-package-V3.txt* (NOT IN REPO) -- multiple choice analogy completion test  
+ *Assignment_Instructions.pdf* -- complete assignment instructions
+ *Writeup.pdf* -- writeup to assignment 
