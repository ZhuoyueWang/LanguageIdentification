import numpy as np
from dicts import DefaultDict
import copy
import string
import re
import math

def convertWord(filename):
    inputFile = open(filename, "r") #all in one line // f = open().read().lower().split() comment out it
    lines = inputFile.readlines()
    inputFile.close()
    sentences = list()
    for line in lines:
        for c in string.punctuation:
            line = line.replace(c,"")
        sentences.append((line.lower()).strip())
    words = list()
    for sentence in sentences:
        words.extend(sentence.split())
    return words


def convertWordTest(line):
    sentences = list()
    for c in string.punctuation:
        line = line.replace(c,"")
    sentences.append((line.lower()).strip())
    words = list()
    for sentence in sentences:
        words.extend(sentence.split())
    return words

def wordBigram(words):
    count = 0
    wordPair = dict()
    prevWord = dict()
    result = dict()
    for i in range(len(words)-1):
        pair = (words[i],words[i+1]) #the case
        if pair not in wordPair.keys():
            wordPair[pair] = 1
        else:
            wordPair[pair] += 1
    for i in range(len(words)):
        if words[i] not in prevWord.keys():
            prevWord[words[i]] = 1
        else:
            prevWord[words[i]] += 1
    for key in wordPair.keys():
        pair = (key,key[0]) #((the,case),the)
        result[pair] =  wordPair[key]/prevWord[key[0]] #p(th | t)
    return result, prevWord, wordPair




def JMSmoothing(result, prevWord, wordPair, prevLetter, letter, lamda):
    totalWords = 0
    for i in prevWord:
        if i not in prevLetter.keys():
            prevLetter[i] = 1
        else:
            prevLetter[i] += 1
        totalWords += prevLetter[i]
    for i in wordPair:
        if i not in letter.keys():
            letter[i] = 1
        else:
            letter[i] += 1
    PML = dict()
    for i in prevLetter.keys():
        PML[i] = prevLetter[i]/totalWords
    for key1 in wordPair:
        pair = (key1, key1[0])
        if pair not in result.keys():
            result[pair] = 0
    for key1 in result.keys():
        result[key1] = lamda*result[key1] + (1-lamda)*PML[key1[1]]
    return result



def test(trainResult, testWords, prevLetter, letter):
    logTrain = 0 #plug the sentence to get the sume of log probibiity, compare three model's performance
    logTest = 0 #smoothing here, update the unseen words

    prevWord = [i for i in testWords]
    wordPair = [(testWords[i], testWords[i+1]) for i in range(len(testWords)-1)]

    isSmoothing = True
    if isSmoothing == True:
        result = JMSmoothing(trainResult, prevWord, wordPair, prevLetter, letter, 0.985)
        for i in range(len(testWords)-1):
            key = (testWords[i], testWords[i+1])
            pair = (key, key[0])
            logTest += math.log(result[pair],2)
    else:
        for i in wordPair:
            key = trainResult.keys()
            wKey = (i,i[0])
            if wKey in key:
                logTest += math.log(trainResult[wKey],2)
    return logTest


def wordLangld():
    englishWords = convertWord("LangId.train.English")
    englishBigram, engPrev, engWord = wordBigram(englishWords)

    frenchWords = convertWord("LangId.train.French")
    frenchBigram, frePrev, freWord = wordBigram(frenchWords)

    italianWords = convertWord("LangId.train.Italian")
    italianBigram, itaPrev, itaWord = wordBigram(italianWords)

    testFile = open("LangId.test", "r")
    lines = testFile.readlines()
    with open('wordLangId2.out', 'w') as the_file:
        count = 1
        for line in lines:
            testWords = convertWordTest(line)
            eng = test(englishBigram,testWords,engPrev, engWord )
            fre = test(frenchBigram,testWords, frePrev, freWord )
            ita = test(italianBigram,testWords, itaPrev, itaWord)
            MAX = max(eng, fre, ita)
            if MAX == eng:
                the_file.write("{} {}\n".format(count,"English"))
            elif MAX == fre:
                the_file.write("{} {}\n".format(count,"French"))
            else:
                the_file.write("{} {}\n".format(count,"Italian"))
            count += 1


def accuracy():
    letter = open("wordLangId2.out", "r")
    letterLines = letter.readlines()
    letter.close()
    sol = open("LangId.sol", "r")
    solLines = sol.readlines()
    sol.close()
    count = 0
    for i in range(len(solLines)):
        if solLines[i] != letterLines[i]:
            count += 1
    print("accuracy rate {}".format((300-count)/300))

def main():
    wordLangld()
    accuracy()

if __name__ == '__main__':
    main()
