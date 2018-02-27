import numpy as np
from dicts import DefaultDict
import copy
import string
import re
import math


def convertWord(filename):
    inputFile = open(filename, "r")
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

def letterBigram(words):
    count = 0
    letter = dict()
    prevLetter = dict()
    result = dict()
    for word in words:
        for i in range(len(word)-1):
            if word[i:i+2] not in letter.keys():
                letter[word[i:i+2]] = 1
            else:
                letter[word[i:i+2]] += 1
        for i in range(len(word)):
            if word[i] not in prevLetter.keys():
                prevLetter[word[i]] = 1
            else:
                prevLetter[word[i]] += 1
    for key in letter.keys():
        pair = (key,key[0]) #('th','t')
        result[pair] = letter[key]/prevLetter[key[0]] #p(th | t)


    return result, prevLetter, letter


def smoothing(result, testprevLetter, testLetter, prevLetter, letter):
    for i in testLetter.keys():
        pair = (i, i[0])
        if i[0] not in prevLetter:
            prevLetter[i[0]] = 0
        if i not in letter:
            letter[i] = 0
        if pair not in result.keys():
            result[pair] = 0
    for i in result:
        result[i] = (letter[i[0]] + 1)/(prevLetter[i[1]] + len(prevLetter.keys()))
    return result

def test(trainResult, testWords, prevLetter, letter):
    logTrain = 0 #plug the sentence to get the sume of log probibiity, compare three model's performance
    logTest = 0 #smoothing here, update the unseen words
    lett = letter.keys()
    testprevLetter = dict()
    testLetter = dict()
    for word in testWords:
        for i in range(len(word)-1):
            if word[i:i+2] not in testLetter.keys():
                testLetter[word[i:i+2]] = 0
        for i in range(len(word)):
            if word[i] not in testprevLetter.keys():
                testprevLetter[word[i]] = 0
    isSmoothing = True
    if isSmoothing == True:
        result = smoothing(trainResult, testprevLetter, testLetter, prevLetter, letter)
        for i in testLetter:
            pair = (i, i[0])
            key = result.keys()
            logTest += math.log(result[pair],2)
    else:
        for i in testLetter:
            pair = (i, i[0])
            key = trainResult.keys()
            if pair in key:
                logTest += math.log(trainResult[pair],2)
#smoothing

    return logTest



def letterLangld():
    englishWords = convertWord("LangId.train.English")
    englishBigram, engPrev, engWord = letterBigram(englishWords)

    frenchWords = convertWord("LangId.train.French")
    frenchBigram, frePrev, freWord  = letterBigram(frenchWords)

    italianWords = convertWord("LangId.train.Italian")
    italianBigram, itaPrev, itaWord  = letterBigram(italianWords)

    testFile = open("LangId.test", "r")
    lines = testFile.readlines()
    with open('letterLangId.out', 'w') as the_file:
        count = 1
        for line in lines:
            testWords = convertWordTest(line)
            eng = test(englishBigram,testWords, engPrev, engWord)
            fre = test(frenchBigram,testWords, frePrev, freWord)
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
    letter = open("letterLangId.out", "r")
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
    letterLangld()
    accuracy()

if __name__ == '__main__':
    main()
