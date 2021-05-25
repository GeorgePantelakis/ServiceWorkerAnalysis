from os import stat
from os import listdir
import os
from os.path import isfile, join
import json

connectionFiles = [f for f in listdir('connection_results') if isfile(join('connection_results', f))]
while(1):
    if connectionFiles[connectionFiles.__len__() - 1][0] == '_':
        connectionFiles.pop()
    else:
        break

resultFile = open("connection_results/_resultsWithoutFilters.txt", "w")

for connectionFile in connectionFiles:
    lines = []
    resultFile.write(connectionFile.split('()')[0] + ' ')
    with open('connection_results/' + connectionFile, 'r') as fp:
        lines = fp.read().splitlines()
    for line in lines:
        resultFile.write(line + ' ')
    resultFile.write('\n')


resultFile.close()
