#!/usr/bin/env

# This program converts .libsvm sparse format into .arff sparse format
# Development has been inspired by the following converter: https://goo.gl/hp3Cke

import argparse
from collections import OrderedDict

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument('-i', '--inputFile')
argumentParser.add_argument('-o', '--outputFile')
arguments = argumentParser.parse_args()

labelsSet = set()
libsvmIdToWekaIndexDictionary = OrderedDict()

with open(arguments.inputFile, 'r') as inputFile:
    for line in inputFile:
        lineSplit = line.split()
        label = lineSplit[0]
        features = lineSplit[1:]
        labelsSet.add(label)
        for feature in features:
            featureId = feature.split(':')[0]
            if featureId not in libsvmIdToWekaIndexDictionary:
                libsvmIdToWekaIndexDictionary[featureId] = len(libsvmIdToWekaIndexDictionary)

print "Exporting..."

with open(arguments.outputFile, 'w') as outputFile, open(arguments.inputFile, 'r') as inputFile:
    outputFile.write('@RELATION {}\n'.format(arguments.inputFile))
    for key, value in libsvmIdToWekaIndexDictionary.iteritems():
        outputFile.write('@ATTRIBUTE libsvmId_{}_to_wekaIndex_{} REAL\n'.format(key,value))
    outputFile.write('@ATTRIBUTE class {}{}{}\n'.format('{', ','.join(labelsSet), '}'))
    outputFile.write('@DATA\n')
    for line in inputFile:
        lineSplit = line.split()
        label = lineSplit[0]
        features = lineSplit[1:]
        tempDict = {}
        outputFile.write('{')
        for feature in features:
            featureId, featureValue = feature.split(':')
            tempDict[int(libsvmIdToWekaIndexDictionary[featureId])] = float(featureValue)
        tempDictSorted = OrderedDict(sorted(tempDict.items()))
        for featureId, featureValue in tempDictSorted.items():
            outputFile.write('{} {}, '.format(featureId, featureValue))
        outputFile.write(str(len(libsvmIdToWekaIndexDictionary)))
        outputFile.write(' {}'.format(label))
        outputFile.write('}\n')
